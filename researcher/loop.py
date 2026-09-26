#!/usr/bin/env python3
"""
loop.py — orchestrazione minima end-to-end: Researcher → Referee → (REJECT → Researcher rilegge l'errore) → …

Perché esiste: finché l'Orchestrator del team non è pronto, serve comunque chiudere il ciclo dell'errore in
automatico. Questo file fa solo il giro; Researcher, Referee e Creative restano componenti separati.

Un'iterazione:
  1. (solo la prima volta, se richiesto) ricerca bibliografica su arXiv → literature.json
  2. Researcher: nuovo tentativo (legge referee_report.json, failed_attempts.md, creative_ideas.json)
  3. Referee: giudica il tentativo (via bridge_referee.py) → referee_report.json
  4. Decisione:
       READY_FOR_HUMAN / ACCEPT   → stop: l'approvazione è umana
       COUNTEREXAMPLE_FOUND       → stop: la cella è falsa
       KNOWN_OPEN                 → stop: colonna chiusa
       UNKNOWN_STATUS             → stop: da investigare a mano (in offline è l'esito normale)
       PARTIAL_PROGRESS           → i claim accettati entrano in state.verified_claims, si continua
       REJECT                     → si continua; se c'è stagnazione si chiama il Creative
  5. Creative: `creative/` del team (--creative cli|rule_based|none, default cli) oppure un comando esterno
     `--creative-cmd` con {workdir} sostituito; in entrambi i casi deve scrivere <workdir>/creative_ideas.json.

Uso:
  python3 researcher/loop.py --workdir runs/X --max-iter 4 --researcher-backend cli --shell full --referee cli \
      --literature "hypercube labelling uphill paths"
Test senza modelli: --researcher-backend mock --referee mock --creative rule_based --mock-rejects 2
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from researcher import read_json, write_json, next_attempt_number  # noqa: E402

FERMA = {"READY_FOR_HUMAN": "pronto per approvazione umana", "ACCEPT": "accettato (verificare che l'approvazione sia umana)",
         "COUNTEREXAMPLE_FOUND": "controesempio trovato: la cella è falsa", "KNOWN_OPEN": "problema aperto: colonna chiusa",
         "UNKNOWN_STATUS": "stato indeterminato: investigare a mano"}


# =============================================================================== passi del ciclo
def esegui(cmd, cwd=HERE.parent):
    """Lancia un sottocomando mostrando la riga; solleva se fallisce, perché un passo rotto non deve passare inosservato."""
    print("[loop] $", " ".join(cmd), file=sys.stderr)
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"comando fallito ({res.returncode}): {res.stderr[-800:]}")
    return res.stdout


def passo_letteratura(args, workdir):
    """Ricerca arXiv una sola volta per cartella: le voci restano in literature.json per tutte le iterazioni."""
    if not args.literature or (workdir / "literature.json").exists():
        return
    cmd = [sys.executable, str(HERE / "literature.py"), "--workdir", str(workdir)]
    for q in args.literature:
        cmd += ["--query", q]
    esegui(cmd)


def passo_researcher(args, workdir):
    """Un tentativo del Researcher; ritorna il record salvato (attempt_NNN.json)."""
    cmd = [sys.executable, str(HERE / "researcher.py"), "run", "--workdir", str(workdir),
           "--backend", args.researcher_backend, "--strict"]
    if args.shell:
        cmd += ["--shell", args.shell]
    if args.effort:
        cmd += ["--effort", args.effort]
    esegui(cmd)
    return read_json(workdir / "attempts" / f"attempt_{next_attempt_number(workdir) - 1:03d}.json")


def passo_referee(args, workdir, attempt, iterazione):
    """Giudizio del tentativo. mock: REJECT per le prime --mock-rejects iterazioni, poi READY_FOR_HUMAN."""
    if args.referee == "mock":
        return _referee_mock(workdir, attempt, iterazione, args.mock_rejects)
    cmd = [sys.executable, str(HERE / "bridge_referee.py"), "review", "--workdir", str(workdir), "--run-code"]
    if args.referee == "offline":
        cmd.append("--offline")
    esegui(cmd)
    return read_json(workdir / "referee_report.json")


def _referee_mock(workdir, attempt, iterazione, rifiuti):
    """Referee finto per i test del ciclo: stesso motivo di rigetto ogni volta, segnale di stagnazione al 2° rifiuto."""
    from bridge_referee import registra_report
    rifiuta = iterazione <= rifiuti
    report = {"attempt_id": attempt["attempt_id"], "verdict": "REJECT" if rifiuta else "UNKNOWN_STATUS",
              "review_status": "NEEDS_WORK" if rifiuta else "READY_FOR_HUMAN", "highest_verified_cell": 0,
              "accepted_claims": [], "proposed_claim_ids": [],
              "fatal_error": "Step 2 asserts the key identity without proof." if rifiuta else None,
              "citation_issue": False, "computation_issue": False,
              "next_blocker": "Prove the key identity explicitly." if rifiuta else "Human approval",
              "reasoning_summary": "mock referee", "stagnation_signal": rifiuta and iterazione >= 2}
    registra_report(workdir, report)
    return report


def comando_creative(args, workdir):
    """Il comando che scrive creative_ideas.json: il Creative del team (creative/) con il backend scelto,
    oppure un comando esterno (--creative-cmd) per chi vuole agganciare altro. None ⇒ nessun Creative."""
    if args.creative_cmd:
        import shlex  # rispetta le virgolette; {workdir} sostituito senza .format (le graffe del JSON lo romperebbero)
        return shlex.split(args.creative_cmd.replace("{workdir}", str(workdir)))
    if args.creative == "none":
        return None
    return [sys.executable, "-m", "creative.creative_agent", "run", "--workdir", str(workdir), "--backend", args.creative]


def passo_creative(args, workdir, motivo):
    """Chiama il Creative quando il ciclo stagna; ritorna True se ha scritto idee nuove per il prossimo tentativo."""
    cmd = comando_creative(args, workdir)
    if cmd is None:
        print(f"[loop] stagnazione ({motivo}) ma nessun Creative collegato: proseguo", file=sys.stderr)
        return False
    esegui(cmd)
    return (workdir / "creative_ideas.json").exists()


def integra_progresso_parziale(workdir, report):
    """PARTIAL_PROGRESS: i claim accettati diventano ipotesi disponibili (compito dell'Orchestrator, fatto qui)."""
    state = read_json(workdir / "state.json")
    nuovi = [c for c in report.get("accepted_claims", []) if c not in state["verified_claims"]]
    state["verified_claims"] += nuovi
    write_json(workdir / "state.json", state)
    return nuovi


# =============================================================================== decisione e ciclo
def serve_creative(workdir, attempt, report, stagnazione_prima):
    """Tre segnali, ognuno sufficiente: il Researcher lo chiede, il Referee segnala stagnazione, il contatore è salito."""
    state = read_json(workdir / "state.json")
    if attempt.get("request_creative"):
        return "request_creative del Researcher"
    if report.get("stagnation_signal"):
        return "stagnation_signal del Referee"
    if state.get("stagnation_count", 0) > stagnazione_prima:
        return f"stagnation_count={state['stagnation_count']}"
    return ""


def registra_log(workdir, voce):
    """Una riga JSON per iterazione in loop_log.jsonl: è la traccia che si consegna e si rilegge."""
    with open(workdir / "loop_log.jsonl", "a") as f:
        f.write(json.dumps(voce, ensure_ascii=False) + "\n")


def voce_di_log(i, attempt, report):
    """La riga di traccia di un'iterazione: non solo i verdetti ma il PERCHÉ di ogni agente, così la consegna
    e il rapporto possono raccontare le decisioni (cosa ha scelto il Researcher e perché, cosa ha bloccato il Referee)."""
    return {"iter": i, "attempt_id": attempt["attempt_id"], "family": attempt.get("approach_family"),
            "subgoal": attempt.get("subgoal"), "claimed_status": attempt.get("claimed_status"),
            "researcher_reason": (attempt.get("reason_for_choice") or "")[:600],
            "literature_position": (attempt.get("literature_position") or "")[:600],
            "verdict": report["verdict"], "review_status": report.get("review_status"),
            "fatal_error": report.get("fatal_error"), "next_blocker": report.get("next_blocker"),
            "creative": "", "creative_analysis": "", "ts": time.strftime("%H:%M:%S")}


def iterazione(args, workdir, i):
    """Un giro completo; ritorna (esito_da_fermare_o_None, voce_di_log)."""
    stagnazione_prima = read_json(workdir / "state.json").get("stagnation_count", 0) if (workdir / "state.json").exists() else 0
    attempt = passo_researcher(args, workdir)
    report = passo_referee(args, workdir, attempt, i)
    esito = report.get("review_status") if report.get("review_status") == "READY_FOR_HUMAN" else report["verdict"]
    voce = voce_di_log(i, attempt, report)
    if esito in FERMA:
        return FERMA[esito], voce
    if report["verdict"] == "PARTIAL_PROGRESS":
        voce["new_claims"] = integra_progresso_parziale(workdir, report)
    motivo = serve_creative(workdir, attempt, report, stagnazione_prima)
    if motivo:
        scritte = passo_creative(args, workdir, motivo)
        voce["creative"] = f"{motivo} → {'idee scritte' if scritte else 'non collegato'}"
        idee = read_json(workdir / "creative_ideas.json") if scritte else None
        voce["creative_analysis"] = (idee or {}).get("blocker_analysis", "")[:600]
    return None, voce


def cmd_loop(args):
    workdir = Path(args.workdir)
    passo_letteratura(args, workdir)
    for i in range(1, args.max_iter + 1):
        esito, voce = iterazione(args, workdir, i)
        registra_log(workdir, voce)
        print(json.dumps(voce, ensure_ascii=False))
        if esito:
            print(f"[loop] STOP all'iterazione {i}: {esito}")
            return 0
    print(f"[loop] STOP: raggiunto --max-iter={args.max_iter} senza esito finale; ultimo verdetto in referee_report.json")
    return 1


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workdir", required=True)
    p.add_argument("--max-iter", type=int, default=4)
    p.add_argument("--researcher-backend", choices=["cli", "api", "mock"], default="cli")
    p.add_argument("--shell", choices=["sandbox", "full"])
    p.add_argument("--effort")
    p.add_argument("--referee", choices=["cli", "offline", "mock"], default="cli")
    p.add_argument("--mock-rejects", type=int, default=2, help="solo --referee mock: quanti REJECT prima di READY")
    p.add_argument("--creative", choices=["cli", "rule_based", "none"], default="cli",
                   help="backend del Creative del team (creative/): cli = modello, rule_based = senza modello")
    p.add_argument("--creative-cmd", help="in alternativa: comando esterno che scrive {workdir}/creative_ideas.json")
    p.add_argument("--literature", action="append", help="query arXiv, ripetibile; eseguita una volta per cartella")
    return p


if __name__ == "__main__":
    sys.exit(cmd_loop(build_parser().parse_args()))
