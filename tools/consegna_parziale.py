#!/usr/bin/env python3
"""
consegna_parziale.py — bozza di consegna PARZIALE (inglese) da un tentativo del loop respinto o non concluso: riporta
i lemmi effettivamente dimostrati, il verdetto del Referee con il motivo, il codice e i gap dichiarati.
Perché: un tentativo respinto contiene spesso risultati intermedi validi; consegnarli descritti onestamente vale.
Uso: .venv/bin/python tools/consegna_parziale.py <run> <attempt_NNN> <N> <K>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(run, attempt, n, k):
    a = json.loads((ROOT / "runs" / run / "attempts" / f"{attempt}.json").read_text())
    r = json.loads((ROOT / "runs" / run / "attempts" / f"referee_{attempt.split('_')[1]}.json").read_text())
    codice = "\n".join(f"- code_{i+1} ({c['language']}, rigor `{c['rigor']}`): {c['purpose']}" for i, c in enumerate(a["code_used"])) or "- none"
    gaps = "\n".join(f"- {g}" for g in a["self_reported_gaps"]) or "- none declared"
    testo = f"""# Problem {n} — Part {k} — submission (PARTIAL)

**Declared status: PARTIAL.** The cell is not solved. What follows is the intermediate progress actually established,
as judged by the automatic Referee (verdict `{r['verdict']}`: {(r.get('fatal_error') or r.get('next_blocker') or '')[:400]}).
The author's own declared status was `{a['claimed_status']}`.

## 1. Result and scope
{a['claimed_progress']}

## 2. Proof
{a['proof_attempt']}

## 3. Verification: instructions, dependencies, timings
Python 3 standard library. Scripts (re-run by the orchestrator, see `runs/{run}/verifica/`):
{codice}

## 4. Sources and contribution
{chr(10).join('- ' + s for s in a['sources_used']) or '- none'}
- Position with respect to the literature: {a['literature_position']}

## 5. Limits and unresolved parts
Referee's blocking point: {r.get('fatal_error') or '—'}
Next step required: {r.get('next_blocker') or '—'}
Gaps declared by the author:
{gaps}
"""
    sub = ROOT / f"problema-{n}" / "submission"
    for nome in (f"parte-{k}.en.md", f"parte-{k}.md"):
        (sub / nome).write_text(testo, encoding="utf-8")
    st = ROOT / "STATUS.md"; s = st.read_text(encoding="utf-8"); sez = s.split(f"## Problema {n}", 1)
    sez[1] = re.sub(rf"(?m)^(\| {k} \| [^|]+\|)[^|]*\|[^\n]*$", lambda m: f"{m.group(1)} parziale | loop {run} {attempt}: {r['verdict']} ({(r.get('fatal_error') or '')[:120]}); lemmi intermedi in submission/parte-{k}.en.md |", sez[1], count=1)
    st.write_text(f"## Problema {n}".join(sez), encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "campi_latex.py"), str(n), str(k)], check=True, capture_output=True)
    print(f"parziale scritta: problema {n} parte {k}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
