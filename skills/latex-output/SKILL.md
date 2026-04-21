---
name: latex-output
description: Use when user asks to output paper as LaTeX, provides a LaTeX template, or targets a journal requiring LaTeX format - converts Markdown chapters to compilable .tex files with BibTeX references
# Hermes Agent
tools: [bash, read, write, edit]
# WorkBuddy MCP
mcp_servers: []
# Claude Code
subagent_types: []
---

# LaTeX Output Skill

将论文内容从 Markdown 格式输出为可编译的 LaTeX 项目，支持用户自定义模板。

---

## 一、触发场景

1. 用户明确要求 LaTeX 输出
2. 用户提供了 LaTeX 模板
3. 目标期刊或学校强制要求 LaTeX 格式
4. Writing Agent 完成初稿后，用户要求生成可提交的编译版本

---

## 二、模板存放与解析

### 2.1 模板路径

模板文件放置在 `latex-templates/` 目录下：

```
latex-templates/
├── README.md              # 模板使用说明
├── .cls 文件              # 文档类文件
├── .sty 文件              # 样式文件
├── main-template.tex      # 主文件示例
└── figures/               # 模板自带的示例图片
```

### 2.2 模板解析重点

| 解析对象 | 识别方式 | 处理策略 |
|----------|----------|----------|
| 文档类 | `\documentclass{...}` | 保留用户的文档类 |
| 章节命令 | `\section`, `\subsection`, `\subsubsection` | 映射 Markdown 标题层级 |
| 特殊环境 | `abstract`, `figure`, `table`, `equation` | 保留环境结构 |
| 引用命令 | `\cite{...}`, `\bibliography{...}` | 转换引用格式 |
| 自定义命令 | `\newcommand`, `\def` | 保留不变 |

---

## 三、执行工作流（Checklist）

### 阶段 1：模板检测与确认

- [ ] 检查 `latex-templates/` 是否存在用户模板
- [ ] 如果存在，询问用户确认使用该模板
- [ ] 如果不存在，根据论文类型选择默认方案：
  - IEEE 会议论文 → `IEEEtran` 文档类
  - IEEE 期刊论文 → `IEEEtran` 文档类（journal 模式）
  - ACM 会议论文 → `acmart` 文档类
  - 用户指定 → 使用用户提供的模板

### 阶段 2：解析模板结构

- [ ] 识别模板中的章节命令层级
- [ ] 识别格式要求（单栏/双栏、页边距、字号）
- [ ] 识别特殊环境（摘要、致谢等）
- [ ] 记录模板的编译方式（pdflatex/xelatex/lualatex）

### 阶段 3：Markdown → LaTeX 转换

- [ ] 将 `chapters/*.md` 逐个转换为 `.tex` 文件
- [ ] 生成 `main.tex` 主入口文件
- [ ] 生成 `references.bib` BibTeX 文件
- [ ] 处理图片引用（路径、格式）
- [ ] 转义 LaTeX 特殊字符

### 阶段 4：验证可编译性

- [ ] 运行编译命令确认无错误
- [ ] 检查引用是否正确解析
- [ ] 检查图片是否正确嵌入
- [ ] 生成 PDF 预览

---

## 四、输出目录结构

```
<project-root>/
├── latex-templates/         # 原始模板（不改动）
├── chapters/                # Markdown 源文件（保留）
│   ├── 00-abstract.md
│   ├── 01-introduction.md
│   ├── 02-related-work.md
│   ├── 03-methodology.md
│   ├── 04-experiments.md
│   ├── 05-discussion.md
│   └── 06-conclusion.md
├── tex/                     # LaTeX 输出目录
│   ├── main.tex             # 主入口文件
│   ├── 00-abstract.tex
│   ├── 01-introduction.tex
│   ├── 02-related-work.tex
│   ├── 03-methodology.tex
│   ├── 04-experiments.tex
│   ├── 05-discussion.tex
│   └── 06-conclusion.tex
├── figures/                 # 图片文件
├── references.bib           # BibTeX 参考文献
└── plan/
    └── compile-notes.md     # 编译说明与错误记录
```

---

## 五、Markdown → LaTeX 转换映射

### 5.1 标题层级

