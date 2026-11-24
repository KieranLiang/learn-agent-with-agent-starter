# Stanford CS146S The Modern Software Developer（2026 秋）读课笔记

- 讲师：Mihail Eric。网址 https://themodernsoftware.dev/ （逐周安排在首页的 Syllabus 标签后面，要用浏览器点开）。课件是 Google Slides，可用 `/export/txt` 导出文字。
- 读于 2026-11-11。全读：第 1–6 周和第 8 周的 9 份讲师课件、9/24 讲课逐字稿、两位嘉宾（Lee Robinson、Eno Reyes）的课件。没读：第 7、10 周（还没放）。2026-11-25 补读了第 9 周课件和 9/29、10/1 两份逐字稿。
- 定位：面向“相当有经验的工程师”的实践课，自称“讲原则不讲工具”。课件很薄，每页几行要点，**真正的内容在现场演示和逐字稿里**。嘉宾分量很重（Claude Code、Devin、Factory、Replit 的负责人）。
- 对我们的用处：Agentic 软件工程部分（单元 15–17）的主干，以及 单元 3 的“拆标本”方法。
- 标记：🟢 概念级可直接教 🟡 需要一点基础

## 第 1 周 Coding agent 的内部 🟢 ★

**9/22：200 行写一个 Claude Code**

- 课程一页总结：人和 agent 协作的工程。专注还没被 AI 取代的能力：理解业务和产品、当架构师并培养对软件系统的品味、沟通。**“LLM 只会和你一样好。好的上下文产出好的代码。你自己看不懂的代码库，LLM 也看不懂。”**
- 最小 agent 的四步：读终端输入并不断追加到对话里；告诉 LLM 有哪些工具；它在合适的时候请求用工具；你在本地执行并把结果送回去。工具只有三个：读文件、列目录、改文件。

**9/24：解剖一个现代 coding agent（逐字稿）★★**

这一讲的做法就是我们“拆”这一步的范本：用一个代理工具截获 Claude Code 发给模型的请求，像用 Wireshark 抓包一样逐块看。

- 看得见的是 harness，看不见的只有模型本身。**“harness 设计大概是 coding agent 里最难也最重要的问题之一。”**
- 一次请求里有什么，按块看：
  - `tools` 块：约 40 个内置工具（文件、Bash、搜索、LSP、子 agent、计划、定时、制品、问用户、调用技能……），加上所有 MCP 工具（名字以 `mcp__` 开头）。**工具的名字、描述、完整签名全都是 prompt 的一部分**，每次请求都带着。
  - `system` 块：先是一句“你是 Claude Code……”，然后是约 50–80 行的系统提示（行为、安全、会话、记忆、环境、上下文管理）。比以前的 200–250 行短了很多，以前教怎么用 git 之类的内容现在被认为不需要了。
  - `messages` 块：用户、助手、工具结果交替。**用户消息前面有一大段不是用户打的字**（system reminder、CLAUDE.md 的内容），是 harness 悄悄加的。
- “到我发第一条请求时，可能已经有几万 token 被我控制不了的东西占掉了。然后我还纳闷它为什么表现不好。”
- MCP 工具全部塞进上下文，技能只先放元数据（渐进式披露），这是技能后来被引入的原因之一。
- 历史观察：Claude Code 去年底走红的原因之一是**极简的 harness**。早期 GitHub 的 MCP 服务器一上来就有约 110 个工具。趋势是找“瑞士军刀”式的强力工具，比如 Bash 和 SQL。
- CLAUDE.md 是系统提示的“用户可控版”。里面放一两条命令（怎么跑测试、怎么起服务）有帮助，放太多会**过度约束**，像过拟合。
- 计划模式就是一段被注入的提示词，描述一个分阶段流程（理解需求、设计、评审、出计划文件），进出各有一个工具。
- 技能被调用时，harness 找到 SKILL.md 并把内容插进上下文。子 agent 通过一次工具调用生成，带全新上下文，只把结果带回来。
- 压缩：比如把 50 万 token 压成 15 万，之后模型看到的就是摘要。
- 大问题：**投资模型还是投资 harness？** 业界在两头来回摆。现在的风向是 harness 尽量简单，更多依赖模型能力。
- 作业 1 就是让学生自己截获并拆解这些请求。

## 第 2 周 进阶上下文工程 🟢

**9/29：进阶提示与 spec 驱动开发**

