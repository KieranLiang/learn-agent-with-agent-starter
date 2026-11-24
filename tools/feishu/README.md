# 讲义与可选飞书同步工具

每个单元的讲义源码都是纯 Markdown，放在 `tools/feishu/notes/unitXX.md`。

**默认无需配置飞书**：直接用编辑器或 GitHub 读本地 Markdown 讲义即可，下课时老师会自动把当天上过的关补成课后版。

如果你习惯用飞书看讲义并安装了 `lark-cli`，可以按下面步骤启用可选的飞书同步（所有命令在 `tools/feishu/` 目录下执行）：

## 1. 首次初始化（填写你自己的飞书 Token）

1. 先登录 `lark-cli`（`lark-cli auth login`），在飞书云空间新建一个课程文件夹，记下文件夹 token `<YOUR_FOLDER_TOKEN>`。
2. 新建一篇空白总览文档与单元 1 讲义文档：

```bash
lark-cli docs +create --as user --parent-token <YOUR_FOLDER_TOKEN> \
  --title "Agent 课｜学习总览" --content "<p></p>" --format json

lark-cli docs +create --as user --parent-token <YOUR_FOLDER_TOKEN> \
  --title "单元 1｜Agent 全景与 Harness 范式之争" --content "<p></p>" --format json
```

3. 把拿到的单元 1 文档 token 填进 `overview.py` 里的 `NOTES` 字典（和 `progress/student.md`），再运行：

```bash
PYTHONPATH=. python3 overview.py
./rebuild.sh <YOUR_OVERVIEW_TOKEN> build/overview

python3 md2feishu.py notes/unit01.md build/unit01
./rebuild.sh <YOUR_UNIT01_TOKEN> build/unit01
```

## 2. 讲义写法（课前版与课后版）

- **课前版**：备课时写好，交代本单元核心问题、关卡地图、观点分歧、开源 Harness 对比、精读论文与单元实验，但不剧透互动题与面试题答案。
- **课后版**：下课时由老师补入当天上过的关——源码/实验结论、你的原话判断与复盘（放进 `> ✍️ **我的回答与复盘**`）、卡住的地方、追问过的问题（放进 `> 📌 **我问过**`）。

## 规矩

- **不要用 `docs +create` 传大文档**：先建空文档，再用 `rebuild.sh` 分块上传并自动调用 `verify.py` 校验。
- **不要手打序号**（例如 ①②③），并列要点用列表。
- `rebuild.sh` 会清空整篇文档，重建前确认没有仅存在飞书端未合并的手工批注。
