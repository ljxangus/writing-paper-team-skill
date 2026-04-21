---
name: writing-paper-team-skill
description: Use when writing academic papers for IEEE/ACM conferences or journals - orchestrates multi-agent teams including DeepSearch, Writing, Experiment, Audit, and triple independent Reviewer agents for end-to-end paper writing from topic selection to citation audit
---

# Multi-Agent Research Paper Writing Skill

面向 IEEE/ACM 顶会顶刊的学术论文写作 Skill，采用 Agent Teams 多智能体协作架构。

## 哲学原则

- **流程优于即兴** — 门禁未开不推进，结构未定不写作
- **证据优于声称** — 引用可追溯，绝不编造文献；数据可验证，绝不捏造结果
- **协作优于独断** — 多 Agent 分工审查，单点盲区由团队弥补
- **简洁优于复杂** — 去AI化写作，拒绝机械表达
- **确认优于假设** — 每阶段用户确认，避免大规模返工

## 核心架构：六阶段 Agent Teams 流水线

```
Stage 1: Brainstorming & Planning  → Main Agent + User（对话确认选题/方法/结构）
Stage 2: Deep Search               → DeepSearch Agent（文献搜索 + RelatedWork 分析）
Stage 3: Writing                   → Writing Agent（按章节撰写论文）
Stage 4: Experiment & Audit        → Experiment Agent + Audit Agent（仿真实验 + 审查）
Stage 5: Triple Review & Revision  → 3× Reviewer Agent + Writing Agent（审稿 + 修改）
Stage 6: Citation Audit            → Audit Agent（引用准确性终审）
```

### 阶段依赖关系

```
Stage 1 ──→ Stage 2 ──→ Stage 3 ──→ Stage 4 ──→ Stage 5 ──→ Stage 6 ──→ 交付
                                      ↑            │              │
                                      └── 审查不通过 ─┘              │
                                                    ← 修改后重审 ←──┘
```

## Agent 职责矩阵

| Agent | 派发时机 | 核心职责 | 输出产物 |
|-------|----------|----------|----------|
| DeepSearch Agent | Stage 2 | 文献搜索、RelatedWork 分析、研究空白识别 | `related-work.md`, `papers/*.json` |
| Writing Agent | Stage 3, 5 | 论文章节写作、综合审稿意见修改 | `chapters/*.md` |
| Experiment Agent | Stage 4 | 仿真设计、代码执行、数据生成 | `experiments/` |
| Audit Agent | Stage 4, 6 | 实验审查 + 引用终审（含五步验证门控） | `audit-report.md` |
| Reviewer Agent ×3 | Stage 5 | IEEE/ACM 标准独立审稿（含两阶段 Review） | `review-1.md`, `review-2.md`, `review-3.md` |

## 子技能模块

### 核心流程技能

| 技能 | 路径 | 说明 |
|------|------|------|
| latex-output | `skills/latex-output/` | LaTeX 输出，模板解析与编译 |
| prompts-collection | `skills/prompts-collection/` | 翻译/润色/去AI化提示词模板 |
| figures-python | `skills/figures-python/` | 顶刊级 Python 图表生成 |
| statistical-analysis | `skills/statistical-analysis/` | 统计分析选择、执行与 APA 报告 |

### 参考文档

| 文档 | 路径 | 说明 |
|------|------|------|
| writing-standards | `references/writing-standards.md` | 去AI化写作标准 + 格式规范 |
| ieee-acm-rubric | `references/ieee-acm-rubric.md` | IEEE/ACM 审稿评分标准 |
| agent-deep-search | `references/agent-deep-search.md` | DeepSearch Agent 角色定义 |
| agent-writing | `references/agent-writing.md` | Writing Agent 角色定义 |
| agent-experiment | `references/agent-experiment.md` | Experiment Agent 角色定义 |
| agent-audit | `references/agent-audit.md` | Audit Agent 角色定义（含五步验证门控） |
| agent-reviewer | `references/agent-reviewer.md` | Reviewer Agent 角色定义（含两阶段 Review） |

### 工具脚本

| 脚本 | 路径 | 说明 |
|------|------|------|
| scholar_search | `scripts/scholar_search.py` | 多数据库文献搜索 |
| citation_verify | `scripts/citation_verify.py` | 引用准确性验证 |
| style_check | `scripts/style_check.sh` | 去AI化风格检查 |

