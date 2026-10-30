"""Test della verifica Lean: analisi dell'output (senza Lean) e aggancio al ponte (con un verificatore finto).
Esecuzione: .venv/bin/python tests/test_verifica_lean.py
Con PP_LEAN=1 compila anche un file vero nel progetto lean/ (serve Mathlib scaricato; circa un minuto)."""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "researcher"))
import verifica_lean as vl  # noqa: E402
import bridge_referee as br  # noqa: E402

STANDARD = "'Verifica.t' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
LEAN = {"code": "import Mathlib\ntheorem Verifica.t : (1:ℕ) + 1 = 2 := by norm_num\n", "theorem": "Verifica.t",
        "covers": "the whole cell"}


def test_compila_senza_sorry_e_assiomi_standard_vale():
    assert vl.analizza(0, STANDARD)["ok"]
    assert vl.analizza(0, "'Verifica.t' does not depend on any axioms\n")["ok"]


def test_sorry_errori_e_assiomi_estranei_non_valgono():
    con_sorry = "f.lean:2:8: warning: declaration uses 'sorry'\n'Verifica.t' depends on axioms: [sorryAx]\n"
    assert not vl.analizza(0, con_sorry)["ok"] and vl.analizza(0, con_sorry)["sorry"]
    assert not vl.analizza(1, "f.lean:2:8: error: unknown identifier 'x'\n")["ok"]
    nativo = "'Verifica.t' depends on axioms: [propext, Lean.ofReduceBool]\n"
    assert not vl.analizza(0, nativo)["solo_assiomi_standard"]
    assert vl.analizza(0, "")["assiomi"] is None   # teorema non stampato: non verificato


def test_nome_non_valido_non_si_compila():
    esito, riga = vl.verifica("inesistente.lean", "t\n#eval 1")
    assert not esito["ok"] and "invalid theorem name" in riga


def _cartella_con_lean():
    d = Path(tempfile.mkdtemp(prefix="pp_lean_")) / "toy_x2"
    shutil.copytree(ROOT / "tests" / "fixtures" / "toy_x2", d)
    p = subprocess.run([sys.executable, str(ROOT / "researcher" / "researcher.py"), "run", "--workdir", str(d),
                        "--backend", "mock"], capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr
    percorso = d / "attempts" / "attempt_001.json"
    tentativo = json.loads(percorso.read_text())
    tentativo["lean_proof"] = LEAN
    percorso.write_text(json.dumps(tentativo))
    return d, tentativo


def test_ponte_passa_la_prova_come_certificato_e_avvisa_i_giudici():
    d, tentativo = _cartella_con_lean()
    job = br.costruisci_review_input(d, tentativo)
    lean = [a for a in job["candidate"]["artifacts"] if a["id"] == "lean_1"]
    assert lean and lean[0]["kind"] == "CERTIFICATE" and "Verifica.t" in lean[0]["content"]
    assert br.NOTA_LEAN in job["rules"]["additional_rules"]
    senza = br.costruisci_review_input(d, {**tentativo, "lean_proof": None})
    assert br.NOTA_LEAN not in senza["rules"]["additional_rules"]   # state.json non è stato toccato


def test_ponte_ricompila_e_registra_l_osservazione():
    d, tentativo = _cartella_con_lean()
    originale = vl.verifica
    vl.verifica = lambda file, teorema, timeout=600: ({"ok": True, "file": str(file)}, f"theorem {teorema} VERIFIED")
    try:
        osservazioni = br.esegui_codice(d, tentativo)
    finally:
        vl.verifica = originale
    assert any("compiled lean_1" in o and "VERIFIED" in o for o in osservazioni)
    cartella = d / "verifica" / "attempt_001"
    assert (cartella / "prova_lean.lean").read_text() == LEAN["code"] and (cartella / "lean.json").exists()
    assert "not compiled" in br.osserva_lean(cartella, LEAN, 10, dove="container")


def test_lean_copiato_in_code_used_rimanda_a_lean_1():
    codice = {"language": "Lean", "purpose": "formal proof", "code": LEAN["code"]}
    assert "compiled separately as lean_1" in br._non_rieseguito(1, codice, {"lean_proof": LEAN})
    assert "not supported" in br._non_rieseguito(1, codice, {})
    assert "not supported" in br._non_rieseguito(1, {"language": "julia"}, {"lean_proof": LEAN})


def test_compilazione_vera():
    if os.environ.get("PP_LEAN") != "1":
        return
    cartella = Path(tempfile.mkdtemp(prefix="pp_lean_vero_"))
    buono = cartella / "buono.lean"
    buono.write_text("import Mathlib\n\ntheorem Verifica.inv_lt (n : ℕ) (h : 2 ≤ n) : (1:ℝ) / n < 1 := by\n"
                     "  have : (2:ℝ) ≤ n := by exact_mod_cast h\n  rw [div_lt_one] <;> linarith\n")
    esito, riga = vl.verifica(buono, "Verifica.inv_lt")
    assert esito["ok"], riga
    cattivo = cartella / "cattivo.lean"
    cattivo.write_text("import Mathlib\n\ntheorem Verifica.falso : (1:ℕ) = 2 := by sorry\n")
    esito, riga = vl.verifica(cattivo, "Verifica.falso")
    assert not esito["ok"] and esito["sorry"], riga


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
