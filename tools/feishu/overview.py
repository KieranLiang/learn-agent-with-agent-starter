"""飞书总览的源码（14 个大单元实战研习版，可选飞书同步）。

用法（在 tools/feishu/ 目录下）：
    PYTHONPATH=. python3 overview.py
    ./rebuild.sh <YOUR_OVERVIEW_TOKEN> build/overview

单元表、各单元范围、五大开源 Harness、原版大项目门禁和已备单元关卡清单均从 curriculum/syllabus.md 读取，
逐讲对照从 curriculum/knowledge_points.json 读取。改课程先改那两个文件，再重建这里。
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from build import Doc

W = "assets/overview"
OUT = "build/overview"
N = 14
ROOT = Path(__file__).resolve().parents[2]
SYLLABUS = (ROOT / "curriculum" / "syllabus.md").read_text(encoding="utf-8")
POINTS = json.loads((ROOT / "curriculum" / "knowledge_points.json").read_text(encoding="utf-8"))
# 可选：在飞书建好单元讲义后填入 {单元号: 飞书文档 token}
NOTES = {}


def table_rows(section_title: str, ncols: int):
    """读 syllabus.md 里某一节的第一张表，返回去掉表头的行。"""
    body = SYLLABUS.split(section_title, 1)[1]
    rows = []
    for line in body.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == ncols and not set(cells[0]) <= set("-"):
            rows.append(cells)
    return rows[1:]


def stages(unit: int):
    """某个已备单元的关卡表：[[组, 关, 主题], ...]。"""
    return [r for r in table_rows(f"## 单元 {unit}｜", 3) if re.fullmatch(r"\d+\.\d+", r[1])]


def units():
    """[[单元, 主题, 核心知识点与学派分歧, 单元实验], ...]。"""
    scope = dict(re.findall(r"^- 单元 (\d+)：(.+)$", SYLLABUS, flags=re.M))
    rows = table_rows("## 14 个单元的路线", 5)
    return [[n, topic, scope[n], lab] for n, topic, _ref, lab, _status in rows]


COURSES = [
    ("CMU", "CMU 11-768 AI Agents（Daniel Fried、Graham Neubig）",
     "研究生研究课，作业覆盖造 Harness（HW1）、评测框架（HW2）与异步 GRPO 强化学习（HW3 scottyrl）。课程页有前 14 讲录像与字幕。",
     "https://www.cmu-agents.com/"),
    ("329Z", "Stanford CS329Z Engineering AI Agents（Diyi Yang 等）",
     "六门里体系最完整、最像教科书的一门：RAG、工具、设计模式、记忆、多 agent、优化、数据、评估、安全一路排下来；公开两份实战作业（Harness 与 Eval Task）。前 10 讲有录像字幕。",
     "https://cs329z.stanford.edu/"),
    ("Harvard", "Harvard CS2680 Modern AI Systems（Juncheng Yang）",
     "系统课。前半深度剖析 Agent 设计与八大开源 Harness，后半深入 LLM 推理服务（GPU、PagedAttention、投机解码）；Mads 1–5 五连环作业围绕同一系统层层接管优化。",
     "https://cs2680.seas.harvard.edu/"),
    ("146S", "Stanford CS146S The Modern Software Developer（Mihail Eric）",
     "聚焦现代 AI 原生软件工程（抓包、MCP、Skill、Agent-Ready 仓库、代码审查、软件工厂），嘉宾含 Claude Code / Devin / Factory / Replit 一线负责人，公开 6 周完整作业。",
     "https://themodernsoftware.dev/"),
    ("EECS498", "UMich EECS 498 Applied Agentic Software Engineering（Marcus Darden）",
     "教学法最讲究的一门：从结对编程一路讲到工具、停止审批、压缩缓存、记忆、LLM Wiki、Codex App Server 与非代码产物检查，课件源码与 5 个 Lab 全部公开。",
     "https://eecs498-aase.github.io/"),
    ("jyy", "南京大学 生成式软件工程（蒋炎岩）",
     "唯一的中文课，从软件工程本质讲起，整讲剖析 DeepSeek Harness、Agent Native 开发与软件演化，配有 3 个刁钻实验与 B 站全套回放。",
     "https://jyywiki.cn/GSE/2026/"),
]


def lecture_key(lec: str):
    m = re.search(r"(\d+)", lec)
    extra = lec.lower().startswith(("lab", "note", "assign", "feedback", "transcript"))
    return (extra, int(m.group(1)) if m else 0, lec)


def lecture_name(course: str, lec: str, title: str) -> str:
    title = re.sub(r"\s*[（(][^（）()]*[A-Za-z][^（）()]*[）)]\s*$", "", title).strip()
    title = re.sub(r"\s*智能体\s*", " agent ", title).strip().replace("  ", " ")
    if course == "CMU":
        lec = re.sub(r"-.*", "", lec)
    elif course == "Harvard":
        m = re.match(r"(\d+)([ab]?)-", lec)
        lec = f"第 {int(m.group(1))}{m.group(2)} 讲" if m else {
            "note-agent-evaluation": "参考笔记", "note-cost-effective-agents": "参考笔记",
            "note-transformers": "参考笔记", "feedback-assignment": "作业反馈讲",
            "assignment1": "作业 1", "assignments-index": "作业总览"}.get(lec, lec)
    elif course == "jyy":
        m = re.match(r"lect(\d+)", lec)
        lec = f"第 {int(m.group(1))} 讲" if m else lec.replace("lab", "实验 ")
        title = re.sub(r"^实验\s*[（(]\d+[）)]\s*[：:]\s*", "", title)
    elif course == "146S":
        m = re.match(r"W(\d+)-(\d{2})(\d{2})", lec)
        if m:
            lec = f"第 {int(m.group(1))} 周 {int(m.group(2))}/{int(m.group(3))}"
        else:
            m = re.match(r"transcript-(\d+)-(\d+)", lec)
            lec = f"{m.group(1)}/{m.group(2)} 逐字稿"
    return f"{lec} {title}"


def coverage_rows(course: str):
    lectures = defaultdict(list)
    for p in POINTS:
        if p["course"] == course:
            lectures[p["lecture"]].append(p)
    rows = []
    for lec in sorted(lectures, key=lecture_key):
        ps = lectures[lec]
        cnt = Counter(p["unit"] for p in ps)
        main = [u for u, n in cnt.most_common() if n >= 2] or [cnt.most_common(1)[0][0]]
        rest = [u for u, n in cnt.most_common() if u not in main]
        note = f"共 {len(ps)} 个知识点" + (f"，零星几条在单元 {'、'.join(map(str, sorted(rest)))}" if rest else "")
        rows.append([lecture_name(course, lec, ps[0]["title"]), "单元 " + "、".join(map(str, main)), note])
    return rows


d = Doc("Agent 课｜学习总览")

d.goal([
    "这是一门面向未来 **Agent 开发 / Agent 算法工程师**的 1 对 1 实战研习课：用你的 Coding Agent（Antigravity、Claude Code、Cursor、Codex 等）当师兄，带你一关一关把底层机制、学派分歧、开源源码、前沿论文与名校原版实验全部吃透。",
    f"**课程分 {N} 个大单元、4 个阶段。** 六门 2026 秋名校课盘点出的 1817 个知识点全部归拢保留、一样不砍；重合内容合并去重，但不同课程/老师有观点分歧的一律明确标出谁怎么看。",
    "**主标本是五大一线开源 Harness 源码**（Pi、DeepSeek Harness、Codex CLI、OpenCode V2、Grok Build）；实验与大项目直接对接 Harvard Mads、CMU HW1–3、CS329Z A1–A2、CS146S、EECS498 与 jyy 原版作业。",
], title="这门课是什么")

# 怎么上课
d.h(1, "怎么上课")
d.h(2, "三步开始")
d.ol([
    "克隆本仓库并在本地用 Antigravity、Claude Code / Claude Desktop、Cursor 或 Codex 打开目录；建议跑一遍 `bash tools/materials/fetch_repos.sh` 拉取五大开源 Harness 和名校原版作业。",
    "说“上课”。首次上课老师会先花 2 分钟建档，之后每次自动拉取最新进度和上次对话记录，从断点接着带。",
    "跟着老师一关一关走。想结束时说“下课”，老师会记录笔记、导出对话并把当天上过的关补进讲义。",
])
d.p("每个新单元第一次上课时，老师先发本单元课前讲义并过一遍地图（核心问题、观点分歧、看的开源框架、精读论文、单元实验）。不要求提前预习。")

d.h(2, "每一关怎么学（五件套弹性组合）")
d.p("Agent 不是原子语法，每个单元只拆成 **4–6 个高密度主题关**，按这关的性质组合五种真实研发动作：")
d.ul([
    "**机制与观点交锋**：讲透底层原理与工程权衡，把不同名校老师的观点分歧亮出来（谁主张薄 Harness、谁主张厚底座、谁力挺文件系统 Wiki 胜过向量 RAG）。",
    "**开源 Harness 源码拆解**：直接翻本机 `materials/harnesses/` 里 Pi、`dsh`、Codex CLI、OpenCode V2、Grok Build 的真实代码，横向对比同一零件的五种写法。",
    "**前沿论文精读**：每 1–2 个单元带读 1 篇核心论文（约 20 分钟/篇）：痛点 → 核心方法与关键图 → 消融表 → 2026 年视角挑刺 → 沉淀面试评价。",
    "**名校原版实验与大项目**：肯定写代码，但不搞古法手撕语法——用现代 Agentic 工作流完成（你写 Spec、定架构、调 Agent 写实现、做 Review、跑 Benchmark、析 Trace、写复盘）。",
    "**真实职场故障与面试拷问**：每单元收尾用 2–3 道大厂 Agent 开发/算法岗高频面试题逐层追问，练到能脱口讲透。",
])

d.h(2, "上课时可以说的话")
d.table(["你说", "老师会"], [
    ["上课（可带单元号）", "拉取进度与最近对话，从断点接着带"],
    ["下课 / 同步飞书", "记笔记、更新进度、把今天上过的关补成飞书课后版并推送"],
    ["看源码", "直接打开五大开源 Harness 对应模块的真实源码一起拆"],
    ["读论文", "按四步套路带读本单元的核心论文并做 2026 视角挑刺"],
    ["做实验", "进入本单元的名校原版实验（读原版要求、写 Spec、实现与复盘）"],
    ["面试拷问", "出 2–3 道大厂高频系统设计 / 算法 / 排障题并逐层追问"],
    ["提示", "给一点方向提示，不直接剧透答案"],
    ["学过 / 太简单 / 跳过", "问两道工程深水区确认题，答对就过关"],
    ["没懂 / 换个讲法", "换例子、换另一个 Harness 对照或画张图重讲"],
    ["原片 / 进度", "给当前单元的原片推荐，或报告当前进度与距离目标节点的节奏"],
], widths=[200, 590])

# 起点与终点
d.h(1, "起点与终点")
d.h(2, "适合谁")
d.table(["方面", "建议基线", "这门课怎么衔接"], [
    ["AI 工具体验", "日常用过 Antigravity / Claude Code / Cursor / Codex 等编程 Agent", "跳过泛泛科普，直接掀开底层机制、开源源码架构、论文与面试深水区"],
    ["编程基础", "会基础 Python 与 Git（不追求古法手撕语法）", "单元 1–2 零代码门槛；单元 3 起用现代 Agentic 工作流做真实名校代码实验"],
    ["算法与系统", "尚未系统打通 LLM 原理、SFT/RLVR/GRPO 或推理服务", "单元 2 补最小集，阶段四（单元 12–14）系统啃下数据/SFT、异步 GRPO 与推理服务"],
], widths=[110, 330, 350])

d.h(2, f"学完 {N} 个单元你能做到")
d.ul([
    "拿到任何一线 Agent Harness（Pi、`dsh`、Codex CLI、OpenCode V2、Grok Build、Claude Code），能直接读懂其核心源码、画出架构图并说清每一处工程权衡",
    "独立设计并落地工业级 Agent 系统：选控制流（Workflow / 单 Agent / 多 Agent）、定工具与编辑协议、建沙箱与抗注入防线、优化上下文与 Prefix Cache 账单、接入检索与长期记忆",
    "用可信方法做评测与把关：设计防泄漏 Benchmark、校准 LLM/Agent Judge、区分 `pass@k` 与 `pass^k`、改造 Agent-Ready 代码库并搭起分层审查闭环",
    "吃透 Agent 算法与推理系统核心：讲清轨迹 SFT、可验证奖励 RLVR、同步/异步 GRPO 与 Reward Hacking，理解 Prefill/Decode Roofline、PagedAttention、Prefix Caching 与投机解码",
    "手里握有 2–3 个对标海外名校原版标准的硬核工程/算法大项目（如 Harvard Mads 1–3、CMU HW1–3、CS329Z A1–A2），并具备自主精读前沿 Agent 论文和从容应对大厂技术面试的能力",
])

# 主标本库
d.h(1, "主标本库：五大一线开源 Harness")
d.p("以下五个代表不同架构哲学的开源框架已浅克隆在本机 `materials/harnesses/`（不进 Git），备课和上课时直接对照真实源码：")
d.table(["开源 Harness", "仓库与语言", "架构范式", "核心解剖点"],
        table_rows("## 主标本库：五大一线开源 Harness 源码", 4),
        widths=[130, 180, 150, 330])

# 路线图与单元表
d.h(1, f"{N} 个大单元的路线图")
d.svg(f"{W}/roadmap.svg")
d.table(["单元", "主题", "核心知识点与学派分歧", "单元实验（名校原版）"], units(), widths=[55, 145, 390, 200])
d.p("每个单元设 4–6 个高密度主题关，不按固定天数排课，通常 1.5–2 个月可完整学完 14 个单元及核心大项目。")

# 名校原版大项目与前置门禁
d.h(1, "名校原版大项目路线与前置知识门禁")
d.p("大项目直接对标海外名校原版课程的公开作业仓库（已落盘在本机 `materials/assignments/` 与各课目录下），方便对照原版评分标准和优秀公开解法。每项大项目均锁定前置单元——**做之前一定先把所需知识学透**：")
d.table(["阶段节点", "原版大项目", "本地位置", "必须先学完", "原版核心验收标准"],
        table_rows("## 名校原版大项目路线与前置知识门禁", 5),
        widths=[115, 165, 130, 120, 260])

# 已备好课的单元
d.h(1, "已备好课的单元：关卡清单")
d.p("下面是已经按新体系备好课的单元。后续单元在上到前一个单元时备课，关卡清单会追加到这里。")
d.h(2, "单元 1｜Agent 全景与 Harness 范式之争")
d.table(["组", "关", "主题"], stages(1), widths=[170, 70, 550])
d.ul([
    "**单元实验（必做）**：Harvard Mads-Lens + CS146S Week 1 融合版——抓包/解析真实 Coding Agent 会话轨迹，用 Agent 搭一台轻量轨迹透视器，并输出落到具体 step 编号的三点工程观测报告（`work/unit01/trace-lens/`）。",
])

# 第二条主线
d.h(1, "第二条主线：和 agent 一起干活的工程习惯")
d.p("每个单元配套一条来自一线实战与 Harvard 全班会话日志统计（“用 agent 的十个坑”）的工程纪律，融入日常研发与实验中：")
d.table(["单元", "习惯", "出处"], [
    ["1", "你能解释它，它才是你的；先按动作影响半径定自主级别", "EECS498 L01/L05、CMU L01"],
    ["2", "不盲信模型断言，要证据并亲手核实一个底层案例", "Harvard 作业反馈讲、CMU L22"],
    ["3", "看轨迹与原始报文下结论；出错贴完整报错让它诊断，不发泄情绪", "Harvard 作业 1、CS146S W1"],
    ["4", "先提交再放手；禁掉破坏性命令；密钥放环境变量绝不进 Prompt", "Harvard 作业反馈讲、329Z L17"],
    ["5", "一个任务一个新会话，改一处测一次对比基线，把缓存未命中当 Bug 看", "Harvard 作业反馈讲、146S W3"],
    ["6", "要求给出处；资料冲突时不静默覆盖，标明来源与新鲜度", "329Z L03、EECS498 L17"],
    ["7", "把反复纠正沉淀成规矩或 Skill，但绝不把局部批评泛化成全局禁令", "jyy 实验 3、CMU L04"],
    ["8", "同步规划、异步执行；选完方案清空上下文；并行会话各占独立 worktree", "CS146S W2/W9、Harvard 反馈讲"],
    ["9", "先把可验证的任务交给 agent，再逐步向开放长程场景放权", "CS146S W5（Eno Reyes）"],
    ["10", "一次有噪声的运行不算结论，多跑算 pass@k/pass^k；私有基准胜过公开刷榜", "Harvard 反馈讲、CS146S W9"],
    ["11", "用技术语言写 Spec；让环境与 CI 把住底线；没审过的代码绝不交付", "jyy 第 8/13 讲、CMU L19"],
    ["12", "评测集要持续攒，别指望一次提示微调一劳永逸", "jyy 实验 3"],
    ["13", "奖励怎么写，agent 就往哪钻空子；先盯 Reward Hacking 再看涨点", "329Z L17、CMU L13"],
    ["14", "延迟与吞吐抢同一份显存/算力余量，先定 SLO 再调服务与上下文策略", "Harvard 第 12 讲"],
], widths=[55, 495, 240])

# 覆盖对照
d.h(1, "名校公开课覆盖对照（1817 条知识点零遗漏）")
d.p("下面逐门课、逐讲列出：每一讲的知识点归拢到新 14 单元的哪个位置。逐条清单在仓库 `curriculum/coverage.md`，备课时用 `python3 tools/coverage.py --unit N` 逐一核对。")
for key, name, intro, url in COURSES:
    d.h(2, name)
    d.p(f"{intro} 课程网址：{url}")
    d.table(["讲次", "本课", "说明"], coverage_rows(key), widths=[400, 140, 250])

d.h(2, "还没放课件的讲次（待放出后补充）")
d.p("六门课都在 2026 秋季持续更新，下面已排期但尚未放出课件的讲次，放出后照样盘点补入对应单元：")
d.table(["课", "讲次", "预定去处"], [
    ["CMU", "L16 Observability and Monitoring（Eric Wallace）", "单元 4"],
    ["CMU", "L23 Lessons in Building a Coding Agent（Sasha Rush）", "单元 8、9"],
    ["329Z", "L14 Andrew Ng 访谈", "单元 11"],
    ["329Z", "L16 嘉宾讲座：SWE-bench", "单元 9、10"],
    ["329Z", "L18 Coding & Software Agents、L19 Personal Agents", "单元 9、11"],
    ["Harvard", "学生讲：agent 安全与自我演化的 harness", "单元 4、8"],
    ["Harvard", "GPU 编程（续）、KV cache 优化、剪枝与量化、Efficient agentic systems", "单元 14、5"],
    ["146S", "第 7 周 安全（嘉宾 Isaac Evans）", "单元 4"],
    ["146S", "第 10 周 AI 原生团队；软件品味和人还剩什么", "单元 5、11"],
    ["146S", "Boris Cherny、Silas Alberti、Rajesh Bhatia、Michele Catasta 嘉宾讲座", "有课件再定"],
    ["498", "L21 以后", "有课件再定"],
], widths=[90, 520, 180])

# 原片
d.h(1, "想看原片的话")
d.p("不要求看。每个单元最多推荐一段，有字幕的讲次（CMU 前 14 讲、CS329Z 前 10 讲、jyy 前 14 讲）均已存好本地时间戳字幕，可按时间点直达重点。")
d.table(["单元", "推荐", "看哪一段"], [r for r in table_rows("### 原片", 3)], widths=[60, 280, 450])
d.p("jyy 的 B 站回放合集：https://space.bilibili.com/202224425/lists?sid=8942017")

# 完成标准与进度打卡
d.h(1, "完成标准与进度打卡")
d.ul([
    "本单元 4–6 关全部过关（含源码拆解、观点对照、核心论文精读与单元面试拷问）",
    "单元实验跑通验收，代码、Spec 或复盘报告落盘进 `work/unitXX/`",
    "你的关键判断、论文挑刺与面试复盘记进 `work/unitXX/notes.md`，飞书讲义已补成课后版",
])
d.h(2, "14 单元进度打卡")
d.checkbox([f"单元 {i}" for i in range(1, N + 1)])

# 讲义索引
d.h(1, "讲义索引")
if NOTES:
    d.raw("<ul>" + "".join(f'<li>单元 {n}：<cite type="doc" doc-id="{tok}"/></li>' for n, tok in sorted(NOTES.items())) + "</ul>")
else:
    d.p("本地讲义源码位于 `tools/feishu/notes/unitXX.md`；如启用飞书同步，将各单元文档 token 填入 `overview.py` 的 `NOTES` 字典后重建即可。")

d.write(f"{OUT}/draft.xml")
print("blocks:", len(d.parts))
