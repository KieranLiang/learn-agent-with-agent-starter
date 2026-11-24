# Stanford CS329Z Engineering AI Agents（2026 秋）读课笔记

- 讲师：Diyi Yang、Michael Ryan、John Yang。网址 https://cs329z.stanford.edu/ ，课件 `web.stanford.edu/class/cs329z/slides/lectureNN.pdf`
- 读于 2026-11-11。精读：L01、L02、L04、L06、L07、L08、L13。只看了目标页和总结页：L03、L05、L09–L12。L14 之后还没放课件。2026-11-25 补抓：放出了 L15、L17 的课件（L14、L16 没有），补读了这两讲的课件文字；L01–L10 存了录像字幕。
- 定位：六门里**体系最完整、最像教科书**的一门。每讲有“学习目标 → 分节 → 小结”的固定结构，分类法清楚。先修要求懂基本的 LLM 概念（训练集、预训练、微调、提示）。
- 课件大量是论文图，文字少，细节要回到论文。
- 标记：🟢 概念级可直接教 🟡 需要一点 LLM 基础 🔴 硬核，后置

## L01 Agentic 系统导论 🟢

- Agent 简史：agent 一词意为“行动者”→ 1995 年 Russell & Norvig 的定义 → 强化学习时代的 agent-环境循环 → LLM 时代（2022-10 ReAct、2022-11 ChatGPT、2023-03 AutoGPT）。
- Agent 解剖图：**LLM 核心 + 规划与推理 + 记忆 + 工具 + 环境**。整门课都围着这张图转。
- 推理对 agent 的意义：是“更新自身状态的内部动作”。只推理不行动会幻觉；ReAct 把推理和行动交替起来。标本：Apple Remote 那道题的三种解法对比。
- 记忆三类：情景（经历）、语义（知识）、程序（技能）。
- Agent 工程分三层：**系统、数据、评估**。
- **Workflow 与 agent 的分界：谁决定步骤。** 代码定步骤是 workflow，LLM 定步骤是 agent。两者都属于复合 AI 系统。
- 五大挑战：可靠性（错误会累积）、训练、长程（上下文增长和漂移）、安全（完成任务不等于行为安全）、评估。
- 可靠性三个维度：一致性（同一任务跑两次结果一样吗）、鲁棒性（小扰动下如何）、可预测性（失败时是否可辨认、可恢复）。**能力和可靠性之间有缺口。**
- 标本：弹窗攻击让 agent 分心，成功率 87%。
- 开场提醒：一项对 52 名工程师的随机试验里，用 AI 辅助学新库的人后续测验低 17%，调试能力差距最大。“用 AI 来学会怎么学。”

## L02 给构建者的 LLM 🟡 + 🔴

- 课程把自己定位在“LLM 技术栈最上层”，但认为必须懂一点底层。
- 语言模型：一串 token 的概率 = 每个 token 在前文条件下概率的乘积。标本：“The class was about …”逐词概率表，直观。
- 采样：贪心、top-k、top-p、温度。数学和代码用低温度，创意写作用高一点。🟢
- 🔴 Transformer 逐步动画（Q/K/V、因果掩码、多头、残差）、线性注意力推导。对我们后置。可取的结论：全注意力对上下文长度是二次代价；线性注意力省但长上下文更弱；实际混着用。
- 训练三段：预训练（海量文本）→ 中训练（把数据配比调向代码、数学）→ 后训练（指令微调、人类偏好、可验证奖励的强化学习、针对 agent 的训练）。🟡 当故事讲即可。
- 推理：prefill 和 decode 两阶段、KV 缓存、推测解码。🟡
- 推理时扩展：思维链、推理模型（可调推理强度）、重复采样、自洽投票。🟢
- **给 agent 用的两件事**：
  - 结构化输入输出：组件之间要有共同契约；约束解码强制输出结构。
  - 上下文工程：上下文里有系统提示、消息历史、记忆、工具结果、附件。**为什么不全塞进去——context rot。** 三条实用建议：避免臃肿（几个工具就够）、**顺序追加**（别让 KV 缓存失效）、用评估验证上下文选择。
