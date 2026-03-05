---
name: career-planner
description: 为用户提供基于个人背景和最新招聘市场数据的职业规划。用户提到职业转型、求职方向选择、岗位要求分析、薪资预期评估、学习路径制定时使用；特别适用于需要综合招聘网站信息和公司官网职位信息来制定可执行计划的场景。
---

# Career Planner

收集用户画像，结合最新招聘网站与公司招聘页信息，输出可执行的职业路线、能力差距和阶段性行动方案。

## Workflow

### 1) 收集用户信息

先使用 [references/questionnaire.md](references/questionnaire.md) 的问题框架，按轮次收集信息。每轮只问 1-2 个问题，避免信息过载。

至少拿到以下字段后再进入市场分析：
- 目标岗位（可多选，但最多 2 个主目标）
- 目标城市（或远程）
- 当前经验年限
- 当前技能列表
- 目标薪资范围
- 可投入学习时间（每周小时数）

如果用户信息不完整，明确标注“假设项”并在最终方案中单列。

### 2) 获取最新岗位市场样本

使用 WebSearch 获取最近 30-90 天的招聘数据与趋势信号，优先来源见 [references/job-source-strategy.md](references/job-source-strategy.md)。

执行规则：
- 优先公司官网招聘页和权威招聘平台，避免仅依赖单一信息源。
- 每个目标岗位至少收集 20 条职位样本；不足时明确说明样本偏差。
- 记录每条样本的来源、发布日期、城市、岗位名称、薪资、核心技能要求。

建议搜索模板：
- `"{城市} {岗位} 招聘 要求 薪资 2026"`
- `"{公司名} careers {岗位关键词}"`
- `"{岗位关键词} JD 技能要求"`

### 3) 结构化岗位需求数据

将采集到的职位样本整理为 `csv/json/jsonl/txt`，再运行：

```bash
python scripts/extract_job_requirements.py --input job_posts.csv --output market_summary.json
```

脚本会输出：
- 高频技能（出现次数和占比）
- 经验要求分布
- 学历要求分布
- 薪资区间统计（可解析样本）
- 职位名称分布

### 4) 执行个人差距分析

准备用户画像 `profile.json` 后运行：

```bash
python scripts/gap_report.py --profile profile.json --market market_summary.json --output gap_report.md
```

脚本会输出：
- 关键技能差距（按市场出现频率排序）
- 经验差距与学历差距
- 目标薪资与市场中位区间差距
- 12 周行动计划草案

### 5) 形成职业规划交付物

按 [references/plan-template.md](references/plan-template.md) 输出最终方案，必须包含：
- 用户目标与约束条件
- 市场证据摘要（含日期和来源）
- 差距优先级（高/中/低）
- 1-3 个月、3-6 个月、6-12 个月计划
- 每周学习与求职动作
- 复盘检查点（每 2 周）

### 6) 质量约束

- 不编造岗位数据或薪资数据；数据缺失时明确写“不足”。
- 所有“最新趋势”结论都给出时间范围（例如“过去 60 天”）。
- 对高不确定性建议标注置信度（高/中/低）。
- 优先给出低成本且可执行的行动项。

## Resources

### references/
- `questionnaire.md`: 用户信息收集问题框架
- `job-source-strategy.md`: 招聘信息采集与来源优先级
- `plan-template.md`: 最终职业规划输出模板
- `tech-trends.md`: 技术趋势参考（仅作背景，不替代实时检索）
- `market-data-2026-02.md`: 北京AI/机器学习岗位最新市场数据（2026年2月）
- `profile-template.md`: 用户画像JSON模板
- `internship-sprint-plan.md`: 实习冲刺12周计划模板

### scripts/
- `extract_job_requirements.py`: 提取职位样本中的技能、经验、学历、薪资分布
- `gap_report.py`: 对比用户画像与市场摘要，生成 Markdown 差距报告

### profiles/
- 用户画像存储目录，每个用户一个 JSON 文件
- 格式见 `references/profile-template.md`

## 快速参考模板

### 实习冲刺场景（3-6个月）
用户目标：3个月找到实习 → 使用 `internship-sprint-plan.md` + `market-data-2026-02.md`

### 完整职业规划场景（6-12个月）
用户目标：长期规划 → 使用完整 6 步流程

## Defaults

- 默认覆盖互联网/软件/AI/数据岗位。
- 默认只分析 1 个主城市和 1 个目标岗位；用户明确要求时再扩展。
- 默认每 4-8 周复查一次市场变化并更新计划。
