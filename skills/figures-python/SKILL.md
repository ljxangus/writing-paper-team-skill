---
name: figures-python
description: Use when creating data visualizations for papers - generates publication-quality plots with top-journal color schemes, 450 DPI output, and both PNG and SVG formats
# Hermes Agent
tools: [bash, read, write, edit]
# WorkBuddy MCP
mcp_servers: []
# Claude Code
subagent_types: []
---

# Figures Python — 顶刊级科研图表生成

使用 Python 生成符合顶级期刊出版标准的科研图表。Experiment Agent 和 Writing Agent 可调用此技能生成实验结果图表。

---

## 一、环境要求

### 1.1 Python 环境

```bash
# 推荐使用项目虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install matplotlib seaborn numpy pandas
```

### 1.2 必需库

| 库名 | 版本要求 | 用途 |
|------|----------|------|
| matplotlib | ≥ 3.7 | 核心绑图库 |
| seaborn | ≥ 0.12 | 统计可视化 |
| numpy | ≥ 1.24 | 数值计算 |
| pandas | ≥ 2.0 | 数据处理 |

---

## 二、图表规范

### 2.1 分辨率要求

| 用途 | DPI | 说明 |
|------|-----|------|
| 期刊投稿 | 300-600 | 大多数期刊要求 |
| 顶刊投稿 | 450+ | Nature/Science 等 |
| 屏幕展示 | 150 | PPT/网页 |

> **本技能默认使用 450 DPI**

### 2.2 输出格式

每张图同时输出两种格式：
- **PNG**：位图，适合网页和 PPT
- **SVG**：矢量图，适合期刊投稿和 LaTeX 嵌入

### 2.3 图表尺寸

| 类型 | 宽度（英寸） | 适用场景 |
|------|-------------|----------|
| 单栏图 | 3.5 | IEEE/ACM 单栏 |
| 双栏图 | 7.0 | 期刊双栏/全宽 |
| PPT 图 | 10.0 | 演示文稿 |

---

## 三、顶刊配色方案

### 3.1 Nature/Science 风格

```python
NATURE_COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#95C623']
```

### 3.2 Cell 风格

```python
CELL_COLORS = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948']
```

### 3.3 色盲友好配色

```python
COLORBLIND_SAFE = ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377']
```

### 3.4 IEEE/ACM 论文推荐配色

```python
IEEE_COLORS = ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747']
```

### 3.5 配色原则

- ❌ 禁止使用 matplotlib 默认颜色
- ❌ 禁止使用纯红、纯蓝、纯绿等基础色
- ✅ 同一图中颜色数量控制在 5 种以内
- ✅ 确保色盲友好（使用 COLORBLIND_SAFE 或验证工具）
- ✅ 相邻颜色在色轮上保持足够距离

---

## 四、全局样式配置

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# 顶刊配色
COLORS = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']

def setup_plot_style():
    """配置顶刊论文绑图全局样式。"""
    plt.rcParams.update({
        # 字体
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'font.size': 10,
        'mathtext.fontset': 'stix',

        # 坐标轴
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.8,
        'axes.grid': True,
        'axes.unicode_minus': False,

        # 网格
        'grid.alpha': 0.3,
        'grid.linewidth': 0.5,

        # 图例
        'legend.frameon': False,
        'legend.fontsize': 9,

        # 刻度
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,

        # 保存
        'savefig.dpi': 450,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,

        # 图表
        'figure.dpi': 150,
        'figure.autolayout': True,

        # 线条
        'lines.linewidth': 1.5,
        'lines.markersize': 4,
    })
```

---

## 五、图表类型模板

### 5.1 折线图（Line Plot）

```python
def plot_line(x, y_list, labels, title='', xlabel='', ylabel='',
              colors=COLORS, markers=['o', 's', '^', 'D', 'v']):
    """生成顶刊级折线图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 5))

    for i, (y, label) in enumerate(zip(y_list, labels)):
        ax.plot(x, y, color=colors[i % len(colors)],
                marker=markers[i % len(markers)],
                label=label, linewidth=1.5, markersize=4)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()

    return fig, ax
```

### 5.2 柱状图（Bar Chart）

```python
def plot_bar(categories, values_list, labels,
             colors=COLORS, bar_width=0.15):
    """生成分组柱状图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    n_groups = len(categories)
    n_bars = len(values_list)
    indices = np.arange(n_groups)

    for i, (values, label) in enumerate(zip(values_list, labels)):
        offset = (i - n_bars / 2 + 0.5) * bar_width
        ax.bar(indices + offset, values, bar_width,
               color=colors[i % len(colors)], label=label,
               edgecolor='white', linewidth=0.5)

    ax.set_xticks(indices)
    ax.set_xticklabels(categories)
    ax.legend()
    return fig, ax