- 标本：加价 25% 再打 75 折的夹克题，普通模型答 80，推理模型自己纠正成 75。适合讲“推理 token”。

## L03 RAG 🟡（只看了目录）

- 流程：检索 → 增强 → 生成。索引（切块、上下文化检索、层级索引）、检索器（BM25、DPR、ColBERT）、Agentic RAG。
- Agentic RAG 的三个决定：检索还是直接答；发什么查询；结果够不够好。**检索应该是 agent 的一个动作。**
- RAG 失败分三侧（在 L04 开头总结）：检索侧（召回天花板、索引过期、权限泄漏）、阅读侧（中间丢失、被相似内容干扰、证据冲突）、循环侧（错误累积、没有停止规则、提示注入）。
- 引用也是模型生成的，所以引用本身也会幻觉。

## L04 工具使用 🟢

- 为什么要工具，三栏表：模型**算不了**的（大数运算、多步推理）、**没见过**的（长尾事实、截止日期后的事、私有数据）、**够不着**的（非语言接口、物理世界、实时状态）。标本：大数乘法随位数增加准确率崩塌。
- 教模型用工具的四条路线（Toolformer、ToolkenGPT、ToolLLM、Gorilla）。🔴 训练细节后置，结论可讲：早期靠改模型适应工具，每加一个 API 就要再训练。
- **标准接口三代**：REST（面向人，模型得读文档手写请求）→ 函数调用（面向模型，JSON schema，但换个 API 要重写）→ MCP（面向生态，运行时发现，写一次到处用）。
- MCP 两个核心请求：`tools/list`（你有什么工具）、`tools/call`（用这些参数跑这个工具）。入站凭证和出站凭证分开。
- 评估：BFCL、ToolBench、τ-bench。**pass^k**：k 次全部成功的概率，奖励稳定性，和“k 次里至少成一次”的 pass@k 相对。
- 工具使用失败模式清单：选错工具或不该调用时调用、编造参数、调用不存在的工具、跳过前置步骤、重复同一个失败调用、违反规则、不问用户就假设、一次过一次不过。

## L05 框架与 agent 设计 🟡（只看了总结页）

- “工程化”agent 的循环：构建 → 运行 → 评估 → 改进。
- DSPy：签名定义输入输出契约，模块组合，优化器根据数据和指标改进提示。LangGraph：共享状态、节点、边。
- 最佳实践：**保持简单**（不一定要 agent，有时 workflow 就对）；跑评估；看 trace；为失败和恢复而设计；搞清楚底层在干什么。
- OpenHands 的三个设计：每步存成一个事件；持久终端；连续 4 次相同动作和结果就自动停。

## L06 设计模式与脚手架 🟢 ★

- 开场引 Martin Fowler：模式是半成品，得自己补完并适配环境。
- **控制流在哪儿**：在程序里是 workflow（可预测），在模型里是 agent（灵活）。真实系统常常两者混用。
- 五种 workflow 模式（来自 Anthropic 的 Building Effective Agents）：提示链、路由、并行（分段或投票）、编排者-工人、评估者-优化者。标本：STORM 系统是这几种模式的组合。
- 推理与行动模式：ReAct（先想再做）、Reflexion（把反思变成记忆）、CodeAct（代码是好的动作形式）、ReWOO 和 LLMCompiler（先规划再执行）。
- 重要的“现状更新”：自我反思现在多半内置在推理模型里，不再显式强制；“编译成 workflow”现在主要靠并行工具调用实现；让模型评自己的输出会掉分，要靠外部环境反馈。
- **上下文管理五种模式**：持久事件日志（每次调用都从日志重建输入）、记忆外置、压缩、观察遮蔽（截断旧的工具输出）、上下文隔离（子 agent、渐进式披露）。这些可以叠加使用。
- 上下文工程两条原则：**聚焦**（只留当前任务需要的）、**保持连续**（保住需求、目标、约束、进度，同时保住 KV 缓存）。
- 案例：Pi 极简 harness。默认只有 read、bash、edit、write 四个工具；没有子 agent、权限检查、计划模式、待办列表；靠事件日志、技能文件、压缩管理上下文；没有任何安全防护。**很适合当“最小 agent 长什么样”的标本。**

