---
name: prompts-collection
description: Use when translating, polishing, or de-AIifying academic text - provides ready-to-use prompt templates for translation, revision, de-AIification, and figure/table caption generation
allowed-tools: Read Write Edit
---

# Prompts Collection — 学术文本提示词集合

整合了学术论文写作中常用的翻译、润色、去AI化、扩写缩写、逻辑检查、图表标题生成、审稿视角等提示词模板。Writing Agent 可按需选用。

---

## 一、翻译类

### 1.1 中文转英文（学术写作）

```
You are a senior researcher and experienced reviewer for IEEE/ACM top venues. Translate the following Chinese text into formal academic English for a research paper.

Rules:
- Remove all AI-flavored expressions (leverage, delve into, comprehensive, etc.)
- Use rigorous, objective academic tone
- No bullet-point lists in body text; convert to flowing paragraphs
- Preserve all LaTeX commands and citation markers (e.g., \cite{}, [1])
- Keep technical terms consistent with the field
- Output only the translated text, no explanations

Text to translate:
[PASTE CHINESE TEXT HERE]
```

### 1.2 英文转中文（计算机科学领域）

```
将以下英文学术论文片段翻译为中文。要求：
- 删除所有 LaTeX 引用命令（如 \cite{key}、[1] 等），仅保留纯文字
- 严格直译，不添加解释或润色
- 只输出纯中文段落，不加任何格式标记或注释

Text:
[PASTE ENGLISH TEXT HERE]
```

---

## 二、润色类

### 2.1 英文论文深度润色

```
You are an expert academic editor for IEEE/ACM journals. Deeply revise the following text for:
1. Formal academic register — eliminate colloquialisms, contractions, and informal phrasing
2. Sentence variety — alternate sentence lengths and structures
3. Logical flow — ensure each sentence builds on the previous one
4. Grammar and precision — fix errors, tighten word choice
5. No abbreviations in body text (e.g., write "cannot" not "can't")

Rules:
- Preserve all LaTeX commands and citation markers
- Output the revised text followed by a brief change summary

Original text:
[PASTE TEXT HERE]
```

### 2.2 中文论文润色

```
润色以下中文学术论文片段。要求：
- 修正口语化表达和语法错误
- 补全逻辑断层
- 使用全角标点
- 清晰处保留原样，不要过度修改
- 只输出润色后的文本

Text:
[PASTE CHINESE TEXT HERE]
```

---

## 三、去AI化类

### 3.1 英文去AI味

```
De-AIify the following academic text. Remove these hallmarks of AI-generated writing:
- Overused words: leverage, delve into, comprehensive, multifaceted, intricate, nuanced, paramount, pivotal, notably, underscores, landscape, realm
- Mechanical transitions: Moreover, Furthermore, Additionally, Firstly/Secondly/Lastly
- Empty emphasis: It is worth noting that, Importantly, It should be emphasized that
- Bullet-point paragraphs → convert to connected prose with subject-verb-object
- Repetitive sentence structures

Replace with:
- Direct factual statements
- Evidence-based claims
- Semantic transitions (cause-effect, contrast, elaboration)
- Varied sentence lengths

Output only the revised text.

Text:
[PASTE TEXT HERE]
```

### 3.2 AI味词汇替换表

| ❌ AI 高频词 | ✅ 替代词 |
|-------------|----------|
| leverage | use, employ, utilize (sparingly) |
| delve into | examine, analyze, investigate |
| comprehensive | complete, thorough, full |
| multifaceted | complex, multi-step, layered |
| intricate | detailed, fine-grained, complex |
| nuanced | subtle, context-dependent |
| paramount | critical, essential, primary |
| pivotal | key, central, crucial |
| notably | specifically, in particular |
| underscores | shows, demonstrates, confirms |
| landscape | area, domain, field |
| realm | area, domain, context |
| showcases | shows, demonstrates, presents |
| depict | show, illustrate, present |
| facilitate | enable, allow, support |
| harness | use, exploit, employ |
| aforementioned | previously discussed, earlier |
| plethora | many, numerous, a range of |
| embark on | begin, start, initiate |
| ensure that | guarantee, make certain |

### 3.3 中文去AI味

