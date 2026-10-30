#!/bin/bash
# Lancia il loop end-to-end (Researcher → Referee → Creative) su tutte le celle di un problema, in parallelo.
# Con la shell `full` (default) va avviato da un terminale umano (prefisso `!` in Claude Code): il Researcher gira con
# permessi pre-autorizzati. Con RESEARCHER_SHELL=sandbox il Researcher ha solo python3 nella sua cartella e il
# lanciatore può partire anche da un agente.
# Uso: tools/lancia_loop.sh p1 [max_iter] [celle...]   es. tools/lancia_loop.sh p2 2 3 4 5 6  (salta C1-C2 già chiuse)
#      RESEARCHER_SHELL=sandbox tools/lancia_loop.sh p5 2   (celle di default: tutte quelle di runs/celle.json)
#      log in runs/p1_cK/loop.out, traccia delle decisioni in runs/p1_cK/loop_log.jsonl
cd "$(dirname "$0")/.."
P=${1:?problema, es. p1}; ITER=${2:-2}; shift 2 2>/dev/null; SHELL_R=${RESEARCHER_SHELL:-full}
CELLE=${@:-$(.venv/bin/python -c "import json,sys; print(' '.join(json.load(open('runs/celle.json'))[sys.argv[1]]['cells']))" "$P")}
.venv/bin/python tools/prepara_runs.py "$P" >/dev/null
for k in $CELLE; do d=runs/${P}_c$k
  nohup .venv/bin/python researcher/loop.py --workdir "$d" --max-iter "$ITER" --researcher-backend cli --shell "$SHELL_R" \
        --referee cli --creative cli > "$d/loop.out" 2>&1 &
  echo "avviato $d (pid $!, shell $SHELL_R)"
done
echo "stato: tail -n 3 runs/${P}_c*/loop.out ; verdetti: cat runs/${P}_c*/loop_log.jsonl"
