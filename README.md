# Learn Agent with Agent · 14 个大单元实战研习

一套开箱即用的 **1 对 1 Agent 工程与算法实战学习系统**——用你自己的 Coding Agent（Antigravity、Claude Code、Cursor、Codex 等）当资深师兄，带你系统打通 **Agent 架构与 Harness 工程、现代 Agentic 软件工程、评测与安全、轨迹训练（SFT / RLVR / GRPO）与推理服务**。

课程整合了六门 2026 秋季顶尖名校课（**CMU 11-768、Stanford CS329Z、Harvard CS2680、Stanford CS146S、UMich EECS498、南大 jyy 生成式软件工程**）的全部 1,817 个知识点与学派观点交锋，直接解剖 **Pi、DeepSeek Harness (`dsh`)、Codex CLI、OpenCode V2、Grok Build** 五大一线开源 Harness 源码，并衔接前沿论文带读、名校原版实验与 Capstone 大项目。

---

## 快速开始（3 步开课）

### 1. 克隆并准备自己的学习仓库

建议先 Fork 一份到你自己的 GitHub 私有仓库（方便跨电脑/手机同步学习进度和笔记），再 clone 到本地：

```bash
git clone <你的仓库地址> learn-agent-with-agent
cd learn-agent-with-agent
```

### 2. 拉取本地源码标本与名校资料（推荐，约 1 GB，不进 Git）

```bash
# 一键浅克隆五大一线开源 Harness 源码 + 六个公开名校原版作业仓库到 materials/
bash tools/materials/fetch_repos.sh

# （可选）增量下载六门名校课公开课件并转为纯文本（需本机装有 pdftotext）
bash tools/materials/fetch.sh tools/materials/manifest.tsv materials
python3 tools/materials/to_text.py materials

# 生成本地资料总索引 materials/README.md
python3 tools/materials/index.py
```

> 仓库本身已经自带了整理好的六门课读课笔记（`sources/`）、1817 条知识点映射（`curriculum/coverage.md`）、14 单元总表和单元 1 完整教案/讲义；即便暂时不跑上面下载脚本，也可以直接开课。

### 3. 打开 Agent 开始上课

用 **Antigravity、Claude Code / Claude Desktop、Cursor 或 Codex** 打开本目录，直接发一句：

> **上课**

第一次说“上课”时，老师会先花 2 分钟问清你的技术背景、职业目标和学习偏好，自动写进 `progress/student.md`，接着发给你单元 1 的课前讲义并正式进关 1.1。

每次上课建议新开一个会话，进度和上下文全部靠 `progress/student.md`、`work/` 和 `logs/` 接力，换工具或换设备也能接着上一句继续聊。

---

## 每一关怎么学（五件套弹性组合）

每个单元拆成 **4–6 个高密度主题关**，按这关的性质组合五种真实研发动作：

- **机制与观点交锋**：合并六门课重合内容，保留不同老师与学派之间的观点分歧，明确交代是谁怎么看（例如：薄 Harness vs 厚 Harness、向量 RAG vs 文件系统/LLM Wiki、单 Agent 基线 vs 多 Agent 协作）。
- **开源 Harness 源码拆解**：直接翻本机 `materials/harnesses/` 里的 Pi、`dsh`、Codex CLI、OpenCode V2、Grok Build 真实代码，横向对比同一零件的五种写法。
- **前沿论文精读**：每 1–2 个单元带读 1 篇核心论文（痛点 → 核心方法与关键图 → 消融表 → 2026 年视角挑刺 → 面试 3 句总结）。
- **名校原版实验与大项目**：按单元落地真实代码与实验，直接对标 Harvard Mads 1–5、CMU HW1–3、CS329Z A1–A2、CS146S Week 1–6、EECS498 Lab01–05、jyy Lab1–3。用现代 Agentic 工作流完成（你写 Spec、定架构、调 Agent 实现、做 Review、跑评测、析 Trace），且大项目严格锁定前置单元门禁，学完所需知识再动手。
- **职场场景与面试拷问**：每单元收尾用大厂 Agent 开发 / 算法岗高频题逐层追问，练到能脱口讲透。

---

## 14 个大单元总览

- **阶段一（单元 1–5）· 解剖与构建 Harness**：Agent 全景与 Harness 范式之争 → 面向建造者的 LLM 最小集 → 核心循环、工具协议、编辑格式与 MCP → 停止、审批、沙箱与安全攻防 → 上下文工程、Prefix Cache 与成本优化
- **阶段二（单元 6–9）· 知识、记忆、搜索与编排**：RAG / Agentic Search / LLM Wiki → 长期记忆、Skills 与自进化 → 控制流、规划、推理时搜索与多 Agent 编排 → 垂直形态解剖（Coding / Computer Use / Deep Research / 常驻）
- **阶段三（单元 10–11）· 评测科学与 Agentic SWE**：Agent 评估体系、裁判校准与 `pass^k` → Spec 驱动、Agent-Ready 仓库、分层审查与 Software Factory
- **阶段四（单元 12–14）· 算法训练与推理系统**：Agent 数据工程、轨迹 SFT 与自动优化 → RLVR、GRPO 与异步 RL 系统 → LLM 推理服务与 Agent 全栈优化

完整路线、学派分歧、精读论文清单与原版大项目前置门禁见 [curriculum/syllabus.md](curriculum/syllabus.md)。

---

## 常用口令

| 你说 | 老师会做什么 |
|---|---|
| 上课（可带单元号） | 拉取最新进度和最近对话记录，从断点接着带（首次自动建档） |
| 下课 | 更新进度、导出对话、把本单元讲义补成课后版并提交 |
| 看源码 | 直接打开 `materials/harnesses/` 里对应开源框架的真实代码一起读 |
| 读论文 | 按四步套路带读当前单元的核心论文 |
| 做实验 | 进入当前单元的名校原版实验（读要求、写 Spec、实现与验收复盘） |
| 面试拷问 | 针对当前主题出 2–3 道大厂高频面试题并逐层追问 |
| 提示 | 一步步给点拨，不直接给答案 |
| 学过 / 太简单 / 跳过 | 问两道工程深水区确认题，答对就跳过这一关 |
| 没懂 / 换个讲法 | 换个例子、换一个 Harness 对照或画张图重新讲 |
| 原片 / 进度 | 推荐当前单元的原课视频片段，或汇报整体学习进度 |

---

## 目录结构

| 路径 | 说明 |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | 老师带教守则（Claude Code / Antigravity / Cursor / Codex 共用） |
| `progress/student.md` | 你的学习档案与断点进度（首次上课时由老师互动填写） |
| `logs/` | 每个会话导出的师生对话原文，用于跨会话/跨端接力 |
| `work/` | 你的研习笔记、单元实验代码、评测报告与原版大项目 |
| `curriculum/` | 14 单元总表、1817 条知识点覆盖表、原版大项目前置路线与单元教案 |
| `sources/` | 六门名校课的读课笔记索引 |
| `materials/` | 本机资料库（不进 Git）：通过 `tools/materials/` 拉取的课件、五大开源 Harness 源码、名校原版作业 |
| `tools/` | 对话导出、轨迹统计、知识点覆盖校验、教案校验、讲义（含可选飞书同步）工具 |
