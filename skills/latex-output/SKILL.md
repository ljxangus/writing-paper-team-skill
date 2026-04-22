---
name: latex-output
description: Use when user asks to output paper as LaTeX, generate PDF from LaTeX, provides a LaTeX template, or targets a journal requiring LaTeX format - converts Markdown chapters to compilable .tex files, compiles to PDF with latexmk/xelatex/pdflatex, and validates the output
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

## 七、LaTeX → PDF 编译流程

### 7.1 编译环境检测

编译前**必须**先检测系统 LaTeX 环境：

```bash
# 检测编译工具链
which latexmk && latexmk --version
which xelatex && xelatex --version | head -1
which pdflatex && pdflatex --version | head -1
which bibtex && bibtex --version | head -1
which biber && biber --version | head -1

# 检测 IEEEtran / acmart 文档类是否可用
kpsewhich IEEEtran.cls
kpsewhich acmart.cls
```

**环境不满足时的处理：**

| 缺失组件 | 处理方式 |
|----------|----------|
| 无 latexmk | 使用手动编译流程（xelatex → bibtex → xelatex ×2） |
| 无 xelatex | 降级为 pdflatex（不支持中文） |
| 无 bibtex/biber | 警告用户引用可能无法解析 |
| 缺少文档类 | 提示安装：`tlmgr install ieee-conf` 或 `tlmgr install acmart` |

### 7.2 编译策略选择

根据论文特征自动选择编译策略：

| 场景 | 编译引擎 | 命令 |
|------|----------|------|
| 中文论文 / 含 Unicode | XeLaTeX | `latexmk -xelatex main.tex` |
| 纯英文 IEEE 论文 | pdfLaTeX | `latexmk -pdf main.tex` |
| 含复杂字体需求 | LuaLaTeX | `latexmk -lualatex main.tex` |
| 用户指定引擎 | 用户选择 | 按用户指定 |

**自动判断逻辑：**
1. `main.tex` 中含 `\usepackage{ctex}` 或 `\usepackage{xeCJK}` → XeLaTeX
2. `main.tex` 中含中文内容（正则检测 `[\x{4e00}-\x{9fff}]`）→ XeLaTeX
3. 用户模板 `.cls` 文件名含 `ctex` → XeLaTeX
4. 默认 → pdfLaTeX（纯英文 IEEE 论文最快）

### 7.3 一键编译（推荐）

```bash
# 进入 tex 输出目录
cd <project-root>/tex/

# XeLaTeX 编译（中文 / Unicode）
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex

# pdfLaTeX 编译（纯英文）
latexmk -pdf -interaction=nonstopmode -file-line-error main.tex

# 清理辅助文件（编译成功后）
latexmk -c
```

**latexmk 参数说明：**

| 参数 | 说明 |
|------|------|
| `-xelatex` / `-pdf` / `-lualatex` | 指定编译引擎 |
| `-interaction=nonstopmode` | 遇到错误不停止（收集所有错误） |
| `-file-line-error` | 错误信息含文件名和行号 |
| `-c` | 清理辅助文件（保留 PDF） |
| `-C` | 清理所有生成文件（含 PDF） |
| `-outdir=build/` | 输出到指定目录 |

### 7.4 手动编译（标准四步流程）

当 `latexmk` 不可用时：

```bash
cd <project-root>/tex/

# Step 1: 首次编译（生成 .aux 文件）
xelatex -interaction=nonstopmode main.tex

# Step 2: 处理引用（生成 .bbl 文件）
bibtex main

# Step 3: 第二次编译（解析引用）
xelatex -interaction=nonstopmode main.tex

# Step 4: 第三次编译（确保交叉引用正确）
xelatex -interaction=nonstopmode main.tex
```

> ⚠️ 四步流程不可省略，否则引用和交叉引用可能不正确。

### 7.5 中文论文编译

中文环境**必须**使用 XeLaTeX 或 LuaLaTeX：

```bash
latexmk -xelatex -interaction=nonstopmode main.tex
```

并在 `main.tex` 中添加：

```latex
\usepackage{ctex}  % 或 \usepackage{xeCJK}
```

### 7.6 编译结果验证

编译完成后**必须**验证 PDF 生成：

