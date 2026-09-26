"""Test del ponte Researcher→Referee in modalità offline (nessun modello). Esecuzione: .venv/bin/python tests/test_bridge_referee.py"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
B = [PY, str(ROOT / "researcher" / "bridge_referee.py")]


def run(*args):
    return subprocess.run(B + list(args), capture_output=True, text=True, cwd=ROOT)


def cartella_con_tentativo_mock():
    """Cartella di lavoro con un tentativo prodotto dal Researcher mock."""
    d = Path(tempfile.mkdtemp(prefix="pp_bridge_")) / "toy_x2"
    shutil.copytree(ROOT / "tests" / "fixtures" / "toy_x2", d)
    p = subprocess.run([PY, str(ROOT / "researcher" / "researcher.py"), "run", "--workdir", str(d), "--backend", "mock"],
                       capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr
    return d


def test_to_review_produce_input_valido():
    d = cartella_con_tentativo_mock()
    p = run("to-review", "--workdir", str(d)); assert p.returncode == 0, p.stderr
    j = json.loads((d / "review_input.json").read_text())
    assert j["candidate"]["attempt_id"] == "attempt_001" and j["cell"]["target_claim_id"] == "main"
    assert j["candidate"]["claims"][0]["statement"] == j["cell"]["statement"]  # il Referee protegge questo testo


def test_review_offline_archivia_il_verdetto():
    d = cartella_con_tentativo_mock()
    p = run("review", "--workdir", str(d), "--offline"); assert p.returncode == 0, p.stderr
    r = json.loads((d / "referee_report.json").read_text())
    assert r["verdict"] == "UNKNOWN_STATUS" and r["review_status"] == "INCOMPLETE"
    assert (d / "attempts" / "referee_001.json").exists() and (d / "attempts" / "packet_001.json").exists()
    assert not (d / "failed_attempts.md").exists()   # UNKNOWN_STATUS non è un fallimento


def test_normalizza_rapporto_con_limitazione():
    """Rapporto + limitazione insieme: il verdetto resta, la riserva finisce nelle note (prima si perdeva il PASS)."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from bridge_referee import CliBackend
    grezzo = {"report": {"mathematical_verdict": "PASS", "math_notes": "ok"}, "limitation": "no code execution"}
    out = CliBackend._normalizza("A", grezzo)
    assert out["limitation"] is None and "no code execution" in out["report"]["math_notes"]
    assert CliBackend._normalizza("B", {"report": None, "limitation": "x"})["report"] is None  # caso legittimo intatto


def test_provenienza_ristretta_ai_claim_del_candidato():
    """Il giudice B classifica anche i claim già verificati; il merge ammette solo quelli del candidato: si filtra."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from bridge_referee import CliBackend
    payload = {"submission": {"candidate": {"claims": [{"id": "main"}]}}}
    raw = {"report": {"evidence_verdict": "PASS", "claim_provenance": [{"claim_id": "main"}, {"claim_id": "verified_1"}]}, "limitation": None}
    out = CliBackend._solo_claim_candidato(raw, payload)
    assert [v["claim_id"] for v in out["report"]["claim_provenance"]] == ["main"]


def test_riesecuzione_codice_produce_osservazioni():
    """Gli script di code_used vengono rilanciati dall'orchestratore e l'esito (exit, stdout) diventa osservazione."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from bridge_referee import esegui_codice
    d = Path(tempfile.mkdtemp(prefix="pp_code_"))
    attempt = {"attempt_id": "attempt_001", "code_used": [
        {"language": "python", "purpose": "conta", "code": "print(2+2)", "rigor": "exact"},
        {"language": "lean", "purpose": "no", "code": "", "rigor": "exact"}]}
    oss = esegui_codice(d, attempt, timeout=30)
    assert len(oss) == 2 and "exit 0" in oss[0] and "'4'" in oss[0] and "not re-run" in oss[1]
    assert (d / "verifica" / "attempt_001" / "osservazioni.json").exists()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