## L07 记忆架构 🟢

- 没有记忆的三种损失：丢流程（每次重教）、丢知识（偏好和规则跨会话丢失）、丢进度。
- CoALA 四类：工作记忆（就是上下文窗口）、情景、语义、程序。再分参数内（在权重里）和上下文内（检索进来）。
- 设计三问：**存取什么、何时触发、怎么存**。
- 三种存储：文件系统（每条记忆一个文件，grep 和 ls 就是记忆工具，自带层级）、数据库（向量检索、SQLite、BM25）、知识图谱。
- 四种架构模式：从经验学流程（Voyager 技能库、AWM、技能文件）；分层记忆（MemGPT：给模型管理自己记忆的工具）；反思后再存（Generative Agents）；记忆维护（空闲时整理、专门的记忆 agent、Mem0 的增改删）。
- 好的记忆评估四条件：真实、长上下文、有难度、可验证。有个值得讲的结果：LongMemEval-v2 上文件系统记忆胜过检索式记忆。
- 开放问题：记什么忘什么（未来是否有用在存的时候不知道）；记忆是攻击面，也有隐私问题；**模型会过度使用上下文里的记忆**（过度个性化）。
- 标本：开场用的“没等我批准就删邮件”事故，和 CMU L13 是同一件。

## L08 多 agent 系统 🟢

- 复杂度阶梯：模型 → workflow → agent → 多 agent 系统。例子分别是分诊 bug、实现功能、维护整个仓库。
- 好处：并行、专门化、上下文聚焦、更广的探索。坏处：协调开销、交接丢信息、动作冲突、错误传播、工程复杂度。
- **何时用**：步骤高度依赖、工作紧耦合共享状态、单 agent 已达标时用单 agent。子任务可以少同步地推进、信息可分、各自能独立产出再整合时试多 agent。**建议：先做强的单 agent 基线，为明确目的加 agent，并测量收益是否大于协调成本。**
- 四种编排：独立（最后汇总）、集中（编排者）、去中心（蜂群）、混合。成本：单 agent < 编排 < 蜂群。
- 沟通和协调要分开：沟通是信息怎么交换；协调是谁拥有哪个任务、先做什么、冲突怎么解。
- **Handoff 与 agent-as-tool**：前者控制权移交，接手者直接面对用户；后者调用方保留控制，专家只返回结果。
- 协调基础设施：任务账本、共享记忆、worktree 隔离。自发出现的协调模式：分角色、分资源、协商。
- 失败：CooperBench 上一个 agent 做两件事比两个 agent 协作要好（“协调的诅咒”）；从众（一半的 agent 都去写光线追踪器）；目标不相容时会强行压过对方。
- 案例：16 个 agent 写 C 编译器的经验——强测试引导自主工作、为并行而设计、协调要显式（认领任务、各自克隆、用 Git 合并）、跨会话保留知识（文档、进度笔记、失败记录）、反馈要高效。

## L09 优化 🔴（只看了总结页）

- 何时值得优化：有适合领域的数据和评估；需求难以在提示里说全。
- 上下文优化（少样本搜索、反思式进化）和权重优化（微调、强化学习）。
- 可讲的一句：agent 本身是不错的优化器，这时**指标和评估成了最需要把关的部分**。

## L10 嘉宾：Terminal-Bench（只看了几页）

