#!/usr/bin/env python3
"""
Generate a gap analysis report between user profile and market summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set


EDU_LEVEL = {
    "none": 0,
    "highschool": 1,
    "college": 2,
    "bachelor": 3,
    "master": 4,
    "phd": 5,
}

EDU_ALIAS = {
    "不限": "none",
    "无学历要求": "none",
    "高中": "highschool",
    "中专": "highschool",
    "大专": "college",
    "专科": "college",
    "本科": "bachelor",
    "学士": "bachelor",
    "硕士": "master",
    "研究生": "master",
    "博士": "phd",
    "none": "none",
    "highschool": "highschool",
    "college": "college",
    "bachelor": "bachelor",
    "master": "master",
    "phd": "phd",
}

SKILL_ALIAS = {
    "golang": "go",
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
}


def normalize_skill(skill: str) -> str:
    s = skill.strip().lower()
    return SKILL_ALIAS.get(s, s)


def normalize_education(raw: str) -> str:
    if not raw:
        return "none"
    lowered = raw.strip().lower()
    return EDU_ALIAS.get(raw.strip(), EDU_ALIAS.get(lowered, "none"))


def parse_profile(path: Path) -> Dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Profile file must be a JSON object")
    data.setdefault("skills", [])
    if not isinstance(data["skills"], list):
        raise ValueError("profile.skills must be a list")
    return data


def parse_market(path: Path) -> Dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Market summary must be a JSON object")
    return data


def most_common_market_education(degree_distribution: Dict[str, int]) -> str:
    if not degree_distribution:
        return "none"
    best = max(degree_distribution.items(), key=lambda x: x[1])[0]
    return best if best in EDU_LEVEL else normalize_education(best)


def classify_skill_gap(skill_ratio: float, rank: int) -> str:
    if rank <= 5 or skill_ratio >= 0.35:
        return "high"
    if rank <= 10 or skill_ratio >= 0.2:
        return "medium"
    return "low"


def build_12_week_plan(missing_skills: List[Dict], weekly_hours: float) -> List[str]:
    if not missing_skills:
        return [
            "Week 1-4: Continue current strengths, build one portfolio project.",
            "Week 5-8: Improve interview stories and system design fundamentals.",
            "Week 9-12: Intensify applications and mock interviews.",
        ]

    top = [x["skill"] for x in missing_skills[:3]]
    while len(top) < 3:
        top.append("project-quality")

    pace = "standard"
    if weekly_hours >= 15:
        pace = "fast"
    elif weekly_hours <= 8:
        pace = "light"

    return [
        f"Week 1-4 ({pace} pace): Fill skill gap on '{top[0]}' and ship one mini project.",
        f"Week 5-8 ({pace} pace): Fill skill gap on '{top[1]}' and add production-like feature.",
        f"Week 9-12 ({pace} pace): Fill skill gap on '{top[2]}', then refine resume + interview set.",
    ]


def generate_report(profile: Dict, market: Dict, top_n: int) -> str:
    target_role = profile.get("target_role", "unknown")
    target_city = profile.get("target_city", "unknown")
    years = float(profile.get("experience_years", 0))
    weekly_hours = float(profile.get("weekly_study_hours", 8))
    target_salary_k = profile.get("target_salary_k")

    profile_skills: Set[str] = {normalize_skill(s) for s in profile.get("skills", []) if isinstance(s, str)}
    top_skills = market.get("top_skills", [])[:top_n]

    missing = []
    for idx, item in enumerate(top_skills, start=1):
        skill = normalize_skill(str(item.get("skill", "")))
        if not skill or skill in profile_skills:
            continue
        ratio = float(item.get("ratio", 0))
        missing.append(
            {
                "skill": skill,
                "ratio": ratio,
                "priority": classify_skill_gap(ratio, idx),
            }
        )

    exp_avg_min = market.get("experience", {}).get("avg_min_years")
    exp_gap = None
    if isinstance(exp_avg_min, (int, float)):
        exp_gap = round(float(exp_avg_min) - years, 2)

    market_edu = most_common_market_education(market.get("degree_distribution", {}))
    user_edu = normalize_education(str(profile.get("education", "")))
    edu_gap = EDU_LEVEL.get(market_edu, 0) - EDU_LEVEL.get(user_edu, 0)

    market_salary_mid = market.get("salary", {}).get("median_mid_k")
    salary_gap = None
    if isinstance(target_salary_k, (int, float)) and isinstance(market_salary_mid, (int, float)):
        salary_gap = round(float(target_salary_k) - float(market_salary_mid), 2)

    high = [x for x in missing if x["priority"] == "high"]
    med = [x for x in missing if x["priority"] == "medium"]
    low = [x for x in missing if x["priority"] == "low"]
    plan = build_12_week_plan(missing, weekly_hours)

    lines: List[str] = []
    lines.append("# Gap Analysis Report")
    lines.append("")
    lines.append("## Profile Snapshot")
    lines.append(f"- Target role: {target_role}")
    lines.append(f"- Target city: {target_city}")
    lines.append(f"- Experience years: {years}")
    lines.append(f"- Education: {user_edu}")
    lines.append(f"- Weekly study hours: {weekly_hours}")
    lines.append(f"- Current skills: {', '.join(sorted(profile_skills)) or 'none'}")
    lines.append("")
    lines.append("## Market Baseline")
    lines.append(f"- Job sample size: {market.get('total_jobs', 0)}")
    lines.append(f"- Avg required min experience: {exp_avg_min}")
    lines.append(f"- Most common education requirement: {market_edu}")
    lines.append(f"- Market median monthly salary (k): {market_salary_mid}")
    lines.append("")
    lines.append("## Priority Gaps")
    lines.append(f"- High: {', '.join(x['skill'] for x in high[:8]) or 'none'}")
    lines.append(f"- Medium: {', '.join(x['skill'] for x in med[:8]) or 'none'}")
    lines.append(f"- Low: {', '.join(x['skill'] for x in low[:8]) or 'none'}")
    lines.append("")
    lines.append("## Structured Findings")
    if exp_gap is not None:
        if exp_gap > 0:
            lines.append(f"- Experience gap: lacking about {exp_gap} years vs market baseline.")
        else:
            lines.append(f"- Experience gap: no deficit (ahead by {-exp_gap} years).")
    else:
        lines.append("- Experience gap: insufficient market data.")

    if edu_gap > 0:
        lines.append("- Education gap: market commonly asks for a higher degree than current profile.")
    elif edu_gap < 0:
        lines.append("- Education gap: education level is above common market baseline.")
    else:
        lines.append("- Education gap: aligned with common market baseline.")

    if salary_gap is not None:
        if salary_gap > 0:
            lines.append(f"- Salary gap: target is {salary_gap}k above market median; need stronger proof of value.")
        else:
            lines.append(f"- Salary gap: target is within or below market median by {-salary_gap}k.")
    else:
        lines.append("- Salary gap: insufficient salary data.")

    lines.append("")
    lines.append("## 12-Week Action Draft")
    for item in plan:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Next Step")
    lines.append("- Update this report every 2-4 weeks with fresh job samples.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate gap report from profile and market summary")
    parser.add_argument("--profile", required=True, help="Path to profile JSON")
    parser.add_argument("--market", required=True, help="Path to market summary JSON")
    parser.add_argument("--output", default="gap_report.md", help="Output markdown file")
    parser.add_argument("--top-n", default=12, type=int, help="Use top N skills from market summary")
    args = parser.parse_args()

    profile_path = Path(args.profile)
    market_path = Path(args.market)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile file not found: {profile_path}")
    if not market_path.exists():
        raise FileNotFoundError(f"Market file not found: {market_path}")

    profile = parse_profile(profile_path)
    market = parse_market(market_path)
    report = generate_report(profile, market, args.top_n)

    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote gap report to: {output_path}")


if __name__ == "__main__":
    main()
