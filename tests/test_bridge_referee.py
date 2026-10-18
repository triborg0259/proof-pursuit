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
    assert r["esito"] == "UNKNOWN_STATUS"   # campo unificato: senza READY_FOR_HUMAN vale il verdict
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


def test_copia_di_verifica_non_segue_i_link_simbolici():
    """Un link nella sandbox verso un file dell'host resta un link nella copia di verifica: il contenuto dell'host
    non deve finire in runs/.../verifica, che è versionata e pubblica."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from bridge_referee import _cartella_verifica
    base = Path(tempfile.mkdtemp(prefix="pp_link_"))
    segreto = base / "segreto_host.txt"
    segreto.write_text("SEGRETO")
    (base / "run" / "sandbox").mkdir(parents=True)
    (base / "run" / "sandbox" / "x.txt").symlink_to(segreto)
    dest = _cartella_verifica(base / "run", {"attempt_id": "attempt_001", "code_used": []})
    assert (dest / "x.txt").is_symlink()


def test_estratto_interno_resta_dentro_il_repo():
    """Una fonte citata con un percorso che esce dal repo (../ o link verso l'host) non viene allegata al Referee."""
    sys.path.insert(0, str(ROOT / "researcher"))
    import bridge_referee
    base = Path(tempfile.mkdtemp(prefix="pp_fonti_"))
    (base / "repo").mkdir()
    (base / "fuori.md").write_text("SEGRETO")
    (base / "repo" / "link.md").symlink_to(base / "fuori.md")
    (base / "repo" / "nota.md").write_text("ok")
    originale, bridge_referee.ROOT = bridge_referee.ROOT, base / "repo"
    try:
        assert bridge_referee._estratto_interno("../fuori.md") == ""
        assert bridge_referee._estratto_interno("link.md") == ""
        assert bridge_referee._estratto_interno("nota.md") == "ok"
    finally:
        bridge_referee.ROOT = originale


def test_riesecuzione_in_container_senza_rete():
    """In modalità container gli script del Researcher girano in Docker senza rete né credenziali, mai con il
    Python dell'host; fuori dal container resta il comportamento di prima."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from bridge_referee import _comando_script
    cmd = _comando_script("code_1.py", Path("/tmp/v"), "container", 600)
    assert cmd[:2] == ["docker", "run"] and cmd[cmd.index("--network") + 1] == "none"
    assert "/tmp/v:/work" in cmd and not any(".claude" in parte for parte in cmd)
    assert sys.executable not in cmd and cmd[-2:] == ["python3", "code_1.py"]
    assert _comando_script("code_1.py", Path("/tmp/v"), "host", 600) == [sys.executable, "code_1.py"]


def test_esito_unificato_sui_report_vecchi():
    """I report della gara non hanno `esito`: READY_FOR_HUMAN vince sul verdict grezzo, altrimenti vale il verdict."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from researcher import esito_unificato
    assert esito_unificato({"verdict": "UNKNOWN_STATUS", "review_status": "READY_FOR_HUMAN"}) == "READY_FOR_HUMAN"
    assert esito_unificato({"verdict": "REJECT", "review_status": "NEEDS_WORK"}) == "REJECT"
    assert esito_unificato({"esito": "PARTIAL_PROGRESS", "verdict": "REJECT"}) == "PARTIAL_PROGRESS"
    assert esito_unificato({}) == "UNKNOWN_STATUS"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
