# 单元 1 教案｜Agent 全景与 Harness 范式之争

> 只给老师看，学生不读这个文件。上课规范见根目录的 `CLAUDE.md`。
>
> **讲法提醒**：每关的要点只是备忘提纲，不要照着念。按 `CLAUDE.md`“让他读着不累”来：先抛真实工程痛点铺路，一段两三句，并列内容用表格或分点，观点分歧必须点明出处和讲师姓名。聊天里不挂【】标签。
> 标本标记（给老师看）：【真实】真实开源源码/日志/课程实测数据；【论文】经典或前沿论文；【改编】来自某门课的例子；【示意】讲解用示例。
> 改完教案后运行 `python3 tools/check_unit.py curriculum/unit01.md`。

## 单元概览

- **目标**：跳出产品科普层，建立 Agent 工程师的系统级心智模型——能用“下一步动作由谁选”剖析任何产品；算得清多步错误累积与验证纠偏的账；讲透“薄 Harness vs 厚 Harness”“训模型 vs 做系统”两大业界范式分歧；亲手翻过 Pi、`dsh`、Codex CLI、OpenCode V2、Grok Build 五大一线开源 Harness 的源码架构；走完第一篇论文精读与第一轮大厂面试拷问。
- **知识点覆盖**：覆盖 `curriculum/coverage.md` 分到单元 1 的全部 94 条知识点（六门课高度重叠部分已合并去重，并在对应关里保留不同老师的差异化观点）。
- **学情提醒**：
  - 先读 `progress/student.md` 判断学员背景：若对产品层概念已熟悉，关 1.1 先问两道工程深水区确认题加速过，把核心时间留给关 1.2（错误累积与自我条件化）、关 1.3（范式交锋）、关 1.4（五大开源源码横评）和关 1.5（论文精读 + 面试拷问）。
  - 主标本直接翻 `materials/harnesses/` 里的五大开源仓库（若本地尚未拉取则用教案里的真实结构数据）。
  - 避开学员档案里标注不熟悉的语言类比。
  - 本单元不展开 Token/注意力细节（单元 2）、Tool Schema 与编辑协议细节（单元 3）、具体沙箱与注入防御（单元 4），碰到就声明黑盒。
- **单元实验**：见文末（Harvard Mads-Lens + CS146S Week 1 融合版）。
- **原片**：见 `curriculum/syllabus.md`。

---

# A 组 · 界定与底层机制

## 关 1.1｜感知-行动闭环与自主梯度：谁来选下一步

- **核心主题**：用工程四要素（环境、观察、动作、目标）与“下一步动作由谁选”这把不会过时的尺子，精准界定聊天机器人、Workflow 与五级自主 Agent，理清 AI 编程四波浪潮下开发者从“打字员”到“策展人”的角色迁移。
- **覆盖知识点与出处**：Russell & Norvig 经典定义与 LLM 对应（CMU L01 p.9、329Z L01 p.19-21）；Agent 简史（1973 ACTOR → 1980 Contract Net → 1995 R&N → 2022 ReAct/ChatGPT → 2023 AutoGPT → 2024 Devin/SWE-agent → 2026 部署期，329Z L01、CMU L14）；聊天助手 vs Agent 分界（jyy 第 1 讲、Harvard L03）；Workflow vs Agent 控制流归属（329Z L01、CS329Z L06）；自主五级阶梯与 Aider 四原语（EECS498 L01、L05）；AI 编程四波与打字员/策展人角色转变（EECS498 L01、CS146S W1、jyy 第 1 讲）。
- **前置**：日常用过 Antigravity / Claude Code。
- **黑盒**：模型发出动作的 JSON 协议格式（单元 3）、上下文窗口如何装下历史（单元 2、5）。
- **确认题**：
  1. 同样都有循环、工具、规划和记忆这四个原语，为什么 EECS498 把 Aider 归在第 3 级（结对 CLI），把 Claude Code 归在第 4 级（Agentic CLI）？分界线到底是哪一个设计决定？
  2. 如果你已经明确知道只需要改 `auth.py` 里的两行 bug，用第 4 级自主 Agent 和第 3 级定向修改相比，真正的工程代价差在哪？

### 机制与观点交锋

- **从“说”到“做”的核心不在会动手，而在能看到反馈**：聊天机器人交回建议，Agent 交回验证过的结果。关键是形成 `动作 → 环境变化 → 观察 → 调整下一步` 的闭环（jyy 第 1 讲“U 盘装 Debian 遇设备正忙后卸载重试”的例子）。“问用户”本身也是一种动作，“目标”必须是可验收的状态而不是一句模糊提示。
- **一套跨越 50 年的谱系**：Agent 不是 LLM 发明的词——1973 ACTOR 模型、1980 Contract Net、1995 Russell & Norvig 教材（传感器感知、执行器行动），再到 2022 ReAct 把推理作为“更新自身状态的内部动作”与外部行动交替，2024 SWE-bench/Devin/OpenHands 把战场拉到仓库级任务。
- **一把三年后工具全换名依然好用的尺子（UMich EECS498 Marcus Darden L05）**：“下一步动作由谁选？”
  - **Workflow vs Agent**（CS329Z Diyi Yang L01）：代码写死步骤的是 Workflow，LLM 动态选下一步的是 Agent，二者都属于复合 AI 系统，不存在“Agent 天然比 Workflow 高级”。
  - **自主五级梯度**（EECS498 L05）：1 级补全 → 2 级旁侧聊天 → 3 级结对 CLI（如 Aider：人选文件与边界，程序跑固定 6 步并在编辑失败时最多重试 3 次）→ 4 级 Agentic CLI（把“选下一步”交还模型，模型自己 grep/读文件/跑测/修错）→ 5 级多 Agent 并行。
  - **自主的价钱**：级别越高，换来的是“问你更少”，付出的是“多轮探索的 token/延迟翻倍 + 失控半径放大”。工程本事在于**按任务挑对级别**，而不是一律无脑上最高级。
