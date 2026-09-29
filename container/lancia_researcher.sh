#!/bin/bash
# Esegue `claude -p ...` dentro il container del Researcher.
# Uso: container/lancia_researcher.sh <sandbox della cella> <cartella del problema> <argomenti di claude...>
# Monta: sandbox → /work (scrivibile), tools/ → /repo/tools (ro), problema-N/ → /repo/problema-N (ro),
#        ~/.proof-pursuit/claude → /home/researcher/.claude (ro: credenziali estratte dal portachiavi, vedi README).
set -euo pipefail
SANDBOX=$1; PROBLEMA=$2; shift 2
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CRED="${PROOF_PURSUIT_CLAUDE_HOME:-$HOME/.proof-pursuit/claude}"
[ -f "$CRED/.credentials.json" ] || { echo "manca $CRED/.credentials.json: vedi container/README.md" >&2; exit 3; }
exec docker run --rm \
  -v "$SANDBOX":/work \
  -v "$ROOT/tools":/repo/tools:ro \
  -v "$ROOT/$PROBLEMA":/repo/"$PROBLEMA":ro \
  -v "$CRED":/home/researcher/.claude:ro \
  -e HOME=/home/researcher \
  proof-pursuit-researcher claude "$@"
