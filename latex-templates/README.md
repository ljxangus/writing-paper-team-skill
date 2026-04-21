# LaTeX Templates — 用户模板存放目录

将你的 LaTeX 模板文件放在此目录下，`latex-output` 技能会自动检测并使用。

## 支持的模板类型

| 模板类型 | 典型文件 | 示例 |
|----------|----------|------|
| IEEE 会议论文 | `IEEEtran.cls` | `\documentclass[conference]{IEEEtran}` |
| IEEE 期刊论文 | `IEEEtran.cls` | `\documentclass[journal]{IEEEtran}` |
| ACM 会议论文 | `acmart.cls` | `\documentclass[sigconf]{acmart}` |
| 高校学位论文 | 校级 `.cls` 文件 | 如 `thuthesis.cls`, `ucasthesis.cls` |
| 自定义模板 | 用户提供的 `.cls` + `.sty` | 任意 |

## 目录结构

```
latex-templates/
├── README.md                  ← 你正在看的文件
├── [document-class].cls       ← 文档类文件
├── [style].sty                ← 样式文件（如有）
├── main-template.tex          ← 主文件示例
├── bibliography/              ← 参考文献样式文件
│   └── [bst-file].bst
└── figures/                   ← 模板自带示例图片
```

## 使用说明

1. 将模板的所有文件（`.cls`, `.sty`, `.bst`, 示例 `.tex` 等）复制到此目录
2. 不要修改模板原始文件
3. `latex-output` 技能会自动解析模板结构并生成对应的输出文件
4. 编译说明会写入 `plan/compile-notes.md`

## 默认模板

如果此目录为空，`latex-output` 技能会根据论文类型使用内置默认模板：

- IEEE 论文 → `IEEEtran` 文档类（内置）
- ACM 论文 → `acmart` 文档类（内置）
- 其他 → `article` 文档类（内置）