- **观点交锋（人的新角色）**：
  - UMich EECS498（Marcus Darden）：“从打字员变成策展人（Curator）”，铁律是“你能解释它，它才是你的”。
  - 南大 jyy（第 1 讲）：提出大学与工程师剩三件事——“信息差、能坐牢（担责）、能驾驭”，并直白追问“为什么我要招你，而不是买一个 200 美元的 Claude Max？”
  - Stanford CS146S（Mihail Eric）：强调稀缺能力收敛到业务产品理解、架构品味、与清晰沟通。

### 源码或论文拆解

- 【改编】UMich EECS498 L05 现场对比标本：Aider 的 6 步固定流水线（组装 → 回答 → 解析 → 应用 → 修复重试最多 3 次 → 提交）vs Claude Code 自主给 `taskr` 加 `--priority` 参数（无人敲 `/add`，自主 grep → 读 3 个文件 → 修改 → 测试挂了自行读报错修复）。
  - 重点点出：Aider 其实也有循环（失败重试）、工具（搜索替换）、规划和记忆，但它只是第 3 级——**从第 3 级跃迁到第 4 级不需要更强的模型，只需要把“选下一步”的控制权从代码移交给模型**。
- 【真实】CMU L01 第 14–15 页展示的 `mini-swe-agent` 极简循环原型（约 20 行 Python `while` 循环：查模型 → 解析动作执行 → 追加观察，直到模型输出结束信号）。

### 互动与实战

给三个真实研发任务，让他在自主五级梯级里选最合适的一级，并说清理由（不许只说“全用 4/5 级”）：
1. 线上报警指明了具体报错栈和文件行号，确认是把 `>=` 写成了 `>`。
2. 刚接手一个 400 个文件的陌生服务，要排查“高并发下偶发订单重复扣款”的根因。
3. 仓库里 30 个微服务要统一把一个废弃的日志库迁移到新库，且每个服务都有完善的单测和 CI。

- **参考**：1 选 1–3 级（目标明确、改动局部，直接定位改比让自主 agent 满仓库 grep 便宜、快且稳）；2 选 4 级只读探索（未知根因、需要多步假设-查日志-看代码反馈循环，但此时应限制写权限）；3 选 4–5 级批量并行（子任务独立、有明确自动化测试验证边界，最适合用后台多 agent 买吞吐）。

### 面试拷问

- **题 1**：如果面试官问你“你在项目里什么时候选确定性 Workflow，什么时候选自主 Agent？举一个你们团队（或真实场景）做过这个取舍的例子”，你怎么答？
  - **参考与追问**：不能只背“固定流程用 Workflow、开放任务用 Agent”。高分答法要落到四个工程判据：**路径是否可枚举**、**SLA 与成本/延迟上限**、**单步错的返工/副作用代价**、**是否具备便宜的自动验证器**。追问：“如果一个长流程里 80% 步骤固定、20% 需要判断怎么办？”→ 混合编排（主骨架用代码状态机，只在决策节点嵌窄接口 Agent，如 Stripe 做法）。

### 常见误区

- 以为“用了 Claude Code / Cursor 就是 Agent，用了脚本就不是”——看的是**这次运行里谁在选下一步**，不是产品名。
- 以为“级别越高越先进”——高自主梯度本质是用更多推理算力和更高风控成本换取更少人工介入。

---

## 关 1.2｜模型提议、Harness 执行与错误累积的算术

- **核心主题**：捅破“模型自己在操作电脑”的错觉，确立“动作也是 token、模型提议、Harness 执行”的底层原理；用可靠性的复利算术和自我条件化现象讲透为什么单步很准的模型做长任务依然高频翻车，以及“自主 / 审批 / 禁止”边界怎么划。
- **覆盖知识点与出处**：动作也是 token（CMU L01 p.11）；Model Proposes, Harness Executes（Harvard L02 p.9、EECS498 L06）；文字是请求、代码和权限才是强制（EECS498 L05、jyy 第 2 讲）；循环概览与一次调用的真实放大倍数（CMU L01 p.14、Harvard L02）；错误累积算术 `0.95^50 ≈ 7.7%`（Harvard L06、CS329Z L01）与逐步检查重试算术 `0.90^20 ≈ 12%` → 逐步重试 `≈ 98%`（CS146S Eno Reyes）；Vending-Bench 自我条件化（CMU L05 p.28-30）；六任务自主/审批/禁止划分（CMU L01 开场互动题）；“先扎实做第 3 级安全网再加循环”（EECS498 L05）。
- **前置**：关 1.1。
- **黑盒**：六个完整停止条件与 OS 沙箱实现（单元 4）、工具调用的 JSON Schema 与解析（单元 3）。
- **确认题**：
  1. 有人在系统提示词里用全大写写了“ABSOLUTE RULE: NEVER RUN rm -rf OR DELETE USER DATA”，从工程架构看，这能构成安全边界吗？为什么？
  2. 如果一个 Agent 单步准确率是 95%，一个 50 步的任务全做对的概率大约是多少？为什么现实中往往比这个数字更糟，或者怎样才能把成功率拉回 90% 以上？

