#!/bin/bash
# usage: fetch.sh <manifest> <materials-root>
# 只下载，不执行任何下载来的内容。已存在且非空的文件跳过。
while IFS=$'\t' read -r course name url; do
  d="$2/$course/raw"; mkdir -p "$d"
  out="$d/$name"
  if [ -s "$out" ]; then echo "SKIP $course/$name"; continue; fi
  code=$(curl -sL -A "Mozilla/5.0" --max-time 180 -o "$out" -w '%{http_code}' "$url")
  size=$(wc -c < "$out" | tr -d ' ')
  kind=$(file -b "$out" | cut -c1-30)
  echo "$code $size $course/$name [$kind]"
done < "$1"