```

### 5.3 热力图（Heatmap）

```python
def plot_heatmap(matrix, xlabels, ylabels, title='',
                 cmap='RdBu_r', annot=True, fmt='.2f'):
    """生成热力图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 6))

    im = ax.imshow(matrix, cmap=cmap, aspect='auto')
    if annot:
        for i in range(len(ylabels)):
            for j in range(len(xlabels)):
                ax.text(j, i, fmt.format(matrix[i, j]),
                        ha='center', va='center', fontsize=8)

    ax.set_xticks(range(len(xlabels)))
    ax.set_yticks(range(len(ylabels)))
    ax.set_xticklabels(xlabels, rotation=45, ha='right')
    ax.set_yticklabels(ylabels)
    ax.set_title(title)
    plt.colorbar(im, ax=ax, shrink=0.8)
    return fig, ax
```

### 5.4 箱线图（Box Plot）

```python
def plot_boxplot(data_list, labels, colors=COLORS):
    """生成箱线图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 5))

    bp = ax.boxplot(data_list, patch_artist=True, labels=labels,
                    medianprops=dict(color='black', linewidth=1.5),
                    whiskerprops=dict(linewidth=1),
                    capprops=dict(linewidth=1))

    for patch, color in zip(bp['boxes'], colors[:len(data_list)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel('Value')
    return fig, ax
```

### 5.5 散点图（Scatter Plot）

```python
def plot_scatter(x, y, sizes=None, colors_data=None,
                 xlabel='', ylabel='', title='',
                 cmap='viridis', alpha=0.6):
    """生成散点图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 5))

    sc = ax.scatter(x, y, c=colors_data, s=sizes,
                    cmap=cmap, alpha=alpha, edgecolors='white', linewidth=0.5)

    if colors_data is not None:
        plt.colorbar(sc, ax=ax, shrink=0.8)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return fig, ax
```

### 5.6 消融实验图（Ablation Bar Chart）

```python
def plot_ablation(baselines, ablations, metric_name='Accuracy (%)',
                  colors=COLORS):
    """生成消融实验对比柱状图。"""
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(7, 4))

    all_labels = list(baselines.keys()) + list(ablations.keys())
    all_values = list(baselines.values()) + list(ablations.values())

    bar_colors = [colors[0]] * len(baselines) + [colors[1]] * len(ablations)
    bars = ax.barh(all_labels, all_values, color=bar_colors,
                   edgecolor='white', height=0.6)

    # 在柱状条上标注数值
    for bar, val in zip(bars, all_values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}', va='center', fontsize=9)

    ax.set_xlabel(metric_name)
    ax.invert_yaxis()
    return fig, ax
```

---

## 六、文件管理

### 6.1 目录结构

```
figures/
├── chapter3/                    # 方法论相关图
│   ├── fig1_system_arch.py
│   ├── fig1_system_arch.png
│   └── fig1_system_arch.svg
├── chapter4/                    # 实验结果图
│   ├── fig2_accuracy_comparison.py
│   ├── fig2_accuracy_comparison.png
│   └── fig2_accuracy_comparison.svg
└── chapter5/                    # 讨论相关图
```

### 6.2 命名规范

- 文件名格式：`fig{序号}_{描述}.py`
- 示例：`fig1_system_architecture.py`, `fig2_accuracy_comparison.py`
- 序号与论文中的 Figure 编号一致

### 6.3 保存代码模板

```python
def save_figure(fig, name, output_dir='figures/'):
    """保存图表为 PNG 和 SVG 双格式。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path / f'{name}.png', dpi=450, bbox_inches='tight')
    fig.savefig(output_path / f'{name}.svg', bbox_inches='tight')
    print(f"Saved: {output_path / name}.png/svg")
```

---

## 七、质量检查（Checklist）

### 图表内容
- [ ] 数据准确无误
- [ ] 坐标轴标签完整（含单位）
- [ ] 图例清晰可读
- [ ] 无冗余装饰（3D 效果、阴影等）

### 视觉效果
- [ ] 使用顶刊配色（非 matplotlib 默认）
- [ ] 分辨率达到 450 DPI
- [ ] 字体大小适中（正文 10pt, 标题 12pt）
- [ ] 色盲友好

### 文件输出
- [ ] PNG 格式已生成
- [ ] SVG 格式已生成
- [ ] 文件命名符合 `fig{N}_{desc}` 规范
- [ ] 图片尺寸匹配论文排版（单栏 3.5" / 双栏 7.0"）

---

## 八、常见问题

### Q1: 中文显示为方块

```python
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')
ax.set_xlabel('中文标签', fontproperties=font)
```

### Q2: 图片模糊

```python
plt.savefig('figure.png', dpi=450, bbox_inches='tight')
```

### Q3: 图例遮挡数据

```python
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
```

### Q4: LaTeX 公式渲染

```python
plt.rcParams['text.usetex'] = True  # 需要系统安装 LaTeX
ax.set_ylabel(r'Accuracy ($\%$)')
```

### Q5: 多子图对齐

```python
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharey=True)
for ax in axes:
    ax.tick_params(labelbottom=True)
fig.tight_layout()
```
