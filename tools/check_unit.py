"""校验 Agent 课教案的结构。只查能机械判断的东西，内容准确度要老师核实源码与一手资料。

用法：python3 tools/check_unit.py curriculum/unit01.md

检查项：
1. 有“## 单元概览”和“# 单元实验”。
2. 每一关开头都有五个字段：核心主题、覆盖知识点与出处、前置、黑盒、确认题。
3. 每一关都有五个小节，顺序是：机制与观点交锋、源码或论文拆解、互动与实战、面试拷问、常见误区。
4. “源码或论文拆解”里标了标本/来源标记：【真实】【论文】【改编】【示意】之一。
5. “互动与实战”和“面试拷问”里都有“参考”。
6. “常见误区”里至少有一条列表项。
7. 关卡编号连续，并且和 curriculum/syllabus.md 里的清单一致。
"""
import re
import sys
from pathlib import Path

FIELDS = ["核心主题", "覆盖知识点与出处", "前置", "黑盒", "确认题"]
SECTIONS = ["机制与观点交锋", "源码或论文拆解", "互动与实战", "面试拷问", "常见误区"]
MARKS = ["【真实】", "【论文】", "【改编】", "【示意】"]


def split_levels(text: str):
    """返回 [(编号, 标题, 正文)]。"""
    parts = re.split(r"^## 关 (\d+\.\d+)｜(.+)$", text, flags=re.M)
    levels = []
    for i in range(1, len(parts), 3):
        body = parts[i + 2]
        body = re.split(r"^# ", body, maxsplit=1, flags=re.M)[0]
        levels.append((parts[i], parts[i + 1].strip(), body))
    return levels


def split_sections(body: str):
    parts = re.split(r"^### (.+)$", body, flags=re.M)
    head = parts[0]
    secs = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    return head, secs


def check(path: str):
    text = Path(path).read_text(encoding="utf-8")
    errors = []
    levels = split_levels(text)
    if not levels:
        return ["没有找到任何“## 关 N.M｜标题”"], 0

    if "## 单元概览" not in text:
        errors.append("缺少“## 单元概览”")
    if not re.search(r"^# 单元实验", text, flags=re.M):
        errors.append("缺少“# 单元实验”")

    unit = levels[0][0].split(".")[0]
    for idx, (num, title, body) in enumerate(levels, start=1):
        tag = f"关 {num}"
        if num != f"{unit}.{idx}":
            errors.append(f"{tag}：编号不连续，这里应该是 {unit}.{idx}")
        head, secs = split_sections(body)
        for f in FIELDS:
            if f"**{f}**" not in head:
                errors.append(f"{tag}：缺少字段“{f}”")
        names = [n for n, _ in secs]
        if names != SECTIONS:
            errors.append(f"{tag}：小节应为 {SECTIONS}，实际是 {names}")
            continue
        sec = dict(secs)
        if not any(m in sec["源码或论文拆解"] for m in MARKS):
            errors.append(f"{tag}：“源码或论文拆解”里没有来源标记（{'、'.join(MARKS)}）")
        for s in ("互动与实战", "面试拷问"):
            if "参考" not in sec[s]:
                errors.append(f"{tag}：“{s}”里没有参考要点")
        if not re.search(r"^- ", sec["常见误区"], flags=re.M):
            errors.append(f"{tag}：“常见误区”里没有条目")

    syl = Path(path).parent / "syllabus.md"
    if syl.exists():
        listed = re.findall(rf"\|\s*({unit}\.\d+)\s*\|", syl.read_text(encoding="utf-8"))
        mine = [n for n, _, _ in levels]
        if listed != mine:
            errors.append(f"和 syllabus.md 不一致：总表里是 {listed}，教案里是 {mine}")
    else:
        errors.append("找不到同目录下的 syllabus.md")

    return errors, len(levels)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    errors, n = check(sys.argv[1])
    if errors:
        print(f"{sys.argv[1]}：{len(errors)} 个问题")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"{sys.argv[1]}：{n} 关，结构检查全部通过")
