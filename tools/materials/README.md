# 本地资料库拉取说明

六门课的原始课件、五大一线开源 Harness 源码和名校原版作业存在仓库根目录的 `materials/` 里（已在 `.gitignore` 中排除，不进 Git）。

## 一键拉取开源 Harness 与名校原版作业（推荐）

```bash
bash tools/materials/fetch_repos.sh
```

- 浅克隆五大一线开源 Harness（`pi-mono` / `deepseek-harness` / `codex` / `opencode` / `grok-build`）到 `materials/harnesses/`。
- 浅克隆六个公开名校原版作业仓库（CMU HW1–3、CS329Z A1–A2、CS146S W1–6）到 `materials/assignments/`。
- 重复运行会跳过已存在目录；加上 `--pull` 可拉取最新提交。

## 增量拉取六门名校课公开课件

`manifest.tsv` 记录了六门课公开课件的下载地址。在仓库根目录运行（需系统安装 `pdftotext`，macOS 可 `brew install poppler`）：

```bash
bash tools/materials/fetch.sh tools/materials/manifest.tsv materials
python3 tools/materials/to_text.py materials
python3 tools/materials/index.py
```

- `fetch.sh` 自动跳过已下载的非空文件，可随时追加新讲次重复运行。
- `to_text.py` 将 PDF / HTML / Markdown 转为纯文本存入 `materials/<课>/text/`。
- 即使暂不下载原始课件，仓库里的 `sources/` 读课笔记与 `curriculum/coverage.md`（1,817 条知识点）也足够直接开课。

## 目录结构

```text
materials/
  README.md                 本地资料总索引（python3 tools/materials/index.py 生成）
  <课>/raw/                 原始课件（PDF / HTML / Slidev slides.md）
  <课>/text/                纯文本课件
  <课>/subtitles/LNN.txt    可选：本地课程字幕（格式“时间点  文字”）
  harnesses/                五大开源 Harness 源码
  assignments/              六个公开名校原版作业仓库
```
