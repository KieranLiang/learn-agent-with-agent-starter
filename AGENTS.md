@[CLAUDE.md](./CLAUDE.md)

## Antigravity / 多端 Agent 补充说明

- 上方 `CLAUDE.md` 是 Antigravity、Claude Code、Cursor、Codex 等所有编程 Agent 共用的唯一带教准则，请严格按其中的说话规矩（“让读者读着不累”）、五件套带教法和上下课流程执行。
- `.claude/output-styles/tutor.md` 写了带教时的师兄沟通口吻和“后台杂事不写旁白”的规矩，非 Claude Code 的 Agent 也照着它说话。
- 本地一手资料库在 `materials/`（不进 Git，运行 `tools/materials/` 下脚本即可拉取）：
  - 六门名校课课件文字：`materials/<course>/`（通过 `tools/materials/fetch.sh` + `to_text.py` 拉取）
  - 五大一线开源 Harness 源码（主标本库）：`materials/harnesses/` 下的 `pi-mono`、`deepseek-harness`、`codex`、`opencode`、`grok-build`（通过 `tools/materials/fetch_repos.sh` 一键浅克隆）。讲到任何架构或实现细节时，只要本地已拉取就直接读真实源码核实，不要凭印象说。
  - 名校原版作业仓库：`materials/assignments/` 下的 `cmu-hw1`、`cmu-hw2`、`cmu-hw3`、`cs329z-a1`、`cs329z-a2`、`cs146s`（同样由 `fetch_repos.sh` 一键拉取）。
- 本机原始会话日志常见位置（`tools/export_chat.py` 和 `tools/count_turn.py` 会自动按当前仓库名匹配）：
  - Antigravity：`~/.gemini/antigravity/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`
  - Claude Code / Claude Desktop：`~/.claude/projects/` 下与当前仓库路径对应的目录里的 `*.jsonl`
- 命令用 `python3` 直接跑；部分名校原版作业（CMU / CS329Z）用 `uv`，按对应作业 README 执行。
