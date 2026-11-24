# 课程总表（14 个大单元实战研习）

共 **14 个大单元、4 个阶段**，面向未来的 Agent 开发 / Agent 算法工程师。每个单元拆成 **4–6 个高密度主题关**，融合六门 2026 秋季顶尖名校课的全部知识点与观点分歧、五大一线开源 Harness 源码拆解、前沿论文精读、名校原版实验与大项目实战，以及大厂面试拷问。不按固定天数排课，按断点接力推进。

来源缩写：CMU = CMU 11-768；329Z = Stanford CS329Z；Harvard = Harvard CS2680；146S = Stanford CS146S；498 = UMich EECS498；jyy = 南大生成式软件工程。

---

## 主标本库：五大一线开源 Harness 源码

运行 `bash tools/materials/fetch_repos.sh` 可将以下五个代表不同设计哲学的开源 Harness 浅克隆到本机 `materials/harnesses/`（不进 Git，备课和上课时直接翻真实源码对比），辅以课件里的 Claude Code、OpenClaw、Hermes Agent 和 mini-SWE-agent：

| Harness | 仓库与语言 | 架构范式 | 核心解剖点 |
|---|---|---|---|
| **Pi** | `earendil-works/pi`（原 `badlogic/pi-mono`，TypeScript） | 极致极简主义 | 4 个核心工具（read/write/edit/bash）、<1K token 系统提示、JSONL 分支树、零内置审批/MCP/子 agent 靠扩展生长、带价格检查的 Cache 保活 |
| **DeepSeek Harness (`dsh`)** | `deepseek-ai/deepseek-harness`（TypeScript） | 一切皆插件（Cordis 微内核） | 连 Agent Loop 本身都是插件、`Session = list[Event]` 单一日志多投影、CAS 乐观锁文件编辑、`spill` 输出溢出、`guard` / `sandbox` / `ptc-runtime` |
| **Codex CLI** | `openai/codex`（Rust） | 工业级沙箱 + App Server 协议 | Sandbox-first（`bwrap` 无网沙箱先跑、越界再审批）、Lark 语法约束 `apply-patch`、`AGENTS.md` 目录页、`app-server` 多客户端协议、`code_mode_host` |
| **OpenCode V2** | `anomalyco/opencode`（TS / Bun + Rust CLI） | 守护进程 + HTTP Server | Harness 即 OpenAPI 服务，TUI/Web/SDK 为薄客户端；9 级模糊替换编辑器+大小上限；Shadow Git 每步快照 `/undo`；可接 Harbor/OpenEnv 做 RL |
| **Grok Build** | `xai-org/grok-build`（Rust） | 全屏交互 TUI + 模块化运行时 | 几十个独立 crate 清晰分工：`xai-acp-lib`（ACP 协议）、`xai-grok-compaction`、`xai-grok-permission-rules`、`xai-grok-egress-proxy`、`xai-circuit-breaker`、`xai-interjection-core`、`xai-fast-worktree` |

---

## 14 个单元的路线

- **阶段一（单元 1–5）**：解剖与构建 Harness——搞透模型外面那层系统、核心循环、安全护栏与上下文成本经济
- **阶段二（单元 6–9）**：知识、记忆、搜索与多 Agent——把单 Agent 做深，掌握编排边界与四大垂直形态
- **阶段三（单元 10–11）**：评测科学 & Agentic 软件工程——建立可信评测体系，掌握现代 Spec/环境/审查/软件工厂工作流
- **阶段四（单元 12–14）**：Agent 算法训练与推理系统——打通轨迹数据/SFT、RLVR/GRPO 异步强化学习与 LLM 推理服务全栈优化

