"""把 Agent 课上课会话的师生对话导出成 Markdown，放进 logs/，让不同 Agent 和设备互相看得到。

每个会话对应一个文件：logs/<开始日期>_<agent>_<会话id前8位>.md。重复运行只会覆盖同一个文件。
只保留学生说的话和老师的回复，工具调用、命令输出、思考过程都去掉。

用法：
    python3 tools/export_chat.py          # 导出当前会话（最近还在写入的那个）
    python3 tools/export_chat.py --all    # 导出本机所有属于本仓库的会话
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
PROJECT_NAMES = (ROOT.name,)


def clean_user_text(text: str) -> str:
    """去掉系统注入的内容，只留学生自己说的话。"""
    m = re.search(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", text, flags=re.S)
    if m:  # Antigravity
        text = m.group(1)
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    text = re.sub(r"<local-command-[a-z]+>.*?</local-command-[a-z]+>", "", text, flags=re.S)
    text = re.sub(r"<command-[a-z]+>.*?</command-[a-z]+>", "", text, flags=re.S)
    text = re.sub(r"<!-- reply \d+ -->", "", text)
    # 学生在终端里敲的命令和输出，转成代码块
    text = re.sub(r"<bash-input>(.*?)</bash-input>", r"```\n$ \1\n```", text, flags=re.S)
    text = re.sub(r"<bash-stdout>(.*?)</bash-stdout>", r"```\n\1\n```", text, flags=re.S)
    text = re.sub(r"<bash-stderr>(.*?)</bash-stderr>", "", text, flags=re.S)
    text = re.sub(r"\[Image: source: [^\]]*\]", "[图片]", text)
    text = re.sub(r"\[Image #?\d*\]", "[图片]", text)
    text = text.strip()
    if text.startswith(("[Usage limit reached", "[Earlier usage-limit", "[Request interrupted")):
        return ""
    return text


def parse_claude(path: Path):
    turns, start = [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") not in ("user", "assistant") or obj.get("isMeta"):
            continue
        # fork 出来的会话会把父会话的记录原样复制一份，那些行的 sessionId 是父会话的，跳过
        if obj.get("sessionId") not in (None, path.stem):
            continue
        start = start or obj.get("timestamp")
        msg = obj.get("message") or {}
        content = msg.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts = []
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif c.get("type") == "image" and msg.get("role") == "user":
                    parts.append("[图片]")
            text = "\n".join(parts)
        else:
            continue
        role = msg.get("role")
        text = clean_user_text(text) if role == "user" else text.strip()
        if text:
            turns.append((role, text))
    return turns, start


def parse_antigravity(path: Path):
    turns, start = [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind, content = obj.get("type"), obj.get("content")
        if not isinstance(content, str) or kind not in ("USER_INPUT", "PLANNER_RESPONSE"):
            continue
        start = start or obj.get("created_at")
        role = "user" if kind == "USER_INPUT" else "assistant"
        text = clean_user_text(content) if role == "user" else content.strip()
        if text:
            turns.append((role, text))
    return turns, start


def merge(turns):
    """连续几条同一个人说的话合成一段。"""
    out = []
    for role, text in turns:
        if out and out[-1][0] == role:
            out[-1] = (role, out[-1][1] + "\n\n" + text)
        else:
            out.append((role, text))
    return out


def find_sessions():
    """返回 [(修改时间, agent, 会话id, 路径)]，最新的在前。同一个会话只留一份。"""
    home = Path.home()
    found = {}
    for proj in (home / ".claude" / "projects").glob("*"):
        # Claude 按工作目录的绝对路径给会话目录命名，非字母数字都换成 -；云端的目录名也以仓库名结尾
        mangled = re.sub(r"[^A-Za-z0-9]", "-", str(ROOT))
        if proj.is_dir() and (proj.name.endswith(PROJECT_NAMES) or proj.name == mangled):
            for f in proj.glob("*.jsonl"):
                key = ("Claude", f.stem)
                if key not in found or f.stat().st_mtime > found[key][0]:
                    found[key] = (f.stat().st_mtime, "Claude", f.stem, f)
    for f in (home / ".gemini" / "antigravity" / "brain").glob("*/.system_generated/logs/transcript.jsonl"):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(name in text for name in PROJECT_NAMES):
            sid = f.parents[2].name
            found[("Antigravity", sid)] = (f.stat().st_mtime, "Antigravity", sid, f)
    return sorted(found.values(), reverse=True)


def export(agent, sid, path, mtime):
    turns, start = parse_claude(path) if agent == "Claude" else parse_antigravity(path)
    turns = merge(turns)
    if not turns:
        return None
    try:
        started = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone()
    except (AttributeError, ValueError):
        started = datetime.fromtimestamp(mtime)
    out = LOG_DIR / f"{started:%Y-%m-%d}_{agent.lower()}_{sid[:8]}.md"
    lines = [
        f"# {agent} 会话 {sid[:8]}",
        "",
        f"开始于 {started:%Y-%m-%d %H:%M}，最后更新 {datetime.fromtimestamp(mtime):%Y-%m-%d %H:%M}。"
        "由 `tools/export_chat.py` 导出，只含师生对话。",
        "",
    ]
    for role, text in turns:
        lines += ["---", "", "**学生：**" if role == "user" else f"**老师（{agent}）：**", "", text, ""]
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="导出本机所有属于这门课的会话")
    args = parser.parse_args()

    sessions = find_sessions()
    if not sessions:
        print("没找到本机的会话记录，跳过导出。")
        return
    LOG_DIR.mkdir(exist_ok=True)
    for mtime, agent, sid, path in sessions if args.all else sessions[:1]:
        out = export(agent, sid, path, mtime)
        if out:
            print(f"已导出 {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
