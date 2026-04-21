# Multi-Agent Research Paper Writing Skill

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Stage](https://img.shields.io/badge/Stage-6%20phase%20pipeline-orange)
![Standard](https://img.shields.io/badge/Standard-IEEE%2FACM-green)

面向 IEEE/ACM 顶会顶刊的学术论文写作 Skill，采用 **Agent Teams** 多智能体协作架构。从选题到引用终审，全流程自动化。

---

## 目录

- [核心架构](#核心架构)
- [快速开始](#快速开始)
- [六阶段流水线](#六阶段流水线)
- [Agent 角色](#agent-角色)
- [子技能模块](#子技能模块)
- [目录结构](#目录结构)
- [设计原则](#设计原则)
- [版本历史](#版本历史)
- [致谢](#致谢)

---

## 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Stage 1: Brainstorming                       │
│                    Main Agent + User 对话确认选题/方法/结构        │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Stage 2: Deep Search                      │
│                    DeepSearch Agent                              │
│            多数据库文献搜索 + RelatedWork + 研究空白识别          │
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
│               仿真实验设计与执行 + 审查验证                        │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stage 5: Triple Review & Revision                │
│              3× Reviewer Agent + Writing Agent                    │
│         三视角独立审稿（方法论/创新性/表达）+ 综合修改               │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Stage 6: Citation Audit                     │
│                       Audit Agent                                 │
│               引用准确性终审（DOI 验证 + 格式统一）                 │
└─────────────────────────────────────────────────────────────────┘
```

**特点：**
- 每个阶段有 **HARD-GATE** 门禁，未通过不得推进
- 所有审查结论必须基于**证据**而非"应该"、"看起来"
- 三审并行（Team 模式）确保独立性

---

## 快速开始

### 安装

将本仓库克隆到 WorkBuddy skills 目录：

```bash
git clone https://github.com/ljxangus/writing-paper-team-skill.git \
  ~/.workbuddy/skills/writing-paper-team-skill
```

### 使用流程

1. **激活 Skill**：在 WorkBuddy 中输入论文写作需求
2. **Stage 1 对话**：确认论文类型、目标期刊、研究主题
3. **自动执行**：Agent Teams 接管后续所有阶段
4. **用户确认**：每个关键节点等待用户确认
5. **交付输出**：完整论文草稿 + 审稿报告 + Response Letter

---

## 六阶段流水线

### Stage 1 — Brainstorming & Planning

主 Agent 与用户对话，确认：
- 论文类型（会议/期刊）
- 目标会议或期刊（IEEE/ACM）
- 研究主题与核心问题
- 技术路线与方法
- 章节结构

> ⚠️ **HARD-GATE**：用户确认前禁止写任何正文内容。

### Stage 2 — Deep Search

DeepSearch Agent 执行：
- 多数据库文献搜索（Semantic Scholar / CrossRef / arXiv）
- 高相关性论文筛选（相关性评分 ≥ 7/10）
- RelatedWork 按主题分类
- 研究空白识别

> ⚠️ **HARD-GATE**：至少 15 篇高相关性论文 + DOI 全验证。

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
- 仿真方案设计
- 代码编写与执行
- 结果图表生成

Audit Agent：
- 实验设计与论文声称一致性
- 数据合理性验证
- 可复现性确认
- 统计有效性审查

> ⚠️ **HARD-GATE**：审查不通过则退回修改，最多 3 轮。

### Stage 5 — Triple Review & Revision

三名 Reviewer Agent 并行独立审稿：

| Reviewer | 视角 | 侧重维度 |
|----------|------|----------|
| Reviewer 1 | 方法论严谨性 | 实验设计、统计方法、可复现性、威胁分析 |
| Reviewer 2 | 创新性与贡献 | 新颖性、技术贡献、与现有工作区分 |
| Reviewer 3 | 表达与呈现 | 写作质量、图表清晰度、结构逻辑 |

每名 Reviewer 执行两阶段审稿，Writing Agent 综合意见修改并生成 Response Letter。

### Stage 6 — Citation Audit

Audit Agent 引用终审：
- DOI 批量验证（CrossRef API）
- 作者/年份准确性交叉验证
- 引用格式统一性检查
- 正文-文献列表双向对应检查

> ⚠️ **HARD-GATE**：最终门禁，不可跳过。

---

## Agent 角色

| Agent | Stage | 核心职责 | 输出产物 |
|-------|-------|----------|----------|
| DeepSearch Agent | 2 | 文献搜索 + RelatedWork + 研究空白 | `related-work.md`, `papers/*.json` |
| Writing Agent | 3, 5 | 论文章节写作 + 综合修改 | `chapters/*.md` |
| Experiment Agent | 4 | 仿真实验设计与执行 | `experiments/` |
| Audit Agent | 4, 6 | 实验审查 + 引用终审 | `audit-report.md` |
| Reviewer ×3 | 5 | IEEE/ACM 标准独立审稿 | `review-*.md` |

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

## 子技能模块

| 技能 | 路径 | 说明 |
|------|------|------|
| **latex-output** | `skills/latex-output/` | LaTeX 输出：模板解析 → Markdown→LaTeX 转换 → IEEEtran/acmart 适配 → XeLaTeX 编译 → 错误处理 |
| **prompts-collection** | `skills/prompts-collection/` | 8 大类提示词：中英翻译 / 深度润色 / 去AI化（含替换表）/ 扩写缩写 / 逻辑检查 / 图表标题 / 审稿视角 |
| **figures-python** | `skills/figures-python/` | 顶刊配色（Nature/Cell/IEEE/色盲友好）+ 6 种图表模板（折线/柱状/热力/箱线/散点/消融）+ 450 DPI 双格式 |
| **statistical-analysis** | `skills/statistical-analysis/` | 统计检验决策表 + 假设检验 + 效应量 + APA 报告 + 8 大统计陷阱（HARD-GATE） |

---

## 目录结构

```
writing-paper-team-skill/
├── SKILL.md                           # 主入口（WorkBuddy Skill 定义）
├── README.md                          # 本文件
│
├── references/                        # Agent 角色定义与参考文档
│   ├── agent-deep-search.md           # DeepSearch Agent prompt
│   ├── agent-writing.md               # Writing Agent prompt
│   ├── agent-experiment.md            # Experiment Agent prompt
│   ├── agent-audit.md                 # Audit Agent prompt（含五步验证门控）
│   ├── agent-reviewer.md              # Reviewer Agent prompt（含两阶段 Review）
│   ├── writing-standards.md           # 去AI化写作标准 + AI高频词替换表
│   └── ieee-acm-rubric.md             # IEEE/ACM 审稿评分标准
│
├── scripts/                           # 工具脚本
│   ├── scholar_search.py               # 多数据库文献搜索
│   ├── citation_verify.py              # 引用准确性验证
│   └── style_check.sh                  # 去AI化风格检查
│
├── skills/                            # 子技能模块
│   ├── latex-output/SKILL.md
│   ├── prompts-collection/SKILL.md
│   ├── figures-python/SKILL.md
│   └── statistical-analysis/SKILL.md
│
├── assets/                            # 模板与资源
│   └── chapter-templates/
│       ├── conference-paper.md         # 会议论文章节结构模板
│       └── journal-article.md           # 期刊论文章节结构模板
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

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| v1.1.0 | 2026-04-21 | 新增 latex-output / prompts-collection / figures-python / statistical-analysis 子技能；强化 Audit Agent 五步验证门控；强化 Reviewer Agent 两阶段审稿；latex-templates 目录 |
| v1.0.0 | 2026-04-10 | 初始版本：六阶段 Agent Teams 流水线 + 三审机制 |

---

## 致谢

本 Skill 基于以下开源项目改造：

- [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill) v3.1.0 — 单 Agent 写作流程
- [ljxangus/research-writing-skill](https://github.com/ljxangus/research-writing-skill) — 多 Agent 协作实践

核心改造：**单 Agent → Agent Teams 多智能体协作架构**

---

## License

MIT