### 机制与观点交锋

- **长期不变的第一原理：模型只会接龙写字，碰不到任何外部世界**。
  - “动作也是 token”（CMU L01）：工具调用不是魔法，只是模型预测出的特定格式 token 序列。
  - 真实闭环永远是三步：**模型提议（Propose）→ Harness 解析、校验权限并执行（Execute）→ 结果转回文字送回模型（Observe）**。
  - 由此直接推出全课最重要的安全铁律（EECS498 L05）：**“文字是请求，代码和权限才是强制（Prose asks. Code and permissions enforce.）”**。模型永远只能从一份**不是它自己写的菜单**里挑动作。
- **长程任务的致命算术**：
  - **独立错误累积（Harvard L06）**：假设每步 95% 准确，且彼此独立，50 步全对的概率是 $0.95^{50} \approx 7.7\%$（大约 13 次才成 1 次）。
  - **比独立乘法更致命的“自我条件化”（Self-conditioning，CMU L05 Vending-Bench 实测）**：每步并不独立！一旦第 5 步产生一个错误推断或错误文件修改，它就会留进上下文历史里，持续把后面 45 步全部带偏——而且反直觉的是，**更强的模型虽然单步更准，但一旦出错反而更擅长自圆其说、更容易自我条件化**。
  - **破局杠杆（CS146S 嘉宾 Eno Reyes）**：20 步任务单步 90% 准确，只在最后检查一次成功率约 12%；如果**每一步都有便宜的自动检查器且失败允许最多重试 3 次**，单步通过率变成 $1 - 0.1^4 = 99.99\%$，20 步整体成功率飙到约 **98%**！这就是为什么后面所有工程都在死磕“缩短反馈距离”。
- **自主边界怎么划（CMU L01）**：按**动作的影响半径与可逆性**分三栏——自主执行（只读、可逆本地改动）、先问人批准（对外发声、不可逆变更、花钱）、绝不赋予能力（高危不可逆操作直接不进工具菜单，而不是靠提示词劝阻）。

### 源码或论文拆解

- 【真实】CMU L01 开场互动标本：把 6 个真实任务（排查结账故障、给 5 万客户发邮件、报税、迁移支付 API、抢演唱会票、调整胰岛素剂量）划入“自主 / 先问 / 绝不”，直击“按动作分栏，而不是按任务名分栏”——比如“迁移支付 API”里的读代码/写测试可以自主，切生产流量必须人批。
- 【真实】本机开源代码佐证：查看 `materials/harnesses/codex/codex-rs/bwrap/` 与 `materials/harnesses/grok-build/crates/codegen/xai-grok-permission-rules/` 的目录存在本身，直观印证“权限和沙箱是独立于 Prompt 之外的硬代码层”。（本关只看架构层次，具体实现留到单元 4 细拆。）

### 互动与实战

场景判断：你们团队正在做一个自动修线上 Bug 的 Coding Agent，目前它在 20 步任务里端到端成功率只有 18%。老板说：“换一个更贵的旗舰模型吧，单步准确率从 92% 提到 95% 就行了。”请你用算术和工程机制反驳或修正老板的方案，并给出性价比高得多的改进方向。

- **参考**：先算账：$0.92^{20} \approx 18.9\%$，花几倍预算换旗舰模型提到 95%，$0.95^{20} \approx 35.8\%$，依然远不到可用线，而且更强模型还有自我条件化风险。正确高杠杆是**拆步 + 加每步便宜的外部验证器（lint/typecheck/单测）+ 允许局部重试**，把“只在第 20 步查”变成“每 1–2 步自动查”，同时确保错误尝试不污染主上下文。

### 面试拷问

- **题 1**：为什么说“给 Agent 加安全护栏不能靠在 System Prompt 里写规则”？如果面试官追问“那你觉得 Prompt 里的安全指令完全没用吗”，你怎么回答才显出工程老练？
  - **参考与追问**：Prompt 是**概率性引导**（把 95% 正常请求引导到合规路径，减少撞墙和无谓重试），但对抗 Prompt Injection、长程退化和极端边缘情况时**安全保证为 0**；真正的不可逾越边界必须由 Harness 代码层的**最小权限工具菜单 + 沙箱隔离 + 执行前确定性校验**强制执行。两层是“软引导 + 硬门禁”的纵深防御，不是二选一。

### 常见误区

- 把“模型吐出错误结论后，自己再反思一下”等同于“外部验证”——没有外部环境反馈的自我反思仍可能保留盲区（关 1.5 和单元 8 细讲）。
- 按“任务名”一刀切决定放不放权，忘了同一个任务拆成动作后风险天差地别。