- 目标：从随手写提示，走到稳定可靠的同步开发流程。
- “Vibe coding 搞乱了预期。”写生产级的 AI 代码要有方法；你脑子里应该有一个能用的心智模型，知道自己会怎么做。
- **RePPIT**：Research（理解陌生代码库）→ Propose（提几个方案）→ Plan（把最有希望的方案计划出来）→ Implement → Test。
- **“聪明区”和“笨区”**：上下文窗口的前一半到四分之三是“聪明 token”，再往后就进了笨区。系统提示、AGENTS.md、任务上下文都占着聪明区。
- 实践：非常仔细地审你的 spec；大功能拆成任务清单；每完成一项就把 agent 做了什么写成文档，作为下一项的上下文。
- 任务委派四档：直接提示 → 先做计划 → 先调研再计划 →（调研再计划）× N。
- Spec 放哪儿：Linear，或者本地和 Git。设计取舍可以放 `.notes/`。

**10/1：MCP 与工具调用**

- 为什么：LLM 的知识是静态的，要做自主系统就得有办法喂动态数据。
- MCP 把集成数量从 M × N 降到 M + N。流程五步：问问题 → 取工具列表 → 模型选工具和参数 → 调用并取回结果 → 返回。
- **好的 MCP 服务器怎么设计**：
  - 它不是 REST API 的包装。小工具太多会让 agent 把时间花在编排上。
  - **为结果设计，不为操作设计**：一个 `send_payment(user_email)`，而不是 `get_users` → `list_account` → `send_payment` 三步。
  - 参数要显式，不要嵌套字典。**说明就是上下文**：文档字符串、报错信息都是提示词。工具名带服务前缀便于发现。
  - 另一条路：MCP 服务器多到爆炸时，只暴露 `search` 和 `execute` 两个工具，token 能省九成以上。
- **API、MCP、Skill 三者对比**（这张表在三讲里反复出现）：API 是给开发者调的服务接口，你自己管认证和重试；MCP 是给 agent 运行时调的标准化工具定义；Skill 是教 agent 怎么完成一件事的可复用流程包，常常编排多个工具。

## 第 2 周逐字稿补充 🟢 ★（2026-11-25 补读 9/29、10/1 两份逐字稿）

- 9/29 逐字稿补出了“聪明区 / 笨区”背后的量化依据与真实规模背景：课程针对的是数百到上千个文件、数百万行代码（如 Google 级别）的复杂仓库。讲者引用一篇研究上下文压缩（compaction）的博客（作者与具体模型名称逐字稿未提，课件没说清），指出该研究根据运行轨迹建议在累积“250,000 and 450,000 tokens”时做一次压缩；尽管模型宣传有“a million tokens”上下文，但研究发现真正能被有效利用的更接近“half a million truly useful tokens”。另外讲者追述了“vibe coding”一词的由来——约一年半前 Andrej Karpathy 一条“洗澡灵感（shower thought）”推文，核心态度是“Jesus, take the wheel”（9/29 逐字稿）。
- 9/29 逐字稿完整演示了用 REPIT 给自己几乎不懂前端（“Vue? I have no idea”）的 Mint 记账克隆应用加“按类别消费趋势线”，全程讲解和运行耗时 45 分钟，补出大量实操细节：
  - Research（调研）阶段用到了讲者花“a year or a year and a half”逐行迭代并在团队仓库反复打磨的 `research codebase` 技能（内含接入第三方库最新文档的 Context7 MCP）。他明确要求调研只记录现状与行为契约（behavioral contracts），严禁提改进建议；被问到是否复用已有 Markdown 文档时，表示若文档长期失修，宁可从零调研以免陈旧信息误导 agent。
  - Propose（提案）阶段刻意只让技能给出两个正交（类比机器学习 PCA 主成分）的方案，因为超过两个会出现边际收益递减。现场出了“后端改响应”和“纯前端算已上传交易”两案，他为避免现场演示翻车选了后者，但事后反思演示里犯了一个不建议效仿的错：选定方案后通常应清空上下文（clear context），否则落选方案留在上下文里会干扰模型实现。
  - Plan（规划）阶段模板专门用大写强调把需求外的内容放进未来考虑事项，指令写着“Don't touch this. Only implement the work in scope. Defer everything else.”，甚至要求写到行号；并指出自己现在对调研结果人工校验越来越少（因为模型压缩信息已很强），人的高杠杆点应重押在调研、提案、规划的意图与架构把关以及最后的代码审查。
  - Implement 与 Test（实现与测试）阶段提示词极其简单，但 Cursor 会自动拉起内置浏览器（不具备此能力的 harness 可接 Playwright MCP）造合成 CSV 数据上传，将实现与行为验证合在一步；模型选择上建议前段（调研、提案、规划）用最强模型，后段（实现、测试）可换轻量模型。
  - 讲者还现场拆解了 GitHub 上拥有“300,000 stars”的热门规划框架 Superpowers，指出它本质上“就是一组技能（a set of skills）”，里面装的正是头脑风暴、写计划、执行计划、代码审查这些流程（9/29 逐字稿）。