```
去除以下中文文本的AI腔调。具体要求：
- 删除"首先、其次、最后、此外、另外"等机械连接词
- 删除"值得注意的是、需要指出的是、重要的是"等空壳强调句
- 将项目符号列表转为连贯叙述段落
- 删除格式标记（如加粗、代码块等）
- 使用学术书面语替代口语化表达
- 只输出修改后的文本

Text:
[PASTE CHINESE TEXT HERE]
```

### 3.4 中文 AI 味替换表

| ❌ AI 高频表达 | ✅ 替代 |
|---------------|--------|
| 首先 | （删除，直接陈述） |
| 其次 | （删除，语义衔接） |
| 最后 | （删除，自然收束） |
| 此外/另外 | （删除，并列叙述） |
| 值得注意的是 | （删除，直接说事实） |
| 需要指出的是 | （删除，直接说事实） |
| 重要的是 | （删除，用数据支撑） |
| 综上所述 | 综上 / 实验结果表明 |
| 具有重要意义 | 对 X 有 Y 影响 |
| 发挥着关键作用 | 直接描述具体作用 |
| 不可或缺的 | 必要的、核心的 |

---

## 四、扩写与缩写

### 4.1 缩写（约减 5-15 词）

```
Slightly condense the following academic paragraph by 5-15 words. Use syntactic compression:
- Convert subordinate clauses to phrases
- Change passive to active where possible
- Remove redundant modifiers
- Do NOT lose any factual content or technical detail
- Preserve all LaTeX commands and citations

Text:
[PASTE TEXT HERE]
```

### 4.2 扩写（约增 5-15 词）

```
Slightly expand the following academic paragraph by 5-15 words. Add content by:
- Uncovering implicit causal relationships
- Expanding implicit premises
- Adding brief context where assumptions are unstated
- Do NOT add meaningless adjectives or filler
- Preserve all LaTeX commands and citations

Text:
[PASTE TEXT HERE]
```

---

## 五、逻辑检查

### 5.1 终稿逻辑检查

```
You are a strict logic reviewer for an IEEE/ACM paper. The following text is assumed to be near-final quality. Check ONLY for:
1. Fatal logical contradictions
2. Terminology inconsistency across sections
3. Severe grammatical errors that change meaning

Do NOT flag:
- Style preferences
- Minor word choices
- Things that could go either way

Output format:
- If no issues: "No fatal issues found."
- If issues found: list each with [SECTION] location and exact quote

Text:
[PASTE TEXT HERE]
```

---

## 六、图表标题生成

### 6.1 图标题（Figure Caption）

```
Generate a professional figure caption for an IEEE/ACM paper.

Rules:
- Use noun phrase with Title Case if the caption is a noun phrase
- Use sentence case if the caption is a complete sentence
- Do NOT start with "Figure showing..." or "Diagram of..."
- Start directly with the descriptive content
- Include brief explanation of key elements if needed

Figure description:
[DESCRIBE THE FIGURE HERE]

Generated caption:
```

### 6.2 表标题（Table Caption）

```
Generate a professional table caption for an IEEE/ACM paper.

Rules:
- Prefer structures: "Comparison with ...", "Ablation study on ...", "Performance of ... on ..."
- Avoid: "showcase", "depict", "demonstrates that"
- Keep concise and informative
- Table captions typically go above the table in IEEE format

Table description:
[DESCRIBE THE TABLE HERE]

Generated caption:
```

---

## 七、审稿视角模拟

### 7.1 Reviewer 视角审视

```
You are a harsh senior reviewer for a top IEEE/ACM venue. Analyze the following paper section and output:
1. One-sentence summary of the section's contribution
2. Contribution points (numbered)
3. 3-5 fatal weaknesses with specific locations
4. Overall score (1-10)
5. Strategic improvement suggestions

Be constructive but uncompromising. Focus on technical substance over presentation.

Text:
[PASTE TEXT HERE]
```

---

## 八、使用建议

1. 提示词可直接复制使用，将 `[PASTE TEXT HERE]` 替换为实际内容
2. 根据任务按需选择对应的提示词类别
3. 保持提示词完整以获得最佳效果
4. 多次润色时，每次只使用一个提示词，避免过度修改
5. 去AI化后必须运行 `scripts/style_check.sh` 验证