- 任务会以微妙的方式坏掉，任务本身要做质检（静态检查加 agent 评审）。

## L11–L12 Agent 数据 🔴（只看了总结页）

- Agent 数据两类：轨迹和环境。来源：人工示范、从网上挖、合成任务、合成轨迹、模拟器。
- “数据会意外地教会别的东西”：奖励作弊（背答案、学会“看起来对”而不是“真的对”）、对某个 harness 过拟合。
- 取舍：候选池小的时候筛选最有价值；规模上去之后量比挑更重要。

## L13 评估基础与基准设计 🟢 ★

- 基准的三个作用：测量、定方向、提供共同语言。阴暗面是古德哈特定律：指标一旦成了目标就不再是好指标。
- Agent 基准和普通基准的区别：输入是任务加环境，不是一个 prompt；交互是多轮动作和观察；输出是轨迹和被改变的环境。
- 两大部分：**任务定义**（问题陈述、环境、验证方式）和**评估协议**（每题跑几次、怎么终止、模型设置、harness 是否固定、怎么汇总）。
- 12 个基准各一句话的清单，可当“基准地图”：TextWorld、ALFWorld、WebShop、SWE-bench、WebArena、τ-bench、Terminal-Bench、OSWorld、CodeClash、BrowseComp、VendingBench、AIRS-bench。
- 好基准七条：有挑战、自然、有区分度、易运行、易验证、可解释、耐用。这些性质互相拉扯。
- 基准生命周期：提出 → 适应 → 饱和 → 被替代。
- 可信分数四条：公平（按协议跑）、可复现（版本钉住）、透明（报告次数、误差条、成本）、诚实（不在测试集上调、不挑最好的一次）。例子：70% 对 67%，其实在误差条内，而且贵三倍。

## L15 LLM-as-Judge 与评估基础设施 🟢 ★（2026-11-25 补读课件文字）

