#!/usr/bin/env python3
"""Banco di prova del Referee con errori piantati: misura quante prove sbagliate passano e quante giuste cadono.

Perché: senza questo numero il Referee è un'opinione. La letteratura (settembre 2026) dice che un giudice LLM
singolo accetta il 10-15 % delle prove sottilmente sbagliate; qui si misura A da solo, B da solo e il merge.

Come: ogni caso è una cartella `banco/caso_NN/` identica a una cartella del loop (problem.md, state.json,
attempts/attempt_001.json, sandbox/), così il Referee la giudica con lo stesso bridge di sempre e non sa di
essere sotto esame. Le etichette (origine, categoria, esito atteso) stanno SOLO in `banco/etichette.json`,
mai dentro il caso: gli identificatori sono neutri (caso_01, caso_02, ...).

Uso:
  banco_prova.py crea --run runs/p3_c1 --attempt attempt_002 --categoria corretta
  banco_prova.py crea --da caso_01 --categoria caso_mancante --proof-file variante.md --nota "salta il caso r=0"
  banco_prova.py esegui [--casi caso_01 caso_02] [--ripetizioni 3] [--model M] [--model-b M]
  banco_prova.py tabella
Categorie di errore (dal rapporto, sezione 3): corretta · caso_mancante · circolarita · lemma_falso ·
obiettivo_cambiato · calcolo_non_riproducibile · citazione_inventata · enumerazione_incompleta.
"""
import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANCO = ROOT / "banco"
ETICHETTE = BANCO / "etichette.json"
RISULTATI = BANCO / "risultati.jsonl"
BRIDGE = ROOT / "researcher" / "bridge_referee.py"
CATEGORIE = ["corretta", "caso_mancante", "circolarita", "lemma_falso", "obiettivo_cambiato",
             "calcolo_non_riproducibile", "citazione_inventata", "enumerazione_incompleta"]
# Cosa ci si aspetta dai giudici per categoria: la prova corretta deve passare, tutto il resto deve cadere.
# Il giudice B vede solo l'evidenza: su un errore puramente matematico può legittimamente dire PASS.
ATTESO = {"corretta": {"A": "PASS", "B": "PASS", "esito": "READY_FOR_HUMAN"}}
ERRORI_DI_EVIDENZA = {"calcolo_non_riproducibile", "citazione_inventata", "enumerazione_incompleta"}


# ================================================================== file di appoggio
def leggi_json(percorso, default):
    """JSON del file o il default se manca: il banco deve partire da zero senza preparazione."""
    return json.loads(percorso.read_text(encoding="utf-8")) if percorso.exists() else default


def scrivi_json(percorso, dati):
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")


def atteso_per(categoria):
    """Esito atteso per giudice e merge. Per gli errori matematici B può passare; per quelli di evidenza deve cadere."""
    if categoria in ATTESO:
        return ATTESO[categoria]
    b = "FAIL" if categoria in ERRORI_DI_EVIDENZA else None   # None = non conta nella matrice
    a = None if categoria in ERRORI_DI_EVIDENZA else "FAIL"
    return {"A": a, "B": b, "esito": "REJECT"}


# ================================================================== crea
def prossimo_id(etichette):
    """caso_01, caso_02, ... in ordine di creazione: nomi neutri, niente che riveli la categoria."""
    return f"caso_{len(etichette) + 1:02d}"


def copia_caso(origine, attempt_file, destinazione):
    """Copia dal run (o da un altro caso) solo ciò che serve al Referee: enunciato, stato, sandbox, un tentativo."""
    destinazione.mkdir(parents=True)
    for nome in ("problem.md", "state.json"):
        shutil.copy(origine / nome, destinazione / nome)
    if (origine / "sandbox").exists():
        shutil.copytree(origine / "sandbox", destinazione / "sandbox", ignore=shutil.ignore_patterns("__pycache__"))
    attempt = json.loads(attempt_file.read_text(encoding="utf-8"))
    attempt["attempt_id"] = "attempt_001"
    scrivi_json(destinazione / "attempts" / "attempt_001.json", attempt)
    return attempt


