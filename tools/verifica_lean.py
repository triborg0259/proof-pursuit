#!/usr/bin/env python3
"""
verifica_lean.py — compila un file Lean 4 con Mathlib (progetto lean/ del repo) e dice cosa certifica davvero.

Cosa controlla: (1) il file compila (exit 0, nessun errore); (2) nessun `sorry` (anche `admit` lo produce);
(3) gli assiomi da cui dipende il teorema indicato (`#print axioms`) sono solo quelli standard di Mathlib:
propext, Classical.choice, Quot.sound. Un `axiom` dichiarato nel file o `native_decide` (Lean.ofReduceBool,
fiducia nel compilatore) compaiono qui e fanno fallire il controllo.
Perché: è l'unico verificatore della pipeline che non è un modello. Certifica però solo l'enunciato Lean: che
coincida con l'enunciato della cella resta un giudizio (Referee A, poi la firma umana).
Uso: python3 tools/verifica_lean.py FILE.lean --teorema NOME [--timeout 600]   → JSON su stdout, exit 0 se ok
Lo usano il Researcher (nella sua sandbox) e l'orchestratore (researcher/bridge_referee.py, sulla copia pulita).
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

PROGETTO = Path(__file__).resolve().parents[1] / "lean"
ASSIOMI_STANDARD = {"propext", "Classical.choice", "Quot.sound"}
# Un nome Lean qualificato (es. Verifica.inv_nat_tendsto); niente spazi né a capo da accodare al file.
NOME_VALIDO = re.compile(r"^[A-Za-z_][\w.'!?₀-₉]*$")


def compila(file_lean, teorema, timeout=600):
    """Compila una copia del file con in coda `#print axioms teorema`; ritorna (exit, output, secondi).
    exit None = tempo scaduto. La copia sta accanto all'originale e viene tolta alla fine."""
    originale = Path(file_lean).resolve()
    copia = originale.with_name(originale.stem + "_verifica.lean")
    copia.write_text(originale.read_text(encoding="utf-8") + f"\n\n#print axioms {teorema}\n", encoding="utf-8")
    inizio = time.time()
    try:
        res = subprocess.run(["lake", "env", "lean", str(copia)], cwd=PROGETTO, capture_output=True, text=True,
                             timeout=timeout)
        return res.returncode, res.stdout + res.stderr, time.time() - inizio
    except subprocess.TimeoutExpired:
        return None, f"TIMEOUT after {timeout}s", time.time() - inizio
    finally:
        copia.unlink(missing_ok=True)


def assiomi_del_teorema(output):
    """Gli assiomi stampati da `#print axioms` (l'ultima stampa del file); None se la stampa manca, cioè il
    teorema non esiste o il file non compila fino in fondo."""
    stampe = re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]", output, re.S)
    if stampe:
        return [a.strip() for a in stampe[-1][1].split(",") if a.strip()]
    return [] if re.search(r"'[^']+' does not depend on any axioms", output) else None


def analizza(exit_code, output):
    """Esito strutturato dall'output di Lean. Funzione pura: i test la provano senza Lean installato."""
    errori = [riga.strip() for riga in output.splitlines() if re.search(r":\d+:\d+: error", riga)]
    sorry = bool(re.search(r"declaration uses .sorry.", output))
    assiomi = assiomi_del_teorema(output)
    standard = assiomi is not None and set(assiomi) <= ASSIOMI_STANDARD
    ok = exit_code == 0 and not errori and not sorry and standard
    return {"ok": ok, "exit": exit_code, "errori": errori[:5], "sorry": sorry, "assiomi": assiomi,
            "solo_assiomi_standard": standard}


def riassunto(esito, teorema, secondi):
    """Una riga leggibile dal giudice B, come per la riesecuzione degli script Python."""
    if esito["exit"] is None:
        return f"Lean: TIMEOUT after {secondi:.0f}s compiling theorem {teorema}: not verified"
    stato = "VERIFIED" if esito["ok"] else "NOT VERIFIED"
    dettagli = (f"exit {esito['exit']} in {secondi:.1f}s; errors: {esito['errori'] or 'none'}; sorry: "
                f"{'yes' if esito['sorry'] else 'no'}; axioms of {teorema}: {esito['assiomi']} "
                f"(standard only: {'yes' if esito['solo_assiomi_standard'] else 'no'})")
    return f"Lean 4 + Mathlib ({PROGETTO.name}/ project): theorem {teorema} {stato}; {dettagli}"


def verifica(file_lean, teorema, timeout=600):
    """Compila e analizza; ritorna (esito, riga di riassunto). Un nome di teorema non valido non si compila."""
    if not NOME_VALIDO.match(teorema or ""):
        esito = {"ok": False, "exit": -1, "errori": [f"invalid theorem name {teorema!r}"], "sorry": False,
                 "assiomi": None, "solo_assiomi_standard": False}
        return esito, f"Lean: not compiled, invalid theorem name {teorema!r}"
    exit_code, output, secondi = compila(file_lean, teorema, timeout)
    esito = analizza(exit_code, output)
    esito["secondi"] = round(secondi, 1)
    return esito, riassunto(esito, teorema, secondi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file")
    parser.add_argument("--teorema", required=True, help="nome qualificato del teorema principale")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    esito, riga = verifica(args.file, args.teorema, args.timeout)
    print(json.dumps({**esito, "riassunto": riga}, ensure_ascii=False, indent=1))
    sys.exit(0 if esito["ok"] else 1)
