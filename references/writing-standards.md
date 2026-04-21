# Writing Standards — 学术论文写作规范

面向 IEEE/ACM 顶会顶刊的英文论文写作标准。所有 Writing Agent 必须严格遵守。

---

## 一、去 AI 化语言规范

### 1.1 禁用表达

#### AI 高频词替换表

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
| showcase | show, demonstrate, present |
| depict | show, illustrate, present |
| facilitate | enable, allow, support |
| harness | use, exploit, employ |
| aforementioned | previously discussed, earlier |
| plethora | many, numerous, a range of |
| embark on | begin, start, initiate |
| ensure that | guarantee, make certain |

#### 机械过渡词（Mechanical Transitions）

| 禁用 | 替代策略 |
|------|----------|
| Firstly / Secondly / Thirdly | 语义衔接：Following this approach, Building upon X, In contrast to X |
| Moreover / Furthermore / Additionally | 逻辑连接：This improvement stems from..., A complementary finding is... |
| Lastly / Finally (作为过渡) | 自然收束：These results collectively suggest..., Taken together,... |
| In addition / Besides | 并列表达：X also achieves..., Concurrent with this,... |

#### 空壳强调句（Empty Emphasis）

| 禁用 | 替代策略 |
|------|----------|
| It is worth noting that | 直接陈述事实 |
| It should be pointed out that | 直接陈述事实 |
| Importantly / Significantly | 用数据支撑：X achieves 15% improvement over Y |
| It is obvious that / Clearly | 如真则显而易见，无需声明；如不真则不可声称 |
| Needless to say | 真的不用说 |

#### 空洞修饰词（Hollow Modifiers）

| 禁用场景 | 替代策略 |
|----------|----------|
| very / extremely / highly (无数据时) | 量化描述：improves by 23.5% |
| significantly (无统计检验时) | 仅在有 p-value 时使用 |
| huge / massive / tremendous | 量化描述或使用 moderate, substantial |

#### 主观引导句（Subjective Openers）

| 禁用 | 替代策略 |
|------|----------|
| We believe / We think | The evidence suggests / The results demonstrate |
| In our opinion / In our view | Based on the experimental findings |
| We feel that | The data indicate that |

### 1.2 推荐表达模式

#### 因果衔接

```
X enables Y by... → X mitigates Y through... → X arises from Y because...
```

#### 对比衔接

```
Unlike X, Y achieves... → In contrast to X, Y... → While X requires..., Y eliminates...
```

#### 递进衔接

```
Building upon X, this work... → Extending the framework of X,... → A natural question beyond X is...
```

### 1.3 句法与信息密度

1. 一句话只承载一个核心动作
2. 避免等长句连续出现（长短句交替）
3. 保留方法、条件、对象和数据，不用模糊表述
4. 列表转段落时补足主语、谓语和连接成分

---

## 二、输出排版规范

### 2.1 正文规范

1. 段落之间空一行
2. 正文不使用加粗（除术语首次定义）
3. 不使用斜体强调（仅用于数学变量和拉丁术语如 et al.）
4. 正文段落优先连续叙述，不用项目符号堆砌观点
5. 同一段保持单一中心观点

### 2.2 允许使用列表的场景

仅以下场景可用列表：
- 实验参数配置
- 明确的枚举型定义
- 检查清单

**论文正文默认不用列表。**

---

## 三、段落构建规则

### 标准学术段落结构

1. **主题句**（Topic Sentence）：本段核心论点
2. **支撑句**（Supporting Sentences）：证据、数据、引用
3. **收束句**（Concluding Sentence）：过渡或小结

### 段落长度

- 英文正文：100-200 词
- Abstract：整体 150-300 词
- Introduction 各段：120-180 词

### 段落间过渡

不使用显式过渡词，而通过语义逻辑自然过渡：

```
[前段末尾提出问题或现象]
[后段开头直接回应或展开]
```

---

## 四、引用规范

### 4.1 引用格式

#### IEEE 格式（默认）

正文引用：`[1]`, `[1], [2]`, `[1]-[3]`

参考文献格式：
```
[1] A. Author and B. Author, "Title of paper," in Proc. Conf. Name, City, Country, Year, pp. 1-10.
[2] A. Author, "Title of article," Journal Name, vol. X, no. Y, pp. 1-10, Month Year.
```

#### ACM 格式

正文引用：`[1]`, `[Author Year]`（取决于具体会议要求）

参考文献格式：
```
[1] Author, A. and Author, B. Year. Title. In Proceedings of Conference Name (Abbreviation 'Year). Publisher, City, Country, Pages.
```

### 4.2 引用规则

1. **绝不编造文献**
2. 引用必须可追溯（作者、年份、出处至少完整两项）
3. 全文引用格式统一
4. 正文引用与参考文献列表一一对应
5. 每个引用都有上下文说明其与本研究的关系

### 4.3 引用位置

- 论点引用：紧跟在声称之后
- 方法引用：在方法描述处
- 数据引用：在数据来源处
- 不在段首引用，除非引用本身是段落主题

---

## 五、IEEE/ACM 论文结构标准

### 会议论文（Conference Paper）

典型结构（8-10 页）：

```
Abstract
I. Introduction
II. Related Work
III. System Architecture / Methodology
IV. Experiment Setup
V. Results and Discussion
VI. Threats to Validity (可选但推荐)
VII. Conclusion
References
```

### 期刊论文（Journal Article）

典型结构（12-20 页）：

```
Abstract
I. Introduction
II. Background and Motivation
III. Related Work
IV. System Design / Methodology
V. Implementation
VI. Evaluation
   A. Experiment Setup
   B. Results
   C. Discussion
VII. Threats to Validity
VIII. Conclusion
References
```

---

## 六、三轮质量检查

### 第一轮：结构检查

- [ ] 正文是否存在列表化
- [ ] 段落是否围绕单一中心
- [ ] 章节逻辑是否连续
- [ ] 引用分布是否均匀

### 第二轮：语言检查

- [ ] 是否出现禁用过渡词
- [ ] 是否出现禁用强调句式
- [ ] 是否存在无信息量形容词堆积
- [ ] 是否出现主观化表述
- [ ] 长短句是否交替

### 第三轮：排版检查

- [ ] 是否有无意义加粗
- [ ] 段间是否统一空一行
- [ ] 引用格式是否统一
- [ ] 图表标题是否规范
