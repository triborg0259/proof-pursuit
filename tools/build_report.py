#!/usr/bin/env python3
"""
build_report.py — genera report/proof_pursuit.tex, il rapporto LaTeX completo della gara.

Cosa contiene, per ogni problema e per ogni cella: enunciato ufficiale, stato (da STATUS.md), consegna (la prova,
da problema-N/submission), la traccia delle DECISIONI degli agenti iterazione per iterazione (cosa ha scelto il
Researcher e perché, cosa ha bloccato il Referee, se e perché è entrato il Creative), il CODICE su cui la prova
poggia con l'esito della riesecuzione fidata e il verdetto del Referee, e le CITAZIONI arXiv trovate dalla ricerca
deterministica. Perché: la consegna deve mostrare non solo il risultato ma come ci si è arrivati e cosa lo sostiene.
Uso: .venv/bin/python tools/build_report.py   (usa pandoc per Markdown→LaTeX; senza pandoc i .md vanno in verbatim)
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "proof_pursuit.tex"
CELLE = json.loads((ROOT / "runs" / "celle.json").read_text(encoding="utf-8"))
# Run storiche fatte prima della numerazione pN_cK: vanno lette sotto la cella giusta.
RUN_STORICHE = {("p2", "1"): ["p2_q3", "p2_q4"], ("p2", "2"): ["p2_q5"]}
PUNTI = {"1": 1, "2": 2, "3": 3, "4": 5, "5": 8, "6": 13}


# =============================================================================== utilità LaTeX
def tex(testo):
    """Escape del testo libero (motivi, errori, enunciati testuali) per LaTeX."""
    sost = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
            "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}", "<": r"\textless{}", ">": r"\textgreater{}"}
    return "".join(sost.get(c, c) for c in str(testo or ""))


def md_a_tex(percorso: Path, shift=2):
    """Markdown (con formule $...$) → frammento LaTeX via pandoc; i titoli scendono di `shift` livelli.
    Senza pandoc il file va in verbatim: si perde la resa ma non il contenuto."""
    if shutil.which("pandoc"):
        res = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", f"--shift-heading-level-by={shift}", str(percorso)],
                             capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout
    return "\\begin{verbatim}\n" + percorso.read_text(encoding="utf-8") + "\n\\end{verbatim}\n"


def md_testo_a_tex(testo_md, shift=3):
    """Come md_a_tex ma da una stringa: usato per i pezzi di enunciato ritagliati (preambolo, singola parte)."""
    tmp = ROOT / "report" / "_frammento.md"
    tmp.write_text(testo_md, encoding="utf-8")
    try:
        return md_a_tex(tmp, shift)
    finally:
        tmp.unlink(missing_ok=True)


def pezzo_enunciato(numero_problema, k=None):
    """k=None: il preambolo ufficiale (tutto ciò che precede la prima '## Parte'); altrimenti la sezione '## Parte k'.
    Perché: la richiesta ufficiale di ogni cella va riportata alla lettera e con le formule rese, non parafrasata."""
    testo = (ROOT / f"problema-{numero_problema}" / "enunciato.md").read_text(encoding="utf-8")
    sezioni = re.split(r"(?m)^(?=## Parte )", testo)
    if k is None:
        return sezioni[0]
    return next((sz for sz in sezioni[1:] if re.match(rf"## Parte {k}\b", sz)), "")


def listing(codice, titolo):
    """Blocco di codice; `end{lstlisting}` nel testo spezzerebbe il blocco, quindi viene neutralizzato."""
    codice = codice.replace("\\end{lstlisting}", "\\end{lst listing}")
    return f"\\begin{{lstlisting}}[caption={{{tex(titolo)}}}]\n{codice}\n\\end{{lstlisting}}\n"


# =============================================================================== lettura dei dati
def leggi_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def stato_cella(numero_problema, k):
    """Riga della cella nella tabella di STATUS.md: (stato, evidenza)."""
    testo = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    sezione = testo.split(f"## Problema {numero_problema}", 1)[-1].split("\n## ", 1)[0]
    for riga in sezione.splitlines():
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if len(celle) >= 4 and celles_ok(celle, k):
            return celle[2], celle[3]
    return "non iniziato", ""


def celles_ok(celle, k):
    return celle[0] == str(k)


def cartelle_run(pid, k):
    """Le run che riguardano la cella: quella standard runs/pN_cK più le storiche."""
    nomi = [f"{pid}_c{k}"] + RUN_STORICHE.get((pid, k), [])
    return [ROOT / "runs" / n for n in nomi if (ROOT / "runs" / n).exists()]


def iterazioni(run: Path):
    """Traccia delle iterazioni: loop_log.jsonl se c'è, altrimenti ricostruita dalle coppie attempt/referee."""
    log = run / "loop_log.jsonl"
    if log.exists():
        return [json.loads(r) for r in log.read_text(encoding="utf-8").splitlines() if r.strip()]
    voci = []
    for i, att in enumerate(sorted((run / "attempts").glob("attempt_*.json")), start=1):
        a = leggi_json(att)
        r = leggi_json(run / "attempts" / att.name.replace("attempt_", "referee_")) or {}
        voci.append({"iter": i, "attempt_id": a["attempt_id"], "family": a.get("approach_family"), "subgoal": a.get("subgoal"),
                     "claimed_status": a.get("claimed_status"), "researcher_reason": a.get("reason_for_choice", ""),
                     "literature_position": a.get("literature_position", ""), "verdict": r.get("verdict", "(nessun verdetto)"),
                     "review_status": r.get("review_status"), "fatal_error": r.get("fatal_error"),
                     "next_blocker": r.get("next_blocker"), "creative": "", "creative_analysis": ""})
    return voci


