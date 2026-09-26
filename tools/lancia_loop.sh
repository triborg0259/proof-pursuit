#!/bin/bash
# Lancia il loop end-to-end (Researcher shell full → Referee → Creative) su tutte le celle di un problema, in parallelo.
# Va avviato da un terminale umano (prefisso `!` in Claude Code): il Researcher gira con permessi pre-autorizzati.
# Uso: tools/lancia_loop.sh p1 [max_iter] [celle...]   es. tools/lancia_loop.sh p2 2 3 4 5 6  (salta C1-C2 già chiuse)
#      log in runs/p1_cK/loop.out, traccia delle decisioni in runs/p1_cK/loop_log.jsonl
cd "$(dirname "$0")/.."
P=${1:?problema, es. p1}; ITER=${2:-2}; shift 2 2>/dev/null; CELLE=${@:-1 2 3 4 5 6}
.venv/bin/python tools/prepara_runs.py "$P" >/dev/null
for k in $CELLE; do d=runs/${P}_c$k
  nohup .venv/bin/python researcher/loop.py --workdir "$d" --max-iter "$ITER" --researcher-backend cli --shell full \
        --referee cli --creative cli > "$d/loop.out" 2>&1 &
  echo "avviato $d (pid $!)"
done
echo "stato: tail -n 3 runs/${P}_c*/loop.out ; verdetti: cat runs/${P}_c*/loop_log.jsonl"
