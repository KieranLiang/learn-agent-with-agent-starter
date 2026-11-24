"""Tiny builder: write lecture content in Python, emit Feishu doc XML with correct escaping.

Inline markup in text: `code` -> <code>, **bold** -> <b>.
"""
import html
import re
import textwrap


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def inline(s: str) -> str:
    codes = []

    def stash_code(m: re.Match) -> str:
        idx = len(codes)
        codes.append(f"<code>{esc(m.group(1))}</code>")
        return f"\x00CODE{idx}\x00"

    masked = re.sub(r"`([^`]+)`", stash_code, s)
    t = esc(masked)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    for idx, tag in enumerate(codes):
        t = t.replace(f"\x00CODE{idx}\x00", tag)
    return t


class Doc:
    def __init__(self, title: str):
        self.parts = [f"<title>{esc(title)}</title>"]

    def h(self, level: int, text: str, seq=True):
        s = ' seq="auto"' if seq else ""
        self.parts.append(f"<h{level}{s}>{inline(text)}</h{level}>")

    def p(self, text: str):
        self.parts.append(f"<p>{inline(text)}</p>")

    def code(self, code: str, lang: str = "python", caption: str | None = None):
        code = textwrap.dedent(code).strip("\n")
        cap = f' caption="{esc(caption)}"' if caption else ""
        self.parts.append(f'<pre lang="{lang}"{cap}><code>{esc(code)}</code></pre>')

    def ul(self, items):
        self.parts.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")

    def ol(self, items):
        self.parts.append("<ol>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ol>")

    def callout(self, emoji: str, color: str, lines, title: str | None = None):
        body = ""
        if title:
            body += f"<p><b>{esc(title)}</b></p>"
        for ln in lines:
            if isinstance(ln, list):
                body += "<ul>" + "".join(f"<li>{inline(i)}</li>" for i in ln) + "</ul>"
            else:
                body += f"<p>{inline(ln)}</p>"
        self.parts.append(
            f'<callout emoji="{emoji}" background-color="light-{color}" border-color="{color}">{body}</callout>'
        )

    # semantic callouts
    def knowhow(self, lines, title="老手 Know-how"):
        self.callout("🧠", "purple", lines, title)

    def warn(self, lines, title="小心踩坑"):
        self.callout("⚠️", "orange", lines, title)

    def guess(self, lines, title="先猜后跑"):
        self.callout("🤔", "yellow", lines, title)

    def ai(self, lines, title="AI / Agent 场景"):
        self.callout("🤖", "green", lines, title)

    def school(self, lines, title):
        self.callout("🎓", "blue", lines, title)

    def goal(self, lines, title=None):
        self.callout("🎯", "blue", lines, title)

    # Agent 课的课后笔记用这四个
    def take(self, text):
        """这一关带走的那一句话。"""
        self.callout("💡", "yellow", [text], "带走")

    def mine(self, lines, title="我的回答"):
        """学生在“判”和“设”里自己的回答。"""
        self.callout("✍️", "green", lines, title)

    def ask(self, lines, title="我问过"):
        """学生上课时问过的问题和当时的回答。"""
        self.callout("📌", "orange", lines, title)

    def src(self, text):
        """出处：哪门课的哪一讲。"""
        self.callout("🎓", "blue", [text], "出处")

    def table(self, headers, rows, widths=None):
        x = "<table>"
        if widths:
            x += "<colgroup>" + "".join(f'<col width="{w}"/>' for w in widths) + "</colgroup>"
        x += "<thead><tr>" + "".join(
            f'<th background-color="light-gray"><p>{inline(h)}</p></th>' for h in headers
        ) + "</tr></thead><tbody>"
        for r in rows:
            x += "<tr>" + "".join(f"<td><p>{inline(str(c))}</p></td>" for c in r) + "</tr>"
        x += "</tbody></table>"
        self.parts.append(x)

    def grid_code(self, left_title, left_code, right_title, right_code, lang="python", lang_left=None):
        def col(t, c, lg):
            c = textwrap.dedent(c).strip("\n")
            return (
                f'<column width-ratio="0.5"><p><b>{esc(t)}</b></p>'
                f'<pre lang="{lg}"><code>{esc(c)}</code></pre></column>'
            )
        self.parts.append(
            "<grid>" + col(left_title, left_code, lang_left or lang) + col(right_title, right_code, lang) + "</grid>"
        )

    def svg(self, path: str):
        self.parts.append(f'<whiteboard type="svg" path="@./{path}"></whiteboard>')

    def checkbox(self, items):
        for i in items:
            self.parts.append(f'<checkbox done="false">{inline(i)}</checkbox>')

    def hr(self):
        self.parts.append("<hr/>")

    def raw(self, xml: str):
        self.parts.append(xml)

    def write(self, path: str):
        import json
        import os
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.parts) + "\n")
        with open(path.replace(".xml", ".parts.json"), "w", encoding="utf-8") as f:
            json.dump(self.parts, f, ensure_ascii=False)