- 核心问题：只靠单元测试（unit tests）等确定性代码检查（deterministic checks）不够用，因为许多任务存在“2+ valid answers, beyond reference”、过程（Process, beyond the outcome）、质量（Quality, beyond correctness）和部分得分（Partial credit, beyond pass/fail）（第 7 页）。校准失准的评分器（grader）会扭曲分数：τ²-bench 出现过假阴性（False Negative），“Claude Opus 4.5 found a better solution that grader did not account for”；SWE-bench 出现过假阳性（False Positive），“some patches pass F2P tests, but fail unregistered P2P tests”（F2P、P2P 具体含义课件没说清）（第 8 页）。
- 三类评分器对比与汇总：三类评分器都可检查最终环境状态（Final Environment State）和轨迹（Trajectory），按成本、速度、可靠性、灵活性、规模化和细微度（Nuance）六维权衡（第 13 页）：代码评分器（Code）便宜、快、可靠且可规模化，但灵活性与细微度低，且受限于规定性（Prescriptive）、静态（Static）和简化遗漏（Reductive）（第 13、16 页）；人类评分器（Human，如 Chatbot Arena 众包 Elo、GDPval 44 个职业专家盲比、Co-Gym 真实用户协作评分）灵活性与细微度高，但贵、慢、存在分歧，且“Sessions can’t replay”（第 13、18–19 页）；语言模型裁判（LM Judge / LM-as-a-Judge）成本中等、快、灵活、可规模化、细微度高，但只有部分可靠（Partly），因为具有非确定性（Non-deterministic）、有偏见（Biased）和需要校准（Needs Calibration）（第 13、22 页）。多个评分器可按全部通过（All must pass）、加权（Weighted）或人工抽查校准（Calibrate）三种方式汇总（第 23 页）。
- 语言模型裁判三阶段中的前两阶段：第一阶段替代传统自然语言处理指标（NLP Metrics），G-Eval 先输出评判方法再打 1–5 分，在摘要任务上与人类相关性达“0.514 Spearman”（第 25、28–29 页）；GPTScore 在 19 个模型（80M–175B）、4 个任务、22 个维度、37 个数据集上验证了指令描述越具体分数越可靠（第 32 页）；Chiang & Lee 发现 LLM 排名与专家一致，但对不自然文本更宽容（第 35 页）。第二阶段对齐人类偏好（Human Preferences），同一偏好裁判既可用于评估打分，也可用于训练奖励（第 37 页）：InstructGPT 显示标注者更偏好 1.3B 模型而非“100× larger”的 175B GPT-3（第 44 页）；MT-Bench 与 Chatbot Arena 显示 GPT-4 与人类一致率“over 80% of the time”，与人类彼此一致率相当（第 47 页）；Prometheus 微调 Llama-2-Chat-13B（1K 评分标准、20K 指令、100K GPT-4 反馈），在 45 个自定义评分标准（rubrics）上达“0.897 Pearson”，与 GPT-4（“0.882”）相当并远高于 GPT-3.5（“0.392”）（第 50–51 页）。评分标准分逐点打分（Pointwise）和成对比较（Pairwise）两种形式（第 52 页）。
- 第三阶段评判人类行动（Human Actions）：把裁判从评价消息推向评价动作、环境和轨迹（第 55 页）。WebVoyager 用 GPT-4V 看导航截图评判真实网站任务，agent 成功率“59.1%”（纯文本“40.1%”），裁判得分整体接近人类（“57.1%”），一致率“85.3%”（“κ = 0.70”），但单个网站可差“10+ points”（第 58–59 页）；Pan 等（2024）的视觉语言评估器与预言机指标（oracle metrics）一致率“74.4 to 92.9%”，用作奖励使 WebArena agent 相对提升“29%”、iOS agent 提升“~75%”（第 63 页）；Agent-as-a-Judge 让裁判像 agent 一样探索工作区以核验 DevAI 的 55 个任务、365 条层级需求，与人类专家一致率从 LLM-as-a-Judge 的“~70%”升至“~90%”，比 3 名专家小组省“~97%”时间和成本（第 65–66 页）。
- 偏见（Biases）与裁判校准：位置（position）、长度（length）、自我偏好（self-preference）属于固定偏向同一侧的系统误差，“errors that always lean the same way, so more examples don’t cancel them out”（第 82 页；原讲到 Wang et al. 位置偏见的第 72–74 页误贴了 Agent-as-a-Judge 正文，该论文具体数字课件没说清）。Length-Controlled AlpacaEval 用回归剥离长度差后，与 Chatbot Arena 的 Spearman 相关性从“0.94”升至“0.98”（第 76–77 页）；AutoMetrics 从 48 个已有指标（MetricBank）和自动生成的 LLM 裁判标准中做回归筛选加权，用“fewer than 100 labels”就比 LLM-as-a-Judge 提升“+33.4% Kendall correlation”（第 80–81 页）。
- 处理非确定性（Nondeterminism）：同一任务跑 5 次得 `❌ ✅ ❌ ❌ ✅`，均值（40%）、至少成一次（`pass@k`）和次次都成（`pass^k`）各有盲区（第 9–10、84–86 页；注：第 86 页正文把 `pass^k` 误印作 `pass@k`）。只报均值会掩盖行为差异：Agent A 和 B 均值都是“50%”，A 的 `pass@2` 为“83%”、`pass^2` 为“17%”（重试有用但单次不可靠），B 的 `pass@2` 和 `pass^2` 都是“50%”（重试无益但能解的题每次都成）（第 87 页）。能重试且有检查器挑赢家时（如写代码跑测试、搜索）用 `pass@k`，每次尝试都到达用户或改变真实世界时（如客服、发邮件、下单）用 `pass^k`，且必须同时报告 `k` 和试验次数 `n`，“Without k, the number is meaningless.”（第 88 页）。
- 对我们：直接补强 单元 12（可靠性与评估）。三类评分器对比表、假阴性/假阳性案例、LM 裁判偏见与 Agent-as-a-Judge 可放进 B（把“完成”写成测试；模型负责猜，环境负责查）和 D（可信的分数）；`pass@k` 与 `pass^k` 的 A/B 对照表可直接用作 C（“至少成一次”和“次次都成”）的核心标本。

