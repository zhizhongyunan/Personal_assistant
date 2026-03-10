# 第三周 - 第八周：RAG 核心技术完整学习路线

> **学习目标**：4 周内从 RAG 入门到中阶，能独立搭建知识库问答系统
> **时间**：2026.03.10 - 2026.04.06
> **最终产出**：可展示的个人知识库问答项目（面试作品）

---

## 📚 整体学习路线（4 周）

```
Week 3: 向量数据库基础（入门）
    ↓
Week 4: Retriever 与检索优化（入门→中阶）
    ↓
Week 5: 高级 RAG 技巧（中阶）
    ↓
Week 6: RAG 项目实战 + LangChain 1.0 整合（中阶→熟练）
```

---

## 📖 Week 3: 向量数据库基础（入门）

### 🎯 学习目标
- 理解 RAG 核心概念和工作流程
- 掌握 Chroma 向量数据库使用
- 理解 Embedding 原理与选型
- 掌握文本分块（Chunking）策略
- **了解主流向量数据库选型对比（Chroma vs Qdrant vs Milvus）**

### 📋 具体知识点

#### 方向 1: RAG 核心概念
- RAG 是什么（Retrieval-Augmented Generation）
- RAG 解决了 LLM 的哪些问题（知识截止、私有数据、幻觉）
- RAG 完整工作流程（用户提问 → 检索 → 增强 → 生成）
- RAG vs Fine-tuning 的区别与适用场景

#### 方向 2: 向量数据库基础
- 向量是什么（文本 → 数值列表）
- 向量数据库与传统数据库的区别
- Chroma 的两种模式（Serverless vs Server）
- Chroma 安装与基本操作（创建、添加、检索、删除）
- 向量相似度概念（余弦相似度、欧氏距离、点积）

#### 方向 3: Embedding 原理与选型
- Embedding 工作原理
- Embedding 模型维度概念（768/1536/3072）
- OpenAI Embedding 模型对比（text-embedding-3-small/large）
- 免费中文 Embedding 模型（m3e-base、bge-large-zh）
- Embedding API 调用方式与错误处理

#### 方向 4: 文本分块（Chunking）策略
- 为什么需要分块（上下文限制、检索精度）
- 分块大小对检索效果的影响（太大/太小的问题）
- chunk_overlap 的作用（保持上下文连贯）
- 递归字符分块（RecursiveCharacterTextSplitter）
- 分隔符优先级设置（\n\n → \n → 。 → . → 空格）

#### 方向 5: 向量数据库选型对比（新增 - 技术广度）
- **Chroma**: 轻量级、适合本地开发和演示
  - 优点：简单易用、Python 原生、无需额外部署
  - 缺点：不适合高并发、大规模场景
- **Qdrant**: 生产级向量数据库
  - 优点：支持 HNSW 索引、过滤查询、REST/gRPC API
  - 缺点：需要额外部署（Docker/云服务）
- **Milvus**: 大规模分布式向量数据库
  - 优点：支持亿级向量、高可用、多语言 SDK
  - 缺点：部署复杂、资源消耗高
- **选型建议**:
  - 学习/原型：Chroma
  - 中小规模生产：Qdrant
  - 大规模/高并发：Milvus

### ✅ 量化标准
| 检查项 | 标准 |
|--------|------|
| 概念理解 | 能口述 RAG 工作流程，解释清楚向量检索原理 |
| Chroma 使用 | 能独立创建 Chroma 知识库，完成增删查操作 |
| Embedding 调用 | 能正确调用 Embedding API，理解维度选择 |
| Chunking 调优 | 能根据文档类型设置合适的 chunk_size 和 overlap |
| **数据库选型** | **能口述 Chroma vs Qdrant vs Milvus 的区别和适用场景** |
| 实战完成 | 完成本地 Chroma 知识库 Demo，能检索相关笔记 |

### 📝 面试常问问题

#### 🟢 基础题 (必须掌握 - 核心概念)
> **检查标准**: 能口述核心概念，解释清楚基本原理

- [ ] **Q1**: RAG 是什么？它解决了 LLM 的哪三个核心问题？
- [ ] **Q2**: 向量数据库与传统数据库（如 MySQL）的本质区别是什么？
- [ ] **Q3**: Embedding 的工作原理是什么？为什么语义相近的文本向量距离近？
- [ ] **Q4**: 什么是余弦相似度？它的取值范围和含义？
- [ ] **Q5**: 为什么 RAG 需要文本分块？不分块直接检索会有什么问题？
- [ ] **Q6**: `chunk_overlap` 的作用是什么？设置为 0 会怎样？
- [ ] **Q7**: 如何选择合适的 Embedding 模型？small 和 large 的区别？
- [ ] **Q8**: Chroma 的 Serverless 模式和 Server 模式有什么区别？