def sostituisci_prova(destinazione, proof_file):
    """La variante con errore piantato: stesso tentativo, testo della prova preso dal file scritto a mano."""
    percorso = destinazione / "attempts" / "attempt_001.json"
    attempt = json.loads(percorso.read_text(encoding="utf-8"))
    attempt["proof_attempt"] = Path(proof_file).read_text(encoding="utf-8")
    scrivi_json(percorso, attempt)


def cmd_crea(args):
    """Registra un caso nuovo. Da un run del loop (--run/--attempt) o come variante di un caso (--da)."""
    etichette = leggi_json(ETICHETTE, {})
    caso_id = prossimo_id(etichette)
    if args.da:
        origine, attempt_file = BANCO / args.da, BANCO / args.da / "attempts" / "attempt_001.json"
    else:
        origine, attempt_file = ROOT / args.run, ROOT / args.run / "attempts" / f"{args.attempt}.json"
    copia_caso(origine, attempt_file, BANCO / caso_id)
    if args.proof_file:
        sostituisci_prova(BANCO / caso_id, args.proof_file)
    etichette[caso_id] = {"origine": args.da or args.run, "categoria": args.categoria, "nota": args.nota or "",
                          "atteso": atteso_per(args.categoria), "creato": datetime.now().isoformat(timespec="seconds")}
    scrivi_json(ETICHETTE, etichette)
    print(f"{caso_id}: {args.categoria} da {etichette[caso_id]['origine']}")


# ================================================================== esegui
def giudica(caso_dir, args):
    """Una chiamata al Referee vero (bridge review, cli): stesso percorso del loop, codice rieseguito."""
    cmd = [sys.executable, str(BRIDGE), "review", "--workdir", str(caso_dir), "--run-code", "--timeout", str(args.timeout)]
    if args.offline:
        cmd.append("--offline")   # solo controlli esatti e riesecuzione del codice: per provare la catena, non per misurare
    for flag, valore in (("--model", args.model), ("--model-b", args.model_b)):
        if valore:
            cmd += [flag, valore]
    esito = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if esito.returncode != 0:
        raise RuntimeError(f"bridge fallito su {caso_dir.name}: {esito.stderr[-600:]}")


def estrai_verdetti(caso_dir):
    """Dal packet salvato dal bridge: verdetto di A, di B, esito unificato, errore fatale, costo."""
    packet = leggi_json(caso_dir / "attempts" / "packet_001.json", {})
    report = leggi_json(caso_dir / "referee_report.json", {})
    a = (packet.get("math") or {}).get("report") or {}
    b = (packet.get("evidence") or {}).get("report") or {}
    return {"A": a.get("mathematical_verdict", "UNAVAILABLE"), "B": b.get("evidence_verdict", "UNAVAILABLE"),
            "esito": report.get("esito"), "fatal_error": report.get("fatal_error"),
            "costo_usd": sum(u.get("cost_usd") or 0 for u in report.get("usage", []))}


def cmd_esegui(args):
    """Giudica ogni caso N volte e appende una riga per ripetizione a risultati.jsonl (mai sovrascritto)."""
    etichette = leggi_json(ETICHETTE, {})
    casi = args.casi or sorted(etichette)
    with open(RISULTATI, "a", encoding="utf-8") as out:
        for caso_id in casi:
            for ripetizione in range(1, args.ripetizioni + 1):
                giudica(BANCO / caso_id, args)
                riga = {"caso": caso_id, "ripetizione": ripetizione, "ts": datetime.now().isoformat(timespec="seconds"),
                        "model": args.model, "model_b": args.model_b, **estrai_verdetti(BANCO / caso_id)}
                print(f"{caso_id} #{ripetizione}: A={riga['A']} B={riga['B']} esito={riga['esito']}")
                if not args.offline:   # senza modelli non c'è nulla da misurare: la riga non entra nei risultati
                    out.write(json.dumps(riga, ensure_ascii=False) + "\n")
                    out.flush()