```bash
# 检查 PDF 是否生成
ls -la main.pdf

# 检查 PDF 页数
pdfinfo main.pdf 2>/dev/null || echo "pdfinfo not available"

# 检查编译日志中的错误
grep -c "^!" main.log || echo "0 errors"

# 检查未定义引用
grep -c "Citation.*undefined" main.log || echo "0 undefined citations"

# 检查缺失图片
grep -c "File.*not found" main.log || echo "0 missing files"
```

**验证门控：**

| 检查项 | 通过条件 | 不通过处理 |
|--------|----------|------------|
| PDF 生成 | `main.pdf` 存在且 > 0 bytes | 检查编译日志修复错误 |
| 无致命错误 | `grep "^!" main.log` 返回 0 条 | 逐条修复后重新编译 |
| 引用完整 | 无 "Citation undefined" 警告 | 重新运行 bibtex + xelatex |
| 图片完整 | 无 "File not found" 警告 | 检查图片路径 |
| 页数合理 | PDF 页数 ≥ 预期（非 0 页或 1 页） | 检查 main.tex 结构 |

### 7.7 常见编译错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Undefined control sequence` | 使用了未定义的命令 | 检查是否缺少宏包 |
| `Missing $ inserted` | 数学符号不在数学环境中 | 用 `$...$` 包裹 |
| `File not found` | 图片或 .tex 文件路径错误 | 使用相对路径 |
| `Citation undefined` | BibTeX 未正确运行 | 执行完整编译流程 |
| `Encoding error` | 非ASCII字符 | 使用 XeLaTeX + ctex |
| `Overfull hbox` | 行溢出 | 调整 `\sloppy` 或调整文字 |
| `Missing package` | 缺少 LaTeX 宏包 | `tlmgr install <package>` |
| `Font not found` | 缺少字体 | 检查字体路径或使用 ctex 默认字体 |
| `BibTeX/Biber mismatch` | 引用处理器与配置不匹配 | 检查 `biblatex` 使用 biber，`natbib` 使用 bibtex |
| `Too many unprocessed floats` | 浮动体过多 | 添加 `\clearpage` 或使用 `[H]` 选项 |

### 7.8 编译辅助文件清理

编译成功后清理辅助文件，保持目录整洁：

```bash
# 仅清理辅助文件（保留 PDF）
latexmk -c

# 或手动清理
rm -f *.aux *.log *.out *.bbl *.blg *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
```

---

## 八、PDF 交付

### 8.1 PDF 输出路径

```
<project-root>/
├── tex/
│   ├── main.tex
│   ├── main.pdf          ← 编译生成的 PDF
│   └── ...
├── output/               ← 交付目录（可选）
│   ├── paper-v1.0.pdf    ← 带版本号的交付 PDF
│   └── compile-report.md ← 编译报告
└── ...
```

### 8.2 编译报告

编译完成后生成 `compile-report.md`：

```markdown
# LaTeX Compilation Report

## 基本信息
- 编译时间: YYYY-MM-DD HH:MM
- 编译引擎: XeLaTeX / pdfLaTeX / LuaLaTeX
- 编译次数: N 次（含 bibtex）
- 文档类: IEEEtran / acmart / 其他

## 编译结果
- ✅ PDF 生成成功
- PDF 路径: tex/main.pdf
- PDF 页数: N 页
- PDF 大小: X.XX MB

## 警告统计
- Undefined citations: 0
- Missing files: 0
- Overfull hbox: N
- Other warnings: N

## 错误列表
（如有错误，逐条列出文件名:行号:错误信息）
```

### 8.3 PDF 预览

编译成功后，使用系统默认 PDF 阅读器打开预览：

```bash
# macOS
open main.pdf

# Linux
xdg-open main.pdf

# 或使用 WorkBuddy 的预览功能
```

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
- [ ] **PDF 文件已生成**且大小 > 0 bytes
- [ ] **PDF 页数合理**（非 0 页或异常 1 页）
- [ ] **无未定义引用**（`grep "Citation.*undefined" main.log` 返回 0）
- [ ] **无缺失图片**（`grep "File.*not found" main.log` 返回 0）
- [ ] **编译报告已生成**（`compile-report.md`）
