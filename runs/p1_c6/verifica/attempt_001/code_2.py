cd runs/p1_c6/sandbox
for dN in "3 6" "3 7" "3 8" "3 9" "4 7" "4 8" "4 9" "4 10" "5 8" "5 9" "5 11" "6 10" "6 13"; do
  d=${dN%% *}; N=${dN##* }
  ../../../.venv/bin/python ../../../tools/autoloop.py ../../../problema-1/esperimenti/lines_Rd.py \
      --budget 5 --seeds 3 --restarts 8 --ledger esplora_Rd.jsonl --tag "c6_d${d}_N${N}" -- $d $N
done
# riassunto: per ogni (d,N) best trovato, target congetturato, gap (float)
../../../.venv/bin/python - <<'EOF'
import json
for riga in open("esplora_Rd.jsonl"):
    r = json.loads(riga)
    print(f"d={r['args'][0]} N={r['args'][1]:>2}  best={r['best_score']:.6f}  target={r['target']:.6f}  target-best={r['gap_target_minus_best']:+.2e}")
EOF
# Output osservato: (3,6) best 18.828661 < 18.849556 (non convergente); tutti gli altri 12 casi best = target entro 2e-7
# (residuo negativo ~1e-7 = artefatto float di arccos vicino a 1, non una violazione).