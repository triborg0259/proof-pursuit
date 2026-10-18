"""Test del ciclo end-to-end senza modelli: Researcher mock + Referee mock + Creative finto. Esecuzione: .venv/bin/python tests/test_loop.py"""
import argparse, json, shutil, subprocess, sys, tempfile
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
    assert [r["esito"] for r in righe] == ["REJECT", "REJECT", "READY_FOR_HUMAN"]   # campo unificato
    assert "idee scritte" in righe[1]["creative"]            # al 2° REJECT il Referee segnala stagnazione → Creative
    assert righe[2]["family"] == "extremal"                  # il Researcher segue l'idea del Creative
    assert (d / "failed_attempts.md").read_text().count("attempt_") == 2


def test_senza_creative_il_loop_prosegue():
    d = cartella()
    p = subprocess.run([PY, str(ROOT / "researcher" / "loop.py"), "--workdir", str(d), "--max-iter", "3",
                        "--researcher-backend", "mock", "--referee", "mock", "--mock-rejects", "2", "--creative", "none"],
                       capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr + p.stdout
    righe = [json.loads(l) for l in (d / "loop_log.jsonl").read_text().splitlines()]
    assert "non collegato" in righe[1]["creative"] and righe[-1]["review_status"] == "READY_FOR_HUMAN"


def test_creative_del_team_rule_based_scrive_idee():
    """Stagnazione al 2° REJECT → il Creative di creative/ (senza modello) scrive creative_ideas.json."""
    d = cartella()
    p = subprocess.run([PY, str(ROOT / "researcher" / "loop.py"), "--workdir", str(d), "--max-iter", "3",
                        "--researcher-backend", "mock", "--referee", "mock", "--mock-rejects", "2", "--creative", "rule_based"],
                       capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr
    assert (d / "creative_ideas.json").exists()
    righe = [json.loads(r) for r in (d / "loop_log.jsonl").read_text().splitlines()]
    assert any("idee scritte" in r["creative"] for r in righe)


def test_perimetro_di_verifica():
    """L'impronta del perimetro cambia se si tocca un file protetto (enunciato, stato) e include il Referee;
    NON cambia se il Researcher incrementa solo stagnation_count, l'unico campo che gli spetta."""
    sys.path.insert(0, str(ROOT / "researcher"))
    from integrita import impronta, differenze
    d = cartella()
    prima = impronta(d)
    assert str(ROOT / "referee" / "referees" / "merge.py") in prima
    stato = json.loads((d / "state.json").read_text()); stato["stagnation_count"] = 3
    (d / "state.json").write_text(json.dumps(stato))
    assert differenze(prima, impronta(d)) == []
    (d / "problem.md").write_text((d / "problem.md").read_text() + "\n(enunciato ammorbidito)")
    assert differenze(prima, impronta(d)) == [str(d / "problem.md")]
    (d / "state.json").unlink()
    assert str(d / "state.json") in differenze(prima, impronta(d))

def test_referee_riesegue_in_container_se_il_researcher_era_in_container():
    """Il codice di un Researcher chiuso in Docker non deve poi girare sull'host durante la verifica."""
    sys.path.insert(0, str(ROOT / "researcher"))
    import loop
    d = cartella()
    (d / "referee_report.json").write_text("{}")
    comandi = []
    originale, loop.esegui = loop.esegui, lambda cmd, cwd=None: comandi.append(cmd)
    try:
        for shell in ("container", "full"):
            loop.passo_referee(argparse.Namespace(referee="cli", shell=shell), d, {"attempt_id": "attempt_001"}, 1)
    finally:
        loop.esegui = originale
    assert comandi[0][-2:] == ["--run-code-in", "container"]
    assert "--run-code-in" not in comandi[1]


def test_perimetro_toccato_durante_il_referee_ferma_il_loop():
    """Il codice rieseguito dal Referee gira DOPO il controllo sul Researcher: se tocca l'enunciato, il loop si
    ferma e non si fida del verdetto, anche se dice READY_FOR_HUMAN."""
    sys.path.insert(0, str(ROOT / "researcher"))
    import loop
    d = cartella()
    tentativo = {"attempt_id": "attempt_001", "approach_family": "x", "subgoal": "s"}

    def referee_che_manomette(args, workdir, attempt, i):
        (workdir / "problem.md").write_text("enunciato ammorbidito")
        report = {"attempt_id": "attempt_001", "verdict": "UNKNOWN_STATUS", "review_status": "READY_FOR_HUMAN"}
        (workdir / "referee_report.json").write_text(json.dumps(report))
        return report

    originali = loop.passo_researcher, loop.passo_referee
    loop.passo_researcher, loop.passo_referee = (lambda args, workdir: tentativo), referee_che_manomette
    try:
        motivo, voce = loop.iterazione(argparse.Namespace(), d, 1)
    finally:
        loop.passo_researcher, loop.passo_referee = originali
    assert "perimetro" in motivo and voce["esito"] == "REJECT"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