- 10/1 逐字稿先补了课上的开源伙伴协作（OSS Partners，包括 OpenHands、Pi、CrewAI、Browserbase、Arize、Marimo、Warp 等）工程底线：允许且鼓励用 coding agent 写 PR，但严禁把未经审查的“AI 垃圾（AI-slop PR）”甩给维护者，“AI slop gets a zero”（10/1 逐字稿）。
- 10/1 逐字稿在 MCP 概念上补清了宿主机（host，如 Cursor、Claude Desktop）与客户端（client，宿主机里维护有状态会话的 SDK）的工程区分——实战里大家几乎只说 client；本地自建 MCP 服务器常用 `stdio`，远程第三方服务通常走 `HTTP` 并靠 `OAuth` 鉴权（令牌带生存时间 TTL）。更关键的是给出了工具膨胀（tool bloat）的真实测量：在第 1 周抓包的 Claude Code harness 记录中，整个 JSONL 约“10,000 lines”，真正对话与提示只有“600 or 700 lines”，其余全是工具的 schema 和参数定义；而早期 Cursor IDE 一度最多只允许挂“88 tools”，GitHub 的 MCP 服务器一个就占“120 to 150 tools”（前文亦称约 150 个），导致装一个服务器就塞满（10/1 逐字稿）。
- 10/1 逐字稿补出了工具设计的演化过程与报错细节：团队初期常为了覆盖率一口气建 100 个小工具，直到发现 LLM 连简单任务都犯糊涂，才回看运行轨迹（traces）做合并重构——例如把分别搜会议、逐字稿、Slack 线索的三个工具合并成一个带资源类型参数的 `search_resource` 工具。写 Python 工具时也别只抛出泛泛的 `Exception`，而应抛出 `ValueError`、`NameError` 或自定义错误类型给模型提供调试线索。讲者并引用格言界定何时需要严谨设计：“software engineering is what happens when you add time and people to programming”（只给自己用的可随意，多人长期共用必须精心设计）（10/1 逐字稿）。
- 10/1 逐字稿用具体例子讲透了只暴露 `search` 和 `execute`、能带来“more than 90% token reduction”的“代码模式（code mode）”如何运作：以“找一个 Jira 工单并用 Google Drive 里的信息更新它”为例，模型上下文里不塞任何全量工具，而是由模型在 `code-mode SDK` 支持下先动态生成一段代码去检索过滤工具（可以是语义搜索，演示中采用词法过滤 lexical filtering——识别出 Jira 和 Google Drive 后生成用 `includes` 过滤的 JavaScript）；拿到命中的工具定义后，模型再动态生成第二段确定性代码把“JQL 搜 Jira → 读 Google Drive → 更新 Jira 工单”串起来，放进虚拟机（VM）进程一口气跑完并把结果交回模型，省去模型一轮轮做单个工具调用的开销（10/1 逐字稿）。
- 对我们：两份逐字稿大幅充实了 单元 3（循环与工具）、单元 5（上下文工程）、单元 8（设计模式与规划）、单元 9（多 agent）和 单元 15（说清楚要什么）。其中 1 万行 JSONL 里对话仅占六七百行、25 万–45 万 token 压缩阈值、选完方案清上下文是 单元 5 的现成数字与反面教材；`search_resource` 合并重构、具体异常类型和 code mode 的两段动态代码机制可直接放进 单元 3 分组 D/E；Mint 演示里的研究禁提建议、正交双方案、Plan 划定 `"Don't touch this"` 边界及强弱模型分层则可直接支撑单元 8 与单元 15。

## 第 3 周 Agent Skills 🟢

