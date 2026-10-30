#!/usr/bin/env python3
"""
prepara_runs.py — crea le cartelle di lavoro runs/pN_cK per il loop, una per cella.

Cosa fa: per ogni problema e cella in runs/celle.json scrive problem.md (enunciato ufficiale completo + cella
bersaglio) e state.json (contratto shared/state), e copia la bibliografia arXiv già cercata (problema-N/fonti/arxiv.json)
filtrata per pertinenza. Non sovrascrive cartelle esistenti: le run in corso o finite restano intatte.
Perché: il loop lavora per cella; le cartelle devono avere lo stesso formato e lo stesso enunciato protetto.
Ogni voce di runs/celle.json può portare, oltre a title e cells, campi facoltativi che rendono il file il solo
punto da toccare per un nuovo insieme di problemi: `parole_arxiv` (filtro di pertinenza), `verified_claims`,
`regola_generale` (sostituisce la regola sulle citazioni della gara; "" la toglie), `regole_squadra` (vincoli del
team, passati al Referee come NON ufficiali), `lunghezza_max` ({cella: caratteri massimi del proof_attempt}),
`lean_richiesto` (celle per cui il team chiede una formalizzazione Lean 4 + Mathlib, vedi tools/verifica_lean.py).
Uso: python3 tools/prepara_runs.py [p1 p2 ...]
     python3 tools/prepara_runs.py p5 --aggiorna [--blocker "..."] [--celle 2 3]   riscrive regole (e blocco) delle celle esistenti,
     senza toccare enunciato e tentativi: serve quando cambiano le regole di consegna dopo un primo giro.
"""
import argparse
import json
import re
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


# Regola generale della gara Proof Pursuit, valida per ogni colonna anche dove l'enunciato non la ripete (P2).
CITAZIONE_GARA = ("Citing a published result for the statement you are asked to prove does not count as a solution; "
                  "a proof written out in full does, whatever its source.")


def cartella_problema(pid):
    """Da 'p12' a ROOT/problema-12: il numero può avere più cifre."""
    return ROOT / f"problema-{pid[1:]}"


def pertinente(voce, parole):
    """Una voce arXiv è pertinente se titolo o abstract contengono almeno una parola chiave del problema.
    Senza parole chiave (problema nuovo) si tengono tutte: il filtro serve solo a togliere rumore noto."""
    testo = (voce["title"] + " " + voce["abstract"]).lower()
    return not parole or any(p in testo for p in parole)


def regole_ufficiali(enunciato, voce=None, cella=None):
    """Le regole di consegna della colonna, prese alla lettera dal paragrafo 'What to hand in' dell'enunciato.
    Perché: il Referee B marca MISSING ogni punto che dipende dal regolamento; con il testo ufficiale non deve.
    Le regole del team (voce `regole_squadra`) seguono separate e marcate come non ufficiali."""
    voce = voce or {}
    m = re.search(r"\*\*What to hand in\.\*\*(.*?)(?=\n## )", enunciato, re.S)
    handin = " ".join(m.group(1).split()) if m else ""
    generale = voce.get("regola_generale", CITAZIONE_GARA)
    regole = f"OFFICIAL hand-in rules of this column (verbatim from the problem statement): {handin} {generale}".strip()
    if voce.get("regole_squadra"):
        regole += "\n\n" + voce["regole_squadra"]
    limite = voce.get("lunghezza_max", {}).get(cella)
    if limite:
        regole += (f"\n\nLENGTH LIMIT for this cell (team rule): proof_attempt at most {limite} characters of "
                   "Markdown+LaTeX source, figures included; an answer over the limit does not meet the hand-in rules.")
    if cella in voce.get("lean_richiesto", []):
        regole += ("\n\nFORMAL VERIFICATION required for this cell (team rule): include lean_proof, a Lean 4 + Mathlib "
                   "file whose main theorem states the cell's target (explain the match in `covers`), checked with "
                   "tools/verifica_lean.py: it must compile with no sorry and standard axioms only. The written "
                   "proof_attempt is still required and is what the grader reads.")
    return {"allow_literature_as_proof": False, "allow_computation": True, "require_machine_verification": False,
            "additional_rules": regole}


def scrivi_cella(pid, k, testo_cella, enunciato, fonti):
    """Crea runs/<pid>_c<k>: problem.md, state.json, literature.json. Ritorna False se esisteva già."""
    d = ROOT / "runs" / f"{pid}_c{k}"
    if d.exists():
        return False
    d.mkdir(parents=True)
    (d / "problem.md").write_text(enunciato + f"\n\n# TARGET CELL {k}\n{testo_cella}\n", encoding="utf-8")
    state = {"problem_id": f"{pid}_c{k}", "highest_verified_cell": 0, "current_target": f"cell_{k}",
             "cell_statement": testo_cella, "current_blocker": "", "rules": regole_ufficiali(enunciato, CELLE[pid], k),
             "verified_claims": CELLE[pid].get("verified_claims", VERIFICATI.get(pid, [])), "failed_attempts": [], "stagnation_count": 0, "cell_status": {}}
    (d / "state.json").write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (d / "literature.json").write_text(json.dumps(fonti, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def aggiorna_cella(pid, k, enunciato, blocker):
    """Riscrive le regole (dal manifesto aggiornato) e, se dato, il blocco corrente di una cella già preparata.
    Enunciato protetto, tentativi e claim verificati restano come sono: cambia solo cosa si chiede alla consegna."""
    percorso = ROOT / "runs" / f"{pid}_c{k}" / "state.json"
    state = json.loads(percorso.read_text(encoding="utf-8"))
    state["rules"] = regole_ufficiali(enunciato, CELLE[pid], k)
    if blocker:
        state["current_blocker"] = blocker
    percorso.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main(problemi, aggiorna=False, blocker="", solo_celle=None):
    for pid in problemi:
        enunciato = (cartella_problema(pid) / "enunciato.md").read_text(encoding="utf-8")
        fonti_file = cartella_problema(pid) / "fonti" / "arxiv.json"
        parole = CELLE[pid].get("parole_arxiv", PAROLE.get(pid, []))
        fonti = [v for v in json.loads(fonti_file.read_text()) if pertinente(v, parole)] if fonti_file.exists() else []
        for k, testo in CELLE[pid]["cells"].items():
            nuova = scrivi_cella(pid, k, testo, enunciato, fonti)
            aggiornata = not nuova and aggiorna and (not solo_celle or k in solo_celle)
            if aggiornata:
                aggiorna_cella(pid, k, enunciato, blocker)
            print(f"runs/{pid}_c{k}: {'creata' if nuova else 'regole aggiornate' if aggiornata else 'già presente'}"
                  f" ({len(fonti)} fonti arXiv)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("problemi", nargs="*")
    parser.add_argument("--aggiorna", action="store_true", help="riscrive le regole delle celle già presenti")
    parser.add_argument("--blocker", default="", help="con --aggiorna: nuovo current_blocker delle celle")
    parser.add_argument("--celle", nargs="*", help="con --aggiorna: solo queste celle (es. 2 3)")
    args = parser.parse_args()
    main(args.problemi or list(CELLE), args.aggiorna, args.blocker, args.celle)