#### 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能解释清楚技术选型理由，理解参数调优逻辑

- [ ] **Q9**: chunk_size 设置太大或太小分别会导致什么问题？如何选择最优值？
- [ ] **Q10**: 递归字符分块的分隔符优先级为什么是 `["\n\n", "\n", "。", ".", " "]`？
- [ ] **Q11**: 向量检索返回的 `similarity_score` 代表什么？如何设置阈值过滤低质量结果？
- [ ] **Q12**: 如何处理长文档（如 10 万字小说）的向量化存储？
- [ ] **Q13**: Chroma 的 `persist_directory` 作用是什么？数据具体存在哪里？
- [ ] **Q14**: 批量添加文档 vs 单条添加，性能差异有多大？为什么？
- [ ] **Q15**: 如果 Embedding API 调用失败（网络/限额），应该如何处理？

#### 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解生产环境的挑战

- [ ] **Q16**: 如何设计一个支持多用户的 RAG 系统？（数据隔离、权限控制）
- [ ] **Q17**: 向量数据库的索引原理是什么？（HNSW、IVF 等）
- [ ] **Q18**: 如何评估 RAG 系统的检索效果？有哪些核心指标？
- [ ] **Q19**: 向量检索 + 关键词检索（Hybrid Search）的优势是什么？
- [ ] **Q20**: 如何设计向量数据库的备份与恢复策略？

---

## 📖 Week 4: Retriever 与检索优化（入门→中阶）

### 🎯 学习目标
- 掌握 Retriever 配置与优化
- 理解向量检索 + 关键词检索（Hybrid Search）
- 掌握 Rerank 重排序技术
- 实现检索准确率>80%

### 📋 具体知识点

#### 方向 1: Retriever 基础
- Retriever 是什么（检索器接口）
- VectorStoreRetriever 配置参数
- `search_kwargs` 参数详解（k、score_threshold、filter）
- 检索返回类型（Document 列表）
- Retriever 与 VectorStore 的关系

#### 方向 2: 检索策略与优化
- 稠密检索（向量检索）原理与优缺点
- 稀疏检索（BM25）原理与优缺点
- 为什么向量检索会漏掉关键信息
- 多路召回（Hybrid Search）工作原理
- 融合策略（RRF、加权融合）

#### 方向 3: Rerank 重排序
- 为什么需要 Rerank
- Rerank 模型工作原理（Cross-Encoder）
- 主流 Rerank 模型（Cohere、BGE-Reranker）
- Rerank 调用方式与时机
- Rerank 对检索效果的提升

#### 方向 4: 检索效果评估
- 召回率（Recall）概念
- 准确率（Precision）概念
- NDCG 指标
- 如何构建评估集
- 检索效果调优流程

#### 方向 5: RAGAS 自动化评估（新增 - 工业界标准）
- **RAGAS 框架介绍**
  - 什么是 RAGAS（Retrieval Augmented Generation Assessment）
  - 为什么需要自动化评估（人工评估成本高、不可持续）
- **核心评估指标**
  - Context Precision（上下文精确度）
  - Context Recall（上下文召回率）
  - Faithfulness（忠实度）- 答案是否忠于检索内容
  - Answer Relevance（答案相关性）- 答案是否回答用户问题
- **RAGAS 实战**
  - 安装与配置
  - 构建测试数据集（question, ground_truth, contexts, answer）
  - 运行自动化评估
  - 解读评估报告并优化

### ✅ 量化标准
| 检查项 | 标准 |
|--------|------|
| Retriever 配置 | 能熟练配置 retriever，理解 k 和 score_threshold |
| Hybrid Search | 能实现向量+BM25 多路召回 |
| Rerank 集成 | 能集成 Rerank 模型，提升检索排序质量 |
| 效果评估 | 能构建评估集，测试检索准确率>80% |
| **RAGAS 使用** | **能使用 RAGAS 进行自动化评估，输出 Faithfulness 等指标** |
| 实战完成 | 完成文档问答 Demo，能准确回答基于文档的问题 |

### 📝 面试常问问题

#### 🟢 基础题 (必须掌握 - 核心概念)
> **检查标准**: 能口述核心概念，解释清楚基本原理

