#!/usr/bin/env python3
"""Dashboard a celle nel terminale, in sola lettura, per seguire il loop mentre gira.

Legge le cartelle runs/pN_cK/ (state, referee_report, approval, loop_log) e i metadati di costo
dei tentativi. Non tocca nulla: il loop resta l'unica cosa che scrive.

Uso:
  .venv/bin/python tools/dashboard.py          # interattiva (curses): frecce, Invio, r, q
  .venv/bin/python tools/dashboard.py --once   # stampa la griglia una volta ed esce
"""
import argparse
import curses
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
RUNS = RADICE / "runs"
# Problemi e celle vengono dal manifesto runs/celle.json: un nuovo insieme di problemi non richiede di toccare il
# codice. Se il file manca si torna alla griglia della gara (4 problemi × 6 celle).
try:
    MANIFESTO = json.loads((RUNS / "celle.json").read_text())
except (OSError, ValueError):
    MANIFESTO = {}
PROBLEMI = list(MANIFESTO) or ["p1", "p2", "p3", "p4"]
CELLE = sorted({c for voce in MANIFESTO.values() for c in voce.get("cells", {})} or set("123456"), key=int)
# Punti della gara (1/2/3/5/8/13); una voce del manifesto può dichiarare i propri con `punti` ({} = senza punti).
PUNTI_GARA = {"1": 1, "2": 2, "3": 3, "4": 5, "5": 8, "6": 13}
# Stato → (etichetta corta, coppia colore curses). Le etichette sono spiegate nella legenda a schermo.
STATI = {"ok": ("✔ ok", 1), "cand": ("~ cand", 2), "loop": ("● loop", 3), "rej": ("✗ rej", 4),
         "unk": ("? unk", 5), "parz": ("~ parz", 5), "none": ("· -", 0), "nd": ("", 0)}
INTERVALLO_REFRESH = 2.0  # secondi tra due riletture dei file


# ================================================================== lettura dei file (nessuna scrittura)
def leggi_json(percorso):
    """Ritorna il JSON del file oppure {} se manca o è corrotto: la dashboard non deve mai cadere."""
    try:
        return json.loads(Path(percorso).read_text())
    except (OSError, ValueError):
        return {}


def somma_costi(oggetto):
    """Somma ricorsivamente ogni campo `cost_usd` dentro un JSON: i tentativi lo tengono in `meta`,
    i report del Referee dentro la lista `usage`. È l'equivalente USD stimato dalla CLI, non un addebito."""
    if isinstance(oggetto, dict):
        return sum(float(v) if k == "cost_usd" and isinstance(v, (int, float)) else somma_costi(v)
                   for k, v in oggetto.items())
    if isinstance(oggetto, list):
        return sum(somma_costi(x) for x in oggetto)
    return 0.0


def costo_cella(cartella):
    """Equivalente USD di tutti i tentativi e verdetti salvati in runs/pN_cK/attempts/."""
    return sum(somma_costi(leggi_json(f)) for f in (cartella / "attempts").glob("*.json"))


def loop_attivo(cartella):
    """True se un processo loop.py sta girando su questa cartella (cerca il --workdir nella riga di comando)."""
    try:
        esito = subprocess.run(["pgrep", "-f", f"loop.py --workdir {cartella.relative_to(RADICE)}"],
                               capture_output=True, text=True)
        return esito.returncode == 0
    except OSError:
        return False


def bozza_esiste(problema, cella):
    """Una bozza di submission (anche solo parziale) per problema-N/submission/parte-K.md."""
    return (RADICE / f"problema-{problema[1:]}" / "submission" / f"parte-{cella}.md").exists()