- “像给 agent 用的脚本。”LLM 非常擅长照着较长的流程做事。
- 技能分类：代码理解与规划、验证、代码风格、杂项（比如浏览器解析）。
- 最佳实践：
  - 范围聚焦，一个技能一件事。
  - 维护自己的技能集，跨项目带着走。“厨师换厨房会带自己的刀。”
  - **挖自己的聊天记录**：技能就是写成 Markdown 的流程，去看你在哪儿插手或纠正过。
  - 写清楚应该触发这个技能的情形和说法。
  - 渐进式披露；模块化组合。
  - **维护一个验证技能，让 agent 检查自己的工作**，这样才有改进闭环。

**嘉宾 Lee Robinson：常驻 agent 怎么工作 🟡**

- 从“第一周写的那个循环”出发：它在你关掉终端时就停了。常驻 agent 跑在服务器上，有自己的云端电脑，状态存盘，能被消息、定时任务、webhook 唤醒。
- 人和 agent 的关系：从“每一步都批准”变成“它一直干，你随时改方向”。**“模型越强，界面越简单。”**
- **agent 知道的东西都放在文件里**：`memory/profile.md`（一直在提示里）、`memory/log/`（按日期的事实，一行一条）、`skills/`、`routines/`。理由：模型极其擅长用 Linux 和 shell；纯文本你能直接读和改。
- 工具设计建议：两轮之间不要增删工具（用不了就返回清楚的错误）；每个工具的描述和 schema 不超过 4000 字符；保存状态用专门的工具而不是 shell 命令，方便审查。
- 取信息先试最便宜的：已知的 → 应用的 API → 自己登录的浏览器 → 整个桌面 → 网页搜索 → 问你。
- 安全：另一个模型在高风险动作执行前审查；来自邮件和 webhook 的文本标记为不可信；密码不经过模型。
- 上下文工程：**提示的开头保持不变**以复用缓存；“把缓存未命中当 bug 对待”；长输出进文件，上下文里只留路径；趁用户离开时做摘要。
- 记忆分层：档案（一直在提示里，最多 100 条事实）、日志（最相关的 30 条）、短期笔记、其余靠搜索。
- **“删掉产品。”** 假设模型会强很多，在它周围尽量少建东西，它不再需要的就拿掉。
- 每个 agent 产品都会有的新积木：持久化工作流、能用电脑、记忆和技能、触发器、连接器和认证、评估和可观测性。

## 第 4 周 定制你的 agent 和仓库 🟢 ★

- 四种定制手段：行为文件（CLAUDE.md、AGENTS.md）、hooks、skills、子 agent。
- **好的 AGENTS.md**：它是“给 agent 的 README”。结构：项目概览（代码库地图）、构建和测试命令、代码风格、测试说明、安全注意、语言或技术栈的坑。
  - 指令要尽量普遍适用；**避免贴代码片段，过时很快**；控制在 300 行以内；大仓库用嵌套配置，根文件当路由。
  - 加载顺序从根到最近的文件，最相关的最后被处理。
- Hooks：在预定事件上运行的确定性脚本（工具使用前后、用户提交提示时、压缩前）。用途：清洗用户提示、拦截敏感动作、对生成的代码跑格式化、任务完成后跑测试。
- 子 agent：干净地隔离不同工作流的上下文，只返回最后一条消息。适合探索代码库、改完后简化代码、端到端测试这类“支线任务”。对比 CLAUDE.md，后者是用来“锚定行为”的。
- MCP 用途举例：项目管理（Jira、Linear）、文档（Notion）、可观测性（Sentry）、数据库、技术文档（防止用过时的库定义）。
- **“上下文的故事”** 一张图：系统提示、Memory.md、环境信息、MCP 工具、技能、全局 AGENTS.md、本地 AGENTS.md。

## 第 5 周 让代码库对 agent 友好 🟢 ★

- 大多数代码库没为 agent 的成功做好准备。LLM 的很多困惑来自又乱又不完整的开发环境。
- **人能绕过去的，agent 会卡住**（一张对照表）：没测试（人手动测）→ agent 没法验证对错；文档过时（人去问同事）→ 没法保证一致；构建不稳（人重试）→ 没法验证改动；没有可观测性 → 没法调试；环境搭建复杂 → 不可复现。
- Agent-ready 清单：足够的测试覆盖、封闭可复现的构建、有文档且一致的设计模式、没有过时的 README、可验证的检查、给 agent 的手册（AGENTS.md）。
- 能力演进三级：Tab 补全（2021，约 15% 增效）→ 同步完成单个任务（2024，25–35%）→ 后台多任务（2026 起，2 倍以上）。后台 agent 需要的条件和 agent-ready 清单几乎是同一页。
- 隔离方式：git worktree、多 agent 编排器、云端 agent。