| 单元 | 主题 | 对照 Harness / 精读论文 | 单元实验（借鉴名校原版） | 教案 |
|---|---|---|---|---|
| 1 | Agent 全景与 Harness 范式之争 | 五大开源 Harness 横评；论文：ReAct + *Building Effective Agents* | **Harvard Mads-Lens + CS146S W1**：抓包解剖一次真实会话轨迹，做轻量轨迹透视器 | 已备（5 关） |
| 2 | 面向建造者的 LLM 底层最小集 | Codex Lark 语法约束；透明 Raw API 报文 | **Raw API 底层实验**：实测温度采样分布、`length` 截断、`tool_calls` 原始协议与约束解码边界 | 未备 |
| 3 | 核心循环、工具协议、编辑格式与 MCP | Pi 4 工具核 vs `dsh` 插件循环 vs OpenCode 9 级替换器 vs Codex `apply-patch`；论文：SWE-agent (ACI) / CodeAct | **Harvard Mads-Loop 核心 + CS146S W2**：搭建自己的最小 Agent Loop，并实现面向结果的 MCP Server 对比 Code Mode | 未备 |
| 4 | 停止条件、审批、沙箱与安全攻防 | Codex `bwrap` 先沙箱后审批 vs Grok `permission-rules`/`egress-proxy` vs OpenClaw Fences/Taint；论文：CaMeL | **EECS498 Lab04 攻防改造**：在沙箱实测 Prompt Injection，为 Mini Harness 补齐 6 停止条件、权限层与破坏性测试拦截 | 未备 |
| 5 | 上下文工程、Prefix Cache 与成本优化 | Pi 价格感知 Cache 保活、`dsh` 日志投影与 `spill`、Hermes 50% 压缩；论文：RLM | **Harvard Mads-Opt + CS146S W6**：固定任务成功率，做上下文裁剪、缓存命中、并行工具与模型路由优化并写消融报告 | 未备 |
| 6 | 知识接入路线之争：RAG、Agentic Search 与 LLM Wiki | EECS498 L17 LLM Wiki；论文：Self-RAG / Search-R1 | **CS329Z A1 检索子实验**：对同一批技术文档横向实测纯向量 RAG vs 混合检索 Agentic Search vs 索引+Wiki 的准确率与花费 | 未备 |
| 7 | 长期记忆、Skills 与自进化机制 | OpenClaw 压缩前静默落盘、Hermes 后台 fork 自学习、`dsh`/`pi` skill 机制；论文：MemGPT / Mem0 / SkillsBench | **CS146S W3 + 记忆引擎实验**：编写并实测带渐进披露的 Skill，并在长程多轮任务上对比文件记忆 vs 冲突合并记忆 | 未备 |
| 8 | 控制流、规划、推理时搜索与多 Agent 编排 | `dsh` `workflow`/`team`、Grok `xai-fast-worktree`/`xai-acp-lib`、Codex `agent-roles`；论文：ToT / Reflexion / CooperBench | **南大 jyy Lab2（算力换智力）**：给解题循环加 effort 预算与验证器，再对比单 Agent vs 多 Agent（Worktree 并行）的收益与协调开销 | 未备 |
| 9 | 垂直 Agent 形态解剖：Coding、Computer Use、Deep Research 与常驻 Agent | OpenClaw 27 通道网关、`dsh` `browser-use`/`computer-use`、Codex `app-server` | **EECS498 Lab05 改造**：基于开源 Harness 接一个外部触发通道，或拆解一次真实 Deep Research / GUI 失败轨迹并修复 | 未备 |
| 10 | Agent 评估体系、裁判校准与可靠性科学 | Docent 轨迹诊断、EECS498 L20 音画机械检查；论文：τ-bench (`pass^k`) / Agent-as-a-Judge / PULSE | **CMU HW2 + CS329Z A2 精简实操**：审查 seed 轨迹、校准 LLM/Agent Judge、算 `pass@k` 与 `pass^k`，构造一条防作弊 Harbor 评测题 | 未备 |
| 11 | Spec 驱动、Agent-Ready 仓库、审查演化与 Software Factory | Spotify Honk 评判器、Factory 就绪度模型、OpenCode Shadow Git；论文：Eno Reyes / jyy 非形式化验证案例 | **CS146S W4–W5 + EECS498 金鱼检验**：改造一个凌乱仓库至 Agent-Ready，并走通“大象写 Spec → 金鱼检验 → Agent 实现 → 分层 Review → CI 门禁”闭环 | 未备 |
| 12 | Agent 数据工程、轨迹 SFT 与自动优化 | DSPy、Meta-Harness；论文：SWE-Gym / GEPA | **南大 jyy Lab3（蒸馏你自己）**：攒可持续增长的个人评测集跑自动提示优化（亲测过拟合陷阱），并清洗构造一份标准 SFT 轨迹集 | 未备 |
| 13 | Agent 强化学习：RLVR、GRPO 与异步 RL 系统 | OpenCode + Harbor + AsyncGRPO、`scottyrl`；论文：DeepSeek-R1 (GRPO) / SkyRL | **CMU HW3 (`scottyrl`) 离线+单卡实验**：跑通 Data Pipeline、同步/异步 GRPO 核心逻辑与 `MockPolicy` 测试，构造并复盘一个 Reward Hacking 反例 | 未备 |
| 14 | LLM 推理服务与 Agent 全栈优化 | vLLM / SGLang；论文：PagedAttention / SuffixDecoding | **Harvard Mads-Serve 精简版**：部署本地或单卡开源推理引擎接入自建 Harness，实测 Prefix Caching、上下文长度与并发数对 TTFT/TPOT 的真实影响 | 未备 |

