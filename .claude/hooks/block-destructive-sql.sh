#!/bin/bash
# PreToolUse (Bash) : bloque les commandes destructrices (rm -rf, DROP/TRUNCATE/DELETE
# sans WHERE envoyés à un client SQL, dbt sur la cible prod).
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
UPPER=$(echo "$CMD" | tr '[:lower:]' '[:upper:]')

deny() { echo "Bloqué par la politique projet : $1" >&2; exit 2; }

[[ "$CMD" =~ rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f ]] && deny "suppression récursive (rm -rf)."
[[ "$UPPER" =~ (DROP|TRUNCATE)[[:space:]]+(TABLE|SCHEMA|DATABASE) ]] && deny "DROP/TRUNCATE interdit : passer par une revue humaine."
if [[ "$UPPER" =~ DELETE[[:space:]]+FROM ]] && ! [[ "$UPPER" =~ WHERE ]]; then
  deny "DELETE sans WHERE."
fi
[[ "$CMD" =~ --target[[:space:]=]+prod ]] && deny "exécution dbt sur la cible prod réservée à la CI."
exit 0
