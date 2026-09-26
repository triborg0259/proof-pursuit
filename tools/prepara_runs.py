#!/usr/bin/env python3
"""
prepara_runs.py — crea le cartelle di lavoro runs/pN_cK per il loop, una per cella.

Cosa fa: per ogni problema e cella in runs/celle.json scrive problem.md (enunciato ufficiale completo + cella
bersaglio) e state.json (contratto shared/state), e copia la bibliografia arXiv già cercata (problema-N/fonti/arxiv.json)
filtrata per pertinenza. Non sovrascrive cartelle esistenti: le run in corso o finite restano intatte.
Perché: il loop lavora per cella; le cartelle devono avere lo stesso formato e lo stesso enunciato protetto.
Uso: python3 tools/prepara_runs.py [p1 p2 ...]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLE = json.loads((ROOT / "runs" / "celle.json").read_text(encoding="utf-8"))
# Parole che una voce arXiv deve contenere per essere pertinente (le ricerche a frase esatta pescano rumore).
PAROLE = {"p1": ["fejes", "angles between lines", "sum of angles", "sum of the angles"],
          "p2": ["uphill", "hypercube labell", "increasing path", "acyclic orientation", "monotone path"],
          "p3": ["bulgarian", "solitaire"], "p4": ["covering system", "residue class", "disjoint congruence", "disjoint coset"]}
# Claim già verificati (Referee o revisione umana registrata in STATUS.md) riutilizzabili come ipotesi.
VERIFICATI = {"p2": ["For any labelling of any graph: #uphill paths >= |E| + #valleys",
                     "U(Q_3) = 14", "U(Q_4) = 34, attained by 0000,1111,0111,1101,1110,1011,0001,1000,0010,0100,1001,0110,0011,1010,0101,1100"]}


def pertinente(voce, parole):
    """Una voce arXiv è pertinente se titolo o abstract contengono almeno una parola chiave del problema."""
    testo = (voce["title"] + " " + voce["abstract"]).lower()
    return any(p in testo for p in parole)


def regole_ufficiali(enunciato):
    """Le regole di consegna della colonna, prese alla lettera dal paragrafo 'What to hand in' dell'enunciato.
    Perché: il Referee B marca MISSING ogni punto che dipende dal regolamento; con il testo ufficiale non deve."""
    m = re.search(r"\*\*What to hand in\.\*\*(.*?)(?=\n## )", enunciato, re.S)
    handin = " ".join(m.group(1).split()) if m else ""
    cit = ("Citing a published result for the statement you are asked to prove does not count as a solution; "
           "a proof written out in full does, whatever its source.")
    return {"allow_literature_as_proof": False, "allow_computation": True, "require_machine_verification": False,
            "additional_rules": f"OFFICIAL hand-in rules of this column (verbatim from the problem statement): {handin} {cit}"}


def scrivi_cella(pid, k, testo_cella, enunciato, fonti):
    """Crea runs/<pid>_c<k>: problem.md, state.json, literature.json. Ritorna False se esisteva già."""
    d = ROOT / "runs" / f"{pid}_c{k}"
    if d.exists():
        return False
    d.mkdir(parents=True)
    (d / "problem.md").write_text(enunciato + f"\n\n# TARGET CELL {k}\n{testo_cella}\n", encoding="utf-8")
    state = {"problem_id": f"{pid}_c{k}", "highest_verified_cell": 0, "current_target": f"cell_{k}",
             "cell_statement": testo_cella, "current_blocker": "", "rules": regole_ufficiali(enunciato),
             "verified_claims": VERIFICATI.get(pid, []), "failed_attempts": [], "stagnation_count": 0, "cell_status": {}}
    (d / "state.json").write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (d / "literature.json").write_text(json.dumps(fonti, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main(problemi):
    for pid in problemi:
        n = pid[1]
        enunciato = (ROOT / f"problema-{n}" / "enunciato.md").read_text(encoding="utf-8")
        fonti_file = ROOT / f"problema-{n}" / "fonti" / "arxiv.json"
        fonti = [v for v in json.loads(fonti_file.read_text()) if pertinente(v, PAROLE[pid])] if fonti_file.exists() else []
        for k, testo in CELLE[pid]["cells"].items():
            nuova = scrivi_cella(pid, k, testo, enunciato, fonti)
            print(f"runs/{pid}_c{k}: {'creata' if nuova else 'già presente'} ({len(fonti)} fonti arXiv)")


if __name__ == "__main__":
    main(sys.argv[1:] or list(CELLE))
