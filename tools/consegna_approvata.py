#!/usr/bin/env python3
"""
consegna_approvata.py — dopo l'approvazione umana di una cella READY_FOR_HUMAN scrive la bozza di consegna in inglese
(problema-N/submission/parte-K.en.md e .md), registra approval.json, aggiorna la riga di STATUS.md e genera i campi LaTeX.
Uso: .venv/bin/python tools/consegna_approvata.py <run> <attempt_NNN> <N> <K> "<chi approva>"
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def testo_consegna(run, a, n, k):
    fonti = "\n".join(f"- {s}" for s in a["sources_used"]) or "- No external source used: the proof is self-contained."
    codice = "\n".join(f"- code_{i+1} ({c['language']}, rigor `{c['rigor']}`): {c['purpose']}" for i, c in enumerate(a["code_used"])) or "- No computation needed."
    oss = ROOT / "runs" / run / "verifica" / a["attempt_id"] / "osservazioni.json"
    rieseg = "\n".join(f"- {o[:300]}" for o in json.loads(oss.read_text())) if oss.exists() else "- (no scripts to re-run)"
    gaps = "\n".join(f"- {g}" for g in a["self_reported_gaps"]) or "- none declared"
    return f"""# Problem {n} — Part {k} — submission

**Declared status: SOLVED (approved).** Complete proof; automatic Referee READY_FOR_HUMAN (judge A, mathematics: PASS;
judge B, evidence: PASS; code re-run by the orchestrator); human approval recorded in `runs/{run}/approval.json`.

## 1. Result and scope
{a['claimed_progress']}

## 2. Proof
{a['proof_attempt']}

## 3. Verification: instructions, dependencies, timings
Python 3 standard library only. Scripts (also saved in `runs/{run}/sandbox/` and re-run in `runs/{run}/verifica/`):
{codice}

Trusted re-runs by the orchestrator (exit code, wall clock, output):
{rieseg}

## 4. Sources and contribution
{fonti}
- Position with respect to the literature: {a['literature_position']}
- Contribution: the proof above is written out in full by the team's Researcher and checked by two independent judges and by a human.

## 5. Limits and unresolved parts
Gaps declared by the author (all accepted by the judges):
{gaps}
"""


def main(run, attempt, n, k, chi):
    a = json.loads((ROOT / "runs" / run / "attempts" / f"{attempt}.json").read_text())
    testo = testo_consegna(run, a, n, k)
    sub = ROOT / f"problema-{n}" / "submission"
    (sub / f"parte-{k}.en.md").write_text(testo, encoding="utf-8")
    (sub / f"parte-{k}.md").write_text(testo, encoding="utf-8")
    (ROOT / "runs" / run / "approval.json").write_text(json.dumps({"attempt_id": attempt, "approved_by": chi, "approved_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "approved_claim_ids": ["main"]}, indent=1))
    st = ROOT / "STATUS.md"
    s = st.read_text(encoding="utf-8")
    sez = s.split(f"## Problema {n}", 1)
    sez[1] = re.sub(rf"(?m)^(\| {k} \| [^|]+\|)[^|]*\|[^\n]*$", lambda m: f"{m.group(1)} revisionato | loop {run} {attempt}: Referee READY_FOR_HUMAN (A PASS, B PASS); approvata da {chi}; submission/parte-{k}.en.md |", sez[1], count=1)
    st.write_text(f"## Problema {n}".join(sez), encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "campi_latex.py"), str(n), str(k)], check=True)
    print(f"approvata problema {n} parte {k}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