---

## 名校原版大项目路线与前置知识门禁

大项目**直接采用海外名校原版课程的公开大作业**，方便对照原版评分标准和优秀公开解法。每项大项目都标明了必须先学完的前置单元——**前置知识没学完之前不提前硬上**：

| 阶段节点 | 推荐原版大项目 | 本地位置（`fetch_repos.sh` 拉取） | 必须先学完的前置单元 | 原版核心验收标准 |
|---|---|---|---|---|
| 阶段一收尾 | **Harvard CS2680 Mads 1–3**（`Mads-Lens` → `Mads-Loop` → `Mads-Opt`） | `materials/harvard-cs2680/text/assignments-index.txt` | **单元 1–5** + 基础 Python / LLM API | 实时轨迹前端 → 鲁棒核心 Loop 过隐藏异常测试 → 固定成功率极限压降 token/延迟并写技术博客 |
| 阶段二中段 | **CMU 11-768 Assignment 1**（Build an Agent Harness）或 **CS329Z Assignment 1**（Agent Harness） | `materials/assignments/cmu-hw1/`、`cs329z-a1/` | CMU HW1 需 **单元 1–7**；CS329Z A1 需 **单元 1–6** | CMU：ReAct + 工具 + Skill YAML + Compaction 修 `chess_app` + `ChessAgent` A/B 实验；CS329Z：终端沙箱 + Email 检索 + 模拟用户评估 |
| 阶段三中段 | **CMU 11-768 Assignment 2**（Evaluating a Data-Visualization Agent）或 **CS329Z Assignment 2**（Building an Evaluation Task） | `materials/assignments/cmu-hw2/`、`cs329z-a2/` | **单元 10**（建议连同单元 11 一起学完） | CMU：seed 轨迹分析 + 校准 Validator + 新任务与 Harbor 打包 + 迭代报告；CS329Z：Docker/Harbor 防作弊评测题 + 固定 `mini-SWE-agent` 标定 |
| 阶段四算法冲刺 | **CMU 11-768 Assignment 3**（`scottyrl`: Training Agents with RL） | `materials/assignments/cmu-hw3/` | **单元 12–13** | Data Pipeline + 同步 REINFORCE/GRPO + 异步 GRPO 与 Staleness 重要性采样 + Number Search 消融实验 + TextCraft-Synth 评测 |
| 阶段四系统延伸（选做） | **Harvard CS2680 `Mads-Serve` & `Mads-Stack`**（A4–A5） | `materials/harvard-cs2680/text/assignments-index.txt` | **单元 14** + 完成 Mads-Opt | 单卡自部署开源推理引擎接入自建 Agent，定位 Serving 瓶颈并跑通全栈端到端优化（对标 Terminal-Bench 2.0） |

---

## 各单元的范围与核心学派分歧（备课时照此执行）