- [ ] **Q1**: Retriever 和 VectorStore 的区别是什么？
- [ ] **Q2**: `search_kwargs={"k": 3}` 中的 `k` 代表什么？设置太大/太小的影响？
- [ ] **Q3**: 什么是向量检索（稠密检索）？它的优缺点？
- [ ] **Q4**: 什么是 BM25（稀疏检索）？它擅长什么场景？
- [ ] **Q5**: 为什么需要多路召回（Hybrid Search）？
- [ ] **Q6**: Rerank 的作用是什么？为什么检索后还需要重排序？
- [ ] **Q7**: Cross-Encoder 和 Bi-Encoder 的区别？
- [ ] **Q8**: `score_threshold` 的作用是什么？如何设置合理阈值？

#### 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能解释清楚技术选型理由，理解参数调优逻辑

- [ ] **Q9**: 如何融合向量检索和 BM25 的结果？（RRF、加权融合）
- [ ] **Q10**: Rerank 模型应该放在检索链路的哪个位置？为什么？
- [ ] **Q11**: 如何评估检索效果？构建评估集需要多少样本？
- [ ] **Q12**: 检索结果中包含不相关文档，如何过滤？
- [ ] **Q13**: 如何调试检索效果不好的问题？（系统化的 debug 流程）
- [ ] **Q14**: 元数据过滤（filter）的使用场景？（按时间、类型筛选）
- [ ] **Q15**: MMR（Maximal Marginal Relevance）是什么？解决什么问题？

#### 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解生产环境的挑战

- [ ] **Q16**: 如何设计一个支持实时更新的 RAG 系统？（增量索引）
- [ ] **Q17**: 大规模向量检索的优化策略？（10 亿 + 向量）
- [ ] **Q18**: 如何设计 RAG 系统的缓存层？（缓存检索结果）
- [ ] **Q19**: 多语言 RAG 系统如何设计？（跨语言检索）
- [ ] **Q20**: 如何保证检索结果的新鲜度？（文档更新后的处理）

---

## 📖 Week 5: 高级 RAG 技巧（中阶）

### 🎯 学习目标
- 掌握 Contextual Compression
- 掌握 Parent Document Retriever
- **理解 GraphRAG 基础概念（2025-2026 SOTA 范式）**
- **理解 Agentic RAG / Self-RAG 概念**
- 能优化复杂场景下的检索效果

### 📋 具体知识点

#### 方向 1: Contextual Compression
- 什么是 Contextual Compression
- LLMChainExtractor 工作原理
- 如何压缩检索结果（保留关键信息）
- 压缩对 Token 消耗的影响
- 压缩器的配置与调优

#### 方向 2: Parent Document Retriever
- Parent Document Retriever 工作原理
- 父子文档关系设计
- 小 chunk 检索，大 chunk 注入原理
- 如何平衡检索精度与上下文完整性
- 实现方式与配置

#### 方向 3: 多路召回进阶
- 多向量检索（Multi-Query）
- 假设性问题生成（HyDE）
- 检索查询改写（Query Rewriting）
- 自适应检索策略
- 多路结果融合策略优化

#### 方向 4: 检索失败处理
- 检索结果为空的处理
- 低相似度结果的处理
- 降级策略（fallback）
- 错误日志与监控
- 用户反馈收集与优化

#### 方向 5: GraphRAG 基础（新增 - 2025-2026 SOTA）
- **GraphRAG 是什么（Microsoft 提出）**
  - 知识图谱 + RAG 的结合
  - 解决传统 RAG 的全局理解能力不足
- **核心概念**
  - 实体提取（Entity Extraction）
  - 关系抽取（Relation Extraction）
  - 社区发现（Community Detection）
  - 全局摘要（Global Summary）
- **适用场景**
  - 多跳推理（Multi-hop Reasoning）
  - 全局摘要类问题
  - 跨文档关联查询
- **面试话术**: "除了传统向量检索，我还研究过 GraphRAG 来解决全局理解和多跳推理问题"

#### 方向 6: Agentic RAG（新增 - 2025-2026 趋势）
- **Agentic RAG 是什么**
  - 让 Agent 自主决定何时检索、检索什么
  - 自我反思检索结果质量
- **Self-RAG / Corrective RAG**
  - 让 LLM 生成"检索令牌"（Retrieval Token）
  - 自主判断是否需要检索
  - 评估检索结果质量（Relevant / Irrelevant）
  - 支持多轮检索迭代