def stati_da_status_md():
    """Legge STATUS.md e ritorna {(problema, cella): stato}. Serve per le celle chiuse a mano prima che
    esistesse il loop (es. problema 2 parti 1-2), che non hanno approval.json in runs/."""
    stati, problema = {}, None
    try:
        righe = (RADICE / "STATUS.md").read_text().splitlines()
    except OSError:
        return stati
    for riga in righe:
        if riga.startswith("## Problema "):
            problema = "p" + riga.split()[2]
        elif problema and riga.startswith("| ") and riga[2] in CELLE and riga[3] == " ":
            colonne = [c.strip() for c in riga.split("|")]
            stati[(problema, riga[2])] = colonne[3] if len(colonne) > 3 else ""
    return stati


def stato_cella(problema, cella, status_md):
    """Decide lo stato di una cella con regole in ordine di priorità: firma umana (approval.json o
    "revisionato" in STATUS.md) > loop attivo > verdetto del Referee > bozza presente > niente.
    Ritorna (stato, ultima riga del loop_log)."""
    cartella = RUNS / f"{problema}_c{cella}"
    approvazione = leggi_json(cartella / "approval.json")
    report = leggi_json(cartella / "referee_report.json")
    ultima = ultima_riga_log(cartella)
    if approvazione.get("approved_by") or status_md.get((problema, cella)) == "revisionato":
        return "ok", ultima
    if loop_attivo(cartella):
        return "loop", ultima
    esito = esito_del_report(report)
    if esito == "READY_FOR_HUMAN":
        return "cand", ultima
    if esito in ("REJECT", "COUNTEREXAMPLE_FOUND"):
        return "rej", ultima
    if esito:
        return "unk", ultima
    return ("parz" if bozza_esiste(problema, cella) else "none"), ultima


def esito_del_report(report):
    """Esito unificato di un referee_report: il campo `esito` se c'è, altrimenti la stessa regola dei report
    vecchi (READY_FOR_HUMAN vince, poi `verdict`). Stringa vuota se non c'è nessun verdetto."""
    if not report:
        return ""
    if report.get("esito"):
        return report["esito"]
    if report.get("review_status") == "READY_FOR_HUMAN":
        return "READY_FOR_HUMAN"
    return report.get("verdict", "")


def righe_log(cartella):
    """Tutte le righe di loop_log.jsonl come dizionari, saltando quelle malformate."""
    righe = []
    try:
        for riga in (cartella / "loop_log.jsonl").read_text().splitlines():
            try:
                righe.append(json.loads(riga))
            except ValueError:
                continue
    except OSError:
        pass
    return righe


def ultima_riga_log(cartella):
    """L'ultima decisione registrata dal loop, oppure {} se il loop non ha mai girato qui."""
    righe = righe_log(cartella)
    return righe[-1] if righe else {}


def titolo_problema(problema, celle_json):
    """Titolo breve del problema da runs/celle.json (prime due parole), con fallback al codice."""
    titolo = celle_json.get(problema, {}).get("title", problema)
    return titolo[:10]


def celle_del_problema(problema):
    """Le celle che il manifesto dichiara per il problema (tutte, se il problema non è nel manifesto)."""
    return list(MANIFESTO.get(problema, {}).get("cells", {})) or CELLE


def punti_cella(problema, cella):
    """Punti di una cella: quelli dichiarati nel manifesto, altrimenti la scala della gara."""
    return MANIFESTO.get(problema, {}).get("punti", PUNTI_GARA).get(cella, 0)


def raccogli():
    """Fotografia completa: per ogni problema le sue celle con stato, punti ottenuti e spesa equivalente.
    Le colonne che il problema non ha restano vuote ("nd")."""
    celle_json = leggi_json(RUNS / "celle.json")
    status_md = stati_da_status_md()
    quadro = []
    for problema in PROBLEMI:
        proprie = celle_del_problema(problema)
        celle = {c: stato_cella(problema, c, status_md) if c in proprie else ("nd", {}) for c in CELLE}
        punti = sum(punti_cella(problema, c) for c, (stato, _) in celle.items() if stato == "ok")
        spesa = sum(costo_cella(RUNS / f"{problema}_c{c}") for c in proprie)
        quadro.append({"id": problema, "titolo": titolo_problema(problema, celle_json), "celle": celle,
                       "punti": punti, "massimo": sum(punti_cella(problema, c) for c in proprie), "spesa": spesa})
    return quadro