**嘉宾 Eno Reyes（Factory）：“能验证的，agent 就能解决” 🟢 ★★**

整套讲法很适合直接改编成一关。

- 通常的诊断是“模型太笨”。他的主张：**多半是环境的问题。**
- 类比：人脑 30 万年基本没变，世界却变了。进步来自让事情**可检查**的工具：文字（“这是我们说好的吗”）、度量衡、记账（“账平吗”）、实验、单元测试。“我们没有变聪明，我们变得可检查了。”
- **Agent 是一台“猜了再查”的机器：模型负责猜，环境负责查。**
- 基准测试是世界上最 agent-ready 的代码库，因为每道题都带评分器。
- 两个旋钮：检查有多精确、步子有多细。
- **算术**：20 步的任务，每步 90% 对。只在最后查一次，成功率约 12%；每步都查并最多重试 3 次，约 98%。
- 检查越快，试的次数越多：5 秒的 pre-commit 钩子每小时能试 720 次，10 分钟的 CI 只能 6 次，一天的代码评审不到 1 次。
- Agent 就绪度九个支柱（风格与校验、构建、测试、文档、开发环境、可观测性等），五个等级。
- 作业（一个下午）：写 AGENTS.md、加 `.env.example`、一条命令跑测试、先写失败的测试。
- 推广到代码之外：哪个领域检查便宜，agent 就先到哪儿。数学有证明检查器，代码有测试和类型，医学的最终检查是临床试验。
- **“你的工作：造检查器。稀缺的能力是把‘好’变成机器能验证的东西。”**

## 第 6 周 Agentic 代码审查 🟢

- 代码审查的价值：发现 bug、让团队形成共同的心智模型、讨论设计、保持风格一致。
- **代码审查成了新瓶颈**：跟不上代码生成的速度。
- 成熟度三级：人审一切（没法扩展）→ 单 agent 审查（配上自动修复循环更好）→ 多 agent、按风险分级、能自我改进（工程规范存在技能知识库里）。
- 多 agent 审查的结构：安全、架构、代码质量、性能各一个 agent，最后一个汇总裁判。
- 设计要点：审查用的模型和生成用的模型要不一样；起一个开发容器实际跑代码来验证；按任务复杂度选模型；用历史上有已知 bug 的 PR 做评估。

## 第 8 周 后台 agent 🟢

- “Localhost 的终结”：不再有“在我机器上能跑”；一切可复现；几乎无限并行。
- 自建后台 agent 平台：接一个任务，起一个接近生产的开发环境，端到端执行，交回一个 PR。有些公司每周全自动合入上千个 PR。
- 多 agent 模式：agent 团队（让 5 个队友各查一个假设并互相反驳）、生成者-验证者、主模型配一个“聪明朋友”。
- **多 agent 编排需要的元能力**：委派和多线程；规划、定范围、做架构；对任务保持控制和上下文；动手前先花时间判断任务复杂度；读代码和读计划的能力；逐步增加 agent 数量。

## 第 9 周 软件工厂 🟢 ★（2026-11-25 补读课件文字）

