#!/usr/bin/env bash
# 一键浅克隆五大一线开源 Harness 源码 + 六个公开名校原版作业仓库到本机 materials/（不进 Git）。
# 用法（在仓库根目录运行）：
#   bash tools/materials/fetch_repos.sh
# 幂等：已存在的目录会自动跳过；想更新最新提交可加 --pull。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PULL=0
if [[ "${1:-}" == "--pull" ]]; then
  PULL=1
fi

clone_or_update() {
  local dest="$1"
  local url="$2"
  if [[ -d "$dest/.git" ]]; then
    if [[ "$PULL" -eq 1 ]]; then
      echo "[PULL] $dest"
      GIT_TERMINAL_PROMPT=0 git -C "$dest" pull --ff-only --depth 1 || echo "[WARN] pull 跳过：$dest"
    else
      echo "[SKIP] $dest 已存在"
    fi
    return
  fi
  mkdir -p "$(dirname "$dest")"
  echo "[CLONE] $dest <- $url"
  GIT_TERMINAL_PROMPT=0 git clone --depth 1 --single-branch "$url" "$dest"
}

echo "=== 1/2 拉取五大一线开源 Harness 源码 -> materials/harnesses/ ==="
clone_or_update "$ROOT/materials/harnesses/pi-mono"          "https://github.com/earendil-works/pi.git"
clone_or_update "$ROOT/materials/harnesses/deepseek-harness" "https://github.com/deepseek-ai/deepseek-harness.git"
clone_or_update "$ROOT/materials/harnesses/codex"            "https://github.com/openai/codex.git"
clone_or_update "$ROOT/materials/harnesses/opencode"         "https://github.com/anomalyco/opencode.git"
clone_or_update "$ROOT/materials/harnesses/grok-build"       "https://github.com/xai-org/grok-build.git"

echo "=== 2/2 拉取六个公开名校原版作业仓库 -> materials/assignments/ ==="
clone_or_update "$ROOT/materials/assignments/cmu-hw1"   "https://github.com/cmu-agents/assignment-1.git"
clone_or_update "$ROOT/materials/assignments/cmu-hw2"   "https://github.com/cmu-agents/assignment-2.git"
clone_or_update "$ROOT/materials/assignments/cmu-hw3"   "https://github.com/cmu-agents/assignment-3.git"
clone_or_update "$ROOT/materials/assignments/cs329z-a1" "https://github.com/cs329z/assignment1-harness.git"
clone_or_update "$ROOT/materials/assignments/cs329z-a2" "https://github.com/cs329z/assignment2-evals.git"
clone_or_update "$ROOT/materials/assignments/cs146s"    "https://github.com/mihail911/modern-software-dev-assignments.git"

echo "=== 重新生成本地资料索引 materials/README.md ==="
python3 "$ROOT/tools/materials/index.py" "$ROOT/materials"
echo "完成！"
