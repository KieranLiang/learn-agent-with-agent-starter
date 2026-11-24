import json, os, re, subprocess, sys
ENV = dict(os.environ, LARKSUITE_CLI_NO_UPDATE_NOTIFIER="1", LARKSUITE_CLI_NO_SKILLS_NOTIFIER="1")
doc = sys.argv[1]
r = subprocess.run(["lark-cli","docs","+fetch","--as","user","--doc",doc,"--doc-format","xml","--format","json"], capture_output=True, text=True, env=ENV)
c = json.loads(r.stdout)["data"]["document"]["content"]
print("chars:", len(c))
print("h1:", re.findall(r"<h1[^>]*>(.*?)</h1>", c))
print("whiteboards:", c.count("<whiteboard"), " pre:", c.count("<pre"), " tables:", c.count("<table"), " callouts:", c.count("<callout"))
print("double-escaped:", c.count("&amp;gt;") + c.count("&amp;lt;"))
print("svg leak:", "font-size" in c)
print("手打序号残留:", len(re.findall(r"[①-⑩]", c)))
print("tail:", re.sub(r"<[^>]+>", "", c[-300:]))