- 核心命题是把软件开发从“人在环内（humans in the loop）”推进到“人在环上（humans on the loop）”，用一套围绕孤立后台 agent 运转的软件工厂（Software Factory）编排任务，人则从执行转向意图、判断、治理与系统设计。工厂由三根支柱构成：流水线（production line，云端后台 agent 舰队从 issue、Slack 线索、Sentry 告警或定时任务接活，在隔离环境完成并返回 PR）、质量控制（quality control，用 CI、静态分析 static analysis、测试和 AI 审查者对所有产出执行同一标准）、反馈闭环（feedback loop，每漏过一个缺陷就把原因固化成文档、skill、lint 规则或工具，让缺陷率随时间下降）（课件文字未标页码）。
- 工厂有三条前置条件：工具访问权限（tool access）、隔离的控制面（isolated control plane）以及 agent 就绪度（agent readiness）。其中就绪度引用 Cursor 的 Eric Zakariasson（AIE Europe 2026）拆成三条：可运行（Runnable，“without… any human in the loop?”，0:08:58，之后才能在独立虚拟机上扩展）、可访问（Accessible，能拿到任务所需的外部上下文与工具）、可验证（Verifiable，能自行验证改动，Eric 原话称人们“should be spending a lot more time… building verifiable systems”，0:09:57）（课件文字未标页码）。
- 工厂内部按代码化的工厂定义（factory definition：skills、rules / AGENTS.md、自动化配置）运转，编排器（orchestrator）在独立沙箱（sandbox）里串联分诊（triage）→ 规格（spec）→ 实现（implement）→ 代码审查（code review）→ 验证（verify，含 CI 与计算机操作检查 computer-use checks）→ 发布（ship）→ 监控（monitor）。人只把守三道关卡：批准 spec、按风险分级的审查（risk-tiered review，安全、数据和支付必须归人）以及产品检查（product check）；另有两条反馈回路，一是监控发现问题重新开单回流分诊，二是观察者 agent（observer agents）根据遥测（telemetry）向工厂定义提 PR 改进并由人合并。课件详细步骤清单编号从 6 直接跳到 8，缺第 7 步，且未展开第 7 步内容（课件没说清）（课件文字未标页码）。
- 人的工作原则是“同步规划，异步执行（plan synchronously, execute asynchronously）”和“agent 跑偏是改进工厂的信号（An agent going off the rails is a signal to improve the factory）”，人对最终上线结果负责。工厂擅长接手的任务包括：PR 审查、CI 失败、合并冲突（merge conflicts）、线上故障初步排查（first pass investigation into production incidents）和安全漏洞（课件文字未标页码）。
- 评判与度量不能靠感觉，要“给每次运行打分，而非凭氛围（Score runs, not vibes）”。评判器（AI judge）按 spec 给整次运行打分（如 Zach 的演示中会抓出 agent 写冗余测试，AIE NYC，0:12:45）；Spotify 的 Honk 评判器则把改动 diff 对照原始提示检查，“It vetoes about a quarter of agent sessions, and the agent course-corrects about half the time after a veto. Most common trigger: going outside the prompt.”（Spotify Honk part 3，2025 年 12 月）。评测要坚持“私有基准优于公开基准（Private benchmarks > public benchmarks）”，直接回放自身历史 PR 比较模型与 harness 的成本和质量；工厂核心指标是单 PR 成本（cost per PR）、周期时间（cycle time）、单 PR 人工介入次数（human touches per PR）以及通过工厂合入的 PR 占比，“不是代码行数或 token 数（Not lines of code or tokens）”（课件提到 Warp 推行工厂后单 PR 成本呈下降趋势，但注明“His exact figures vary across sources, so present it as a trend only”）（课件文字未标页码）。
- 搭建与推广策略分两种模式和三步走：模式上要么“拼装（Frankenstein）”，把 Claude automations、Devin 等现有工作流拼起来；要么像 Warp 那样把工厂做成仓库里受版本控制的基础设施即代码（Infrastructure-as-code），可 diff、审查和回滚。推广走“爬、走、跑（Crawl, walk, run）”：爬阶段先在测试良好的标准仓库做杂活自动化（分诊、审查、修 Sentry、CI 自愈）；走阶段在简单场景跑通端到端工厂；跑阶段再进复杂仓库。触发入口要“到人工作的地方去（Meet people where they work）”（直接从 Slack、Linear 或 GitHub 发起，别另造门户），遵循“鼓励但不强制（Encourage but don't require it）”，用风险分级让低风险改动自动合入、高风险改动转交人工（物流栏还列了 Replit 总裁 Michele Catasta 的嘉宾讲座，但课件里没有其内容）（课件文字未标页码）。
- 对我们：主干落在 单元 16（给 agent 搭环境）和 单元 17（审查、演化与交付）、单元 21（放手与把关），也能补充 单元 12（可靠性与评估）。其中 Runnable / Accessible / Verifiable 三前提直接对应 单元 16 的代码库就绪度体检；三道人工关卡、按风险分级审查、以周期与单 PR 成本替代代码行数的度量，可用来收束单元 17；Spotify Honk 评判器的数据和“回放历史 PR 做私有基准”则是 单元 12 极佳的工业界标本。

## 还没放出的

第 7 周安全（只有主题）、第 10 周（2026-11-11 时课表写的是 Software Factory；第 9 周放出的课件已经讲了软件工厂，见上）。
