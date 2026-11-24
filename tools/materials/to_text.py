"""把 materials/<课>/raw/ 里的课件转成纯文字，放到 materials/<课>/text/。只读下载来的文件，不执行。"""
import html, re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])

def html2text(t):
    t = re.sub(r'<(script|style|svg|nav|footer)\b.*?</\1>', '', t, flags=re.S | re.I)
    t = re.sub(r'<(h[1-6])[^>]*>', lambda m: '\n\n' + '#' * int(m.group(1)[1]) + ' ', t, flags=re.I)
    t = re.sub(r'<li[^>]*>', '\n- ', t, flags=re.I)
    t = re.sub(r'<(br|/p|/div|/tr|/pre|/blockquote|/h[1-6])[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()

n = 0
for course in sorted(p for p in root.iterdir() if p.is_dir()):
    raw, out = course / 'raw', course / 'text'
    if not raw.exists():
        continue
    for src in sorted(raw.rglob('*')):
        if not src.is_file():
            continue
        rel = src.relative_to(raw)
        dst = (out / rel).with_suffix('.txt')
        dst.parent.mkdir(parents=True, exist_ok=True)
        ext = src.suffix.lower()
        if ext == '.pdf':
            if src.with_suffix('.txt').exists():   # CS146S 同时有 txt 导出，用那份
                continue
            r = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(src), '-'], capture_output=True)
            pages = r.stdout.decode('utf-8', 'ignore').split('\f')
            text = '\n'.join(f'=== 第 {i+1} 页 ===\n{p.strip()}' for i, p in enumerate(pages) if p.strip())
        elif ext == '.html':
            text = html2text(src.read_text(encoding='utf-8', errors='ignore'))
        else:
            text = src.read_text(encoding='utf-8', errors='ignore')
        dst.write_text(text, encoding='utf-8')
        n += 1
print('转换了', n, '个文件')
