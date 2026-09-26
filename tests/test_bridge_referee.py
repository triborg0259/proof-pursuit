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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
