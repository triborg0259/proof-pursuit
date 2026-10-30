"""Test di tools/compila_template.py senza modelli né run reali. Esecuzione: python3 tests/test_compila_template.py"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import compila_template as ct  # noqa: E402

TEMPLATE = r"""\documentclass{article}
\begin{document}
\textbf{SOLUTION}
\begin{enumerate}
    \item
    \item
\end{enumerate}
\textbf{SOLUTION}
\begin{enumerate}
    \item
\end{enumerate}
\end{document}"""


def test_riempie_i_blocchi_nell_ordine():
    out = ct.riempi_template(TEMPLATE, r"\textbf{SOLUTION}", [["uno", "due"], ["tre"]])
    assert out.index("uno") < out.index("due") < out.index("tre")
    assert out.count(r"\item") == 3


def test_numero_di_item_diverso_si_ferma():
    try:
        ct.riempi_template(TEMPLATE, r"\textbf{SOLUTION}", [["uno"], ["tre"]])
    except ValueError as e:
        assert "2" in str(e)
    else:
        raise AssertionError("doveva fermarsi: 2 item nel template, 1 risposta")


def test_titoli_diventano_grassetto_anche_con_graffe():
    out = ct.titoli_in_grassetto(r"\subsection{The set \(\{c_n\}\)}" + "\ntesto")
    assert "section" not in out and r"\textbf{The set \(\{c_n\}\)}" in out


def test_unicode_riscritto():
    out = ct.sostituisci_unicode("x ≤ 1 — ε")
    assert ct.non_ascii_residui(out) == [] and r"\le" in out and "---" in out


def test_tentativo_respinto_mai_usato():
    run = "pz_test_c1"
    d = ct.RUNS / run
    try:
        (d / "attempts").mkdir(parents=True)
        (d / "loop_log.jsonl").write_text(json.dumps({"attempt_id": "attempt_001", "esito": "REJECT"}) + "\n")
        tentativo, motivo = ct.tentativo_scelto(run)
        assert tentativo is None and "REJECT" in motivo
        (d / "attempts" / "attempt_002.json").write_text(json.dumps({"attempt_id": "attempt_002", "proof_attempt": "x"}))
        with open(d / "loop_log.jsonl", "a") as f:
            f.write(json.dumps({"attempt_id": "attempt_002", "review_status": "READY_FOR_HUMAN"}) + "\n")
        tentativo, motivo = ct.tentativo_scelto(run)
        assert tentativo["attempt_id"] == "attempt_002" and "firma umana mancante" in motivo
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_dal_tentativo_ignora_le_versioni_vecchie():
    run = "pz_test_c2"
    d = ct.RUNS / run
    try:
        (d / "attempts").mkdir(parents=True)
        (d / "attempts" / "attempt_001.json").write_text(json.dumps({"attempt_id": "attempt_001", "proof_attempt": "lunga"}))
        (d / "loop_log.jsonl").write_text(json.dumps({"attempt_id": "attempt_001", "review_status": "READY_FOR_HUMAN"}) + "\n")
        assert ct.tentativo_scelto(run)[0]["attempt_id"] == "attempt_001"
        assert ct.tentativo_scelto(run, minimo=2)[0] is None
        testo, manca, avviso = ct.risposta_cella(run, limite=3)
        assert not manca and "5 caratteri, limite 3" in avviso
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_elenco_della_risposta_non_sposta_le_part():
    out = ct.elenchi_annidati("\\begin{enumerate}\n\\def\\labelenumi{(\\Alph{enumi})}\n\\setcounter{enumi}{5}\n")
    assert "\\setcounter{enumii}{5}" in out and "\\labelenumii{(\\Alph{enumii})}" in out
    assert "\\begin{enumerate}" in out and ct.elenchi_annidati("enumiii") == "enumiv"


def test_pandoc_lascia_passare_tikz():
    if not shutil.which("pandoc"):
        return
    out = ct.md_a_latex("## Graph\n\n\\begin{tikzpicture}\\draw (0,0)--(1,1);\\end{tikzpicture}\n\nSo $x_1=1$.")
    assert r"\begin{tikzpicture}" in out and r"\textbf{Graph}" in out


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