---

## 关 1.3｜范式之争：薄 Harness 还是厚 Harness，训模型还是做系统

- **核心主题**：建立 Agent 完整六组件技术栈全景，厘清“提升 Agent 能力的六大维度 × 训模型与做 Harness 两条互补路线”，深度拆解 2026 年业界最核心的架构范式之争——薄 Harness（顺应模型演进、删掉产品）vs 厚 Harness（系统工程红利与可靠性底座）。
- **覆盖知识点与出处**：Agent 六大核心能力（工具准确、长上下文一致、可定制、复杂任务管理、环境理解、安全）× 两条路线（模型权重训练 vs Harness 工程）（CMU L01 p.17-25）；Agent 完整技术栈六组件（沙箱、Harness、推理服务、模型、训练系统、可观测监控）（CMU L01 p.26-31）；Agent = 模型 × Harness 实证数据（Harvard L04：同模型换 Harness 在 SWE-bench Verified 从 43/169 → 72/169）；薄 Harness 观点（CS146S W1 逐字稿、Lee Robinson“Delete product”、Pi 设计哲学）vs 厚 Harness 观点（Harvard CS2680、DeepSeek `dsh`、jyy 第 9 讲“本质复杂性 vs 附带复杂性”）；工程化三层（系统、数据、评估，CS329Z L01）。
- **前置**：关 1.1、1.2。
- **黑盒**：SFT / RLVR 训模型的具体算法（单元 12–13）、推理服务与 KV Cache（单元 14）。
- **确认题**：
  1. 同样一个底层模型（权重一个字节没改），只是换了一套 Harness，为什么在 SWE-bench 上的解决率能差出近一倍？Harness 到底改变了什么？
  2. 2026 年业界一直在争“投资模型还是投资 Harness”，你觉得哪些 Harness 里的模块迟早会被更强的模型吞掉（应该越做越薄），哪些模块哪怕模型再强 10 倍也绝不可能消失？

### 机制与观点交锋

- **Agent 是系统，不是单个模型（CMU L01 p.26–31）**：完整工业级 Agent 技术栈有六根支柱——**模型（Model）、Harness（控制流/状态/工具/权限）、沙箱（Docker/Modal/bwrap）、推理服务（vLLM/SGLang）、可观测监控（Trace/Eval）、训练系统（SFT/RL）**。整门 14 单元课就是逐一拆解这六根支柱。
- **六种能力 × 两条路线（CMU 11-768 Daniel Fried & Graham Neubig）**：
  - 准确用工具：训模型侧用轨迹 SFT/RL ↔ Harness 侧用清晰工具接口 + 语法受限解码。
  - 长上下文一致：训模型侧拉长上下文训练 ↔ Harness 侧用压缩、外置、检索与子 Agent 隔离。
  - 可定制 / 复杂任务管理 / 环境理解 / 安全：每一项都可以靠改权重（快、内化、但黑盒且更新贵）或改 Harness（透明、可热更新、硬边界、但吃上下文且可能过度约束）。
- **核心观点交锋：薄 Harness vs 厚 Harness（2026 年业界真正的大分歧）**：
  - **薄 Harness 派（Stanford CS146S Mihail Eric、嘉宾 Lee Robinson、Pi 作者 Mario Zechner）**：
    - 论据：今天花三个月写死的复杂多步引导和手搓工作流，半年后模型升一代就被吞掉了（Bitter Lesson）。Lee Robinson 直言“Delete product（删掉多余产品层）”；CS146S 指出 Claude Code 的系统提示词已从早期 200–250 行缩减到 50–80 行，因为教模型怎么用 git 已经过时；Pi 更是砍到只剩 4 个核心工具和不到 1,000 token 的系统提示。
  - **厚 Harness / 系统工程派（Harvard CS2680 Juncheng Yang、南大 jyy、DeepSeek `dsh` / OpenClaw 团队）**：
    - 论据：Harvard L04 实测数据表明 `Agent = 模型 × Harness`，同一个模型换 Harness，SWE-bench Verified 从 43/169 跃升到 72/169（另一组从 31/316 到 72/316）。而且 jyy 第 9 讲点破了本质——**150 行玩具循环悄悄假设了网络不断、动作可逆、没有并发、不需要暂停恢复**；一旦进入生产，**沙箱隔离、权限审计、幂等恢复、Prefix Cache 经济、事件日志持久化、可观测评估**属于“本质复杂性”，模型再聪明 100 倍也替代不了这些系统底座。
  - **调和与判断准则**：把 Harness 拆成两半看——**“替笨模型打补丁的启发式规则”应该越做越薄、随时准备删掉**；**“连接真实世界的系统机制（隔离、权限、状态持久化、验证、观测）”必须做厚做硬**。这正好呼应 jyy 第 13 讲名言：“Policy 交给模型，Mechanism 自己把住”。

### 源码或论文拆解