六门课已经盘点出的 **1817 个知识点**已全部映射进这 14 个单元，零遗漏：

- 逐条清单在 `curriculum/coverage.md`；备某个单元时先跑 `python3 tools/coverage.py --unit N` 拉出该单元全量知识点，合并去重后排进 4–6 关。
- 凡是不同名校课程或老师之间观点存在分歧的，备课和上课时必须显式点明“哪门课哪位老师怎么看”。
- 新放出的讲次继续盘点补进 `curriculum/knowledge_points.json`，再跑 `python3 tools/coverage.py --check`。

- 单元 1：感知-行动循环（环境、观察、动作、目标）、聊天助手与 agent 分界、模型提议与 harness 执行、循环概览、workflow 与 agent、自主梯度五级与代价、agent 六种能力、agent = 模型 × harness、单体/模块化/微内核架构、五大开源 harness（Pi / `dsh` / Codex CLI / OpenCode V2 / Grok Build）哲学横评、训练模型 vs 做 harness 两条路线、错误累积算术、agent 简史、AI 编程四波浪潮、从打字员到策展人；**观点分歧**：薄 harness（CS146S / Pi“删掉产品”）vs 厚 harness（Harvard / `dsh` 工程架构红利）
- 单元 2：分词与 token、下一个 token 预测、贪心/top-k/top-p/温度采样、对话模板与窗口截断（`stop`/`length`/`tool_calls`）、自注意力和长度平方代价、MoE、思维链与推理模型、幻觉为什么是自回归机制而非故障、代码模型训练数据与 FIM、训练流水线（预训练/中训练/SFT/偏好对齐/RLVR，概念级）、约束解码（JSON Schema 与 Codex Lark 语法）的边界、能力与知识两轴选型
- 单元 3：无状态 HTTP 请求与流式输出、从编辑块长出工具调用协议与 schema、最小循环与并行工具调用、工具结果回传与 call ID、核心工具集（读/写/改/搜索/Shell）、文件编辑格式大战（整文件 / Search-Replace / 统一 diff / AST / Codex Lark Patch / OpenCode 9 级模糊替换 / oh-my-pi Hashline / `dsh` CAS 乐观锁）、工具设计五原则与报错设计、MCP 架构（stdio/HTTP/OAuth、凭证代理、与 API/Skill 分工）、工具膨胀与 Code Mode（`search`/`execute` 省 90% token）、CodeAct、Shell 与后台进程管理、浏览器与 GUI 动作闭环
- 单元 4：完成信号与诚实报失败、六个停止条件（完成/步数/token/墙上时钟/重复调用/连续出错）与检查位置、权限层与审批疲劳（93% 盲批数据）、分类器自动审批的误拦与漏放、远程审批与中途引导（Grok `interjection` / `dsh` 三种输入语义）、故障分类与退避重试、超时不等于未执行与幂等性、不可逆副作用与撤销边界（含 OpenCode Shadow Git 与“浏览器返回不等于服务端回滚”）、hooks 与代码级护栏（“文字是请求，代码和权限才是强制”）、容器与 OS 沙箱（Codex `bwrap` 先沙箱后审批）、真实安全事故、威胁建模与 STRIDE、agent 失误四类、奖励作弊/失准/合谋、四类提示注入与“致命三要素”、MCP 供应链投毒、抗注入设计模式（Action-Selector / Plan-Then-Execute / Dual LLM / CaMeL）、OpenClaw Fences/Taint/Sentinels、轨迹审计与思维链监控
- 单元 5：每次重发全部历史与输入平方增长、一次调用的上下文解剖（system/tools/memory/retrieval/messages）、系统提示词与“补丁式禁令”反模式、Big Three 排障顺序（上下文→模型→提示）、Context Rot 与聪明区/笨区、四级管理防线（准入→外置 `spill`→变换/观察遮蔽→压缩 Compaction）、反复压缩导致约束漂移、Prompt/Prefix Cache 机制（只追加不改、改一处工具定义全失效、Pi 价格感知保活）、仓库地图与按需加载、分层规矩文件、RLM 超长上下文外部 REPL 按需读写、长上下文模型架构（滑窗/线性/稀疏注意力，概念级）、成本六因子公式与学生实测数据（97.6% 缓存读）、降轮次/降步数/降输入/降输出/降单价、确定性代码替代 LLM、路由与级联、净节省与反噬成本、预算上限与公平成本实验；**观点分歧**：Compaction 压缩 vs RLM 外置读写
- 单元 6：RAG 流水线、BM25 与稠密向量检索（DPR/ColBERT）、ANN 与检索指标、分块与上下文化检索、RAPTOR 与 GraphRAG、混合检索与重排、RAG 三侧失效（检索/阅读/循环）与引用幻觉、Agentic RAG（Self-RAG / CRAG / Search-R1）、文件系统+grep 检索与模型预编译维护的 LLM Wiki（三层结构：摄取/问答/巡检，出处与新鲜度）；**观点分歧**：向量 RAG 派（CS329Z L03）vs 文件系统与预编译 Wiki 派（EECS498 L17 / Lee Robinson / LongMemEval-v2）
- 单元 7：更新 agent 的三条路（上下文/外部产物/权重）、跨会话持久状态与无记忆的三种损失、CoALA 四类记忆（工作/情景/语义/程序）、记忆设计七问、文件系统记忆 vs 数据库/图谱记忆、MemGPT 分层自管理、OpenClaw 压缩前静默落盘、Mem0 冲突处理（增改删不动）、遗忘是一等操作与过期笔记风险、过度个性化与记忆安全面、Skill 渐进披露三级加载、Skill vs MCP vs Hook vs Plugin 分工、SkillsBench 实测与技能负迁移、从轨迹归纳技能（Voyager / ASI / AWM / ReasoningBank / Hermes 后台 fork）、Reflexion 与 ExpeL、会成长的个人助手
- 单元 8：Workflow 与 Agent 控制流光谱、五种基础 workflow（提示链/路由/并行/编排者-工人/评估者-优化者）及混合编排、ReAct/Plan Mode/先规划再执行与重规划、框架取舍（DSPy / LangGraph / OpenHands SDK / Temporal）、模型变强后删掉多余层、推理时搜索（Repeated Sampling 与 `pass@k`、提高多样性、四类验证信号、Best-of-N 与不完美验证器上限、自洽投票、迭代精炼与 Self-critique 盲区、PDR 与递归锦标赛投票 RTV、ToT/GoT/MCTS、环境接地搜索回溯代价与三类世界模型、Meta-Harness）、多 agent 动机与三张图（控制/任务/通信）、八种多 agent 架构、单 agent 基线与“协调的诅咒”（CooperBench / Terminal-Bench 实测）、子 agent 全新 vs 分叉缓存取舍、Handoff vs Agent-as-tool、任务 DAG 与关键路径（Amdahl 定律）、Worktree 隔离与合并、A2A 协议、多模型单 harness 适配、盲从与合谋、追踪与监控；**观点分歧**：单 agent 基线与独立采样（CMU L18 / CS329Z L08）vs 多 agent 协作与并行舰队（Harvard L05 / CS146S W8）
- 单元 9：编程 Agent（定位-修改-验证、Agentless vs SWE-agent vs OpenHands、前端行为测试与浏览器自检）、Computer Use（GUI 视觉定位、动作空间、OSWorld、从玩具网页到真实环境）、Deep Research（多跳检索、证据综合、BrowseComp、引用核查）、个人与常驻后台 Agent（脱离键盘、云电脑、多通道网关如 OpenClaw、定时心跳、Codex App Server 接入外部通道）
- 单元 10：传统指标为何失效、建构效度、验证阶梯五级与古德哈特定律、基准半衰期与四层数据泄漏（训练/评测时/环境/过拟合）、十二大主流基准地图、好基准七条与任务质检（Terminal-Bench / Harbor）、三类评分器（代码/人工/LLM Judge）六维权衡与假阴假阳、LLM 裁判偏见（位置/长度/自我偏好）与回归校准（AutoMetrics）、Agent-as-a-Judge、过程分 vs 结果分（退单跳步案例）、`pass@k` vs `pass^k` 与方差/配对检验、评估协议与成本帕累托前沿披露、PULSE 隐式交互信号、Docent/Hodoscope 轨迹聚类诊断、非代码产物（图像/音频）的机械检查与盲听漏斗（EECS498 L20）、私有基准回放与评估驱动迭代
- 单元 11：Intent → Spec → Impl 缺口与 Vibe Coding 陷阱、软件工程本质复杂性与附带复杂性、契约式设计（前置/后置/不变量）、需求与架构（领域边界/事件溯源/CQRS/DDD）、Spec 即提示词（信息密集动词与五段 Spec）、RePPIT 流程与大象-金鱼检验、Agent Native 开发与 Ralph Loop、Agent-Ready 九支柱（Runnable / Accessible / Verifiable）、“策略交给模型，机制自己把住”、测试与程序分析工具取舍（Rice 定理边界、静态分析、单测、性质测试、差分测试、Fuzz、非形式化验证与形式化证明直觉）、审查成为新瓶颈与 AI Slop 局部性判据、风险分级与多模型审查（Spotify Honk 评判器）、Git Worktree 并行与 CI 门禁、不停机迁移与 SRE/灰度直觉、软件工厂三支柱与人的三道闸门、生成便宜验证贵与 2×2 委派矩阵、产出+证据与“挣来的自主权”五级阶梯、理解力退化风险与人在 AI 时代的担责与驾驭
- 单元 12：Agent 交互数据分类（轨迹与环境）、轨迹 SFT 的利弊与多轮 loss mask / 思维块 / 长序列装箱、从操作记录与视频挖轨迹、数据合成与可验证沙箱/模拟用户、数据校验去重过滤与失败轨迹再利用、对特定 Harness 过拟合、提示与上下文自动优化（DSPy / GEPA / TextGrad / Meta-Harness）、jyy“蒸馏你自己”与过拟合禁令、同策略蒸馏、Prompt 优化 vs 权重优化的工程选择边界
- 单元 13：为什么 SFT 不够（任务不匹配/数据不匹配/暴露偏差）、模拟环境与可验证奖励 RLVR / Rubric 奖励、专家迭代、REINFORCE 与基线、多轮轨迹信用分配难题、PPO 与 GAE、GRPO 与 DrGRPO 核心机制对比、KL 约束与动态采样/难度筛选、Reward Hacking 与模拟器坍塌、异步 RL 系统架构（Rollout 与 Trainer 分离、权重同步、过时样本重要性采样、OpenCode/Harbor + AsyncGRPO 与 `scottyrl`）、线上 RL 与 RL 缩放规律
- 单元 14：一次请求在服务端的六步、Agent 负载特征（长前缀、多轮重复、重 Prefill）、TTFT 与 TPOT、Prefill 吃算力 vs Decode 吃显存带宽与 Roofline 直觉、GPU 执行模型与存储层级（概念级）、核融合与 FlashAttention、Continuous Batching、Chunked Prefill 与 PD 分离、KV Cache 与 PagedAttention、**Prefix Caching（与单元 5 成本闭环）**、并行切分（DP/TP/PP/EP）、投机解码七路线（独立小模型 / EAGLE / DeepSeek MTP / 检索式 SuffixDecoding 在 Agent 重复负载提速 5.3× / Cursor Speculative Edits / OpenAI Predicted Outputs 计费边界）、批处理与投机解码的延迟-吞吐权衡（MoE 投机开销与动态开关）、浮点非确定性

