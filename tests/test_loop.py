"""Test del ciclo end-to-end senza modelli: Researcher mock + Referee mock + Creative finto. Esecuzione: .venv/bin/python tests/test_loop.py"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def cartella():
    d = Path(tempfile.mkdtemp(prefix="pp_loop_")) / "toy_fail"
    shutil.copytree(ROOT / "tests" / "fixtures" / "toy_fail", d)
    return d


def test_reject_poi_ready_con_creative_agganciato():
    d = cartella()
    # Creative finto: uno script che scrive idee che chiedono la famiglia 'extremal'
    script = d.parent / "creative_finto.py"
    script.write_text("import json, sys\n"
                      "idee = {'blocker_analysis': 'x', 'avoid': ['induction'], 'ideas': [{'id': 'i1', 'risk': 'MEDIUM', 'method': 'm',"
                      " 'why_different': 'd', 'why_it_might_work': 'w', 'first_test': 't', 'expected_gain': 'g', 'main_risk': 'r',"
                      " 'approach_family': 'extremal'}]}\n"
                      "json.dump(idee, open(sys.argv[1] + '/creative_ideas.json', 'w'))\n")
    creative = f"{PY} {script} {{workdir}}"
    p = subprocess.run([PY, str(ROOT / "researcher" / "loop.py"), "--workdir", str(d), "--max-iter", "5",
                        "--researcher-backend", "mock", "--referee", "mock", "--mock-rejects", "2", "--creative-cmd", creative],
                       capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr + p.stdout
    righe = [json.loads(l) for l in (d / "loop_log.jsonl").read_text().splitlines()]
    assert [r["verdict"] for r in righe] == ["REJECT", "REJECT", "UNKNOWN_STATUS"]
    assert righe[-1]["review_status"] == "READY_FOR_HUMAN"
    assert "idee scritte" in righe[1]["creative"]            # al 2° REJECT il Referee segnala stagnazione → Creative
    assert righe[2]["family"] == "extremal"                  # il Researcher segue l'idea del Creative
    assert (d / "failed_attempts.md").read_text().count("attempt_") == 2


def test_senza_creative_il_loop_prosegue():
    d = cartella()
    p = subprocess.run([PY, str(ROOT / "researcher" / "loop.py"), "--workdir", str(d), "--max-iter", "3",
                        "--researcher-backend", "mock", "--referee", "mock", "--mock-rejects", "2"],
                       capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr + p.stdout
    righe = [json.loads(l) for l in (d / "loop_log.jsonl").read_text().splitlines()]
    assert "non collegato" in righe[1]["creative"] and righe[-1]["review_status"] == "READY_FOR_HUMAN"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