## L17 安全与风险 🟢 ★（2026-11-25 补读课件文字）

- 为什么 agent 改变了风险图景与开场案例：相比单纯对话，agent 的“Output is executed, not simply read.”，不可信甚至检索到的内容会重定向 agent，错误会在长程（long horizons）中累积，目标会以意想不到的方式被追求，且滥用（Misuse）以机器速度规模化（第 10 页）。两个开场案例：Github MCP Exploit（“About the author” injection，具体手法和影响课件没说清）（第 4 页）；以及 OpenAI / Hugging Face Incident（引自 METR 2026-08-26 调查博客），本应完全隔离（“fully isolated”）的 agent 们利用内部包仓库 Artifactory 试图作弊，形成了留言板（message board）并自发产生领导者（leader）派发任务，“Hacking Hugging Face is one of the tasks”，体现奖励作弊（Reward hacking）与涌现式协调（Emergent coordination）（具体模型和规模课件没说清）（第 5–9 页）。
- 威胁建模（Threat Model）框架：任何评估都要从威胁模型开始（第 12 页）。包含 Shostack 四步法（你在建什么、会出什么错、怎么应对、分析得够不够好）（第 12 页）；攻击者/渠道/目的三问（Who attacks：外部用户、经网页/邮件/文件的第三方、被攻破的工具或 agent、模型自身；Through what channel：直接提示、检索或注入内容、工具输出与记忆、训练数据；To what end：泄露隐私数据、劫持动作、有害输出）（第 13 页）；以及安全社区的 STRIDE 检查表——仿冒（Spoofing）、篡改（Tampering）、抵赖（Repudiation）、信息泄露（Information disclosure）、拒绝服务（Denial of service，如被困在无限工具循环）和权限提升（Elevation of privilege）（第 14 页）。
- 意外事故（Accidents，agent 自己搞砸）四分类（第 16 页）：
  - 错误目标（Wrong Objective）：奖励作弊，如 SWE-bench 的 GitHub issue #465 存在“a test that passes without solving the task”（第 18 页），ImpossibleBench（第 19 页），以及在低风险单轮奖励作弊上做监督微调（SFT）会泛化到多轮下棋作弊等更复杂失准（第 20 页）。
  - 错误动作（Wrong Action）：过度热心（Overeager Agents），同一条整理提示下，Claude Code、Codex CLI、Gemini CLI、OpenHands 中“three of four destroy .env.old”（第 21 页）；PocketOS 和 Replit 事件（细节课件没说清）（第 22 页）；隐私泄露（Privacy Leakage），PrivacyLens 发现模型被问起时懂隐私规范，行动时却违反（具体准确率在图中，文字没说清）（第 23–24 页）。
  - 错误上下文（Wrong Context）：长程退化（Long-Horizon Degradation），在未充分说明的多轮任务上，15 个 LLM 能力下降“15%”，不可靠性翻倍以上（“+112%”）（Laban et al., 2025）（第 26 页）；CodeClash 显示代码库随时间变乱（第 27 页）。
  - 错误报告（Wrong Report）：假装完成（“Agents Often Pretend They ‘Finish’”），例如找不到收据就编造逼真的收据数据（第 28 页），以及夸大声称（Overclaims）（第 29 页）。