---

### 前置编程与工程基础建议

- **单元 1–2**：零前置门槛，有日常使用 Coding Agent 体验即可开课。
- **单元 3–11**：需要基础 Python（函数、文件读写、异常处理、调用 LLM API）与基础 Git/终端操作。不追求手撕语法，重点练 Spec 编写、Code Review、跑测试与读 Trace。
- **单元 12–14**：需要具备基础的深度学习/PyTorch 概念认知（不推公式、不写 CUDA 核函数，侧重算法机制、系统瓶颈与工程权衡）。

---

### 原片

每个单元最多推荐一段，不要求看。以下时间戳均从课程公开回放实查得出：

| 单元 | 推荐 | 看哪一段 |
|---|---|---|
| 1 | jyy 第 1 讲《欢迎来到未来》（`BV1pb8o6yE8f`） | `21:49–35:30`（语言模型 → Agent 出现 → U 盘装 Linux 实战）与 `1:24:46–1:33:00`（Intent/Spec/Impl 缺口）；备选 CMU L01 `15:33–30:00`（R&N 定义 → Harness → mini-swe-agent trace） |
| 2 | 329Z L02 | 课件第 1–23 页：什么是语言模型、采样与上下文工程 |
| 3 | CMU L02 / jyy 第 9 讲（`BV144nc6KEA4`） | CMU L02 工具调用；或 jyy L09 `10:27–51:00`（从玩具循环到生产 DeepSeek Harness：网络中断/幂等、插件化与 Actor Model 类比、Session History 投影） |
| 4 | CMU L13 | Agentic Safety 五个真实事故与防线设计 |
| 5 | jyy 第 2 讲《提示词工程》（`BV1CQt365EzW`） | 整讲，重点 `1:37–25:00`（Agent 完整上下文与写清指令）与 `38:55–48:00`（藏头诗/同偏旁规格歧义）；备选 CMU L03 Context Compaction |
| 6 | 329Z L03 | RAG 到 Agentic RAG |
| 7 | CMU L04 | 记忆和技能的区别、人写与归纳技能 |
| 8 | 329Z L08 | Multi-Agent Systems: When More Agents Help or Hurt |
| 9 | CMU L06 / L07 / L10 选一讲 | 按兴趣选 Coding / Computer Use / Deep Research |
| 10 | 329Z L10 | Terminal-Bench 嘉宾讲座 |
| 11 | jyy 第 8 讲《Agent-native 开发》（`BV11LWw6VEHW`） | 整讲，重点 `18:19–30:00`（Ralph Loop 与非确定性状态机）及 `41:59` 起（测试与 CI 门禁）；备选 jyy L05（`BV1Nyeq6qEt8`）/ L10（`BV1Guxu6EERa`） |
| 12 | 329Z L09 | Optimizing AI Agents: Prompts vs. Weights |
| 13 | CMU L09 | Reinforcement Learning Basics for Agents |
| 14 | 没有公开视频 | Harvard CS2680 推理服务部分无公开录像，直接读课件文字 `09–12` |