- 【真实】Harvard CS2680 第 4 讲数据标本：固定同一基础模型，仅更换 Harness 架构，SWE-bench Verified 解决数从 `43/169` 提升至 `72/169`（另一基准对照 `31/316` → `72/316`）。
- 【真实】横向对照本机两个极端仓库的体量（2026-11-25 现场核验）：
  - `materials/harnesses/pi-mono/packages/`：共 **12 个 package**，核心 `coding-agent` 走极致极简路线；
  - `materials/harnesses/deepseek-harness/packages/`：共 **61 个目录/包**，把 `session`、`guard`、`sandbox`、`compaction`、`spill`、`ptc-runtime`、`credentials` 等全部做成可热插拔独立基础设施。

### 互动与实战

把下面 6 个 Harness 功能分进两栏——**“模型变强后可能被删掉的补丁（做薄）”** vs **“模型再强也必须保留的系统机制（做硬）”**，并说明理由：
1. 在 System Prompt 里手把手教模型“修改代码前先 `git status` 再 `grep`”。
2. OS 级无网沙箱（`bwrap` / Docker）与敏感目录写保护。
3. 硬编码的 5 步 ReAct 输出模板（强制要求先输出 `Thought:` 再输出 `Action:`）。
4. 每次工具执行前把调用记录持久化写入会话日志，以便网络断掉后幂等恢复。
5. 稳定系统前缀顺序 + 对超长命令输出自动落盘截断（`spill`）以保 Prefix Cache。
6. 专门为了防止小模型输错 JSON 括号而写的 500 行手写正则修复器。

- **参考**：做薄/可删的是 1、3、6（属于弥补模型推理与格式短板的启发式补丁，现代推理模型和原生函数调用/受限解码已大幅替代）；做硬/永存的是 2、4、5（安全隔离、分布式故障恢复、硬件显存与计费经济学属于外部物理与工程约束，与模型智商无关）。

### 面试拷问

- **题 1**：面试官问你“现在大模型迭代这么快，你费劲做一套 Agent Harness，下个季度 GPT/Claude/DeepSeek 新模型一发，你的工作是不是就白干了？”你怎么答？
  - **参考与追问**：直接用“Policy vs Mechanism（策略与机制）”切开回答：① 如果 Harness 只是堆复杂的 Prompt 补丁和死板多步编排，确实会被新模型吞掉（Bitter Lesson）；② 真正穿越模型周期的护城河在四块：**领域环境与可验证反馈（Verifier/Eval）**、**安全隔离与权限治理（Sandbox/Credential Proxy）**、**上下文与缓存成本架构**、**面向真实业务状态的幂等/恢复/可观测基础设施**。顺便引用 Harvard 同模型换 Harness 的大幅差距和 Pi vs `dsh` 的不同取舍。

### 常见误区

- 把“薄 Harness”误解成“什么工程底座都不要，写个 20 行 while 循环就能上线”。
- 把“厚 Harness”误解成“往 System Prompt 里塞 3000 行规则、把每一步逻辑都用 if-else 写死”。

---

## 关 1.4｜横评五大开源 Harness：从单体到微内核与插件化

- **核心主题**：掌握 Harvard CS2680 提出的三类 Harness 软件架构（单体、模块化、微内核），直接打开本机五大一线开源 Harness（**Pi、DeepSeek Harness `dsh`、Codex CLI、OpenCode V2、Grok Build**）的真实源码目录，像架构师一样横评五种截然不同的工程范式。
- **覆盖知识点与出处**：三种 Harness 架构——Monolithic（单体）、Modular（模块化）、Microkernel（微内核）及其七维权衡表（Harvard L08 p.40-45）；主流开源 Harness 特色对比（Harvard L08 p.46-53：Claude Code / Codex CLI / DeepSeek Harness / OpenCode / Pi / oh-my-pi / OpenClaw / Hermes）；Pi 极简设计（CS329Z L06）；DeepSeek `dsh` 的 Cordis 插件架构与 `Session = list[Event]`（jyy 第 9 讲）；Codex App Server 多端解耦（EECS498 Lab05）；Grok Build Rust 模块化架构（本机源码实证）。
- **前置**：关 1.3。
- **黑盒**：各家编辑算法、沙箱实现、压缩策略的具体源码实现细节（将在单元 3、4、5 逐一深拆）。
- **确认题**：
  1. Harvard 第 8 讲把 Harness 分成单体、模块化、微内核三种架构：如果要做一个服务整个公司几百个并发后台 Agent 的平台，为什么不能选单体，微内核又引入了什么新代价？
  2. OpenCode V2 把 Harness 做成一个常驻 OpenAPI HTTP Server、TUI/Web/SDK 全是薄客户端，这种设计和传统“命令行进程直接跑循环”相比，解决了什么核心问题？

### 机制与观点交锋

- **Harness 架构演进的三级光谱（Harvard CS2680 第 8 讲 p.40–45）**：
  - **单体（Monolithic）**：记忆、工具、上下文、规划、执行全在一个进程里写死。优点是极简、低开销、好调试；缺点是难替换组件、隔离难做、多 Agent 无法共享底座。适合独立单机小 Agent。
  - **模块化（Modular）**：仍是一个主控循环，但通过接口抽象接入 `MemoryProvider`、`SandboxProvider`、`ToolProvider`（比如一行配置从 Docker 换成 Firecracker）。适合通用 Agent 框架。
  - **微内核（Microkernel）**：极小的核心 Runtime 只管状态、调度、协调和安全，记忆、工具、沙箱作为独立外部服务通过标准协议接入。优点是故障隔离、独立扩缩容、共享基础设施；缺点是通信开销与分布式排障复杂度上升。适合多 Agent 生产底座。
