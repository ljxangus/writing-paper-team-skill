---
name: paper-drafting
description: Use when drafting academic paper chapters - implements Writing Agent Stage 3 workflow with de-AIification standards, section-by-section writing, and two-stage review process
# Hermes Agent
tools: [bash, read, write, edit]
# WorkBuddy MCP
mcp_servers: [style_check]
# Claude Code
subagent_types: [writing]
---

# Paper Drafting — 学术论文起草技能

独立的学术论文起草技能，基于 Writing Agent Stage 3 工作流程，执行按章节写作、去AI化处理和两阶段审查。

---

## 核心原则

1. **去AI化写作** — 禁用机械过渡词和空壳强调句，追求自然流畅的学术英语
2. **引用真实** — 绝不编造文献，所有引用必须有可追溯来源
3. **结构严谨** — 遵循 IMRAD 结构，逻辑链完整
4. **客观表述** — 使用 "this paper", "the results indicate"，避免主观化表达

---

## 写作规范

### 去 AI 化规则

| 禁用类型 | 禁用表达 | 推荐替代 |
|----------|----------|----------|
| 机械过渡词 | firstly, secondly, lastly, moreover, furthermore, additionally | 语义衔接：Following this, Building upon X, In contrast |
| 空壳强调句 | it is worth noting that, it should be pointed out that, importantly | 直接陈述事实或用数据支撑 |
| 空洞修饰词 | very, extremely, significantly (无数据时) | 提供具体数据或量化描述 |
| 主观引导句 | we believe, we think, in our opinion | this study demonstrates, the evidence suggests |

### 段落构建规则

一个标准学术段落包含：

1. **主题句**：本段核心论点
2. **支撑句**：证据、数据、引用
3. **收束句**：过渡或小结

**段落长度**：英文正文 100-200 词

### 列表转段落规则

❌ 错误：
```
The contributions of this paper are:
- A novel method for X.
- An efficient implementation of Y.
- Comprehensive evaluation on Z.
```

✅ 正确：
```
This paper presents a novel method for X and integrates it into an efficient
implementation of Y. Comprehensive evaluation on Z demonstrates the
effectiveness and scalability of the proposed approach.
```

---

## 写作工作流程

### 首次写作

1. 读取 `plan/outline.md` 获取章节目标
2. 读取 `references/writing-standards.md` 获取写作规范
3. 读取 `related-work.md` 获取文献素材
4. 参考 `assets/chapter-templates/` 的章节结构
5. 按章节顺序写作，输出到 `chapters/XX-name.md`
6. 每章完成后执行两阶段 Review
7. 更新 `plan/progress.md`

---

## 章节写作指南

### Abstract

- **最后写**，在所有章节完成后撰写
- 150-250 词（会议论文），200-300 词（期刊论文）
- 结构：Background → Problem → Method → Key Results → Conclusion
- 不含引用、不含图表

### Introduction

四段式结构：

1. **背景段**：研究领域的重要性与现状
2. **问题段**：现有方法的不足与未解决的问题
3. **贡献段**：本研究的核心贡献（用连贯段落，不列清单）
4. **组织段**：论文结构概述

### Related Work

- 基于文献搜索技能的 `related-work.md` 素材
- 按主题/方法组织，不按论文逐一罗列
- 必须有批判性分析，指出局限性
- 明确指出研究空白和本研究定位

### Methodology / System Architecture

- 详细到可复现
- 包含形式化定义（如有数学模型）
- 架构图需清晰标注各模块关系
- 与现有方法的关键区别需明确说明

### Experiment Setup

- 数据集描述与来源
- 基线方法与选择理由
- 评估指标定义
- 实现细节与超参数
- 硬件与运行环境

### Results & Discussion

- 定量结果用表格呈现
- 关键发现用图表辅助说明
- 与基线对比需公平（相同条件）
- 消融实验验证各模块贡献
- 局限性需诚实讨论

### Conclusion

- 总结核心发现（2-3 句）
- 回应引言中的研究问题
- 指出创新点与影响
- 提出未来方向
- 不引入新信息

---

## 两阶段 Review

### 阶段 1：规范合规检查

| 检查项 | 标准 |
|--------|------|
| 字数 | 符合目标（±10%） |
| 结构 | 章节完整，小节清晰 |
| 引用格式 | IEEE 或 ACM 格式统一 |
| 标题层级 | 符合论文规范 |
| 图表编号 | 连续且有标题 |
| 参考文献完整性 | 每条至少有作者/标题/年份/出处 |

### 阶段 2：质量检查

| 检查项 | 标准 |
|--------|------|
| 去AI化 | 无机械过渡词、无空壳强调句、无 AI 高频词滥用 |
| 语言 | 学术英语，客观表述，长短句交替 |
| 引用 | 所有引用可追溯，无编造 |
| 段落 | 连贯叙述，无列表堆砌 |
| 学术表达 | 贡献声称与实际成果匹配，无过度声称 |

---

## 章节写作顺序

推荐按以下顺序写作（可调整）：

1. Introduction
2. Related Work
3. Methodology / System Architecture
4. Experiment Setup（留占位符，Stage 4 填充）
5. Results & Discussion（留占位符，Stage 4 填充）
6. Conclusion
7. Abstract（最后写）

---

## 质量检查（Checklist）

每章写完后自检：

- [ ] 无禁用过渡词和强调句
- [ ] 段落连贯叙述，无列表堆砌
- [ ] 所有引用格式统一
- [ ] 引用可追溯，无编造
- [ ] 字数符合目标
- [ ] 章节结构完整

---

## 相关参考

- 完整 Agent 定义：`references/agent-writing.md`
- 写作标准：`references/writing-standards.md`
- 去AI化提示词：`skills/prompts-collection/SKILL.md`
- 风格检查脚本：`scripts/style_check.sh`