### 模板与资源

| 资源 | 路径 | 说明 |
|------|------|------|
| 章节模板 | `assets/chapter-templates/` | 会议/期刊论文章节结构模板 |
| LaTeX 模板 | `latex-templates/` | 用户 LaTeX 模板存放目录 |

## Agent 派发规范

### SubAgent 派发流程

每个 Agent 角色通过 Task 工具以 SubAgent 方式派发。派发时遵循以下步骤：

1. **读取角色 prompt**：从 `references/agent-*.md` 加载对应 Agent 的完整指令
2. **构造任务上下文**：将 `plan/project-overview.md`、`plan/outline.md` 及前置阶段产物作为上下文传入
3. **派发 SubAgent**：使用 Task 工具，将角色 prompt + 任务上下文合并为 prompt 参数
4. **收集结果**：SubAgent 返回后，验证输出产物是否完整
5. **更新进度**：将结果写入 `plan/progress.md`，推进阶段

### SubAgent 派发模板

```
派发 DeepSearch Agent：
- subagent_name: "code-explorer"（或任何可用的 subagent）
- prompt: [references/agent-deep-search.md 内容] + "\n\n## 任务上下文\n" + [project-overview.md 内容]
```

### Team 模式派发（三审并行）

Stage 5 的三名 Reviewer Agent 必须**并行派发**以确保独立性：

```
team_create("paper-review-team")
Task(name="reviewer-1", team_name="paper-review-team", prompt=[agent-reviewer.md + 视角1])
Task(name="reviewer-2", team_name="paper-review-team", prompt=[agent-reviewer.md + 视角2])
Task(name="reviewer-3", team_name="paper-review-team", prompt=[agent-reviewer.md + 视角3])
```

三名 Reviewer 完成后，主 Agent 收集三份审稿报告，交给 Writing Agent 综合修改。

---

## Stage 1: Brainstorming & Planning

### 目标

通过对话确认论文的核心信息，创建项目结构。

### Checklist

- [ ] 确认论文类型（会议论文 / 期刊论文）
- [ ] 确认目标会议或期刊
- [ ] 确认论文题目
- [ ] 确认研究背景与问题
- [ ] 确认研究方法与技术路线
- [ ] 确认章节结构（参考 `assets/chapter-templates/`）
- [ ] 用户最终确认所有信息
- [ ] 创建 `plan/` 和 `chapters/` 目录

### 交互方式

采用**对话式**头脑风暴，一次只问一个问题。提供推荐方案，让用户确认或微调。

> "你这次要写的是什么类型的论文？是投 IEEE 还是 ACM？会议还是期刊？"

<HARD-GATE>
在用户最终确认之前，禁止：
- 写任何正文内容
- 派发任何 Agent
- 创建 chapters/ 目录下的正文文件
</HARD-GATE>

### 语言默认规则

| 论文类型 | 默认语言 |
|----------|----------|
| IEEE/ACM 会议论文 | 英文 |
| IEEE/ACM 期刊论文 | 英文 |
| 其他国际会议/期刊 | 英文 |

### 项目结构创建

用户确认后创建：

```
<project-root>/
├── plan/
│   ├── project-overview.md    # 项目概览
│   ├── outline.md             # 详细章节大纲
│   ├── progress.md            # 进度追踪
│   └── notes.md               # 用户偏好与备注
├── chapters/                  # 各章节文件
├── papers/                    # 搜索到的文献记录
├── experiments/               # 实验代码与数据
└── reviews/                   # 审稿报告
```

---

## Stage 2: Deep Search

### 目标

DeepSearch Agent 对课题进行系统性文献搜索，识别高相关性 RelatedWork，分析研究空白。

### 派发方式

读取 `references/agent-deep-search.md`，结合 `plan/project-overview.md` 构造 prompt，派发 SubAgent。

### Checklist

- [ ] 基于课题关键词执行多数据库搜索
- [ ] 筛选高相关性论文（相关性评分 ≥ 7/10）
- [ ] 每篇论文提取：标题、作者、年份、核心贡献、与本研究关系
- [ ] 识别研究空白与本研究定位
- [ ] 生成 `related-work.md` 和 `papers/*.json`
- [ ] 验证所有搜索结果的 DOI 可访问性

