---
name: statistical-analysis
description: Use when performing statistical tests, reporting effect sizes, or writing statistical results in APA format for academic papers - covers test selection, assumption checking, effect size calculation, and reporting
allowed-tools: Read Write Edit Bash
---

# Statistical Analysis — 学术论文统计分析指南

学术论文中统计分析的选择、执行和报告规范。适用于 Experiment Agent 设计实验和 Audit Agent 审查统计有效性。

---

## 一、统计检验选择决策表

### 1.1 比较两组

| 数据特征 | 推荐检验 | 前提条件 |
|----------|----------|----------|
| 独立、连续、正态 | 独立样本 t 检验 | 正态性、方差齐性 |
| 独立、连续、非正态 | Mann-Whitney U 检验 | 无分布假设 |
| 配对、连续、正态 | 配对样本 t 检验 | 差值正态性 |
| 配对、连续、非正态 | Wilcoxon 符号秩检验 | 对称分布 |
| 二分类结果 | 卡方检验或 Fisher 精确检验 | 期望频数 ≥ 5 |

### 1.2 比较三组及以上

| 数据特征 | 推荐检验 | 事后检验 |
|----------|----------|----------|
| 独立、连续、正态 | 单因素方差分析 (ANOVA) | Tukey HSD / Bonferroni |
| 独立、连续、非正态 | Kruskal-Wallis 检验 | Dunn's test |
| 配对、连续、正态 | 重复测量方差分析 | Bonferroni / Holm |
| 配对、连续、非正态 | Friedman 检验 | Nemenyi test |

### 1.3 关系分析

| 分析目标 | 推荐方法 | 适用条件 |
|----------|----------|----------|
| 两个连续变量关系 | Pearson 相关（正态）/ Spearman 相关（非正态） | 线性关系 |
| 连续结果与预测变量 | 线性回归 | 线性、正态残差、同方差 |
| 二分类结果与预测变量 | 逻辑回归 | 大样本 |
| 生存/时间数据 | Cox 比例风险模型 | 比例风险假设 |

---

## 二、假设检验

### 2.1 正态性检验（Shapiro-Wilk）

```python
from scipy import stats

stat, p_value = stats.shapiro(data)
print(f"Shapiro-Wilk: W={stat:.4f}, p={p_value:.4f}")

if p_value > 0.05:
    print("数据符合正态分布假设 (p > .05)")
else:
    print("数据不符合正态分布，考虑使用非参数检验")
```

### 2.2 方差齐性检验（Levene）

```python
from scipy import stats

stat, p_value = stats.levene(group1, group2)
print(f"Levene: F={stat:.4f}, p={p_value:.4f}")

if p_value > 0.05:
    print("方差齐性假设满足")
else:
    print("方差不齐，使用 Welch's t 检验")
```

---

## 三、效应量（Effect Size）

### 3.1 效应量分类标准

| 检验 | 效应量 | 小 | 中 | 大 |
|------|--------|-----|-----|-----|
| t 检验 | Cohen's d | 0.20 | 0.50 | 0.80 |
| ANOVA | η²_p | 0.01 | 0.06 | 0.14 |
| 相关 | r | 0.10 | 0.30 | 0.50 |
| 回归 | R² | 0.02 | 0.13 | 0.26 |

### 3.2 Python 计算效应量

```python
import pingouin as pg

# t 检验返回 Cohen's d
result = pg.ttest(group1, group2)
d = result['cohen-d'].values[0]
print(f"Cohen's d = {d:.2f}")

# ANOVA 返回偏 η²
aov = pg.anova(dv='score', between='group', data=df)
eta_p2 = aov['np2'].values[0]
print(f"Partial η² = {eta_p2:.3f}")
```

---

## 四、APA 格式报告模板

### 4.1 独立样本 t 检验

```
Group A (n = 48, M = 75.2, SD = 8.5) scored significantly higher than
Group B (n = 52, M = 68.3, SD = 9.2), t(98) = 3.82, p < .001,
d = 0.77, 95% CI [0.36, 1.18].
```

### 4.2 单因素方差分析