def approvato(voce):
    """Il tentativo è passato dal Referee? (READY_FOR_HUMAN, ACCEPT o PARTIAL_PROGRESS sui claim)."""
    return voce.get("review_status") == "READY_FOR_HUMAN" or voce.get("verdict") in ("ACCEPT", "PARTIAL_PROGRESS")


# =============================================================================== sezioni del rapporto
def sezione_decisioni(run: Path):
    """Tabella-narrazione delle iterazioni di una run: il momento e il motivo di ogni scelta."""
    righe = [f"\\paragraph{{Run \\texttt{{{tex(run.name)}}}}}"]
    for v in iterazioni(run):
        righe.append(f"\\begin{{description}}\n\\item[Iterazione {v['iter']} — {tex(v['attempt_id'])}]")
        righe.append(f"\\textbf{{Researcher}}: famiglia \\texttt{{{tex(v.get('family'))}}}, sotto-obiettivo: {tex(v.get('subgoal'))}. "
                     f"Stato dichiarato: \\texttt{{{tex(v.get('claimed_status'))}}}.")
        if v.get("researcher_reason"):
            righe.append(f"\\emph{{Perché questa scelta}}: {tex(v['researcher_reason'])}")
        if v.get("literature_position"):
            righe.append(f"\\emph{{Rispetto allo stato dell'arte}}: {tex(v['literature_position'])}")
        righe.append(f"\\textbf{{Referee}}: verdetto \\texttt{{{tex(v.get('verdict'))}}}"
                     + (f" (review\\_status \\texttt{{{tex(v['review_status'])}}})" if v.get("review_status") else "") + ".")
        if v.get("fatal_error"):
            righe.append(f"\\emph{{Errore fatale}}: {tex(v['fatal_error'])}")
        if v.get("next_blocker"):
            righe.append(f"\\emph{{Prossimo passo richiesto}}: {tex(v['next_blocker'])}")
        if v.get("creative"):
            righe.append(f"\\textbf{{Creative}}: attivato perché {tex(v['creative'])}. \\emph{{Analisi del blocco}}: {tex(v.get('creative_analysis'))}")
        righe.append("\\end{description}")
    return "\n".join(righe) + "\n"


def sezione_codice(run: Path):
    """Il codice dei tentativi, con rigore dichiarato, esito della riesecuzione fidata e verdetto del Referee."""
    blocchi = []
    for v in iterazioni(run):
        a = leggi_json(run / "attempts" / f"{v['attempt_id']}.json") or {}
        oss = leggi_json(run / "verifica" / v["attempt_id"] / "osservazioni.json") or []
        esito = "approvato dal Referee" if approvato(v) else f"verdetto del Referee: {v.get('verdict')}"
        for i, c in enumerate(a.get("code_used", []), start=1):
            titolo = f"{v['attempt_id']} code_{i} [{c.get('language')}, rigore {c.get('rigor')}] — {c.get('purpose', '')[:90]} — {esito}"
            blocchi.append(listing(c.get("code", ""), titolo))
            if i <= len(oss):
                blocchi.append(f"\\noindent\\emph{{Riesecuzione fidata dell'orchestratore}}: \\texttt{{{tex(oss[i - 1][:400])}}}\n")
    return "".join(blocchi) or "Nessun codice nei tentativi.\n"


def certificati(numero_problema):
    """Gli script di verifica indipendente scritti dal team (separati dalla ricerca)."""
    cartella = ROOT / f"problema-{numero_problema}" / "certificati"
    return "".join(listing(f.read_text(encoding="utf-8"), f"certificati/{f.name}") for f in sorted(cartella.glob("*.py")))