- **核心流程**
  1. 判断是否需要检索
  2. 执行检索
  3. 评估检索结果质量
  4. 如果质量差，重新检索或使用其他方式
  5. 生成最终答案
- **面试话术**: "我实现过 Self-RAG 逻辑，让模型具备自我反思能力，减少幻觉"

### ✅ 量化标准
| 检查项 | 标准 |
|--------|------|
| Compression | 能使用 LLMChainExtractor 压缩检索结果 |
| Parent Retriever | 能实现父子文档检索策略 |
| Query 改写 | 能实现 HyDE 或多查询改写 |
| 失败处理 | 能处理检索为空的边界情况 |
| **GraphRAG 理解** | **能口述 GraphRAG 原理和适用场景** |
| **Agentic RAG 理解** | **能口述 Self-RAG 工作流程** |
| 效果提升 | 相比 Week 4，检索准确率提升 10%+ |

### 📝 面试常问问题

#### 🟢 基础题 (必须掌握 - 核心概念)
> **检查标准**: 能口述核心概念，解释清楚基本原理

- [ ] **Q1**: Contextual Compression 是什么？它解决了什么问题？
- [ ] **Q2**: Parent Document Retriever 的核心思想是什么？
- [ ] **Q3**: 为什么"小 chunk 检索，大 chunk 注入"能提升效果？
- [ ] **Q4**: 什么是 HyDE（Hypothetical Document Embeddings）？
- [ ] **Q5**: Multi-Query 的工作原理是什么？
- [ ] **Q6**: 检索结果为空时，应该如何处理？
- [ ] **Q7**: 什么是查询改写（Query Rewriting）？有什么作用？
- [ ] **Q8**: 如何判断检索结果质量是否足够好？

#### 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能解释清楚技术选型理由，理解参数调优逻辑

- [ ] **Q9**: LLMChainExtractor 和简单的截取前 N 个字符有什么区别？
- [ ] **Q10**: Parent Document Retriever 中，父子 chunk 大小如何选择？
- [ ] **Q11**: HyDE 为什么能提升检索效果？它在什么场景下会失效？
- [ ] **Q12**: 多路召回的结果融合策略有哪些？（RRF、加权、LLM 融合）
- [ ] **Q13**: 如何设计一个智能的降级策略？（什么时候不用 RAG）
- [ ] **Q14**: 如何收集用户反馈来优化检索效果？
- [ ] **Q15**: 如何处理检索结果中的重复内容？

#### 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解生产环境的挑战

- [ ] **Q16**: 如何设计 RAG 系统的 A/B 测试框架？
- [ ] **Q17**: 如何实现 RAG 系统的可观测性？（追踪检索→生成全链路）
- [ ] **Q18**: 如何设计一个自学习的 RAG 系统？（基于反馈自动优化）
- [ ] **Q19**: 大规模场景下，如何优化 RAG 的延迟？（并行检索、缓存）
- [ ] **Q20**: 如何设计 RAG 系统的安全防护？（防止注入攻击、数据泄露）

---

## 📖 Week 6: RAG 项目实战 + LangChain 1.0 整合（中阶→熟练）

### 🎯 学习目标
- 完成完整的 RAG 项目（个人知识库问答）
- 结合 LangChain 1.0 Middleware
- API 封装与部署
- 项目文档完善（可作为面试作品）

### 📋 具体知识点

#### 方向 1: 完整项目架构
- 项目目录结构设计
- 模块化设计（loader、splitter、retriever、generator）
- 配置文件管理（Hydra/YAML）
- 日志与监控
- 错误处理与重试

#### 方向 2: 文档加载与预处理
- 多种文档格式支持（PDF、TXT、Markdown、Word）
- 文档清洗（去除无关内容、格式统一）
- 元数据提取与标注
- 批量处理与增量更新
- 文档版本管理

#### 方向 3: 复杂数据处理（新增 - 企业痛点）
- **PDF 表格处理方案**
  - 为什么表格难以处理（多栏、合并单元格）
  - 表格结构化解析工具
    - Unstructured.io（推荐）
    - Camelot（专门表格提取）
    - pdfplumber（Python 库）
  - 表格转文本策略
    - Markdown 表格格式
    - HTML 表格格式
    - 描述性文本（将表格转为自然语言描述）
- **图片内容处理**
  - 图片转描述性文本（Image Captioning）
  - 使用多模态模型（如 GPT-4V）生成图片描述
  - 将描述性文本进行 Embedding