### 输出产物

| 产物 | 路径 | 说明 |
|------|------|------|
| RelatedWork 分析 | `related-work.md` | 按主题分类的文献综述素材 |
| 文献元数据 | `papers/*.json` | 每篇论文的结构化记录 |
| 搜索日志 | `papers/search-log.md` | 搜索关键词、数据库、结果数量 |

<HARD-GATE>
DeepSearch Agent 完成后，主 Agent 必须验证：
1. `related-work.md` 存在且非空
2. 至少包含 15 篇高相关性论文
3. 所有论文的 DOI 已验证可访问
4. 研究空白已明确指出
验证不通过则要求 DeepSearch Agent 补充搜索。
</HARD-GATE>

---

## Stage 3: Writing

### 目标

Writing Agent 根据 outline 和 RelatedWork 素材，按章节撰写论文。

### 派发方式

读取 `references/agent-writing.md`，结合 `plan/outline.md` 和 `related-work.md` 构造 prompt，派发 SubAgent。

### Checklist（每章）

- [ ] 读取 `plan/outline.md` 确认本章目标
- [ ] 读取 `references/writing-standards.md` 确认写作规范
- [ ] 参考 `assets/chapter-templates/` 的章节结构
- [ ] 写作输出到 `chapters/XX-name.md`
- [ ] 执行两阶段 Review（规范合规 + 质量检查）
- [ ] 更新 `plan/progress.md`
- [ ] 用户确认后继续下一章

### 两阶段 Review

每章写完后执行两阶段 Review：

**阶段 1：规范合规检查**

| 检查项 | 标准 |
|--------|------|
| 字数 | 符合目标（±10%） |
| 结构 | 章节完整，小节清晰 |
| 引用格式 | IEEE 或 ACM 格式统一 |
| 标题层级 | 符合论文规范 |
| 图表编号 | 连续且有标题 |
| 参考文献完整性 | 每条至少有作者/标题/年份/出处 |

**阶段 2：质量检查**

| 检查项 | 标准 |
|--------|------|
| 去AI化 | 无机械过渡词、无空壳强调句、无 AI 高频词滥用 |
| 语言 | 学术英语，客观表述，长短句交替 |
| 引用 | 所有引用可追溯，无编造 |
| 段落 | 连贯叙述，无列表堆砌 |
| 学术表达 | 贡献声称与实际成果匹配，无过度声称 |

### 章节写作顺序

推荐按以下顺序写作（可调整）：

1. Introduction
2. Related Work
3. Methodology / System Architecture
4. Experiment Setup（留占位符，Stage 4 填充）
5. Results & Discussion（留占位符，Stage 4 填充）
6. Conclusion
7. Abstract（最后写）

<HARD-GATE>
每章写完后必须：
1. 运行 `scripts/style_check.sh` 检查去AI化
2. 用户确认本章内容
3. 更新 progress.md
不得自动跳到下一章。
</HARD-GATE>

---

## Stage 4: Experiment & Audit

### 目标

Experiment Agent 设计并执行仿真实验，Audit Agent 审查实验数据与结果的合理性。

### 4.1 Experiment Agent 派发

读取 `references/agent-experiment.md`，结合 `plan/outline.md` 中方法论部分和已有 `chapters/` 内容，派发 SubAgent。

#### Checklist

- [ ] 基于论文方法论设计实验方案
- [ ] 编写仿真代码（Python/MATLAB 等）
- [ ] 执行仿真并收集数据
- [ ] 生成结果图表
- [ ] 所有代码和数据存入 `experiments/`
- [ ] 记录实验参数、随机种子、运行环境

#### 输出产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 实验代码 | `experiments/code/` | 可执行的仿真脚本 |
| 实验数据 | `experiments/data/` | 原始数据与处理后的数据 |
| 结果图表 | `experiments/figures/` | PDF/PNG 格式 |
| 实验日志 | `experiments/experiment-log.md` | 参数、环境、运行记录 |

### 4.2 Audit Agent 派发（实验审查）

读取 `references/agent-audit.md`，结合 `experiments/` 产物和 `chapters/` 中的方法论描述，派发 SubAgent。

#### 审查维度