| Markdown | LaTeX（article 类） | LaTeX（IEEEtran） |
|----------|---------------------|-------------------|
| `# Title` | `\section{Title}` | `\section{Title}` |
| `## Subtitle` | `\subsection{Subtitle}` | `\subsection{Subtitle}` |
| `### Subsubtitle` | `\subsubsection{Subsubtitle}` | `\subsubsection{Subsubtitle}` |
| `#### Level 4` | `\paragraph{Level 4}` | 不推荐使用 |

### 5.2 格式元素

| Markdown | LaTeX |
|----------|-------|
| `**bold**` | `\textbf{bold}` |
| `*italic*` | `\textit{italic}` |
| `` `code` `` | `\texttt{code}` |
| `[link](url)` | `\href{url}{link}` |
| `![alt](path)` | `\includegraphics[width=\columnwidth]{path}` |
| `$inline math$` | `$inline math$`（保留） |
| `$$display math$$` | `\[display math\]` 或 `\begin{equation}...\end{equation}` |

### 5.3 特殊字符转义

必须转义的 LaTeX 特殊字符：

```
# → \#    $ → \$    % → \%    & → \&    _ → \_
{ → \{    } → \}    ~ → \textasciitilde{}    ^ → \textasciicircum{}
```

注意：已处于数学环境中的字符不需要转义。

---

## 六、IEEE/ACM 模板适配

### 6.1 IEEEtran（默认）

```latex
\documentclass[conference]{IEEEtran}
% 期刊论文使用: \documentclass[journal]{IEEEtran}

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}

% 中文支持（如需要）
% \usepackage{ctex}  % 需要 XeLaTeX 编译

\begin{document}

\title{Paper Title}
\author{\IEEEauthorblockN{Author Name}
\IEEEauthorblockA{Affiliation\\
Email}}

\maketitle

\begin{abstract}
Abstract content here.
\end{abstract}

\input{tex/01-introduction}
\input{tex/02-related-work}
\input{tex/03-methodology}
\input{tex/04-experiments}
\input{tex/05-discussion}
\input{tex/06-conclusion}

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

### 6.2 acmart

```latex
\documentclass[sigconf]{acmart}
% 期刊使用: \documentclass[journal]{acmart}

\acmConference{Conference Name}{Year}{Location}
\acmDOI{10.1145/xxxxxxx}

\begin{document}
\title{Paper Title}
\author{Author Name}
\affiliation{Institution}
\email{email@example.com}

\maketitle

\begin{abstract}
Abstract content here.
\end{abstract}

\input{tex/01-introduction}
% ... 其他章节 ...

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}

\end{document}
```

---

## 七、编译说明

### 7.1 推荐编译命令

```bash
# 一键编译（推荐）
latexmk -xelatex main.tex

# 手动编译（标准流程）
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

### 7.2 中文论文编译

中文环境**必须**使用 XeLaTeX 或 LuaLaTeX：

```bash
latexmk -xelatex main.tex
```

并在 `main.tex` 中添加：

```latex
\usepackage{ctex}  % 或 \usepackage{xeCJK}
```

### 7.3 常见编译错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Undefined control sequence` | 使用了未定义的命令 | 检查是否缺少宏包 |
| `Missing $ inserted` | 数学符号不在数学环境中 | 用 `$...$` 包裹 |
| `File not found` | 图片或 .tex 文件路径错误 | 使用相对路径 |
| `Citation undefined` | BibTeX 未正确运行 | 执行完整编译流程 |
| `Encoding error` | 非ASCII字符 | 使用 XeLaTeX + ctex |
| `Overfull hbox` | 行溢出 | 调整 `\sloppy` 或调整文字 |

---

## 八、无模板时的处理

如果未检测到模板：

1. **提示用户提供模板** — "请将 LaTeX 模板文件放入 `latex-templates/` 目录"
2. **根据论文类型使用默认模板** — IEEEtran 或 acmart
3. **退回 Markdown 格式** — 如果用户不需要 LaTeX 输出

---

## 九、质量检查

- [ ] `main.tex` 可无错误编译
- [ ] 所有章节文件正确 `\input`
- [ ] 引用格式正确（IEEE 或 ACM 标准）
- [ ] 图片路径正确，图片可见
- [ ] PDF 输出内容与 Markdown 原文一致
- [ ] 无 LaTeX 编译警告（或已处理）
