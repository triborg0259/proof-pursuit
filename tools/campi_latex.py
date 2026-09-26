#!/usr/bin/env python3
"""
campi_latex.py — da una bozza di consegna (problema-N/submission/parte-K.md) produce i CAMPI LaTeX da incollare
nella piattaforma, uno per sezione: risultato, dimostrazione, verifica, fonti, limiti.
Perché: la piattaforma chiede la consegna a campi; il Markdown con formule viene reso in LaTeX con pandoc.
Uso: .venv/bin/python tools/campi_latex.py 1 1   → problema-1/submission/parte-1.campi.tex
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sezioni(testo_md):
    """Spezza la bozza nelle sezioni '## n. Titolo' → [(titolo, corpo)]."""
    # solo le cinque sezioni canoniche della consegna: i titoli interni della prova (es. "## 1. The excess identity") restano nel corpo
    pezzi = re.split(r"(?m)^## (\d\.\s*(?:Risultato|Dimostrazione|Verifica|Fonti|Limiti)[^\n]*)\n", testo_md)
    return [(pezzi[i].strip(), pezzi[i + 1].strip()) for i in range(1, len(pezzi) - 1, 2)]


def md_a_tex(corpo):
    """Markdown con formule → LaTeX (frammento) via pandoc; i titoli interni scendono a \\paragraph."""
    res = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--shift-heading-level-by=3"],
                         input=corpo, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else "\\begin{verbatim}\n" + corpo + "\n\\end{verbatim}"


def main(n, k):
    src = ROOT / f"problema-{n}" / "submission" / f"parte-{k}.md"
    out = src.with_suffix(".campi.tex")
    blocchi = [f"% ===== CAMPO: {titolo} =====\n{md_a_tex(corpo)}\n" for titolo, corpo in sezioni(src.read_text(encoding="utf-8"))]
    out.write_text(f"% Problema {n}, parte {k}: campi da incollare nella piattaforma (uno per sezione)\n\n" + "\n".join(blocchi), encoding="utf-8")
    print(f"scritto {out} ({len(blocchi)} campi)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