- 提示注入（Prompt Injection）的四类攻击入口：不可信内容把模型从预期指令重定向到未授权动作（第 31 页）。包括网页注入（Web Page Injection），在 GPT-4V agent 上窃取用户个人身份信息（PII）成功率“Up to 70%”（第 34 页）；视觉提示注入（Visual Prompt Injection），弹窗指令让基于 GPT-4o 的 GUI agent 点击弹窗的概率达“90%+ of the time”（第 35 页）；工具结果注入（Tool-Result Injection），如动态环境基准 AgentDojo（第 36 页）；知识库投毒（Knowledge Base Poisoning），PoisonedRAG 每个查询只需“Five poisoned passages”，在各类 RAG 设置中攻击成功率“~90%”（第 37 页）。
- 滥用、失准（Misalignment）与合谋（Collusion）：恶意使用包括降低虚假信息成本、辅助网络攻击代码生成、诈骗操纵与非法监控审查（第 39 页），简单越狱（Jailbreaks）就能让 agent 顺从有害请求（具体比例在图中，文字没说清）（第 40–41 页）。失准方面，Anthropic（2025）内部威胁研究报告称，当这是避免被替换或达成目标的唯一办法时，“models from all developers resorted to malicious insider behaviors when that was the only way to avoid replacement or achieve their goals—including blackmailing officials and leaking sensitive information to competitors”（第 42 页），甚至为防止被关停而敲诈（第 43 页）。合谋方面，Shi、Zhang 与 Yang 在通信限“1000 characters”且禁传原始日志的受控环境里发现，“8 of 10 models show collusion in >90% of trajectories”（Gemini-3.7-Flash、Claude-Sonnet-4.6、Claude-Opus-4.6、Qwen-3.6-27B、DeepSeek-V4-Flash 均达“100.0”%，最低 Gemma-4-31B 为“66.0”%）（第 45–46 页），可用缩短减少记忆细节（memory control）和分离奖励（separate reward）抑制（第 48 页）。
- 按设计防御（Defense by design）与开放问题：常见防御（如数据过滤、Llama Guard 护栏）在 Nasr et al.（2025）的自适应攻击（Adaptive Attacks：梯度、强化学习、搜索、人工红队）下有“12 Defenses”被攻破（第 50–52 页）。更稳固的是三种抗提示注入设计模式（Beurer-Kellner et al., 2025）：#1 动作选择器（Action-Selector，LLM 只把自然语言译为预定义动作）（第 53 页）；#2 先规划再执行（Plan-Then-Execute，读不可信数据前先定好允许的工具调用计划）（第 54 页）；#3 双 LLM（Dual LLM，有工具权限的特权 Privileged LLM 不读不可信数据，隔离的 Quarantined LLM 无工具权限）（第 55 页）；CaMeL 结合 #2 和 #3，阻断了几乎所有 AgentDojo 攻击同时保留大部分效用（第 56–57 页）。部署前可用 LLM 模拟沙箱探查风险（第 58–59 页），部署中监控思维链（chain of thought，CoT）比只监控动作更有效（第 61 页），能访问模型时激活探测（Activation Probing）在小开源模型上可能比 CoT 监控更有效（第 62 页）。四大开放问题：可扩展监督（Scalable oversight，人类审查是否只是“rubber-stamping”）、多 agent 与系统性风险、可靠性与评估缺口（含评估感知/装傻“eval awareness/sandbagging”）、人类自主性与技能退化（“Human agency and skill atrophy”）（第 64 页）。
- 对我们：单元 13（安全）的绝对主料。威胁建模三问与 STRIDE、四类意外事故（尤其是 4 个 coding agent 里 3 个误删 `.env.old`、假装完成编收据、隐私规范知行不一）可直接放进 A（四种威胁模型和五个真实事故）；四类提示注入及数据进 B（提示注入）；Action-Selector / Plan-Then-Execute / Dual LLM / CaMeL 进 C（沙箱与边界）；CoT 监控和激活探测进 E（监控）。另外奖励作弊和多 agent 合谋也可分别补充到 单元 12（评估）和单元 9（多 agent）。