- **五大一线开源 Harness 真实架构横评（结合 Harvard 第 8 讲与本机 2026-11-25 实证源码）**：

| Harness | 语言与体量（实测） | 核心架构范式 | 最具辨识度的工程选择 |
|---|---|---|---|
| **Pi** (`pi-mono`) | TypeScript，12 packages | 极简模块化核心 + TS 扩展生态 | 仅 4 核心原语（read/write/edit/bash）+ `<1K` prompt、JSONL 分支会话树、零内置审批/MCP、价格校验 Cache 保活；`withFileMutationQueue` 串行写文件 |
| **DeepSeek `dsh`** | TypeScript，61 packages | 极致插件微内核（Cordis） | **连 `agent-loop` 自己都是可替换插件**；`Session = list[Event]` 同一日志多投影；CAS 乐观锁编辑；独立 `spill` / `guard` / `ptc-runtime` 包 |
| **Codex CLI** (`codex`) | Rust，133 crates/dirs | 工业级二进制 + App Server 协议 | **Sandbox-first**（`bwrap` 无网沙箱先跑、越界才问）；Lark 语法约束 `apply-patch`；`app-server` 协议让 CLI/IDE 共用同一引擎；`code_mode_host` |
| **OpenCode V2** (`opencode`) | TS/Bun + Rust CLI，33 packages | 常驻 Daemon + HTTP Server | Harness 本身是 OpenAPI HTTP Server（`packages/server/`），TUI/Desktop/SDK 全是薄客户端；9 级模糊编辑替换器；Shadow Git 快照 `/undo`；可接 Harbor 做 RL |
| **Grok Build** (`grok-build`) | Rust，102 crates | 全屏交互 TUI + 高内聚 Crate 矩阵 | 清晰拆出 `xai-grok-agent`、`xai-grok-compaction`、`xai-grok-permission-rules`、`xai-grok-egress-proxy`、`xai-circuit-breaker`、`xai-interjection-core`（中途插话）、`xai-acp-lib`（ACP 协议） |

- **附带三家补充对照（来自 Harvard L08，后续单元细拆）**：Claude Code（TS 闭源，强策略层+typed hooks）、OpenClaw（27 通道聊天网关+压缩前写记忆+Fences/Taint）、Hermes Agent（后台 fork 自进化写 Skill + 50% 最早压缩 + 执行前写 DB）。

### 源码或论文拆解

- 【真实】上课时直接现场打开本机 `materials/harnesses/` 对比三处真实目录结构：
  1. `materials/harnesses/pi-mono/packages/coding-agent/src/core/tools/index.ts`：看 Pi 怎么把工具接口做成极薄工厂函数，并用 `file-mutation-queue.ts` 防并发改坏文件；
  2. `materials/harnesses/deepseek-harness/packages/core/`：亲眼看到 `agent-loop`、`system-prompt`、`session`、`tool-executor-native`、`tool-executor-ptc` 全部平级并列为独立插件；
  3. `materials/harnesses/grok-build/crates/` 与 `materials/harnesses/codex/codex-rs/`：对照两个工业级 Rust Harness 的零件图，把每个 crate 名字直接映射回我们后面 13 个单元要学的机制（比如 `xai-grok-egress-proxy` → 单元 4 出口代理，`xai-interjection-core` → 单元 4 中途引导，`xai-fast-worktree` → 单元 8 多 Agent 隔离）。

### 互动与实战

架构选型题：假设你加入一家初创公司，要从零搭一个“面向企业内部研发团队的异步代码修复 Agent（从 Jira/GitHub Issue 自动接单、在隔离环境跑测提 PR，同时员工想在网页和 Slack 里随时看进度和中途纠偏）”。请从上面五个开源 Harness 里挑出**最值得借鉴的 2–3 个具体设计**拼成你的初版架构草图，并说清楚**不选哪家的哪个设计**。

- **参考**：值得借鉴：① OpenCode V2 / Codex App Server 的 **Daemon/Server + 协议解耦**（支持网页、Slack、CLI 多入口接入同一会话）；② Codex CLI 的 **Sandbox-first** 与 Grok Build 的 `egress-proxy` / `permission-rules`（企业后台无人值守必须强隔离防外泄）；③ `dsh` 的 `Session = list[Event]` 单一事件日志多投影（既能恢复断点又能实时推给前端/Slack）+ Grok 的 `interjection` 中途插话。不直接照搬：Pi 的“零内置审批与安全防护”（适合极客本机自用，不适合企业后台无人值守）。

### 面试拷问

- **题 1**：面试官问“你研究过哪些开源 Coding Agent Harness？选两家讲讲它们在底层架构上最大的差异，以及各自为了什么场景做出的权衡？”
  - **参考与追问**：能清晰讲出具体架构级差异而不是表面功能（例如对比 **Pi 的极简扩展核心** vs **DeepSeek `dsh` 的一切皆插件+事件日志投影**，或 **Codex 的 Rust Sandbox-first + App Server** vs **OpenCode 的 OpenAPI Server + Shadow Git**）。追问：“`dsh` 把一切都做成插件，jyy 第 9 讲提到这种架构有一个经典的组合隐患是什么？”→ 插件局部合理不保证整体合理（例如 10 个上下文压缩插件各自压缩一半，叠加起来上下文只剩 1/1024）。

