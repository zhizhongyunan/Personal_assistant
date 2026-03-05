# 用户画像模板

## 用途
用于收集用户职业规划相关信息，保存为 JSON 格式供后续分析和计划生成使用。

## 必填字段

```json
{
  "profile_id": "user_001",
  "created_at": "2026-02-28",
  "target_role": ["AI算法工程师", "后端开发"],
  "target_city": "北京",
  "remote_ok": false,
  "experience_years": 0,
  "education": "硕士在读",
  "graduation_year": 2027,
  "current_skills": {
    "programming": ["Python", "Java"],
    "ml_dl": ["机器学习基础", "深度学习基础"],
    "tools": ["Linux基础", "Git基础"]
  },
  "target_salary_min_k": 15,
  "target_salary_max_k": 25,
  "weekly_study_hours": 20,
  "timeline_months": 12,
  "goal": "暑期实习"
}
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| profile_id | string | 是 | 用户唯一标识 |
| created_at | string | 是 | 创建日期 YYYY-MM-DD |
| target_role | array | 是 | 目标岗位，最多2个 |
| target_city | string | 是 | 目标城市 |
| remote_ok | boolean | 否 | 是否接受远程 |
| experience_years | number | 是 | 工作年限（含实习） |
| education | string | 是 | 学历 |
| graduation_year | number | 否 | 毕业年份（学生） |
| current_skills | object | 是 | 当前技能栈 |
| target_salary_min_k | number | 否 | 期望月薪下限（千） |
| target_salary_max_k | number | 否 | 期望月薪上限（千） |
| weekly_study_hours | number | 是 | 每周可投入学习时间 |
| timeline_months | number | 是 | 计划周期（月） |
| goal | string | 否 | 目标（实习/全职/跳槽） |

## current_skills 子字段

| 子字段 | 类型 | 说明 |
|--------|------|------|
| programming | string[] | 编程语言 |
| ml_dl | string[] | 机器学习/深度学习相关 |
| frameworks | string[] | 框架（PyTorch/TensorFlow等） |
| tools | string[] | 工具（Docker/Git/SQL等） |
| other | string[] | 其他技能 |

## 使用示例

### 学生案例（研一）

```json
{
  "profile_id": "user_002",
  "created_at": "2026-02-28",
  "target_role": ["AI算法工程师"],
  "target_city": "北京",
  "remote_ok": false,
  "experience_years": 0,
  "education": "硕士在读",
  "graduation_year": 2027,
  "current_skills": {
    "programming": ["Python", "Java"],
    "ml_dl": ["机器学习", "深度学习", "神经网络", "决策树"],
    "tools": ["Linux", "Git"]
  },
  "target_salary_min_k": 15,
  "target_salary_max_k": 25,
  "weekly_study_hours": 20,
  "timeline_months": 12,
  "goal": "暑期实习"
}
```

### 社招案例（3年经验）

```json
{
  "profile_id": "user_003",
  "created_at": "2026-02-28",
  "target_role": ["机器学习工程师", "后端开发"],
  "target_city": "北京",
  "remote_ok": true,
  "experience_years": 3,
  "education": "硕士",
  "current_skills": {
    "programming": ["Python", "Java", "Go"],
    "ml_dl": ["TensorFlow", "XGBoost"],
    "frameworks": ["Django", "Flask"],
    "tools": ["MySQL", "Redis", "Docker", "K8s"]
  },
  "target_salary_min_k": 35,
  "target_salary_max_k": 50,
  "weekly_study_hours": 15,
  "timeline_months": 6,
  "goal": "跳槽升级"
}
```

## 保存位置

用户画像保存路径：
```
.claude/skills/career-planner/profiles/{profile_id}.json
```

## 下一步

创建用户画像后，可用于：
1. 与市场数据对比，生成差距报告
2. 生成个性化学习计划
3. 生成求职时间线