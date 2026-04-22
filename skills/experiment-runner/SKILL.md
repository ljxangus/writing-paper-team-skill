---
name: experiment-runner
description: Use when designing and running simulation experiments for papers - implements Experiment Agent Stage 4 workflow with reproducibility standards, baseline comparisons, and ablation studies
# Hermes Agent
tools: [bash, read, write, edit]
# WorkBuddy MCP
mcp_servers: []
# Claude Code
subagent_types: [experiment]
---

# Experiment Runner — 仿真实验执行技能

独立的仿真实验设计执行技能，基于 Experiment Agent Stage 4 工作流程，执行实验设计、代码实现、数据生成和结果分析。

---

## 核心原则

1. **可复现性** — 所有实验参数、随机种子、运行环境必须完整记录
2. **与论文一致** — 实验设计必须严格对应论文方法论部分的描述
3. **数据诚实** — 不挑选数据、不调整参数以获得"好看"的结果
4. **对照充分** — 必须包含足够的基线方法进行对比
5. **代码规范** — 代码清晰、有注释、可直接运行

## 仿真方法论要求

> **核心禁令**：禁止通过解析式直接计算生成实验数据并声称仿真。代码必须包含迭代或事件驱动的状态转移。

| 方面 | 合法仿真 | 禁止的解析式捷径 |
|------|---------|----------------|
| 数据生成 | 迭代状态转移、事件处理、随机采样 | `result = formula(params)` |
| 时间建模 | 显式仿真时钟推进 | 无时间概念 |
| 状态演化 | 可记录的中间状态 | 仅最终输出 |
| 证据 | 事件日志、逐步追踪、实际执行时间 | 仅汇总统计 |

必须产出证据产物：事件日志（`.jsonl`）、中间状态快照（至少 3 个）、原始样本数据、wall-clock 计时。详见 `references/agent-experiment.md`。

---

## 工作流程

### Step 1: 理解实验需求

读取以下文件：
- `plan/project-overview.md`：研究方法概述
- `chapters/methodology.md`（或对应章节）：详细方法论
- `plan/outline.md`：实验部分的目标与要求

提取：
- 需要验证的核心假设/声明
- 论文中描述的实验设置
- 预期的对比基线
- 评估指标

### Step 2: 设计实验方案

生成实验方案文档 `experiments/experiment-plan.md`：

```markdown
# Experiment Plan

## 1. Research Questions
- RQ1: [问题1]
- RQ2: [问题2]

## 2. Datasets
| 数据集 | 来源 | 大小 | 用途 |
|--------|------|------|------|

## 3. Baselines
| 方法 | 来源 | 选择理由 |
|------|------|----------|

## 4. Metrics
| 指标 | 定义 | 计算方式 |
|------|------|----------|

## 5. Experimental Setup
- 硬件环境: [CPU/GPU/内存]
- 软件环境: [语言/框架/版本]
- 超参数: [列表]

## 6. Ablation Studies
- 消融1: [移除/替换的模块]
- 消融2: [移除/替换的模块]

## 7. Expected Outputs
- 表格: [列出需要的表格]
- 图表: [列出需要的图表]
```

### Step 2.1: 完成仿真计划

使用模板 `assets/templates/simulation-plan.md` 声明仿真类型、范式、证据产物和反伪造声明。输出到 `experiments/simulation-plan.md`。仿真计划未完成前禁止编写代码。

### Step 3: 实现实验代码

#### 代码组织

```
experiments/
├── code/
│   ├── main.py              # 主入口
│   ├── model.py             # 模型实现
│   ├── data.py              # 数据处理
│   ├── train.py             # 训练逻辑
│   ├── evaluate.py          # 评估逻辑
│   ├── baselines/           # 基线实现
│   └── utils.py             # 工具函数
├── config/
│   └── default.yaml         # 默认配置
├── data/                    # 数据文件
├── figures/                 # 输出图表
├── results/                 # 结果文件
├── experiment-plan.md       # 实验方案
└── experiment-log.md        # 运行日志
```

