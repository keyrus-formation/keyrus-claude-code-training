#!/bin/bash
# PostToolUse (Edit|Write) : formate et lint automatiquement les fichiers Python modifiés.
# Les problèmes restants sont renvoyés à Claude (exit 2) pour qu'il les corrige.
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[[ "$FILE_PATH" == *.py ]] || exit 0
command -v ruff >/dev/null 2>&1 || exit 0

ruff format --quiet "$FILE_PATH"
if ! OUT=$(ruff check --fix --quiet "$FILE_PATH" 2>&1); then
  echo "ruff a trouvé des problèmes dans $FILE_PATH :" >&2
  echo "$OUT" | head -30 >&2
  exit 2
fi
exit 0