- **实战要求**: 项目中必须包含一个带有复杂表格的 PDF 文档，展示完整处理流程

#### 方向 3: LangChain 1.0 整合
- 使用 `create_agent` 整合 RAG
- 添加 Retry Middleware
- 添加日志 Middleware
- 使用 context_schema 管理会话
- 结构化输出配置

#### 方向 4: API 封装与部署
- FastAPI 基础
- RAG API 设计（/ask、/upload、/search）
- 异步并发处理
- Docker 容器化部署
- 性能优化与压测

#### 方向 5: 部署与进阶（新增）
- **Serverless 部署简介**
  - Vercel / AWS Lambda 部署流程
  - Serverless 优缺点分析
  - 成本对比（Serverless vs 传统服务器）
- **GPU 加速推理配置**
  - 什么时候需要 GPU（Embedding 模型、Rerank 模型）
  - GPU 云服务器配置（AutoDL、阿里云）
  - 推理加速技巧（批处理、缓存）
- **技术选型对比表**
  | 部署方式 | 适合场景 | 成本 | 难度 |
  |----------|----------|------|------|
  | 本地运行 | 学习/原型 | 低 | 简单 |
  | Docker 部署 | 中小规模 | 中 | 中等 |
  | Serverless | 间歇性使用 | 按量付费 | 简单 |
  | GPU 云服务 | 大规模推理 | 高 | 中等 |

### ✅ 量化标准
| 检查项 | 标准 |
|--------|------|
| 项目完整度 | 包含文档上传、向量化、检索、问答完整流程 |
| 代码质量 | 模块化设计，有类型注解，有错误处理 |
| 文档完善度 | 有 README、API 文档、部署指南 |
| 性能指标 | 响应时间<3s，支持并发请求 |
| 可展示性 | 可作为面试作品，能演示完整功能 |
| **复杂数据处理** | **能处理带表格的 PDF，展示表格转文本流程** |
| **部署能力** | **了解 Serverless 部署和 GPU 加速配置** |

### 📝 面试常问问题

#### 🟢 基础题 (必须掌握 - 核心概念)
> **检查标准**: 能口述核心概念，解释清楚基本原理

- [ ] **Q1**: 描述一下你做的 RAG 项目的整体架构？
- [ ] **Q2**: 你的项目支持哪些文档格式？如何处理不同格式？
- [ ] **Q3**: 文档上传后，完整的处理流程是什么？
- [ ] **Q4**: 你是如何处理检索结果为空的情况的？
- [ ] **Q5**: 你的系统如何处理并发请求？
- [ ] **Q6**: 如何保证不同用户之间的数据隔离？
- [ ] **Q7**: 你的项目中，chunk_size 设置为多少？为什么？
- [ ] **Q8**: 如何评估你的 RAG 系统的效果？

#### 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能解释清楚技术选型理由，理解参数调优逻辑

- [ ] **Q9**: 如果用户反馈回答不准确，你如何定位问题？（检索问题 vs 生成问题）
- [ ] **Q10**: 你的系统如何处理文档更新？（增量索引 vs 全量重建）
- [ ] **Q11**: 如何优化 RAG 系统的响应延迟？
- [ ] **Q12**: 你使用了哪些 Middleware？它们分别解决了什么问题？
- [ ] **Q13**: 如何防止 RAG 系统的注入攻击？（用户输入恶意 Prompt）
- [ ] **Q14**: 如何设计 RAG 系统的缓存策略？
- [ ] **Q15**: 如何处理长文档（如 100 页 PDF）的检索？

#### 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解生产环境的挑战

- [ ] **Q16**: 如果你的 RAG 系统要支持 10 万用户，架构上需要做什么改动？
- [ ] **Q17**: 如何设计 RAG 系统的监控告警？（哪些指标需要监控）
- [ ] **Q18**: 如何设计一个多租户的 RAG SaaS 系统？
- [ ] **Q19**: 如何保证 RAG 系统的回答不包含敏感信息？
- [ ] **Q20**: 如果让你重新设计这个系统，你会做什么改进？

---

## 📊 学习进度追踪

### 总体进度

| 周次 | 主题 | 时间 | 状态 |
|------|------|------|------|
| Week 3 | 向量数据库基础 | 第 1 周 | ⏳ 进行中 |
| Week 4 | Retriever 与检索优化 | 第 2 周 | ⏳ 待开始 |
| Week 5 | 高级 RAG 技巧 | 第 3 周 | ⏳ 待开始 |
| Week 6 | RAG 项目实战 | 第 4 周 | ⏳ 待开始 |

