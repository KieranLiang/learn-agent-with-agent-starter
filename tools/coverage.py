"""六门课的知识点覆盖表：每个知识点分到哪个单元，有没有漏。

数据在 curriculum/knowledge_points.json，每一项是一个知识点：
  id（课/讲/序号）、course、lecture、title（讲题）、kp（知识点）、kind、where（页码或小节）、
  unit（主讲单元，1–14）、also（也会用到它的单元，列表，可以为空）。

用法：
  python3 tools/coverage.py            生成 curriculum/coverage.md
  python3 tools/coverage.py --check    只检查：每个知识点都有单元、每个单元都有知识点
  python3 tools/coverage.py --unit 5   打印单元 5 要覆盖的全部知识点（备课时用）
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "curriculum" / "knowledge_points.json"
OUT = ROOT / "curriculum" / "coverage.md"
N = 14
UNITS = list(range(1, N + 1))
COURSES = {
    "CMU": "CMU 11-768 AI Agents",
    "329Z": "Stanford CS329Z Engineering AI Agents",
    "Harvard": "Harvard CS2680 Modern AI Systems",
    "146S": "Stanford CS146S The Modern Software Developer",
    "EECS498": "UMich EECS 498 AASE",
    "jyy": "南大 jyy 生成式软件工程",
}


def load() -> list[dict]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def check(points: list[dict]) -> list[str]:
    errors = [f"{p['id']} 没有分到单元" for p in points if p.get("unit") not in UNITS]
    used = {p.get("unit") for p in points}
    errors += [f"单元 {u} 一个知识点都没有" for u in UNITS if u not in used]
    ids = Counter(p["id"] for p in points)
    errors += [f"{i} 重复了 {n} 次" for i, n in ids.items() if n > 1]
    return errors


def lecture_sort(lec: str) -> tuple:
    m = re.search(r"(\d+)", lec)
    extra = lec.lower().startswith(("lab", "note", "assign", "feedback", "transcript"))
    return (extra, int(m.group(1)) if m else 0, lec)


def course_sort(p: dict) -> tuple:
    return (list(COURSES).index(p["course"]), lecture_sort(p["lecture"]))


def render(points: list[dict]) -> str:
    by_unit = defaultdict(list)
    for p in points:
        by_unit[p["unit"]].append(p)
    also = Counter(a for p in points for a in p.get("also", []))
    out = [
        "# 六门课的知识点覆盖表",
        "",
        "由 `python3 tools/coverage.py` 从 `curriculum/knowledge_points.json` 生成，不要手改。",
        "",
        f"六门课已经放出的课件逐讲盘点出 {len(points)} 个知识点（2026-11-25），每个都分到了一个主讲单元。"
        "备某个单元时，用 `python3 tools/coverage.py --unit 5` 列出它要覆盖的全部知识点，逐条排进关卡，或者在教案里写明并进了哪一关。",
        "",
        "## 每个单元分到多少",
        "",
        "| 单元 | 主讲 | 也会用到 |",
        "|---|---|---|",
    ]
    out += [f"| 单元 {u} | {len(by_unit[u])} | {also[u]} |" for u in UNITS]
    out += ["", "## 逐讲对照", ""]
    for c, name in COURSES.items():
        lectures = defaultdict(list)
        for p in points:
            if p["course"] == c:
                lectures[p["lecture"]].append(p)
        if not lectures:
            continue
        out += [f"### {name}", "", "| 讲 | 讲题 | 知识点 | 分到的单元 |", "|---|---|---|---|"]
        for lec in sorted(lectures, key=lecture_sort):
            ps = lectures[lec]
            units = Counter(p["unit"] for p in ps)
            spread = "、".join(f"单元 {u}（{n}）" for u, n in units.most_common())
            out.append(f"| {lec} | {ps[0]['title']} | {len(ps)} | {spread} |")
        out.append("")
    out += ["## 逐单元清单", ""]
    for u in UNITS:
        out += [f"### 单元 {u}（{len(by_unit[u])} 个）", ""]
        for p in sorted(by_unit[u], key=course_sort):
            where = f"，{p['where']}" if p.get("where") else ""
            out.append(f"- {p['kp']}（{p['course']} {p['lecture']}{where}）")
        out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--unit", type=int)
    args = ap.parse_args()
    points = load()
    if args.unit:
        for p in sorted(points, key=course_sort):
            if p["unit"] == args.unit or args.unit in p.get("also", []):
                tag = "" if p["unit"] == args.unit else f"  [主讲在单元 {p['unit']}]"
                print(f"- {p['kp']}（{p['course']} {p['lecture']} {p.get('where', '')}）{tag}")
        return
    errors = check(points)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    if args.check:
        print(f"{len(points)} 个知识点都分到了单元，{N} 个单元都有内容")
        return
    OUT.write_text(render(points), encoding="utf-8")
    print(f"写好了 {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
