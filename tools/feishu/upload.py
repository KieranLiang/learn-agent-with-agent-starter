"""Append a Doc's parts (minus <title>) to an existing Feishu doc in chunks."""
import json, os, subprocess, sys

ENV = dict(os.environ, LARKSUITE_CLI_NO_UPDATE_NOTIFIER="1", LARKSUITE_CLI_NO_SKILLS_NOTIFIER="1")
doc, parts_file = sys.argv[1], sys.argv[2]
work = os.path.dirname(parts_file)
parts = [p for p in json.load(open(parts_file)) if not p.startswith("<title>")]

chunks, cur, size = [], [], 0
for p in parts:
    if cur and (size + len(p) > 5000 or p.startswith("<whiteboard") or p.startswith("<h1")):
        chunks.append(cur); cur, size = [], 0
    cur.append(p); size += len(p)
if cur: chunks.append(cur)

for i, ch in enumerate(chunks):
    path = f"{work}/chunk_{i:02d}.xml"
    open(path, "w").write("\n".join(ch))
    r = subprocess.run(["lark-cli", "docs", "+update", "--as", "user", "--doc", doc, "--command", "append",
                        "--doc-format", "xml", "--content", f"@./{path}", "--format", "json"],
                       capture_output=True, text=True, env=ENV)
    try:
        d = json.loads(r.stdout)
    except Exception:
        print("BAD OUTPUT", i, r.stdout[:500], r.stderr[:500]); sys.exit(1)
    warns = (d.get("data") or {}).get("warnings") or []
    if not d.get("ok") or warns:
        print("chunk", i, "ok=", d.get("ok"), "warnings=", warns, "error=", d.get("error"))
        if not d.get("ok"): sys.exit(1)
print(f"appended {len(chunks)} chunks, {len(parts)} blocks")