### 常见误区

- 只看表面 UI（有没有漂亮 TUI、支不支持某模型）来评价 Harness，没看到底层**状态表示（日志 vs 列表）、进程形态（CLI vs Daemon/Server）、安全边界（先沙箱 vs 先审批）和扩展模型**才是真正的架构分水岭。

---

## 关 1.5｜论文精读：ReAct 与 *Building Effective Agents* + 单元面试拷问

- **核心主题**：建立“四步精读论文法”，精读 Agent 领域最基础的两份奠基材料——学术奠基论文 **ReAct (Yao et al., 2022/ICLR 2023)** 与工业界工程纲领 **Anthropic *Building Effective Agents* (2024)**——并站在 2026 年的视角做批判性复盘（看清哪些结论已经过时、哪些仍是铁律）；随后用一轮综合面试拷问收官单元 1。
- **覆盖知识点与出处**：ReAct 将推理作为更新自身状态的内部动作与外部行动交替（329Z L01、L06、Harvard L04）；仅推理 vs 仅行动 vs ReAct 三态对比与 Apple Remote 标本（329Z L01、Harvard L04）；Anthropic Workflow vs Agent 界定与“保持简单”原则（329Z L05、L06）；CS329Z L06 对 2022–2024 早期模式的“2026 现状更新”（自我反思内置进推理模型、编译式规划被并行工具调用替代、无外部反馈的自我评判会掉分）。
- **前置**：关 1.1–1.4。
- **黑盒**：五种 Workflow 模式的详细编排和代码模式（单元 8 展开）、Reflexion/ToT 论文细节（单元 8）。
- **确认题**：
  1. ReAct 论文在 2022 年解决的核心痛点是什么？如果把 ReAct 放到 2026 年的推理模型（自带内部 CoT）和原生 Tool Calling 体系里，这篇论文的哪个做法已经过时了，哪个核心思想依然活着？
  2. Anthropic 在 *Building Effective Agents* 里为什么一再强调“能用单次调用或 Workflow 解决就不要上 Agent”？这和你在关 1.2 学的算术有什么直接联系？

### 机制与观点交锋

- **教你一套 20 分钟精读 Agent 论文的四步套路**（后面 13 个单元反复用）：
  1. **锚定痛点**：当时（论文发表那年）基线卡在哪？不解决它为什么不行？
  2. **抓骨架与核心图**：一句话讲清方法，看懂架构图里数据流和状态怎么走。
  3. **盯死消融表（Ablation）**：别光看主表 SOTA 吹牛，看去掉每个组件后分数掉多少、成本涨多少、测试集有没有水分。
  4. **用 2026 年视角挑刺**：这篇论文当年隐含了什么模型假设（如无原生 tool call、无 reasoning tokens、短窗口）？今天哪些过时了，哪些升华成了不变的原则？
- **精读材料 1：ReAct (Synergizing Reasoning and Acting in Language Models)**
  - 痛点：2022 年 Chain-of-Thought（只推理）没有外部接地，小幻觉会滚雪球；Act-only（只行动）缺乏高层规划与异常处理，容易原地打转。
  - 核心机制：把自由文本的 `Thought`（内部推理，不改变外部环境但更新上下文工作记忆）和 `Action`（外部工具调用）+ `Observation`（环境返回）交织在同一条序列里。
  - 2026 年视角挑刺（呼应 CS329Z L06）：今天不再需要靠 few-shot prompt 手动逼模型写 `Thought: / Action: / Observation:` 文本前缀——推理模型的 thinking tokens 内化了 Thought，原生 Tool Calling 协议结构化了 Action；但 ReAct 确立的**“推理与环境观察交替接地”**仍是当今几乎所有 Coding Agent 循环（包括 CMU HW1）的共同心脏。
- **精读材料 2：Anthropic *Building Effective Agents***
  - 核心立场：把所有复杂系统沿“控制流归属”切为 **Augmented LLM → Workflows（预定义代码路径）→ Agents（模型自主循环）**，提出三条反直觉工程纪律：**从最简单方案起步**、**只在需要开放式灵活性与模型驱动决策时才加复杂度**、**重视 ACI（Agent-Computer Interface，工具文档与报错格式）就像重视人机界面 HCI 一样**。
  - 观点交锋：这份 2024 年底的文章偏保守务实（警惕过度框架化、推崇裸调 API + 清晰循环）；而 2026 年的 Harvard CS2680 与 DeepSeek `dsh` 补充了另一面——当单 Agent 走向长程后台与多端协作，裸写 20 行脚本撑不住幂等、隔离、缓存和可观测，必须长出严谨的 Harness 系统层。

### 源码或论文拆解

- 【论文】ReAct 经典对比案例（329Z L01 / Harvard L04 引用）：HotpotQA “Apple Remote” 多跳事实题上，Standard（直接答错）vs CoT（自信编造错误中间事实产生幻觉）vs Act-only（查了信息却不会串联推理）vs ReAct（查事实→依据观察修正下一步搜索→答对）。
- 【论文】对照读 *Building Effective Agents* 的 ACI 设计清单（将在单元 3 结合 SWE-agent 论文和五大开源 Harness 源码深拆）：让模型写绝对路径而非相对路径、把工具格式设计得贴近互联网自然代码分布、留出足够思考空间。