# ================================================================== rendering testuale (usato da --once)
def riga_problema(voce):
    """Una riga della griglia: codice, titolo, sei celle, punti e spesa."""
    celle = "  ".join(f"{STATI[voce['celle'][c][0]][0]:<7}" for c in CELLE)
    return f" {voce['id'][1:]:<2} {voce['titolo']:<10} {celle} {voce['punti']:>3}/{voce['massimo']:<2}  ${voce['spesa']:>6.2f}"


def testo_griglia(quadro):
    """Griglia completa come lista di righe, pronta sia per print sia per curses."""
    totale = sum(v["spesa"] for v in quadro)
    ora = datetime.now().strftime("%H:%M:%S")
    righe = [f" PROOF PURSUIT{'':<14}aggiornato {ora}{'':<12}quota equiv. ${totale:.2f}", " " + "─" * 78,
             f" problema      " + "  ".join(f"{c:<7}" for c in CELLE) + "  punti   spesa"]
    righe += [riga_problema(v) for v in quadro]
    righe += [" " + "─" * 78,
              " ok=approvata  cand=READY_FOR_HUMAN senza firma  loop=in esecuzione  parz=solo bozza",
              " rej=ultimo verdetto REJECT  unk=UNKNOWN_STATUS  spesa=equivalente USD della CLI, non addebito"]
    return righe


def testo_dettaglio(voce, cella):
    """Riassunto dell'ultima iterazione della cella selezionata: famiglia, verdetto, errore fatale."""
    stato, ultima = voce["celle"][cella]
    testa = f" ▸ {voce['id']}_c{cella}  stato {stato}"
    if not ultima:
        return [testa + "  (nessuna iterazione registrata)"]
    return [testa + f"  iter {ultima.get('iter', '?')}  famiglia {ultima.get('family', '?')}"
            f"  ·  esito {ultima.get('esito') or esito_del_report(ultima)}",
            f"   errore fatale: {(ultima.get('fatal_error') or '—')[:150]}",
            f"   prossimo blocco: {(ultima.get('next_blocker') or '—')[:150]}"]


# ================================================================== interfaccia curses
def prepara_colori():
    """Coppie colore per gli stati: verde ok, ciano candidata, giallo loop, rosso rifiutata, grigio altro."""
    curses.start_color()
    curses.use_default_colors()
    for indice, colore in enumerate([curses.COLOR_GREEN, curses.COLOR_CYAN, curses.COLOR_YELLOW,
                                     curses.COLOR_RED, curses.COLOR_WHITE], start=1):
        curses.init_pair(indice, colore, -1)


def scrivi(schermo, y, testo, attributi=0):
    """Scrive una riga troncandola alla larghezza del terminale; ignora gli errori ai bordi."""
    altezza, larghezza = schermo.getmaxyx()
    if 0 <= y < altezza:
        try:
            schermo.addstr(y, 0, testo[: larghezza - 1], attributi)
        except curses.error:
            pass


def disegna_griglia(schermo, quadro, selezione):
    """Griglia con la cella selezionata evidenziata e ogni stato nel proprio colore."""
    righe = testo_griglia(quadro)
    for y, riga in enumerate(righe[:3]):
        scrivi(schermo, y, riga, curses.A_BOLD if y == 0 else 0)
    for i, voce in enumerate(quadro):
        scrivi(schermo, 3 + i, riga_problema(voce))
        for j, c in enumerate(CELLE):
            etichetta, coppia = STATI[voce["celle"][c][0]]
            evidenzia = curses.A_REVERSE if (i, j) == selezione else 0
            scrivi_cella(schermo, 3 + i, 15 + j * 9, etichetta, curses.color_pair(coppia) | evidenzia)
    for k, riga in enumerate(righe[3 + len(quadro):]):
        scrivi(schermo, 3 + len(quadro) + k, riga, curses.A_DIM)
    return 3 + len(righe)


