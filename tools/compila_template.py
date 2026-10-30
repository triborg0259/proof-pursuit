#!/usr/bin/env python3
"""
compila_template.py — riempie un template LaTeX di consegna (es. un assignment con blocchi SOLUTION vuoti) con le
risposte delle celle chiuse dal loop e scrive un unico file .tex.

Cosa fa: per ogni problema indicato, nell'ordine, prende l'elenco `\\begin{enumerate}...\\end{enumerate}` che segue
l'n-esimo marcatore (default `\\textbf{SOLUTION}`) e mette in ogni `\\item` la risposta della cella corrispondente
(primo item = cella 1, …). La risposta è il `proof_attempt` del tentativo scelto, convertito da Markdown+LaTeX a
LaTeX con pandoc.
Quale tentativo: quello firmato in approval.json; in mancanza l'ultimo arrivato a READY_FOR_HUMAN. Una cella senza
nessuno dei due resta segnalata nel .tex (mai riempita con un tentativo respinto) e il comando esce con codice 1.
Perché: nella consegna entra solo ciò che ha passato il Referee; la firma resta umana.
Uso: .venv/bin/python tools/compila_template.py --template T.tex --output OUT.tex p5 p6 p7 p8 \\
        [--sostituisci 'VECCHIO=>NUOVO' ...] [--marcatore '\\textbf{SOLUTION}']
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
# Caratteri che pdflatex con inputenc utf8 non conosce: si riscrivono in LaTeX. \ensuremath vale in testo e formula.
UNICODE = {"—": "---", "–": "--", "’": "'", "‘": "`", "“": "``", "”": "''", "…": "\\ldots{}", "−": "\\ensuremath{-}",
           "≤": "\\ensuremath{\\le}", "≥": "\\ensuremath{\\ge}", "≠": "\\ensuremath{\\neq}", "≈": "\\ensuremath{\\approx}",
           "→": "\\ensuremath{\\to}", "⇒": "\\ensuremath{\\Rightarrow}", "⟹": "\\ensuremath{\\Longrightarrow}",
           "⇔": "\\ensuremath{\\Leftrightarrow}", "∞": "\\ensuremath{\\infty}", "∈": "\\ensuremath{\\in}",
           "×": "\\ensuremath{\\times}", "·": "\\ensuremath{\\cdot}", "±": "\\ensuremath{\\pm}", "√": "\\ensuremath{\\surd}",
           "ε": "\\ensuremath{\\varepsilon}", "π": "\\ensuremath{\\pi}", "δ": "\\ensuremath{\\delta}",
           "\u00a0": "~", "\u2009": "\\,", "\u202f": "\\,"}
# Lettere accentate latine: inputenc utf8 le gestisce, non vanno segnalate.
LATINE = set("àèéìòùÀÈÉÌÒÙáíóúçñäöüÄÖÜß")


# ================================================================== scelta del tentativo
def righe_log(run):
    """Righe di loop_log.jsonl della cella, saltando quelle malformate."""
    righe = []
    percorso = RUNS / run / "loop_log.jsonl"
    for riga in (percorso.read_text(encoding="utf-8").splitlines() if percorso.exists() else []):
        try:
            righe.append(json.loads(riga))
        except ValueError:
            continue
    return righe


def _numero(attempt_id):
    """'attempt_007' → 7."""
    return int(attempt_id.split("_")[1])


def tentativo_scelto(run, minimo=1):
    """(tentativo, provenienza) per la cella: prima la firma umana, poi l'ultimo READY_FOR_HUMAN; (None, motivo)
    se non c'è nessuno dei due. Un tentativo respinto non viene mai usato. Con minimo > 1 i tentativi precedenti
    non contano: servono quando le regole di consegna sono cambiate dopo un primo giro."""
    firma = RUNS / run / "approval.json"
    if firma.exists():
        dati = json.loads(firma.read_text(encoding="utf-8"))
        if _numero(dati["attempt_id"]) >= minimo:
            return _carica(run, dati["attempt_id"]), f"approvato da {dati.get('approved_by', '?')}"
    pronti = [r for r in righe_log(run) if "READY_FOR_HUMAN" in (r.get("review_status"), r.get("esito"))
              and _numero(r["attempt_id"]) >= minimo]
    if pronti:
        return _carica(run, pronti[-1]["attempt_id"]), "Referee READY_FOR_HUMAN, firma umana mancante"
    ultimo = (righe_log(run) or [{}])[-1]
    return None, f"nessun tentativo pronto (ultimo esito: {ultimo.get('esito') or ultimo.get('verdict') or 'nessuno'})"


def _carica(run, attempt_id):
    """Il JSON del tentativo attempt_id della cella."""
    return json.loads((RUNS / run / "attempts" / f"{attempt_id}.json").read_text(encoding="utf-8"))


# ================================================================== da Markdown+LaTeX a LaTeX
def md_a_latex(testo):
    """Converte il proof_attempt con pandoc; gli ambienti LaTeX grezzi (tikzpicture, tabular) passano intatti.
    Gli elenchi attaccati al paragrafo precedente (stile dei modelli) restano elenchi e non righe con un trattino."""
    esito = subprocess.run(["pandoc", "-f", "markdown-auto_identifiers+lists_without_preceding_blankline", "-t", "latex",
                            "--wrap=preserve"],
                           input=testo, capture_output=True, text=True, check=True)
    return adatta_larghezza(sostituisci_unicode(titoli_in_grassetto(elenchi_annidati(esito.stdout)))).strip()


def elenchi_annidati(latex):
    """pandoc scrive gli elenchi come se fossero al primo livello (enumi), ma nel template stanno dentro l'elenco
    delle SOLUTION: un suo \\setcounter{enumi} sposterebbe la numerazione delle Part (A, F, G invece di A, B, C;
    succede con un paragrafo che inizia con "(F)"). Si scala ogni riferimento di un livello."""
    sotto = {"i": "ii", "ii": "iii", "iii": "iv"}
    return re.sub(r"enum(iii|ii|i)(?![a-z])", lambda m: "enum" + sotto[m.group(1)], latex)


def adatta_larghezza(latex):
    """Formule in display, disegni TikZ e tabelle più larghi della riga si rimpiccioliscono fino a starci (adjustbox
    `max width`): quelli che già stanno non cambiano e il testo matematico resta identico. Perché: i modelli
    scrivono frazioni esatte lunghe decine di cifre che escono dal margine."""
    latex = re.sub(r"(?<!\\)\\\[(.*?)(?<!\\)\\\]", _display_adattato, latex, flags=re.S)
    # In una formula in linea TeX non va a capo dopo una virgola: gli elenchi di valori uscirebbero dal margine.
    latex = re.sub(r"(?<!\\)\\\((.*?)(?<!\\)\\\)",
                   lambda m: "\\(" + re.sub(r",(?=\\ |\\,|\s)", ",\\\\allowbreak", m.group(1)) + "\\)", latex, flags=re.S)
    return re.sub(r"(\\begin\{(tikzpicture|tabular)\}.*?\\end\{\2\})",
                  lambda m: "\\begin{adjustbox}{max width=\\linewidth}\n" + m.group(1) + "\n\\end{adjustbox}",
                  latex, flags=re.S)


def _display_adattato(m):
    """Un \\[...\\] con il contenuto in una scatola larga al più una riga; un eventuale \\tag resta fuori."""
    corpo, tag = m.group(1), ""
    etichetta = re.search(r"\\tag\*?\{(?:[^{}]|\{[^{}]*\})*\}", corpo)
    if etichetta:
        corpo, tag = corpo.replace(etichetta.group(0), ""), etichetta.group(0)
    return f"\\[\\adjustbox{{max width=\\linewidth}}{{$\\displaystyle {corpo.strip()}$}}{tag}\\]"


def _fine_graffa(testo, inizio):
    """Indice subito dopo la graffa che chiude quella aperta in testo[inizio] (le formule nei titoli ne hanno)."""
    livello = 0
    for i in range(inizio, len(testo)):
        livello += {"{": 1, "}": -1}.get(testo[i], 0)
        if livello == 0:
            return i + 1
    raise ValueError("graffa non chiusa in un titolo")


def titoli_in_grassetto(latex):
    """I titoli Markdown diventano \\section dopo pandoc, che dentro un \\item romperebbe la numerazione del
    template: si trasformano in paragrafi con titolo in grassetto."""
    uscita, pos = [], 0
    for m in re.finditer(r"\\(?:sub)*section\*?(?=\{)", latex):
        if m.start() < pos:
            continue
        fine = _fine_graffa(latex, m.end())
        uscita += [latex[pos:m.start()], "\\par\\medskip\\noindent\\textbf", latex[m.end():fine], "\\par\\smallskip"]
        pos = fine
    return togli_texorpdfstring("".join(uscita) + latex[pos:])


def togli_texorpdfstring(latex):
    """pandoc scrive \\texorpdfstring{formula}{testo} nei titoli con formule; esiste solo con hyperref, e senza
    segnalibri PDF basta il primo argomento."""
    while (inizio := latex.find("\\texorpdfstring{")) >= 0:
        fine_primo = _fine_graffa(latex, inizio + len("\\texorpdfstring"))
        fine_secondo = _fine_graffa(latex, fine_primo)
        latex = latex[:inizio] + latex[inizio + len("\\texorpdfstring") + 1:fine_primo - 1] + latex[fine_secondo:]
    return latex


def sostituisci_unicode(latex):
    """Riscrive in LaTeX i caratteri che pdflatex non conosce (vedi UNICODE)."""
    return "".join(UNICODE.get(c, c) for c in latex)


def non_ascii_residui(latex):
    """Caratteri non ASCII rimasti dopo la sostituzione: vanno segnalati perché pdflatex si fermerebbe."""
    return sorted({c for c in latex if ord(c) > 127 and c not in LATINE})


# ================================================================== riempimento del template
def blocchi_soluzione(template, marcatore):
    """Posizioni (inizio, fine) del contenuto di ogni enumerate che segue il marcatore, nell'ordine."""
    schema = re.escape(marcatore) + r"\s*\\begin\{enumerate\}(.*?)\\end\{enumerate\}"
    return [m.span(1) for m in re.finditer(schema, template, re.S)]