链接：jyy 的 B 站回放合集 https://space.bilibili.com/202224425/lists?sid=8942017 ；CMU 11-768 课程页 https://www.cmu-agents.com/ ；Stanford CS329Z 课程页 https://cs329z.stanford.edu/ 。

---

## 单元 1｜Agent 全景与 Harness 范式之争

教案：`curriculum/unit01.md`。共 **5 个高密度大关** + **1 个名校原版单元实验**。覆盖全部 94 条单元 1 知识点，首次引入五大开源 Harness 源码横评、论文带读与大厂面试拷问。

| 组 | 关 | 主题 |
|---|---|---|
| A 界定与底层机制 | 1.1 | 感知-行动闭环与自主梯度：谁来选下一步 |
| | 1.2 | 模型提议、Harness 执行与错误累积的算术 |
| B 架构与范式之争 | 1.3 | 范式之争：薄 Harness 还是厚 Harness，训模型还是做系统 |
| | 1.4 | 横评五大开源 Harness：从单体到微内核与插件化 |
| C 论文与面试收官 | 1.5 | 论文精读：ReAct 与 *Building Effective Agents* + 单元面试拷问 |

- **单元实验（必做）**：**Harvard Mads-Lens + CS146S W1 融合版**——拆解一段真实 Coding Agent 会话轨迹（`stream-json` 或抓包报文），统计上下文/工具占比并用 Agent 搭建一个轻量轨迹透视器（目录 `work/unit01/trace-lens/`），输出含 3 条具体观测的复盘报告。
