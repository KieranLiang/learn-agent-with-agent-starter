"""生成 materials/README.md：六门课课件文字与字幕、五大开源 Harness 源码、名校原版作业仓库。

用法：python3 tools/materials/index.py [materials 目录，默认 materials]
只读 materials/ 里的文件，不执行它们。
"""
import datetime
import re
import sys
from pathlib import Path

COURSES = {
    "cmu-11768": "CMU 11-768 AI Agents",
    "stanford-cs329z": "Stanford CS329Z Engineering AI Agents",
    "harvard-cs2680": "Harvard CS2680 Modern AI Systems",
    "stanford-cs146s": "Stanford CS146S The Modern Software Developer",
    "umich-eecs498": "UMich EECS 498 AASE",
    "nju-jyy-gse": "南大 jyy 生成式软件工程",
}

HARNESSES = [
    ("pi-mono", "https://github.com/earendil-works/pi", "TypeScript（原 `badlogic/pi-mono`，12 packages）"),
    ("deepseek-harness", "https://github.com/deepseek-ai/deepseek-harness", "TypeScript（61 packages）"),
    ("codex", "https://github.com/openai/codex", "Rust（133 crates/dirs）"),
    ("opencode", "https://github.com/anomalyco/opencode", "TypeScript / Bun + Rust CLI（33 packages）"),
    ("grok-build", "https://github.com/xai-org/grok-build", "Rust（102 crates）"),
]

ASSIGNMENTS = [
    ("cmu-hw1", "https://github.com/cmu-agents/assignment-1", "CMU 11-768 HW1: Build an Agent Harness (`chess_app` + `ChessAgent`)"),
    ("cmu-hw2", "https://github.com/cmu-agents/assignment-2", "CMU 11-768 HW2: Evaluating a Data-Visualization Agent (Harbor + Validator)"),
    ("cmu-hw3", "https://github.com/cmu-agents/assignment-3", "CMU 11-768 HW3: `scottyrl` (Sync/Async GRPO & RL Training)"),
    ("cs329z-a1", "https://github.com/cs329z/assignment1-harness", "Stanford CS329Z A1: Building an Agent Harness (Sandbox + Email RAG)"),
    ("cs329z-a2", "https://github.com/cs329z/assignment2-evals", "Stanford CS329Z A2: Building an Evaluation Task (Harbor + `mini-SWE-agent`)"),
    ("cs146s", "https://github.com/mihail911/modern-software-dev-assignments", "Stanford CS146S Week 1–6 Assignments"),
]


def size(p: Path) -> str:
    n = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else p.stat().st_size
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{n / 1e3:.0f} KB"


def text_info(f: Path) -> str:
    t = f.read_text(encoding="utf-8", errors="ignore")
    pages = len(re.findall(r"^=== 第 \d+ 页 ===$", t, flags=re.M))
    return f"{pages} 页" if pages else f"{len(t) // 1000} 千字符"


def subtitle_info(f: Path) -> tuple[str, str, str]:
    lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
    title = lines[0].lstrip("# ").strip() if lines else ""
    url = lines[1].lstrip("# ").strip() if len(lines) > 1 else ""
    stamps = [l.split()[0] for l in lines[3:] if l.strip() and re.match(r"^\d+(:\d+)+", l)]
    return title, url, stamps[-1] if stamps else "?"


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "materials")
    out = [
        "# 课件、字幕、开源 Harness 与原版作业的本地副本",
        "",
        f"由 `python3 tools/materials/index.py` 生成于 {datetime.date.today()}。怎么抓、怎么补，见仓库里的 `tools/materials/README.md`。",
        "",
    ]
    for key, name in COURSES.items():
        d = root / key
        if not d.exists():
            continue
        out += [f"## {name}（`{key}/`，共 {size(d)}）", ""]
        texts = sorted((d / "text").rglob("*.txt")) if (d / "text").exists() else []
        out += [f"课件文字 {len(texts)} 份，在 `{key}/text/`：", ""]
        out += [f"- `{f.relative_to(d / 'text')}`（{text_info(f)}）" for f in texts]
        subs = sorted((d / "subtitles").glob("*.txt")) if (d / "subtitles").exists() else []
        if subs:
            out += ["", f"字幕 {len(subs)} 份，在 `{key}/subtitles/`：", "", "| 文件 | 视频 | 时长 |", "|---|---|---|"]
            for f in subs:
                title, url, last = subtitle_info(f)
                out.append(f"| `{f.name}` | [{title}]({url}) | {last} |")
        out.append("")

    hdir = root / "harnesses"
    if hdir.exists():
        out += [f"## 五大一线开源 Harness 源码（`harnesses/`，共 {size(hdir)}）", "", "| 本地目录 | 官方仓库 | 语言与说明 | 体积 |", "|---|---|---|---|"]
        for name, url, desc in HARNESSES:
            p = hdir / name
            if p.exists():
                out.append(f"| `harnesses/{name}/` | {url} | {desc} | {size(p)} |")
        out.append("")

    adir = root / "assignments"
    if adir.exists():
        out += [f"## 名校原版作业仓库（`assignments/`，共 {size(adir)}）", "", "| 本地目录 | 官方仓库 | 对应课程与主题 | 体积 |", "|---|---|---|---|"]
        for name, url, desc in ASSIGNMENTS:
            p = adir / name
            if p.exists():
                out.append(f"| `assignments/{name}/` | {url} | {desc} | {size(p)} |")
        out.append("")

    (root / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"写好了 {root / 'README.md'}")


if __name__ == "__main__":
    main()