def scrivi_cella(schermo, y, x, testo, attributi):
    """Sovrascrive una singola etichetta di cella con colore ed evidenziazione."""
    try:
        schermo.addstr(y, x, testo, attributi)
    except curses.error:
        pass


def disegna_dettaglio(schermo, quadro, selezione, y, mostra_log):
    """Pannello inferiore: ultima iterazione della cella selezionata e, se richiesto, il loop_log intero."""
    i, j = selezione
    voce, cella = quadro[i], CELLE[j]
    for riga in testo_dettaglio(voce, cella):
        scrivi(schermo, y, riga)
        y += 1
    if mostra_log:
        y = disegna_log(schermo, RUNS / f"{voce['id']}_c{cella}", y + 1)
    scrivi(schermo, y + 1, " [↑↓←→] cella  [Invio] loop_log  [r] refresh  [q] esci", curses.A_DIM)


def disegna_log(schermo, cartella, y):
    """Le ultime iterazioni del loop_log della cella, una riga ciascuna, quante ne entrano a schermo."""
    altezza = schermo.getmaxyx()[0]
    righe = righe_log(cartella)
    if not righe:
        scrivi(schermo, y, "   loop_log.jsonl assente")
        return y + 1
    for r in righe[-(altezza - y - 3):]:
        scrivi(schermo, y, f"   {r.get('ts', '')}  iter {r.get('iter', '?')}  {r.get('family', '?'):<16}"
                            f" {(r.get('esito') or esito_del_report(r)):<18} {(r.get('fatal_error') or '')[:70]}")
        y += 1
    return y


def muovi(selezione, tasto):
    """Sposta la selezione con le frecce restando dentro la griglia 4×6."""
    i, j = selezione
    if tasto == curses.KEY_UP:
        i = max(0, i - 1)
    elif tasto == curses.KEY_DOWN:
        i = min(len(PROBLEMI) - 1, i + 1)
    elif tasto == curses.KEY_LEFT:
        j = max(0, j - 1)
    elif tasto == curses.KEY_RIGHT:
        j = min(len(CELLE) - 1, j + 1)
    return i, j


def ciclo(schermo):
    """Loop principale: rilegge i file ogni INTERVALLO_REFRESH secondi e ridisegna; i tasti sono non bloccanti."""
    curses.curs_set(0)
    schermo.timeout(200)
    prepara_colori()
    selezione, mostra_log, quadro, ultimo_refresh = (0, 0), False, raccogli(), time.time()
    while True:
        if time.time() - ultimo_refresh > INTERVALLO_REFRESH:
            quadro, ultimo_refresh = raccogli(), time.time()
        schermo.erase()
        y = disegna_griglia(schermo, quadro, selezione)
        disegna_dettaglio(schermo, quadro, selezione, y, mostra_log)
        schermo.refresh()
        tasto = schermo.getch()
        if tasto in (ord("q"), ord("Q")):
            return
        if tasto == ord("r"):
            quadro, ultimo_refresh = raccogli(), time.time()
        elif tasto in (curses.KEY_ENTER, 10, 13):
            mostra_log = not mostra_log
        else:
            selezione = muovi(selezione, tasto)


def main():
    """--once stampa la griglia e il dettaglio di ogni cella con un loop_log; altrimenti apre curses."""
    parser = argparse.ArgumentParser(description="Dashboard a celle di Proof Pursuit (sola lettura)")
    parser.add_argument("--once", action="store_true", help="stampa una volta ed esci, senza interattività")
    args = parser.parse_args()
    if not args.once:
        curses.wrapper(ciclo)
        return
    quadro = raccogli()
    print("\n".join(testo_griglia(quadro)))
    for voce in quadro:
        for cella in CELLE:
            if voce["celle"][cella][1]:
                print("\n".join(testo_dettaglio(voce, cella)))


if __name__ == "__main__":
    main()