```
A one-way ANOVA revealed a significant main effect of treatment condition
on test scores, F(2, 147) = 8.45, p < .001, η²_p = .10. Post hoc
comparisons using Tukey HSD indicated that Condition A (M = 78.2,
SD = 7.3) scored significantly higher than Condition B (M = 71.5,
SD = 8.1, p = .002).
```

### 4.3 多元回归

```
A multiple linear regression was calculated to predict exam scores.
The overall model was significant, F(3, 146) = 45.2, p < .001,
R² = .48. Study time (β = .35, p < .001) and prior GPA
(β = .28, p < .001) were significant predictors.
```

### 4.4 卡方检验

```
A chi-square test of independence revealed a significant association
between group and outcome, χ²(1, N = 200) = 12.34, p < .001,
φ = .25.
```

---

## 五、常见统计陷阱（HARD-GATE）

⚠️ **必须避免以下错误：**

| # | 陷阱 | 说明 | 正确做法 |
|---|------|------|----------|
| 1 | P-hacking | 测试多种方式直到出现显著性 | 预注册分析计划 |
| 2 | HARKing | 将探索性发现呈现为验证性 | 区分探索性与验证性分析 |
| 3 | 忽视假设 | 不检查就使用参数检验 | 报告假设检验结果 |
| 4 | 混淆显著性与重要性 | p < .05 ≠ 有意义的效应 | 始终报告效应量 |
| 5 | 不报告效应量 | 对解释至关重要 | 每个检验都报告效应量 |
| 6 | 挑选结果 | 只报告显著的结果 | 报告所有计划的分析 |
| 7 | 多重比较不校正 | 增加假阳性率 | 使用 Bonferroni / Holm / FDR |
| 8 | 过度解释非显著结果 | 无证据 ≠ 无效应的证据 | 报告统计功效和效应量 |

---

## 六、Python 完整示例

```python
import numpy as np
import pingouin as pg
from scipy import stats

# 数据
group_a = np.array([75, 82, 68, 79, 85, 72, 88, 76])
group_b = np.array([65, 70, 62, 68, 75, 60, 72, 66])

# 1. 描述统计
print(f"Group A: M={group_a.mean():.2f}, SD={group_a.std():.2f}")
print(f"Group B: M={group_b.mean():.2f}, SD={group_b.std():.2f}")

# 2. 正态性检验
_, p_a = stats.shapiro(group_a)
_, p_b = stats.shapiro(group_b)
print(f"Normality: A p={p_a:.3f}, B p={p_b:.3f}")

# 3. t 检验（含效应量）
result = pg.ttest(group_a, group_b)
print(f"t = {result['T'].values[0]:.2f}")
print(f"p = {result['p-val'].values[0]:.4f}")
print(f"Cohen's d = {result['cohen-d'].values[0]:.2f}")

# 4. 置信区间
from scipy.stats import t as t_dist
diff = group_a.mean() - group_b.mean()
se = np.sqrt(group_a.var()/len(group_a) + group_b.var()/len(group_b))
df = len(group_a) + len(group_b) - 2
ci_low = diff - t_dist.ppf(0.975, df) * se
ci_high = diff + t_dist.ppf(0.975, df) * se
print(f"95% CI [{ci_low:.2f}, {ci_high:.2f}]")
```

---

## 七、统计分析检查清单

### 实验设计阶段
- [ ] 定义研究问题和假设
- [ ] 确定适当的统计检验
- [ ] 进行功效分析确定样本量

### 数据分析阶段
- [ ] 检查缺失数据和异常值
- [ ] 验证假设（正态性、方差齐性）
- [ ] 运行主要分析
- [ ] 计算效应量和置信区间
- [ ] 进行事后检验（如需要）

### 报告阶段
- [ ] 按 APA 格式撰写结果
- [ ] 报告检验统计量、p 值、效应量
- [ ] 报告置信区间
- [ ] 区分统计显著性和实际意义

---

## 八、推荐 Python 库

| 库名 | 用途 | 安装 |
|------|------|------|
| **scipy.stats** | 核心统计检验 | `pip install scipy` |
| **statsmodels** | 高级回归和诊断 | `pip install statsmodels` |
| **pingouin** | 用户友好的统计检验，自带效应量 | `pip install pingouin` |
| **numpy** | 数值计算 | `pip install numpy` |
| **pandas** | 数据处理 | `pip install pandas` |
