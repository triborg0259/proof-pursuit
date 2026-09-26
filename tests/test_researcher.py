"""Test del Researcher con backend mock (nessuna chiamata a modelli). Esecuzione: python3 -m pytest tests/ -q  oppure python3 tests/test_researcher.py"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = [sys.executable, str(ROOT / "researcher" / "researcher.py")]


def run(*args):
    return subprocess.run(R + list(args), capture_output=True, text=True, cwd=ROOT)


def fresh(fixture):
    d = Path(tempfile.mkdtemp(prefix="pp_")) / fixture
    shutil.copytree(ROOT / "tests" / "fixtures" / fixture, d)
    return d


def referee(attempt_id, verdict, fatal, claims=None):
    return {"attempt_id": attempt_id, "verdict": verdict, "highest_verified_cell": 1, "accepted_claims": claims or [],
            "fatal_error": fatal, "citation_issue": False, "computation_issue": False,
            "next_blocker": "prove the identity", "reasoning_summary": "test"}


def test_toy_x2_first_attempt():
    d = fresh("toy_x2")
    p = run("run", "--workdir", str(d), "--backend", "mock", "--strict")
    assert p.returncode == 0, p.stderr
    out = json.loads(p.stdout)
    att = json.loads((d / "attempts" / "attempt_001.json").read_text())
    assert out["target_cell"] == 1 and att["approach_family"] == "direct_proof"
    assert att["claimed_status"] == "CELL_SOLVED_CANDIDATE" and att["request_creative"] is False
    assert (d / "attempt.json").exists()


def test_missing_optional_files_ok():
    d = fresh("toy_x2")
    (d / "state.json").unlink()  # deve funzionare anche senza state.json
    p = run("run", "--workdir", str(d), "--backend", "mock")
    assert p.returncode == 0, p.stderr


def test_reject_changes_approach_and_stagnation_triggers_creative():
    d = fresh("toy_fail")
    fams = []
    for i in range(1, 5):
        p = run("run", "--workdir", str(d), "--backend", "mock", "--strict"); assert p.returncode == 0, p.stderr
        att = json.loads((d / "attempts" / f"attempt_{i:03d}.json").read_text()); fams.append(att["approach_family"])
        rep = referee(f"attempt_{i:03d}", "REJECT", "Step 3 assumes the identity for n+1 without proof (circular).")
        rp = d / "rep.json"; rp.write_text(json.dumps(rep))
        assert run("record", "--workdir", str(d), "--report", str(rp)).returncode == 0
    # dopo un REJECT il mock cambia famiglia: nessuna stagnazione (famiglie diverse) => request_creative False
    assert len(set(fams)) == 4, fams
    st = json.loads((d / "state.json").read_text()); assert st["stagnation_count"] == 0
    assert "attempt_001" in (d / "failed_attempts.md").read_text()


def test_same_family_same_reason_three_times_detects_stagnation():
    d = fresh("toy_fail")
    (d / "attempts").mkdir()
    for i in range(1, 4):  # tre tentativi identici nel metodo e nel motivo di fallimento, scritti a mano
        (d / "attempts" / f"attempt_{i:03d}.json").write_text(json.dumps({"attempt_id": f"attempt_{i:03d}", "target_cell": 2,
            "approach_family": "induction", "subgoal": "s", "claimed_status": "CELL_SOLVED_CANDIDATE"}))
        (d / "attempts" / f"referee_{i:03d}.json").write_text(json.dumps(referee(f"attempt_{i:03d}", "REJECT",
            "Inductive step assumes the identity for n+1 without proof: circular reasoning.")))
    p = run("run", "--workdir", str(d), "--backend", "mock", "--strict"); assert p.returncode == 0, p.stderr
    assert "STAGNAZIONE" in p.stderr
    st = json.loads((d / "state.json").read_text()); assert st["stagnation_count"] == 1
    att = json.loads((d / "attempts" / "attempt_004.json").read_text())
    assert att["request_creative"] is True and att["approach_family"] != "induction"
    # con idee creative presenti, il Researcher le segue
    (d / "creative_ideas.json").write_text(json.dumps({"blocker_analysis": "x", "avoid": ["induction"], "ideas": [
        {"id": "idea_1", "risk": "MEDIUM", "method": "telescoping", "why_different": "no induction", "why_it_might_work": "…",
         "first_test": "n=3", "expected_gain": "full proof", "main_risk": "algebra", "approach_family": "algebraic_reformulation"}]}))
    p = run("run", "--workdir", str(d), "--backend", "mock", "--strict"); assert p.returncode == 0, p.stderr
    att = json.loads((d / "attempts" / "attempt_005.json").read_text())
    assert att["approach_family"] == "algebraic_reformulation"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