| 维度 | 检查要点 |
|------|----------|
| 实验设计 | 是否与论文声称的方法一致？对照组是否充分？ |
| 数据合理性 | 数值范围是否合理？是否有异常值未处理？ |
| 可复现性 | 代码是否可直接运行？参数是否完整记录？ |
| 统计有效性 | 样本量是否足够？显著性检验是否正确？ |
| 结果一致性 | 论文中的数据与实验输出是否一致？ |

#### 审查结果

- ✅ **通过**：推进到 Stage 5
- ❌ **不通过**：退回 Experiment Agent 修改，附具体问题清单

<HARD-GATE>
Audit Agent 审查不通过时，必须：
1. 在 `audit-report.md` 中列出所有问题
2. Experiment Agent 必须逐一修复
3. 修复后 Audit Agent 重新审查
4. 最多允许 3 轮修复，超过则上报用户决策
</HARD-GATE>

---

## Stage 5: Triple Review & Revision

### 目标

三名独立 Reviewer Agent 以 IEEE/ACM 顶会顶刊标准审稿，Writing Agent 综合意见修改论文。

### 5.1 三审派发

读取 `references/agent-reviewer.md`，分别以三种审稿视角派发三名 Reviewer：

| Reviewer | 审稿视角 | 侧重维度 |
|----------|----------|----------|
| Reviewer 1 | 方法论严谨性 | 实验设计、统计方法、可复现性、威胁分析 |
| Reviewer 2 | 创新性与贡献 | 新颖性、技术贡献、与现有工作区分、影响力 |
| Reviewer 3 | 表达与呈现 | 写作质量、图表清晰度、结构逻辑、引用规范 |

三名 Reviewer **必须并行派发**（Team 模式），避免意见互相影响。

每名 Reviewer 执行**两阶段审稿**：
1. **阶段一：规范合规检查** — 字数/结构/引用格式/图表编号/参考文献完整性
2. **阶段二：质量深入检查** — 按各自视角深入审查学术质量（详见 `references/agent-reviewer.md`）

### 审稿报告格式

每名 Reviewer 的报告包含：

```markdown
# Review Report — Reviewer [N]

## Overall Assessment
- Rating: [Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject / Strong Reject]
- Confidence: [5: Expert / 4: High / 3: Medium / 2: Low / 1: None]

## Summary
[2-3 句话概括论文]

## Strengths
1. [优点1]
2. [优点2]
...

## Weaknesses
1. [缺点1]
2. [缺点2]
...

## Questions for Authors
1. [问题1]
2. [问题2]
...

## Minor Issues
- [小问题列表]
```

### 5.2 Writing Agent 综合修改

三份审稿报告收集完毕后，派发 Writing Agent 执行修改：

1. **归类意见**：将三份报告的意见分为 Critical / Major / Minor 三级
2. **逐条响应**：对每条意见制定修改方案
3. **执行修改**：更新 `chapters/*.md`
4. **生成 Response Letter**：`reviews/response-letter.md`

<HARD-GATE>
修改完成后必须验证：
1. 所有 Critical 和 Major 意见已处理
2. Response Letter 中逐条说明了修改位置
3. 修改后的章节通过 style_check.sh 检查
</HARD-GATE>

---

## Stage 6: Citation Audit

### 目标

Audit Agent 对论文全文的引用进行最终审核，确保所有引用准确、格式统一、可追溯。

### 派发方式

读取 `references/agent-audit.md`（引用审核部分），结合全部 `chapters/*.md`，派发 SubAgent。

### 审核维度

| 维度 | 检查方法 |
|------|----------|
| DOI 有效性 | 通过 CrossRef API 批量验证 |
| 作者/年份准确性 | 搜索原始来源交叉验证 |
| 格式一致性 | 全文引用格式统一（IEEE 或 ACM） |
| 正文-文献列表对应 | 每条正文引用在参考文献列表中有对应条目 |
| 无孤立引用 | 参考文献列表中每条都在正文中被引用 |

### 审核结果

- ✅ **通过**：论文交付完成
- ❌ **不通过**：Writing Agent 修正引用后重新审核

<HARD-GATE>
引用终审是最后门禁，不可跳过。
即使修改阶段仅改动少量内容，引用终审仍需执行，
因为修改可能引入新引用。
</HARD-GATE>

---

## Red Flags（停止并检查）

### 流程类