def riempi_blocco(contenuto, risposte):
    """Rifà l'elenco con una voce per risposta; il numero di \\item vuoti del template deve coincidere."""
    vuoti = len(re.findall(r"\\item\b", contenuto))
    if vuoti != len(risposte):
        raise ValueError(f"il template ha {vuoti} \\item ma le celle sono {len(risposte)}")
    return "\n" + "\n\n".join(f"    \\item\n{r}" for r in risposte) + "\n"


def riempi_template(template, marcatore, risposte_per_problema):
    """Sostituisce i blocchi dal fondo, così le posizioni di quelli precedenti restano valide."""
    blocchi = blocchi_soluzione(template, marcatore)
    if len(blocchi) < len(risposte_per_problema):
        raise ValueError(f"marcatore trovato {len(blocchi)} volte, problemi {len(risposte_per_problema)}")
    for (inizio, fine), risposte in reversed(list(zip(blocchi, risposte_per_problema))):
        template = template[:inizio] + riempi_blocco(template[inizio:fine], risposte) + template[fine:]
    return template


def completa_preambolo(latex):
    """Aggiunge prima di \\begin{document} solo i pacchetti che le risposte usano davvero."""
    extra = ["\\providecommand{\\tightlist}{\\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}",
             "\\setlength{\\emergencystretch}{3em}  % righe con formule lunghe: spazi più larghi invece di uscire"]
    if "\\adjustbox" in latex:
        extra.append("\\usepackage{adjustbox}")
    if "\\begin{axis}" in latex and "{pgfplots}" not in latex:
        extra += ["\\usepackage{pgfplots}", "\\pgfplotsset{compat=1.18}"]
    if re.search(r"\\(href|url)\{", latex) and "{hyperref}" not in latex:
        extra.append("\\usepackage{hyperref}")
    if "\\begin{longtable}" in latex:
        extra += ["\\usepackage{longtable}", "\\usepackage{booktabs}"]
    return latex.replace("\\begin{document}", "\n".join(extra) + "\n\n\\begin{document}", 1)