# ================================================================== tabella
def classifica(atteso, ottenuto, giudice):
    """Per un giudice: 'ok', 'falso_accettato' (doveva cadere, è passata), 'falso_rifiutato' (doveva passare, è caduta),
    oppure None se per quella categoria il giudice non è chiamato in causa."""
    if atteso is None or ottenuto in ("UNAVAILABLE", None):
        return None
    passa = ottenuto in ("PASS", "READY_FOR_HUMAN")
    if atteso in ("PASS", "READY_FOR_HUMAN"):
        return "ok" if passa else "falso_rifiutato"
    return "falso_accettato" if passa else "ok"


def conteggi(righe, etichette):
    """Conteggi per giudice e per categoria: {giudice: {categoria: Counter(ok/falso_accettato/falso_rifiutato)}}."""
    tabella = {g: defaultdict(Counter) for g in ("A", "B", "esito")}
    for r in righe:
        info = etichette.get(r["caso"])
        if not info:
            continue
        for giudice in ("A", "B", "esito"):
            classe = classifica(info["atteso"][giudice], r.get(giudice), giudice)
            if classe:
                tabella[giudice][info["categoria"]][classe] += 1
    return tabella


def stampa_tabella(tabella):
    """Matrice leggibile: una riga per categoria, tre blocchi (A, B, merge) con ok / FA / FR."""
    print(f"{'categoria':<26}" + "".join(f"{g:>22}" for g in ("A (matematica)", "B (evidenza)", "merge")))
    print(f"{'':<26}" + "".join(f"{'ok  FA  FR':>22}" for _ in range(3)))
    for categoria in CATEGORIE:
        celle = []
        for giudice in ("A", "B", "esito"):
            c = tabella[giudice].get(categoria)
            celle.append(f"{c['ok']:>4}{c['falso_accettato']:>4}{c['falso_rifiutato']:>4}" if c else f"{'—':>12}")
        print(f"{categoria:<26}" + "".join(f"{cella:>22}" for cella in celle))
    print("\nFA = falso accettato (doveva cadere), FR = falso rifiutato (doveva passare). '—' = giudice non in causa.")


def cmd_tabella(args):
    etichette = leggi_json(ETICHETTE, {})
    righe = [json.loads(l) for l in RISULTATI.read_text(encoding="utf-8").splitlines() if l.strip()] if RISULTATI.exists() else []
    if not righe:
        print("nessun risultato: lancia prima `esegui`")
        return 1
    stampa_tabella(conteggi(righe, etichette))
    print(f"\nrighe: {len(righe)}  casi: {len({r['caso'] for r in righe})}  "
          f"spesa equivalente: ${sum(r.get('costo_usd') or 0 for r in righe):.2f}")
    return 0


# ================================================================== argparse
def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("crea", help="registra un caso: da un run del loop o come variante di un caso")
    c.add_argument("--run", help="cartella runs/pN_cK di origine")
    c.add_argument("--attempt", default="attempt_001", help="tentativo da copiare (es. attempt_002)")
    c.add_argument("--da", help="caso esistente da cui derivare la variante (es. caso_01)")
    c.add_argument("--categoria", required=True, choices=CATEGORIE)
    c.add_argument("--proof-file", help="file con la prova modificata (variante con errore piantato)")
    c.add_argument("--nota", help="dove sta l'errore, per chi confronta con fatal_error")
    e = sub.add_parser("esegui", help="giudica i casi con il Referee vero (consuma quota)")
    e.add_argument("--casi", nargs="*")
    e.add_argument("--ripetizioni", type=int, default=1)
    e.add_argument("--model")
    e.add_argument("--model-b")
    e.add_argument("--timeout", type=float, default=600)
    e.add_argument("--offline", action="store_true", help="nessun modello: verifica solo che la catena giri")
    sub.add_parser("tabella", help="matrice falsi accettati / falsi rifiutati per giudice e categoria")
    return p


def main():
    args = build_parser().parse_args()
    if args.cmd == "crea" and not (args.run or args.da):
        build_parser().error("serve --run oppure --da")
    return {"crea": cmd_crea, "esegui": cmd_esegui, "tabella": cmd_tabella}[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
