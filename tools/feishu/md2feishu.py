"""把讲义的 Markdown 源文件转成飞书文档的 XML，交给 rebuild.sh / upload.py 上传（可选功能）。

Agent 课的讲义写成 Markdown（tools/feishu/notes/unitXX.md），本地可直接阅读，
启用飞书同步时再通过本脚本转换上传。

用法（在 tools/feishu/ 目录下）：
    python3 md2feishu.py notes/unit01.md build/unit01
    ./rebuild.sh <文档 token> build/unit01

支持的写法：
    # 标题            第一行是文档标题，后面再出现就是一级标题
    ## / ###          二、三级标题（不自动编号，关卡名自己带编号）
    普通段落           连续几行算一段
    - 列表 / 1. 列表
    ```lang ... ```   代码块，不写语言就当纯文本
    | 表格 |           第二行是分隔线
    > 💡 **标题**      引用块变成飞书的高亮块；第一个字是表情就用它，没有就用 💡
    > 内容
    ---               分隔线
"""
import re
import sys

from build import Doc

COLORS = {"📌": "orange", "💡": "yellow", "✍️": "green", "🎓": "blue", "🎯": "blue",
          "⚠️": "orange", "🤔": "yellow", "🧠": "purple", "🤖": "green"}
EMOJI = re.compile(r"^(📌|💡|✍️|🎓|🎯|⚠️|🤔|🧠|🤖)\s*")


def join(lines):
    """把一段里的几行接起来。中文之间不加空格，英文之间加一个。"""
    out = ""
    for ln in lines:
        ln = ln.strip()
        if out and re.search(r"[A-Za-z0-9`]$", out) and re.match(r"[A-Za-z0-9`]", ln):
            out += " "
        out += ln
    return out


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def list_items(lines, ordered):
    items, pat = [], (r"^\s*\d+\.\s+" if ordered else r"^\s*[-*]\s+")
    for ln in lines:
        if re.match(pat, ln):
            items.append(re.sub(pat, "", ln).strip())
        elif items:
            items[-1] += ln.strip()
    return items


def convert(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or not lines[i].startswith("# "):
        sys.exit("第一行必须是“# 文档标题”")
    d = Doc(lines[i][2:].strip())
    i += 1
    para = []

    def flush():
        if para:
            d.p(join(para))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush()
            lang = s[3:].strip() or "text"
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            d.code("\n".join(lines[i + 1:j]), lang=lang)
            i = j + 1; continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush()
            d.h(len(m.group(1)), m.group(2).strip(), seq=False)
            i += 1; continue
        if s == "---":
            flush(); d.hr(); i += 1; continue
        if s.startswith("|"):
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            rows = [split_row(r) for r in block if not re.match(r"^\|?\s*:?-{2,}", r.strip())]
            d.table(rows[0], rows[1:])
            continue
        if s.startswith(">"):
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            emoji = "💡"
            m = EMOJI.match(block[0])
            if m:
                emoji = m.group(1)
                block[0] = block[0][m.end():]
            title = None
            mt = re.match(r"^\*\*(.+?)\*\*\s*$", block[0].strip())
            if mt:
                title = mt.group(1)
                block = block[1:]
            content, buf = [], []
            k = 0
            while k < len(block):
                b = block[k]
                if re.match(r"^\s*[-*]\s+", b):
                    if buf:
                        content.append(join(buf)); buf = []
                    lst = []
                    while k < len(block) and (re.match(r"^\s*[-*]\s+", block[k]) or (block[k].startswith("  ") and lst)):
                        lst.append(block[k]); k += 1
                    content.append(list_items(lst, False))
                    continue
                if not b.strip():
                    if buf:
                        content.append(join(buf)); buf = []
                else:
                    buf.append(b)
                k += 1
            if buf:
                content.append(join(buf))
            d.callout(emoji, COLORS.get(emoji, "yellow"), content, title)
            continue
        for ordered, pat in ((False, r"^[-*]\s+"), (True, r"^\d+\.\s+")):
            if re.match(pat, s):
                flush()
                block = []
                while i < len(lines) and (re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or
                                          (lines[i].startswith("  ") and lines[i].strip() and block)):
                    block.append(lines[i]); i += 1
                items = list_items(block, ordered)
                (d.ol if ordered else d.ul)(items)
                break
        else:
            para.append(ln); i += 1
    flush()
    return d


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, outdir = sys.argv[1], sys.argv[2].rstrip("/")
    doc = convert(open(src, encoding="utf-8").read())
    doc.write(f"{outdir}/draft.xml")
    print(f"{src} → {outdir}/draft.xml，{len(doc.parts)} 块")