#### 代码规范

1. 所有随机操作设置固定种子（`seed=42`）
2. 配置参数通过 YAML/JSON 文件管理，不硬编码
3. 关键步骤添加注释说明
4. 输出结果保存为结构化格式（JSON/CSV）
5. 图表保存为 PDF（矢量图）和 PNG（位图）双格式

### Step 4: 执行实验

#### 执行前检查

- [ ] 代码可无错误运行（先做 dry-run）
- [ ] 数据集已正确下载/生成
- [ ] 配置文件参数正确
- [ ] 输出目录已创建

#### 执行并记录

在 `experiments/experiment-log.md` 中记录：

```markdown
# Experiment Log

## Run 1: YYYY-MM-DD HH:MM

### Configuration
- Seed: 42
- Dataset: [name]
- Model: [configuration]

### Results
- Metric 1: [value]
- Metric 2: [value]

### Notes
- [任何异常或观察]
```

### Step 5: 生成结果

#### 结果表格

```markdown
| Method | Accuracy | F1-Score | Latency (ms) |
|--------|----------|----------|--------------|
| Baseline 1 | 85.2 | 83.1 | 12.3 |
| Baseline 2 | 87.6 | 85.4 | 15.7 |
| **Ours** | **91.3** | **89.8** | **14.2** |
```

#### 结果图表

使用 Python (matplotlib/seaborn) 生成：
- 对比柱状图
- 消融实验图
- 参数敏感性曲线
- 混淆矩阵（如适用）

#### 图表规范

- 字体：Times New Roman 或 Serif
- 字号：标题 14pt，轴标签 12pt，刻度 10pt
- 颜色：色盲友好配色
- 格式：PDF（矢量）+ PNG（300dpi）
- 标题和标签清晰，无需正文解释即可理解

---

## 输出产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 实验方案 | `experiments/experiment-plan.md` | 完整的实验设计 |
| 实验代码 | `experiments/code/` | 可执行的代码 |
| 配置文件 | `experiments/config/` | 参数配置 |
| 原始数据 | `experiments/data/` | 数据集 |
| 结果数据 | `experiments/results/` | 实验输出 |
| 图表 | `experiments/figures/` | PDF/PNG 图表 |
| 运行日志 | `experiments/experiment-log.md` | 运行记录 |

---

## 实验设计检查（Checklist）

完成实验后自检：

- [ ] 实验设计与方法论描述一致
- [ ] 至少 3 个基线方法进行对比
- [ ] 消融实验验证各模块贡献
- [ ] 随机种子固定，结果可复现
- [ ] 所有参数在 experiment-log.md 中记录
- [ ] 图表格式符合论文规范
- [ ] 数据范围合理，无异常值
- [ ] 统计显著性检验已执行（如适用）
- [ ] 仿真计划已完成（`experiments/simulation-plan.md`）
- [ ] 事件日志有效且时间戳渐进递增
- [ ] 中间状态快照显示渐进演化
- [ ] Wall-clock 执行时长非零
- [ ] 反伪造合规声明已完成

---

## 常见问题处理

### 数据不可用

如果所需数据集无法获取：
1. 在 experiment-log.md 中记录问题
2. 寻找公开替代数据集
3. 如无替代，报告主 Agent 请求用户协助

### 实验运行时间过长

1. 先用小规模数据验证代码正确性
2. 再用完整数据运行
3. 记录完整运行时间

### 结果不理想

1. 不调整参数以获得"好看"的结果
2. 如实记录结果
3. 在实验日志中分析可能原因
4. 报告主 Agent 由用户决策

---

## 相关参考

- 完整 Agent 定义：`references/agent-experiment.md`
- 统计分析技能：`skills/statistical-analysis/SKILL.md`
- 图表生成技能：`skills/figures-python/SKILL.md`