def fonti_arxiv(numero_problema, pid):
    """Voci arXiv pertinenti del problema (stesso filtro di prepara_runs) come \\bibitem."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("prepara_runs", ROOT / "tools" / "prepara_runs.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    voci = leggi_json(ROOT / f"problema-{numero_problema}" / "fonti" / "arxiv.json") or []
    return [v for v in voci if mod.pertinente(v, mod.PAROLE[pid])]


def sezione_cella(pid, numero_problema, k, testo):
    stato, evidenza = stato_cella(numero_problema, k)
    parti = [f"\\subsection{{Cella {k} ({PUNTI[k]} punti) — stato: {tex(stato)}}}",
             md_testo_a_tex(pezzo_enunciato(numero_problema, k), 3),
             f"\\textbf{{Enunciato protetto dato agli agenti (state.json).}} \\texttt{{{tex(testo)}}}\n",
             f"\\textbf{{Evidenza registrata in STATUS.md.}} {tex(evidenza) or '—'}\n"]
    sub = ROOT / f"problema-{numero_problema}" / "submission" / f"parte-{k}.md"
    parti.append("\\subsubsection{Consegna (prova)}\n" + (md_a_tex(sub, 3) if sub.exists() else "Nessuna bozza di consegna ancora scritta.\n"))
    runs = cartelle_run(pid, k)
    parti.append("\\subsubsection{Decisioni degli agenti}\n" + ("".join(sezione_decisioni(r) for r in runs) or "Nessuna run del loop su questa cella.\n"))
    parti.append("\\subsubsection{Codice su cui poggia il tentativo}\n" + ("".join(sezione_codice(r) for r in runs) or "—\n"))
    return "\n".join(parti)


def sezione_problema(pid):
    n = pid[1]
    parti = [f"\\section{{Problema {n} — {tex(CELLE[pid]['title'])}}}", "\\subsection{Enunciato ufficiale: preambolo e regole di consegna}",
             md_testo_a_tex(pezzo_enunciato(n), 2)]
    for k, testo in CELLE[pid]["cells"].items():
        parti.append(sezione_cella(pid, n, k, testo))
    cert = certificati(n)
    if cert:
        parti.append("\\subsection{Certificati di verifica indipendente del team}\n" + cert)
    fonti = fonti_arxiv(n, pid)
    if fonti:
        parti.append("\\subsection{Letteratura arXiv consultata (ricerca deterministica, abstract letti)}\n\\begin{itemize}")
        parti += [f"\\item \\cite{{{v['arxiv_id']}}} {tex(v['title'])} — {tex(', '.join(v['authors'][:4]))} ({v['published'][:4]}). "
                  f"\\emph{{Query}}: \\texttt{{{tex(v.get('query', ''))}}}." for v in fonti]
        parti.append("\\end{itemize}")
    return "\n".join(parti)


def bibliografia():
    voci = {}
    for pid in CELLE:
        for v in fonti_arxiv(pid[1], pid):
            voci[v["arxiv_id"]] = v
    righe = ["\\begin{thebibliography}{99}"]
    righe += [f"\\bibitem{{{i}}} {tex(', '.join(v['authors']))}. \\emph{{{tex(v['title'])}}}. arXiv:{tex(i)} ({v['published'][:4]}). \\url{{{v['url']}}}"
              for i, v in sorted(voci.items())]
    righe += ["\\bibitem{bm18} D. Bilyk, R. Matzke. \\emph{On the Fejes Tóth problem about the sum of angles between lines}. Proc. AMS (2019); letta integralmente, vedi problema-1/fonti/.",
              "\\end{thebibliography}"]
    return "\n".join(righe)


PREAMBOLO = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage[italian,english]{babel}
\usepackage{amsmath,amssymb,amsthm}\usepackage[margin=2.2cm]{geometry}\usepackage{longtable,booktabs,array,calc}
\usepackage{listings,xcolor}\usepackage{hyperref}\usepackage{url}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\lstset{basicstyle=\ttfamily\scriptsize,breaklines=true,frame=single,captionpos=b,columns=fullflexible,keepspaces=true,inputencoding=utf8,extendedchars=true}
\title{Proof Pursuit --- rapporto completo\\ \large prove, decisioni degli agenti, codice verificato, letteratura}
\author{Team Proof Pursuit (Researcher: T. Tumini; Referee: gabundos; Creative: M. Renzi; gio3r3gio)}
\date{\today}
\begin{document}\maketitle\tableofcontents
\section*{Come leggere questo rapporto}
Per ogni cella: la richiesta ufficiale, lo stato dichiarato dal team (mai ``risolto'' senza revisione umana), la consegna
con la prova, poi la traccia delle decisioni degli agenti (Researcher: famiglia e motivo; Referee: verdetto ed errore
fatale; Creative: quando e perché è intervenuto) e il codice su cui il tentativo poggia con l'esito della riesecuzione
fidata. DIMOSTRATO, CITATO, VERIFICATO SU INTERVALLO FINITO e CONGETTURA restano distinti. L'architettura del sistema
è descritta nel README del repository.
"""


def main():
    corpo = "\n".join(sezione_problema(pid) for pid in CELLE)
    OUT.write_text(PREAMBOLO + corpo + "\n" + bibliografia() + "\n\\end{document}\n", encoding="utf-8")
    print(f"scritto {OUT} ({OUT.stat().st_size // 1024} KB)")
    if shutil.which("pandoc"):
        html = OUT.with_suffix(".html")
        res = subprocess.run(["pandoc", "-f", "latex", "-t", "html", "--mathjax", "-s", "--toc", str(OUT), "-o", str(html)],
                             capture_output=True, text=True)
        print(f"anteprima HTML: {html}" if res.returncode == 0 else f"anteprima HTML non generata: {res.stderr[:200]}")


if __name__ == "__main__":
    main()
