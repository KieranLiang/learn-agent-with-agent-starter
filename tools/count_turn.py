"""数一数：一次会话（或其中一轮）背后有几次模型调用、几次工具调用、用了多少 token。

单元 1 轨迹解剖、单元 5 上下文与缓存优化时都能用。只读本机的会话记录，不改任何东西。
Claude Code 和 Antigravity 的记录都能读。

用法：
    python3 tools/count_turn.py --list            # 列出本仓库最近的会话
    python3 tools/count_turn.py                   # 本仓库最近的一次会话，整场统计
    python3 tools/count_turn.py <会话id前几位>     # 按会话编号的前几位找
    python3 tools/count_turn.py <会话id> --turn 3 # 只看这次会话的第 3 轮
    python3 tools/count_turn.py 路径.jsonl         # 直接给记录文件

一“轮”指：从学生发一条消息开始，到他发下一条消息之前。
"""
import argparse
import collections
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
ROOT = Path(__file__).resolve().parent.parent
COURSES = {
    "Agent 课": (ROOT.name,),
}

CATEGORY = {
    # Claude Code
    "Read": "读文件", "Write": "写文件", "Edit": "改文件", "Bash": "跑命令",
    "Glob": "找文件", "Grep": "搜内容", "WebFetch": "抓网页", "WebSearch": "搜索",
    "ToolSearch": "查找工具", "Agent": "子 agent", "Skill": "调用 skill",
    # Antigravity
    "read_file": "读文件", "write_file": "写文件", "edit_file": "改文件",
    "run_command": "跑命令", "list_dir": "找文件", "grep_search": "搜内容",
    "read_url": "抓网页", "search_web": "搜索",
}


def category(name):
    if "Browser" in name or "chrome" in name or "browser" in name:
        return "操作浏览器"
    if name.startswith("mcp__ccd"):
        return "计划和会话类"
    if name.startswith("mcp__"):
        return "外部工具（MCP）"
    return CATEGORY.get(name, name)


# ---------- 找会话 ----------

def course_of(text):
    for course, names in COURSES.items():
        if any(n in text for n in names):
            return course
    return None


def all_sessions():
    """[(修改时间, 课程, 平台, 会话编号, 路径)]，最新的在前。"""
    found = []
    for proj in (HOME / ".claude" / "projects").glob("*"):
        course = next((c for c, names in COURSES.items() if proj.name.endswith(names)), None)
        if course:
            for f in proj.glob("*.jsonl"):
                found.append((f.stat().st_mtime, course, "Claude Code", f.stem, f))
    for f in (HOME / ".gemini" / "antigravity" / "brain").glob("*/.system_generated/logs/transcript.jsonl"):
        try:
            head = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        course = course_of(head)
        if course:
            found.append((f.stat().st_mtime, course, "Antigravity", f.parents[2].name, f))
    return sorted(found, reverse=True)


# ---------- 读记录 ----------

def user_text(content):
    if isinstance(content, str):
        text = content
    else:
        text = " ".join(b.get("text", "") for b in content or [] if b.get("type") == "text")
    m = re.search(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", text, flags=re.S)
    if m:
        text = m.group(1)
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    return " ".join(text.split())


def read_claude(path):
    """把 Claude Code 的记录切成轮。每轮：{问, 模型调用 id 集合, 工具列表, usage}"""
    turns, cur = [], None
    for line in path.open(encoding="utf-8", errors="ignore"):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("isMeta") or e.get("sessionId") not in (None, path.stem):
            continue
        msg = e.get("message") or {}
        if e.get("type") == "user":
            content = msg.get("content")
            is_text = isinstance(content, str) or any(b.get("type") == "text" for b in content or [])
            if is_text:
                q = user_text(content)
                if q:
                    cur = {"q": q, "calls": {}, "tools": []}
                    turns.append(cur)
        elif e.get("type") == "assistant" and cur is not None:
            mid = msg.get("id")
            usage = msg.get("usage") or {}
            cur["calls"][mid] = {
                "input": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0),
                "cache": usage.get("cache_read_input_tokens", 0),
                "output": usage.get("output_tokens", 0),
            }
            for b in msg.get("content") or []:
                if b.get("type") == "tool_use":
                    cur["tools"].append(b["name"])
    return turns


