#!/bin/bash
# usage: rebuild.sh <doc_token> <draft_folder>
set -e
export LARKSUITE_CLI_NO_UPDATE_NOTIFIER=1 LARKSUITE_CLI_NO_SKILLS_NOTIFIER=1
DOC=$1; F=$2
lark-cli docs +update --as user --doc $DOC --command block_delete --start-block-id 0 --end-block-id -1 --format json | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok'], d"
python3 upload.py $DOC $F/draft.parts.json
TITLE=$(python3 -c "import json; print(json.load(open('$F/draft.parts.json'))[0])")
lark-cli docs +update --as user --doc $DOC --command block_insert_after --block-id 0 --doc-format xml --content "$TITLE" --format json | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['ok'], d"
python3 verify.py $DOC