# ================================================================== comando
def risposta_cella(run, minimo=1, limite=None):
    """(testo LaTeX per l'item, mancante?, avviso). Il testo porta un commento che dice da quale tentativo viene;
    l'avviso segnala una risposta oltre il limite di lunghezza della cella (`lunghezza_max` nel manifesto)."""
    tentativo, provenienza = tentativo_scelto(run, minimo)
    if tentativo is None:
        visibile = f"{run}, {provenienza}".replace("_", "\\_")  # il trattino basso fuori formula ferma pdflatex
        return f"% {run}: {provenienza}\n\\textbf{{[Risposta mancante: {visibile}]}}", True, ""
    testa = f"% fonte: runs/{run}/attempts/{tentativo['attempt_id']}.json ({provenienza})"
    lunghezza = len(tentativo["proof_attempt"])
    avviso = f"{run} {tentativo['attempt_id']}: {lunghezza} caratteri, limite {limite}" if limite and lunghezza > limite else ""
    return testa + "\n" + md_a_latex(tentativo["proof_attempt"]), False, avviso


def raccogli_risposte(problemi, minimo):
    """Le risposte di ogni problema nell'ordine delle celle del manifesto, le celle mancanti e gli avvisi."""
    celle = json.loads((RUNS / "celle.json").read_text(encoding="utf-8"))
    risposte, mancanti, avvisi = [], [], []
    for pid in problemi:
        limiti = celle[pid].get("lunghezza_max", {})
        terne = {k: risposta_cella(f"{pid}_c{k}", minimo, limiti.get(k)) for k in celle[pid]["cells"]}
        risposte.append([testo for testo, _, _ in terne.values()])
        mancanti += [f"{pid}_c{k}" for k, (_, manca, _) in terne.items() if manca]
        avvisi += [avviso for _, _, avviso in terne.values() if avviso]
    return risposte, mancanti, avvisi


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("problemi", nargs="+", help="es. p5 p6 p7 p8, nell'ordine dei blocchi del template")
    p.add_argument("--template", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--marcatore", default="\\textbf{SOLUTION}")
    p.add_argument("--sostituisci", action="append", default=[], help="'VECCHIO=>NUOVO', testo letterale")
    p.add_argument("--dal-tentativo", type=int, default=1, help="ignora i tentativi con numero più basso")
    args = p.parse_args(argv)
    risposte, mancanti, avvisi = raccogli_risposte(args.problemi, args.dal_tentativo)
    latex = completa_preambolo(riempi_template(Path(args.template).read_text(encoding="utf-8"), args.marcatore, risposte))
    for regola in args.sostituisci:
        vecchio, nuovo = regola.split("=>", 1)
        latex = latex.replace(vecchio, nuovo)
    Path(args.output).write_text(latex, encoding="utf-8")
    print(f"scritto {args.output}; celle senza risposta pronta: {', '.join(mancanti) or 'nessuna'}")
    for avviso in avvisi:
        print(f"ATTENZIONE: oltre il limite di lunghezza: {avviso}", file=sys.stderr)
    if non_ascii_residui(latex):
        print(f"ATTENZIONE: caratteri non ASCII da sistemare per pdflatex: {non_ascii_residui(latex)}", file=sys.stderr)
    return 1 if mancanti else 0


if __name__ == "__main__":
    sys.exit(main())