def read_antigravity(path):
    turns, cur = [], None
    for line in path.open(encoding="utf-8", errors="ignore"):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = e.get("type")
        if kind == "USER_INPUT":
            cur = {"q": user_text(e.get("content", "")), "calls": {}, "tools": []}
            turns.append(cur)
        elif kind == "PLANNER_RESPONSE" and cur is not None:
            cur["calls"][e.get("step_index")] = {
                "input": e.get("input_tokens", 0),
                "cache": e.get("cache_read_tokens", 0),
                "output": e.get("output_tokens", 0),
            }
            cur["tools"] += [t.get("name", "?") for t in e.get("tool_calls") or []]
    return turns


# ---------- 输出 ----------

def report(title, turns):
    calls = [c for t in turns for c in t["calls"].values()]
    tools = [x for t in turns for x in t["tools"]]
    print(title)
    print(f"学生发了：{len(turns)} 条消息")
    print(f"模型被调用：{len(calls)} 次")
    print(f"工具调用一共：{len(tools)} 次")
    for kind, n in collections.Counter(category(x) for x in tools).most_common():
        print(f"  {kind}：{n}")
    if calls and any(c["input"] or c["cache"] or c["output"] for c in calls):
        fresh = sum(c["input"] for c in calls)
        cache = sum(c["cache"] for c in calls)
        out = sum(c["output"] for c in calls)
        print("token（各次调用加起来）：")
        print(f"  新读入：{fresh:,}　从缓存读：{cache:,}　写出：{out:,}")
        biggest = max(calls, key=lambda c: c["input"] + c["cache"])
        print(f"  单次调用读入最多的一次：{biggest['input'] + biggest['cache']:,}")
    if len(turns) == 1:
        order = []
        for x in turns[0]["tools"]:
            k = category(x)
            if not order or order[-1] != k:
                order.append(k)
        if order:
            print("先后顺序（相邻的同类合并）：")
            print("  " + " → ".join(order))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("target", nargs="?", help="会话编号的前几位，或记录文件路径；不写就用这门课最近的会话")
    p.add_argument("--turn", type=int, help="只看第几轮")
    p.add_argument("--list", action="store_true", help="列出两门课最近的会话")
    args = p.parse_args()

    sessions = all_sessions()
    if args.list:
        for mtime, course, platform, sid, _ in sessions[:20]:
            print(f"{datetime.fromtimestamp(mtime):%Y-%m-%d %H:%M}  {course:8} {platform:12} {sid[:8]}")
        return

    if args.target and Path(args.target).exists():
        path = Path(args.target)
        platform = "Antigravity" if "antigravity" in str(path) else "Claude Code"
        course, sid = "", path.stem
    else:
        pool = [s for s in sessions if s[3].startswith(args.target)] if args.target else \
               [s for s in sessions if s[1] == "Agent 课"]
        if not pool:
            sys.exit("没找到对应的会话记录。用 --list 看看有哪些。")
        _, course, platform, sid, path = pool[0]

    turns = read_antigravity(path) if platform == "Antigravity" else read_claude(path)
    if not turns:
        sys.exit("这份记录里没有学生发的消息。")
    head = f"{course} · {platform} · 会话 {sid[:8]}".strip(" ·")
    if args.turn:
        if not 1 <= args.turn <= len(turns):
            sys.exit(f"这次会话一共 {len(turns)} 轮")
        t = turns[args.turn - 1]
        report(f"{head} · 第 {args.turn} 轮：{t['q'][:50]}……", [t])
    else:
        report(f"{head} · 整场", turns)


if __name__ == "__main__":
    main()