### 每周检查清单

#### Week 3 检查项
- [ ] 理解 RAG 工作流程
- [ ] Chroma 安装与基本使用
- [ ] Embedding 模型调用
- [ ] Chunking 参数实验
- [ ] 完成本地知识库 Demo

#### Week 4 检查项
- [ ] Retriever 配置熟练
- [ ] 实现 Hybrid Search
- [ ] 集成 Rerank 模型
- [ ] 构建检索评估集
- [ ] 检索准确率>80%

#### Week 5 检查项
- [ ] 使用 Contextual Compression
- [ ] 实现 Parent Document Retriever
- [ ] 实现 Query 改写（HyDE/Multi-Query）
- [ ] 处理检索失败边界情况
- [ ] 检索准确率提升 10%+

#### Week 6 检查项
- [ ] 完成完整 RAG 项目
- [ ] 整合 LangChain 1.0 Middleware
- [ ] API 封装与测试
- [ ] 项目文档完善
- [ ] 可展示为面试作品
- [ ] **完成复杂数据处理（PDF 表格解析）**
- [ ] **了解 Serverless 部署和 GPU 加速配置**

---

## 🔗 学习资源

### 核心教程
| 资源 | 链接 |
|------|------|
| LangChain RAG 教程 | https://docs.langchain.com/oss/python/langchain/tutorials/rag |
| Chroma 官方文档 | https://docs.trychroma.com/ |
| LangChain 向量数据库 | https://docs.langchain.com/oss/python/integrations/vectorstores/chroma |
| Embedding 最佳实践 | https://platform.openai.com/docs/guides/embeddings |
| RAG 技术综述 | https://arxiv.org/abs/2312.10997 |

### 高级主题（2025-2026 SOTA）
| 资源 | 链接 | 说明 |
|------|------|------|
| **RAGAS 评估框架** | https://github.com/explodinggradients/ragas | 必学 - 工业界标准评估工具 |
| **Microsoft GraphRAG** | https://github.com/microsoft/graphrag | 选学 - 了解知识图谱+RAG |
| **GraphRAG 论文** | https://arxiv.org/abs/2404.16130 | 选学 - 全局理解能力 |
| **Self-RAG 论文** | https://arxiv.org/abs/2310.11511 | 选学 - 自我反思 RAG |
| **Qdrant 向量数据库** | https://qdrant.tech/ | 了解 - 生产级向量数据库 |
| **Milvus 向量数据库** | https://milvus.io/ | 了解 - 大规模分布式 |
| Unstructured.io | https://unstructured.io/ | 复杂文档解析（PDF 表格） |
| LlamaIndex RAG | https://docs.llamaindex.ai/ | 参考 - 另一种 RAG 实现 |

### 实战项目参考
| 资源 | 链接 |
|------|------|
| LangChain Chat with PDF | https://github.com/langchain-ops/chat-with-pdf |
| RAG 知识库实战 | https://github.com/chainlit/chainlit |
| Dify（开源 RAG 平台） | https://github.com/langgenius/dify |

---

*更新时间：2026-03-11*
*版本：RAG 完整学习路线（4 周版）- 2026 最新优化版*

---

## 📝 更新日志

### 2026-03-11 优化（本次更新）

根据 2025-2026 年 RAG 技术发展趋势，增加以下内容：

| 周次 | 新增内容 | 重要程度 |
|------|----------|----------|
| Week 3 | 向量数据库选型对比（Chroma vs Qdrant vs Milvus） | ⭐⭐⭐ |
| Week 4 | RAGAS 自动化评估框架 | ⭐⭐⭐⭐⭐ |
| Week 5 | GraphRAG 基础（知识图谱+RAG） | ⭐⭐⭐⭐ |
| Week 5 | Agentic RAG / Self-RAG 概念 | ⭐⭐⭐⭐ |
| Week 6 | 复杂数据处理（PDF 表格解析） | ⭐⭐⭐⭐⭐ |
| Week 6 | Serverless 部署与 GPU 加速简介 | ⭐⭐ |

**面试话术升级**：
- "除了传统向量检索，我还研究过 GraphRAG 来解决全局理解和多跳推理问题"
- "我实现过 Self-RAG 逻辑，让模型具备自我反思能力，减少幻觉"
- "我使用 RAGAS 构建自动化评估流水线，评估 Faithfulness 和 Answer Relevance"