| AI 的想法 | 正确做法 |
|-----------|----------|
| "用户说得很清楚了，直接开始写" | 必须先完成 Stage 1 头脑风暴 |
| "这只是修改一小段" | 检查是否需要重新审核 |
| "先写一段看看效果" | 必须先确认论文类型和章节结构 |
| "流程可以简化跳过" | 门禁不可跳过，流程可加速但不能省略 |
| "这章内容很简单，不用确认" | 每章写完都必须让用户确认 |

### 文献类

| AI 的想法 | 正确做法 |
|-----------|----------|
| "文献我可以补充一些" | 绝不编造文献，必须可追溯 |
| "这个引用看起来很合理" | 没有来源的引用一律不写 |
| "搜索结果不够，编几个凑数" | 宁可少引用，不可编造 |

### 验证类

| AI 的想法 | 正确做法 |
|-----------|----------|
| "应该写完了" | 运行验证命令确认（五步验证门控） |
| "引用应该是真的" | 调用 CrossRef API 验证 |
| "实验数据看起来合理" | Audit Agent 必须审查，逐项验证 |
| "我很确信" | 确信 ≠ 证据，运行验证 |
| "就这一次跳过验证" | 没有例外 |
| "部分检查够了" | 部分证明不了什么 |
| "格式应该没问题" | 运行 style_check.sh 和格式检查 |
| "搜索完成了" | 检查结果数量和 DOI 列表 |

### Agent 协作类

| AI 的想法 | 正确做法 |
|-----------|----------|
| "我自己搜一下文献就行" | 必须派发 DeepSearch Agent |
| "审稿我自己做就行" | 必须派发三名独立 Reviewer |
| "实验我自己跑一下" | 必须派发 Experiment Agent |
| "审查太麻烦了跳过" | Audit Agent 审查不可跳过 |

---

## 输出规范

### 去 AI 化

- 禁用机械过渡词：firstly, secondly, lastly, moreover, furthermore, additionally
- 禁用空壳强调句：it is worth noting that, it should be pointed out that, importantly
- 语气客观：使用 "this paper", "this study", "the results indicate"
- 段落连贯叙述，不使用列表堆砌

### 引用规范

- 绝不编造文献
- 引用必须可追溯（作者、年份、出处至少完整两项）
- 全文引用格式统一（IEEE [1] 或 ACM [1] 格式）
- 正文引用与参考文献列表一一对应

### 格式规范

- 段落之间空一行
- 正文不使用加粗（除术语首次定义）
- 标题层级清晰
- 图表有编号和标题

---

## 断点续作

所有进度记录在 `plan/progress.md`，支持从任意断点恢复：

```markdown
# Progress

## Stage 1: Brainstorming
- Status: ✅ Completed
- Date: YYYY-MM-DD

## Stage 2: Deep Search
- Status: ✅ Completed
- Papers found: 42
- High relevance: 18
...
```

恢复时读取 `plan/progress.md`，从最后完成的阶段的下一阶段继续。

---

## 可选：LaTeX 输出

### 触发条件

- 用户明确要求 LaTeX 输出
- 用户提供了 LaTeX 模板（放入 `latex-templates/`）
- 目标期刊强制要求 LaTeX 格式

### 流程

1. 检测 `latex-templates/` 目录是否有用户模板
2. 读取 `skills/latex-output/SKILL.md` 执行 LaTeX 输出
3. 将 `chapters/*.md` 转换为 `tex/*.tex`
4. 生成 `main.tex` 和 `references.bib`
5. 编译验证（`latexmk -xelatex main.tex`）
6. 输出 PDF 预览

### 产物

```
tex/                  # LaTeX 源文件
├── main.tex          # 主入口
├── 00-abstract.tex
├── 01-introduction.tex
└── ...
references.bib        # BibTeX 参考文献
```

---

## 版本信息

- **版本**：1.1.0
- **基础**：Norman-bury/research-writing-skill v3.1.0 + ljxangus/research-writing-skill
- **核心改造**：单 Agent → Agent Teams 多智能体协作
- **v1.1 新增**：latex-output / prompts-collection / figures-python / statistical-analysis / 两阶段 Review / 验证门控五步法 / latex-templates 目录
- **目标**：IEEE/ACM 顶会顶刊论文写作
