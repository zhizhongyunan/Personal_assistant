# 用户信息收集问卷

按轮次提问，每轮 1-2 个问题。优先收集必须字段，再补充偏好信息。

## 必须字段（先收集）
1. 目标岗位是什么？（最多 2 个）
2. 目标城市是哪里？是否接受远程？
3. 当前经验年限是多少？（含实习）
4. 当前技能栈有哪些？（语言、框架、工具）
5. 目标薪资范围是什么？（税前月薪或年包，注明单位）
6. 每周可投入学习时间是多少小时？

## 补充字段（按需）
1. 最高学历和专业是什么？
2. 当前职位和行业是什么？
3. 可转移经验有哪些？（项目管理、业务理解、沟通协作等）
4. 学习方式偏好是什么？（视频/文档/实战/导师）
5. 时间限制和预算限制是什么？

## 记录格式（建议）
将已收集信息整理为如下 JSON，便于脚本复用：

```json
{
  "target_role": "ai engineer",
  "target_city": "shanghai",
  "remote_ok": true,
  "experience_years": 2.5,
  "education": "bachelor",
  "current_title": "backend engineer",
  "skills": ["python", "sql", "fastapi", "docker"],
  "target_salary_k": 40,
  "weekly_study_hours": 12,
  "deadline_months": 6
}
```
