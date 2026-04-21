# Multi-Agent Research Paper Writing Skill

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Stage](https://img.shields.io/badge/Stage-7%20phase%20pipeline-orange)
![Standard](https://img.shields.io/badge/Standard-IEEE%2FACM-green)
![Platform](https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20Hermes%20%7C%20WorkBuddy-purple)

面向 IEEE/ACM 顶会顶刊的学术论文写作 Skill，采用 **Agent Teams** 多智能体协作架构。从选题到引用终审，全流程自动化。

**v2.0.0** 新增跨平台支持（Claude Code / Hermes Agent / WorkBuddy）、多干预模式、研究决策点、知识综合、反伪造验证等 22 项功能改进。

---

## 目录

- [核心架构](#核心架构)
- [跨平台支持](#跨平台支持)
- [快速开始](#快速开始)
- [七阶段流水线](#七阶段流水线)
- [Agent 角色](#agent-角色)
- [干预模式](#干预模式)
- [子技能模块](#子技能模块)
- [目录结构](#目录结构)
- [设计原则](#设计原则)
- [伦理准则](#伦理准则)
- [版本历史](#版本历史)
- [致谢](#致谢)

---

## 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 1: Brainstorming                       │
│              Main Agent + User 对话确认选题/方法/结构              │
│              ← 新增：干预模式选择 + 问题分解                      │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Stage 2: Deep Search                      │
│                    DeepSearch Agent                              │
│        多数据库文献搜索 + RelatedWork + 知识卡片 + 研究空白       │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stage 2.5: Knowledge Synthesis ← 新增           │
│               聚类分析 / 矛盾映射 / 缺口排序 / 研究定位          │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Stage 3: Writing                        │
│                       Writing Agent                               │
│            按章节撰写论文 + 两阶段章节 Review                      │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Stage 4: Experiment & Audit                   │
│              Experiment Agent + Audit Agent                       │
│     仿真实验(含自修复) + 审查验证 + 声明-数据交叉验证              │
│              ← 新增：决策门 PROCEED/REFINE/PIVOT                  │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stage 5: Triple Review & Revision                │
│              3× Reviewer Agent + Writing Agent                    │
│         三视角独立审稿（方法论/创新性/表达）+ 综合修改               │
│              ← 新增：修订后长度守卫 + 论文-证据一致性检查           │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Stage 6: Citation Audit                     │
│                       Audit Agent                                 │
│     引用终审（四层验证：CrossRef + Semantic Scholar + arXiv）      │
└─────────────────────────────────────────────────────────────────┘
```

**特点：**
- 每个阶段有 **HARD-GATE** 门禁，支持 4 种干预模式
- 所有审查结论必须基于**证据**而非"应该"、"看起来"
- 三审并行（Team 模式）确保独立性
- **跨平台**：Claude Code / Hermes Agent / WorkBuddy 三平台兼容

---

## 跨平台支持

| 平台 | 厂商 | Skill 格式 | 特色能力 |
|------|------|-----------|---------|
| **Claude Code** | Anthropic | Markdown SKILL.md | Team mode 多 Agent 协作 |
| **Hermes Agent** | Nous Research | Markdown (name + description + steps) | 自我学习循环，渐进式加载 |
| **WorkBuddy** | Tencent | Skill 包 + MCP 协议 | 企业集成（企微/飞书/钉钉），20+ 内置 Skills |

**兼容设计：**
- 统一元数据头：每个 SKILL.md 包含三平台兼容的 frontmatter
- MCP Server 定义：`mcp/` 目录下 4 个 JSON 文件，WorkBuddy 可直接调用
- 自我学习钩子：所有 Agent 输出含 Learning Feedback 区，Hermes 可消化
- 模块化子 Skill：每个阶段可独立使用，不依赖完整管道

---

## 快速开始

### 安装

```bash
# Claude Code
git clone https://github.com/ljxangus/writing-paper-team-skill.git \
  ~/.claude/skills/writing-paper-team-skill

# WorkBuddy
git clone https://github.com/ljxangus/writing-paper-team-skill.git \
  ~/.workbuddy/skills/writing-paper-team-skill

# Hermes Agent
git clone https://github.com/ljxangus/writing-paper-team-skill.git \
  ~/.hermes/skills/writing-paper-team-skill
```

### 使用流程

1. **激活 Skill**：输入论文写作需求
2. **Stage 1 对话**：确认论文类型、目标期刊、研究主题、干预模式
3. **自动执行**：Agent Teams 接管后续所有阶段
4. **用户确认**：根据干预模式在关键节点暂停确认
5. **交付输出**：完整论文草稿 + 审稿报告 + Response Letter

---

## 七阶段流水线

### Stage 1 — Brainstorming & Planning

主 Agent 与用户对话，确认：
- 论文类型（会议/期刊）
- 目标会议或期刊（IEEE/ACM）
- 研究主题与核心问题
- 技术路线与方法
- 章节结构
- **干预模式**（supervised / auto-approve / checkpoint / co-pilot）
- **问题分解**（生成结构化问题树 → `plan/problem-tree.md`）

> ⚠️ **HARD-GATE**：用户确认前禁止写任何正文内容。

### Stage 2 — Deep Search

DeepSearch Agent 执行：
- 多数据库文献搜索（Semantic Scholar / CrossRef / arXiv / PubMed）
- 高相关性论文筛选（相关性评分 ≥ 7/10）
- **知识卡片**提取（结构化跨论文对比数据）
- RelatedWork 按主题分类
- 研究空白识别

> ⚠️ **HARD-GATE**：至少 15 篇高相关性论文 + DOI 全验证。

### Stage 2.5 — Knowledge Synthesis（新增）

对收集的文献进行综合分析：
- 文献按主题/方法**聚类**
- 识别文献间的**矛盾和分歧**
- 按影响/可行性/相关性**排序研究缺口**
- 明确本研究定位

输出到 `plan/research-gaps.md`。

### Stage 3 — Writing

Writing Agent 按章节撰写：
- Introduction → Related Work → Methodology → Experiment → Discussion → Conclusion → Abstract
- 每章写完执行两阶段 Review
- 用户逐章确认

**两阶段 Review：**
| 阶段 | 检查维度 |
|------|----------|
| 阶段一：规范合规 | 字数/结构/引用格式/图表编号/参考文献完整性 |
| 阶段二：质量深入 | 去AI化/学术表达/引用可追溯/连贯叙述 |

### Stage 4 — Experiment & Audit

Experiment Agent：
- 仿真方案设计（三阶段代码生成：架构→依赖序→预验证）
- 代码编写与执行
- **自修复循环**（代码失败时自动诊断修复，最多 3 轮）
- **数据集发现管道**（自动搜索公开数据集）
- 结果图表生成

Audit Agent：
- 实验设计与论文声称一致性
- 数据合理性验证
- **声明-数据交叉验证**（`scripts/claim_verify.py`）
- 可复现性确认
- 统计有效性审查
- **决策门建议**：PROCEED / REFINE / PIVOT

> ⚠️ **HARD-GATE**：审查不通过则退回修改，最多 3 轮。
> **决策门**：审查通过后根据实验结果判断继续/调参/转向。

### Stage 5 — Triple Review & Revision

三名 Reviewer Agent 并行独立审稿：

| Reviewer | 视角 | 侧重维度 |
|----------|------|----------|
| Reviewer 1 | 方法论严谨性 | 实验设计、统计方法、可复现性、威胁分析 |
| Reviewer 2 | 创新性与贡献 | 新颖性、技术贡献、与现有工作区分 |
| Reviewer 3 | 表达与呈现 | 写作质量、图表清晰度、结构逻辑 |

每名 Reviewer 执行两阶段审稿（含**论文-证据一致性检查**），Writing Agent 综合意见修改并生成 Response Letter。

**修订后长度守卫**：修改完成后自动检查总词数变化（±20% 警告）。

### Stage 6 — Citation Audit

Audit Agent 引用终审：
- **四层引用验证**：CrossRef + Semantic Scholar + arXiv + 格式一致性
- 作者/年份准确性交叉验证
- 引用格式统一性检查
- 正文-文献列表双向对应检查

> ⚠️ **HARD-GATE**：最终门禁，不可跳过。

---

## Agent 角色

| Agent | Stage | 核心职责 | 输出产物 |
|-------|-------|----------|----------|
| DeepSearch Agent | 2 | 文献搜索 + 知识卡片 + RelatedWork + 研究空白 | `related-work.md`, `papers/*.json` |
| Writing Agent | 3, 5 | 论文章节写作 + 综合修改 | `chapters/*.md` |
| Experiment Agent | 4 | 仿真实验（含自修复 + 数据集发现 + 三阶段代码生成） | `experiments/` |
| Audit Agent | 4, 6 | 实验审查 + 决策门 + 声明验证 + 引用终审 | `audit-report.md` |
| Reviewer ×3 | 5 | IEEE/ACM 标准独立审稿（含论文-证据一致性） | `review-*.md` |
| Hypothesis Debate | 1.5 | Proponent/Skeptic 双 Agent 假设辩论 | `plan/hypothesis-debate.md` |

### Audit Agent — 五步验证门控

> **声称完成而没有验证，是不诚实的表现。**

| Step | 操作 |
|------|------|
| Step 1 | 确认 — 什么命令/操作能证明这个声称？ |
| Step 2 | 执行 — 运行完整的验证操作 |
| Step 3 | 读取 — 完整输出，检查结果 |
| Step 4 | 验证 — 输出是否确认声称？ |
| Step 5 | 然后才能 — 做出声称 |

---

## 干预模式

在 Stage 1 选择干预模式，控制 Agent 自主程度：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `supervised`（默认） | 每个 HARD-GATE 暂停等待用户确认 | 初次使用、重要论文 |
| `auto-approve` | 自动通过 HARD-GATE，运行检查并记录 | 经验用户、快速迭代 |
| `checkpoint` | 仅在阶段边界暂停，章节间不暂停 | 中等信心、时间紧迫 |
| `co-pilot` | 关键阶段人工审批，其余自动 | 日常使用推荐 |

**SmartPause**：在 auto-approve/co-pilot 模式下，Agent 信心度为 `low` 时自动暂停通知用户。

---

## 子技能模块

### 核心流程技能

| 技能 | 路径 | 说明 |
|------|------|------|
| **latex-output** | `skills/latex-output/` | LaTeX 输出：模板解析 → Markdown→LaTeX 转换 → IEEEtran/acmart 适配 → XeLaTeX 编译 |
| **prompts-collection** | `skills/prompts-collection/` | 8 大类提示词：翻译 / 润色 / 去AI化 / 扩写缩写 / 逻辑检查 / 图表标题 |
| **figures-python** | `skills/figures-python/` | 顶刊配色 + 6 种图表模板 + 450 DPI 双格式输出 |
| **statistical-analysis** | `skills/statistical-analysis/` | 统计检验决策表 + 假设检验 + 效应量 + APA 报告 |

### 独立子技能（可脱离完整管道单独使用）

| 技能 | 路径 | 说明 |
|------|------|------|
| **literature-search** | `skills/literature-search/` | 独立文献搜索与 RelatedWork 分析 |
| **paper-drafting** | `skills/paper-drafting/` | 独立论文起草与章节写作 |
| **experiment-runner** | `skills/experiment-runner/` | 独立仿真实验设计与执行 |
| **peer-review** | `skills/peer-review/` | 独立同行评审 |
| **citation-audit** | `skills/citation-audit/` | 独立引用审计 |

---

## 目录结构

```
writing-paper-team-skill/
├── SKILL.md                           # 主入口（Skill 定义 + 七阶段编排）
├── README.md                          # 本文件
├── ETHICS.md                          # 伦理准则（AI披露/人工监督/引用诚信）
│
├── references/                        # Agent 角色定义与参考文档
│   ├── agent-deep-search.md           # DeepSearch Agent（含知识卡片 + 信心度）
│   ├── agent-writing.md               # Writing Agent（含长度守卫）
│   ├── agent-experiment.md            # Experiment Agent（含自修复 + 数据集发现 + 三阶段代码生成）
│   ├── agent-audit.md                 # Audit Agent（含决策门 + 声明验证）
│   ├── agent-reviewer.md              # Reviewer Agent（含论文-证据一致性检查）
│   ├── agent-hypothesis-debate.md     # 假设辩论 Agent（Proponent/Skeptic）
│   ├── writing-standards.md           # 去AI化写作标准 + 反免责声明
│   └── ieee-acm-rubric.md             # IEEE/ACM 审稿评分标准
│
├── scripts/                           # 工具脚本
│   ├── scholar_search.py              # 多数据库文献搜索
│   ├── citation_verify.py             # 四层引用验证（CrossRef + Semantic Scholar + arXiv + 格式）
│   ├── claim_verify.py                # 反伪造：论文声称-实验数据交叉验证
│   ├── style_check.sh                 # 去AI化 + 反免责声明风格检查
│   └── manifest.py                    # 可复现性校验和（SHA256）
│
├── mcp/                               # MCP Server 定义（WorkBuddy 兼容）
│   ├── scholar_search.json
│   ├── citation_verify.json
│   ├── style_check.json
│   └── claim_verify.json
│
├── skills/                            # 子技能模块
│   ├── latex-output/SKILL.md
│   ├── prompts-collection/SKILL.md
│   ├── figures-python/SKILL.md
│   ├── statistical-analysis/SKILL.md
│   ├── literature-search/SKILL.md     # 独立文献搜索
│   ├── paper-drafting/SKILL.md        # 独立论文起草
│   ├── experiment-runner/SKILL.md     # 独立实验执行
│   ├── peer-review/SKILL.md           # 独立同行评审
│   └── citation-audit/SKILL.md        # 独立引用审计
│
├── assets/                            # 模板与资源
│   ├── chapter-templates/
│   │   ├── conference-paper.md
│   │   └── journal-article.md
│   └── templates/
│       ├── problem-tree.md            # 问题分解模板
│       ├── research-gaps.md           # 知识综合缺口分析模板
│       └── branch-log.md              # 管道分支并行探索模板
│
├── lessons-learned/                   # 跨项目学习（Hermes Agent 兼容）
│   └── README.md
│
└── latex-templates/                   # 用户 LaTeX 模板存放目录
    └── README.md
```

---

## 设计原则

### 流程优于即兴
门禁未开不推进，结构未定不写作。每个阶段有明确的输入、输出和门禁条件。

### 证据优于声称
- 引用必须可追溯：DOI/API 验证，不编造文献
- 数据必须可验证：实验代码 + 原始数据 + 结果图表
- 审查结论有证据：不使用"应该"、"看起来"

### 协作优于独断
- 三审并行：方法论/创新性/表达三视角独立
- Agent 分工：每个 Agent 专注单一职责
- 团队弥补单点盲区

### 简洁优于复杂
- 去AI化写作：禁用机械过渡词、空壳强调句
- 段落连贯叙述：不使用列表堆砌
- 学术客观表述：长短句交替

### 确认优于假设
- 每章用户确认：避免大规模返工
- 进度透明追踪：每阶段更新 progress.md
- 断点续作支持：从任意断点恢复

---

## 去AI化写作

### 禁用词表

**AI 高频词（英文）：**

| ❌ 禁用 | ✅ 替代 |
|--------|--------|
| leverage | use, employ |
| delve into | examine, analyze |
| comprehensive | complete, thorough |
| multifaceted | complex, multi-step |
| pivotal | key, central |
| notably | specifically, in particular |
| underscores | shows, demonstrates |
| landscape | area, domain |
| showcase | show, demonstrate |
| facilitate | enable, allow |

**机械过渡词：**

| ❌ 禁用 | ✅ 替代 |
|--------|--------|
| firstly, secondly, lastly | 自然过渡 |
| moreover, furthermore | 直接陈述 |
| in conclusion | 直接总结 |

详见 `references/writing-standards.md`

**防御性语言检测（v2.0 新增）：**

| ❌ 禁用 | 原因 |
|--------|------|
| to the best of our knowledge | 直接声明事实即可 |
| arguably / presumably | 如不确定则不应声称 |
| it is generally accepted that | 需引用证据支撑 |
| one could argue that | 直接反驳或论证 |

---

## 伦理准则

所有使用本 Skill 生成的论文须遵守 `ETHICS.md` 中的伦理规范：

- **AI 披露**：论文中须注明 AI 辅助写作
- **人工监督**：所有研究决策须由人类作者做出
- **引用诚信**：绝不编造文献，AI 建议的引用须人工验证
- **数据诚信**：不捏造/篡改数据，如实报告负面结果
- **反滥用**：禁止用于掠夺性发表或论文工厂

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v2.0.0 | 2026-04-22 | **跨平台三平台兼容**（Claude Code / Hermes Agent / WorkBuddy）+ 22 项功能改进：多干预模式 / 研究决策点 / 问题分解 / 实验自修复 / 知识卡片 / 知识综合 / 反伪造验证 / 假设辩论 / SmartPause / 成本防护 / 伦理准则 / 四层引用验证 / 跨项目学习 等 |
| v1.1.0 | 2026-04-21 | 新增 latex-output / prompts-collection / figures-python / statistical-analysis 子技能；强化 Audit Agent 五步验证门控；强化 Reviewer Agent 两阶段审稿；latex-templates 目录 |
| v1.0.0 | 2026-04-10 | 初始版本：六阶段 Agent Teams 流水线 + 三审机制 |

---

## 致谢

本 Skill 基于以下开源项目改造：

- [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill) v3.1.0 — 单 Agent 写作流程
- [ljxangus/research-writing-skill](https://github.com/ljxangus/research-writing-skill) — 多 Agent 协作实践

核心改造：**单 Agent → Agent Teams 多智能体协作架构 → 跨平台三平台兼容**

---

## License

MIT
