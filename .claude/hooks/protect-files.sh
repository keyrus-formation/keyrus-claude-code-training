#!/bin/bash
# PreToolUse (Edit|Write) : interdit toute modification des secrets et des données brutes.
# Code de sortie 2 = l'action est bloquée et le message stderr est renvoyé à Claude.
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
FILE_PATH="${FILE_PATH//\\//}"

PROTECTED_PATTERNS=(".env" "data/raw/" ".git/" "profiles.yml")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Bloqué par la politique projet : $FILE_PATH correspond au motif protégé '$pattern'." >&2
    echo "Les données brutes et les secrets ne se modifient pas depuis Claude Code." >&2
    exit 2
  fi
done
exit 0
