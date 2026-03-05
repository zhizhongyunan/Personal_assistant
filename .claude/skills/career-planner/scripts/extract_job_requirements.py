#!/usr/bin/env python3
"""
Extract market requirements from raw job postings.

Supported input formats:
- CSV (recommended): title, company, location, salary, description, source, published_at
- JSON / JSONL: list of objects with similar fields
- TXT: one posting per line (mapped to description only)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SKILL_PATTERNS = {
    "python": [r"\bpython\b"],
    "java": [r"\bjava\b"],
    "go": [r"\bgo\b", r"\bgolang\b"],
    "c++": [r"\bc\+\+\b"],
    "sql": [r"\bsql\b"],
    "mysql": [r"\bmysql\b"],
    "postgresql": [r"\bpostgres(?:ql)?\b"],
    "redis": [r"\bredis\b"],
    "mongodb": [r"\bmongodb\b"],
    "kafka": [r"\bkafka\b"],
    "spark": [r"\bspark\b"],
    "flink": [r"\bflink\b"],
    "hadoop": [r"\bhadoop\b"],
    "docker": [r"\bdocker\b"],
    "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "linux": [r"\blinux\b"],
    "aws": [r"\baws\b"],
    "azure": [r"\bazure\b"],
    "gcp": [r"\bgcp\b", r"google cloud"],
    "react": [r"\breact\b"],
    "vue": [r"\bvue\b"],
    "angular": [r"\bangular\b"],
    "typescript": [r"\btypescript\b", r"\bts\b"],
    "javascript": [r"\bjavascript\b", r"\bjs\b"],
    "node.js": [r"\bnode\.?js\b", r"\bnode\b"],
    "fastapi": [r"\bfastapi\b"],
    "spring": [r"\bspring\b"],
    "django": [r"\bdjango\b"],
    "pytorch": [r"\bpytorch\b"],
    "tensorflow": [r"\btensorflow\b", r"\btf\b"],
    "llm": [r"\bllm\b", r"大模型", r"语言模型"],
    "rag": [r"\brag\b", r"检索增强"],
    "agent": [r"\bagent\b", r"智能体"],
}

EXPERIENCE_RANGE_PATTERN = re.compile(
    r"(?P<min>\d{1,2})\s*[-~～—到至]+\s*(?P<max>\d{1,2})\s*年"
)
EXPERIENCE_SINGLE_PATTERN = re.compile(r"(?P<min>\d{1,2})\s*\+?\s*年(?:以上)?")

DEGREE_PATTERNS = {
    "phd": [r"博士", r"\bphd\b", r"doctorate"],
    "master": [r"硕士", r"\bmaster\b", r"研究生"],
    "bachelor": [r"本科", r"\bbachelor\b", r"学士"],
    "college": [r"大专", r"专科", r"college"],
    "none_specified": [r"不限", r"无学历要求", r"not required"],
}

SALARY_K_RANGE = re.compile(
    r"(?P<min>\d+(?:\.\d+)?)\s*[-~～—到至]\s*(?P<max>\d+(?:\.\d+)?)\s*[kK]"
)
SALARY_YEAR_WAN_RANGE = re.compile(
    r"(?P<min>\d+(?:\.\d+)?)\s*[-~～—到至]\s*(?P<max>\d+(?:\.\d+)?)\s*万\s*/?\s*年"
)
SALARY_YEAR_WAN_SINGLE = re.compile(r"(?P<value>\d+(?:\.\d+)?)\s*万\s*/?\s*年")


def read_records(input_path: Path) -> List[Dict[str, str]]:
    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        with input_path.open("r", encoding="utf-8-sig", newline="") as f:
            return [dict(row) for row in csv.DictReader(f)]
    if suffix == ".json":
        with input_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [dict(item) for item in data]
            if isinstance(data, dict) and isinstance(data.get("jobs"), list):
                return [dict(item) for item in data["jobs"]]
            raise ValueError("JSON must be a list or {'jobs': [...]}")
    if suffix == ".jsonl":
        records: List[Dict[str, str]] = []
        with input_path.open("r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                records.append(dict(json.loads(line)))
        return records
    if suffix == ".txt":
        records = []
        with input_path.open("r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append({"description": line})
        return records
    raise ValueError(f"Unsupported input format: {suffix}")


def clean_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def detect_skills(text: str) -> List[str]:
    hits = []
    lowered = text.lower()
    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(p, lowered, flags=re.ASCII) for p in patterns):
            hits.append(skill)
    return hits


def parse_experience(text: str) -> Optional[Tuple[float, float]]:
    lowered = text.lower()
    if any(token in lowered for token in ["应届", "校招", "无经验", "经验不限", "fresh graduate"]):
        return (0.0, 1.0)

    m = EXPERIENCE_RANGE_PATTERN.search(text)
    if m:
        min_y = float(m.group("min"))
        max_y = float(m.group("max"))
        if max_y >= min_y:
            return (min_y, max_y)

    m = EXPERIENCE_SINGLE_PATTERN.search(text)
    if m:
        min_y = float(m.group("min"))
        return (min_y, min_y + 2.0)
    return None


def parse_degree(text: str) -> Optional[str]:
    lowered = text.lower()
    for degree, patterns in DEGREE_PATTERNS.items():
        if any(re.search(p, lowered) for p in patterns):
            return degree
    return None


def parse_salary_to_monthly_k(text: str) -> Optional[Tuple[float, float]]:
    if not text:
        return None
    value = text.replace("／", "/")

    m = SALARY_K_RANGE.search(value)
    if m:
        return float(m.group("min")), float(m.group("max"))

    m = SALARY_YEAR_WAN_RANGE.search(value)
    if m:
        min_k = float(m.group("min")) * 10.0 / 12.0
        max_k = float(m.group("max")) * 10.0 / 12.0
        return min_k, max_k

    m = SALARY_YEAR_WAN_SINGLE.search(value)
    if m:
        mid = float(m.group("value")) * 10.0 / 12.0
        return mid, mid
    return None


def exp_bucket(min_years: float) -> str:
    if min_years < 1:
        return "0-1"
    if min_years < 3:
        return "1-3"
    if min_years < 5:
        return "3-5"
    if min_years < 8:
        return "5-8"
    return "8+"


def percentile(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = (len(ordered) - 1) * q
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    if lo == hi:
        return ordered[lo]
    ratio = idx - lo
    return ordered[lo] + (ordered[hi] - ordered[lo]) * ratio


def round_or_none(v: Optional[float]) -> Optional[float]:
    return None if v is None else round(v, 2)


def aggregate(records: Iterable[Dict[str, str]], text_column: str, salary_column: str, title_column: str) -> Dict:
    skills = Counter()
    titles = Counter()
    degrees = Counter()
    exp_ranges: List[Tuple[float, float]] = []
    exp_buckets = Counter()
    salaries: List[Tuple[float, float]] = []

    total = 0
    for row in records:
        total += 1
        title = clean_text(row.get(title_column) or row.get("title"))
        if title:
            titles[title.lower()] += 1

        text = clean_text(row.get(text_column) or row.get("description"))
        if not text:
            text = " ".join(clean_text(v) for v in row.values() if isinstance(v, str))

        for skill in detect_skills(text):
            skills[skill] += 1

        exp = parse_experience(text)
        if exp:
            exp_ranges.append(exp)
            exp_buckets[exp_bucket(exp[0])] += 1

        degree = parse_degree(text)
        if degree:
            degrees[degree] += 1

        salary_text = clean_text(row.get(salary_column) or row.get("salary"))
        salary = parse_salary_to_monthly_k(salary_text)
        if salary:
            salaries.append(salary)

    top_skills = []
    for name, count in skills.most_common(30):
        ratio = (count / total) if total else 0
        top_skills.append({"skill": name, "count": count, "ratio": round(ratio, 4)})

    exp_min_values = [x[0] for x in exp_ranges]
    exp_max_values = [x[1] for x in exp_ranges]

    salary_mids = [((s[0] + s[1]) / 2.0) for s in salaries]

    result = {
        "total_jobs": total,
        "top_skills": top_skills,
        "titles": dict(titles.most_common(20)),
        "experience": {
            "sample_size": len(exp_ranges),
            "avg_min_years": round_or_none(statistics.mean(exp_min_values) if exp_min_values else None),
            "avg_max_years": round_or_none(statistics.mean(exp_max_values) if exp_max_values else None),
            "distribution": dict(exp_buckets),
        },
        "degree_distribution": dict(degrees),
        "salary": {
            "sample_size": len(salaries),
            "avg_min_k": round_or_none(statistics.mean(s[0] for s in salaries) if salaries else None),
            "avg_max_k": round_or_none(statistics.mean(s[1] for s in salaries) if salaries else None),
            "median_mid_k": round_or_none(statistics.median(salary_mids) if salary_mids else None),
            "p25_mid_k": round_or_none(percentile(salary_mids, 0.25) if salary_mids else None),
            "p75_mid_k": round_or_none(percentile(salary_mids, 0.75) if salary_mids else None),
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract market requirements from job postings.")
    parser.add_argument("--input", required=True, help="Input file path: csv/json/jsonl/txt")
    parser.add_argument("--output", default="market_summary.json", help="Output JSON path")
    parser.add_argument("--text-column", default="description", help="Description column name")
    parser.add_argument("--salary-column", default="salary", help="Salary column name")
    parser.add_argument("--title-column", default="title", help="Title column name")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    records = read_records(input_path)
    summary = aggregate(records, args.text_column, args.salary_column, args.title_column)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote market summary to: {output_path}")
    print(f"Total jobs: {summary['total_jobs']}")
    print(f"Top skills: {', '.join(x['skill'] for x in summary['top_skills'][:10])}")


if __name__ == "__main__":
    main()