### 互动与实战

论文复述与挑刺实战：合上笔记，请你用 **3 句话**（模拟面试中“你怎么评价 ReAct 这篇论文”）分别回答：① 它当年解决什么核心问题；② 2026 年今天它的哪部分已经过时；③ 哪部分依然是所有 Agent 的底层铁律。

- **参考**：① 解决纯推理缺乏外部环境接地易幻觉、纯行动缺乏规划与纠错的问题，把推理和外部观察交替闭环；② 当年靠 few-shot 文本提示强制写 `Thought/Action` 格式已经过时，被推理模型原生思维链和结构化 Function Calling 取代；③ “行动必须接受环境观察反馈、在闭环里动态纠偏”的范式依然是今天一切 Coding/Research Agent 的核心循环骨架。

### 面试拷问

单元 1 综合压力面试（逐题口述，老师按面试官标准连追两层）：
- **题 1（系统全景）**：如果让你给一个完全没做过 Agent 的后端资深工程师，在 2 分钟内讲清楚“一个生产级 Coding Agent 系统到底由哪些模块构成，模型在里面究竟干了啥”，你怎么画这张架构图？
- **题 2（范式与取舍）**：你们业务现在有一个复杂多步工单处理需求，团队里一派主张直接上自主 Agent + 开源大框架，另一派主张用 Workflow 状态机 + 几个窄 LLM 节点。你是技术负责人，你怎么定架构，怎么说服另一派？
- **参考**：题 1 必须清晰切出“模型只做无状态文本/动作提议”和“Harness 负责循环/状态/上下文/工具/权限沙箱/可观测”，最好能用 Pi / Codex / `dsh` 的真实模块举证；题 2 必须落到可验证性、错误累积算术、单步副作用代价、SLA 成本与迭代演化路线（先用简单基线跑出真实错误分布，再按瓶颈加自主度），不空喊概念。

### 常见误区

- 读论文只背摘要里的“提升了 X%”，不看实验设置和发表年份，面试时把 2022–2023 年已经被原生能力取代的技巧（比如手写 ReAct 正则解析）当成 2026 年最佳实践去吹。

---

# 单元实验｜轨迹透视与真实请求解剖（Harvard Mads-Lens + CS146S Week 1 融合版）

- **实验定位**：单元 1 唯一动手大练兵，直接融合 **Harvard CS2680 Assignment 1 (`Mads-Lens`)** 与 **Stanford CS146S Week 1 (`Trace Dissection`)** 的原版精髓——在自己造 Harness 之前，先像外科医生一样看透生产级 Coding Agent 的真实一次会话里到底发了什么、花了多少、在哪儿绕了弯。
- **前置检查**：不要求手撕复杂语法，只需会跑基础命令并用 Agent 协助写轻量可视化脚本。
- **实验步骤**（二选一采集，推荐全体验，代码与报告放在 `work/unit01/trace-lens/`）：
  1. **采集一条有血有肉的真实轨迹**（满足 CS146S 要求：跨至少 2 个文件 + 至少经历一次失败与恢复 + 有规划/多步探索）：
     - *路线 A（CS146S W1 原版抓包）*：按 `materials/assignments/cs146s/week1/assignment.md`，用 `mitmweb --mode reverse:https://api.anthropic.com` 抓一次真实 `POST /v1/messages` 请求体，亲眼拆开看 `system`、`tools`、`messages` 三块的真实行数与占比（切记脱敏，绝不把 `x-api-key` 或原始抓包提交进 Git）。
     - *路线 B（Harvard Mads-Lens 事件流）*：跑一次 `agy -p ... --output-format stream-json` 或 `claude -p ... --output-format stream-json --verbose`（或分析本机已有真实会话日志），拿到逐行 JSON 事件流。
  2. **做一台轻量轨迹透视器（Agentic 实战）**：先写一份半页的 Spec（说明输入日志格式、要展示哪些字段：每步调用的工具与参数、输入/缓存/输出 token、单步耗时、报错与重试节点、总花费），交给 Agent 实现一个极简本地网页或终端透视工具，你来 Review 代码并拿刚采的轨迹实测跑通。
  3. **提交三点硬核工程观测报告（`work/unit01/trace-lens/report.md`，借 Harvard Mads-Lens 要求）**：
     - 观测 1（机制）：用户发第一句话前，Harness 已经塞进了多少看不见的上下文/工具定义？哪一步消耗比你预想的多得多？
     - 观测 2（坑）：轨迹里找一个具体 step（给出 step 编号与工具名），说明 Agent 在哪儿走了弯路、报错或重复读文件。
     - 观测 3（架构启示）：如果让你基于这次观测自己设计 Harness（对应单元 3–5），你最先想改哪一条设计？
- **验收标准**：透视器能跑通真实轨迹；报告里的 3 条观测全部落到真实 step 编号、工具名和具体数字，不写空话；确认没有任何密钥或未脱敏敏感日志进 Git。
