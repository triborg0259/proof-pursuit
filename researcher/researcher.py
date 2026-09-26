#!/usr/bin/env python3
"""
researcher.py — Researcher / autoresearch agent (Persona 1) di Proof Pursuit.

Legge il contesto condiviso in una cartella di lavoro, produce UN tentativo strutturato (attempt JSON),
lo salva in attempts/attempt_NNN.json e rileva la stagnazione. NON giudica, NON aggiorna highest_verified_cell.

Uso:
  python researcher/researcher.py run    --workdir runs/problem_1 [--backend cli|api|mock] [--model M] [--effort E]
  python researcher/researcher.py record --workdir runs/problem_1 --report referee_report.json
        (l'Orchestrator lo chiama per archiviare il verdetto accanto al tentativo: attempts/referee_NNN.json)
  python researcher/researcher.py history --workdir runs/problem_1

Backend:
  cli  — `claude -p` (Claude Code headless, usa l'abbonamento; default se nessuna chiave API)
  api  — SDK anthropic (richiede ANTHROPIC_API_KEY o profilo `ant auth login`)
  mock — risposte deterministiche per i test (nessuna chiamata)
"""
import argparse, glob, json, os, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA_PATH = ROOT / "shared" / "schemas" / "attempt.schema.json"
PROMPT_PATH = HERE / "researcher_prompt.md"

CONTEXT_FILES = ["problem.md", "state.json", "verified_claims.md", "failed_attempts.md",
                 "creative_ideas.json", "referee_report.json"]
STAGNATION_WINDOW = 3


# ----------------------------------------------------------------------------- I/O helpers
def read_text(p: Path):
    return p.read_text() if p.exists() else None


def read_json(p: Path):
    try:
        return json.loads(p.read_text()) if p.exists() else None
    except json.JSONDecodeError as e:
        print(f"[researcher] WARN {p.name} non è JSON valido ({e}); ignorato", file=sys.stderr)
        return None


def default_state(problem_id: str):
    return {"problem_id": problem_id, "highest_verified_cell": 0, "current_target": "cell_1",
            "current_blocker": "", "verified_claims": [], "failed_attempts": [], "stagnation_count": 0,
            "cell_status": {}}


def load_context(workdir: Path):
    ctx = {name: (read_json(workdir / name) if name.endswith(".json") else read_text(workdir / name))
           for name in CONTEXT_FILES}
    if ctx["state.json"] is None:
        ctx["state.json"] = default_state(workdir.name)
    ctx["history"] = load_history(workdir)
    return ctx


def load_history(workdir: Path):
    """Coppie (attempt, referee_report) in ordine cronologico, dai file attempts/attempt_NNN.json e referee_NNN.json."""
    hist = []
    for ap in sorted(glob.glob(str(workdir / "attempts" / "attempt_*.json"))):
        n = Path(ap).stem.split("_")[1]
        att = read_json(Path(ap))
        rep = read_json(workdir / "attempts" / f"referee_{n}.json")
        hist.append({"n": int(n), "attempt": att, "report": rep})
    return hist


def next_attempt_number(workdir: Path):
    nums = [int(Path(p).stem.split("_")[1]) for p in glob.glob(str(workdir / "attempts" / "attempt_*.json"))]
    return max(nums, default=0) + 1


def target_cell_from_state(state):
    m = re.search(r"(\d+)", str(state.get("current_target", "")))
    return int(m.group(1)) if m else state.get("highest_verified_cell", 0) + 1


# ----------------------------------------------------------------------------- stagnation
def _norm(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower())) - {"the", "a", "an", "of", "to", "is", "in", "and", "not", "that"}


def similar(a, b, thr=0.5):
    A, B = _norm(a), _norm(b)
    return bool(A and B) and len(A & B) / len(A | B) >= thr


def detect_stagnation(history, window=STAGNATION_WINDOW):
    """Regola del brief: 3 tentativi consecutivi, stesso metodo, stesso motivo di fallimento, nessun claim accettato."""
    recent = [h for h in history if h["attempt"] and h["report"]][-window:]
    if len(recent) < window:
        return False, ""
    if any(h["report"].get("verdict") != "REJECT" for h in recent):
        return False, ""
    if any(h["report"].get("accepted_claims") for h in recent):
        return False, ""
    fams = {h["attempt"].get("approach_family") for h in recent}
    errs = [h["report"].get("fatal_error") or "" for h in recent]
    same_reason = all(similar(errs[0], e) for e in errs[1:])
    if len(fams) == 1 and same_reason:
        return True, f"{window} REJECT consecutivi con approach_family={fams.pop()} e motivo simile: {errs[-1][:120]}"
    return False, ""


# ----------------------------------------------------------------------------- prompt
def build_user_prompt(ctx, stagnating, reason):
    state = ctx["state.json"]
    parts = []
    parts.append("# PROBLEM\n" + (ctx["problem.md"] or "(problem.md mancante: usa solo state.json)"))
    parts.append("# SHARED STATE (state.json)\n```json\n" + json.dumps(state, indent=1, ensure_ascii=False) + "\n```")
    parts.append("# VERIFIED CLAIMS (usable as hypotheses)\n" +
                 (ctx["verified_claims.md"] or "\n".join(f"- {c}" for c in state.get("verified_claims", [])) or "(none)"))
    parts.append("# FAILED ATTEMPTS (do not repeat without a stated change)\n" + (ctx["failed_attempts.md"] or "(none recorded)"))
    hist = [h for h in ctx["history"] if h["attempt"]]
    if hist:
        lines = []
        for h in hist[-6:]:
            a, r = h["attempt"], h["report"] or {}
            lines.append(f"- attempt_{h['n']:03d}: family={a.get('approach_family')} | subgoal={a.get('subgoal')} | "
                         f"verdict={r.get('verdict', 'PENDING')} | fatal_error={r.get('fatal_error')}")
        parts.append("# RECENT ATTEMPT HISTORY (structured)\n" + "\n".join(lines))
    if ctx["referee_report.json"]:
        parts.append("# LAST REFEREE REPORT\n```json\n" + json.dumps(ctx["referee_report.json"], indent=1, ensure_ascii=False) + "\n```")
    if ctx["creative_ideas.json"]:
        parts.append("# CREATIVE IDEAS (the system asked for new directions; prefer these)\n```json\n" +
                     json.dumps(ctx["creative_ideas.json"], indent=1, ensure_ascii=False) + "\n```")
    if stagnating:
        parts.append(f"# STAGNATION DETECTED\n{reason}\nYou MUST change approach_family. If no creative ideas are listed, "
                     "pick a different family yourself and explain why it escapes the repeated fatal error.")
    parts.append(f"# TASK\nTarget: {state.get('current_target')} (cell {target_cell_from_state(state)}). "
                 f"Blocker: {state.get('current_blocker') or '(none stated: choose the first natural subgoal of the cell)'}.\n"
                 "Produce ONE attempt as JSON per the schema.")
    return "\n\n".join(parts)


# ----------------------------------------------------------------------------- backends
def call_cli(system_prompt, user_prompt, schema, model=None, effort=None, timeout=1800):
    cli_schema = {k: v for k, v in schema.items() if k not in ("$schema", "title")}  # il validatore CLI rifiuta $schema 2020-12
    cmd = ["claude", "-p", "--no-session-persistence", "--output-format", "json", "--tools", "",
           "--json-schema", json.dumps(cli_schema), "--system-prompt", system_prompt]
    if model:
        cmd += ["--model", model]
    if effort:
        cmd += ["--effort", effort]
    cmd.append(user_prompt)
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if res.returncode != 0:
        raise RuntimeError(f"claude CLI exit {res.returncode}: {res.stderr[:500]}")
    out = json.loads(res.stdout)
    if out.get("is_error"):
        raise RuntimeError(f"claude CLI error: {out.get('result')}")
    data = out.get("structured_output") or json.loads(out["result"])
    meta = {"backend": "cli", "model": list((out.get("modelUsage") or {}).keys()), "cost_usd": out.get("total_cost_usd"),
            "seconds": round(time.time() - t0, 1), "session_id": out.get("session_id")}
    return data, meta


def call_api(system_prompt, user_prompt, schema, model=None, effort=None):
    import anthropic  # pip install anthropic
    client = anthropic.Anthropic()
    model = model or "claude-opus-5"
    t0 = time.time()
    with client.messages.stream(
        model=model, max_tokens=64000, system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        output_config={"format": {"type": "json_schema", "schema": schema}, **({"effort": effort} if effort else {})},
        extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"},
        extra_body={"fallbacks": "default"},
    ) as stream:
        resp = stream.get_final_message()
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"refusal: {getattr(resp, 'stop_details', None)}")
    text = next(b.text for b in resp.content if b.type == "text")
    meta = {"backend": "api", "model": [resp.model], "seconds": round(time.time() - t0, 1),
            "usage": {"in": resp.usage.input_tokens, "out": resp.usage.output_tokens}}
    return json.loads(text), meta


def call_mock(system_prompt, user_prompt, schema, model=None, effort=None):
    """Backend deterministico per i test: sceglie una famiglia diversa da quelle già fallite; legge CREATIVE IDEAS."""
    families = ["direct_proof", "induction", "contradiction", "algebraic_reformulation", "extremal"]
    used = re.findall(r"family=(\w+)", user_prompt)
    idea = re.search(r'"approach_family":\s*"(\w+)"', user_prompt.split("# CREATIVE IDEAS")[-1]) if "# CREATIVE IDEAS" in user_prompt else None
    if idea:
        fam = idea.group(1)
    elif "# STAGNATION DETECTED" in user_prompt or "# LAST REFEREE REPORT" in user_prompt and '"REJECT"' in user_prompt:
        fam = next((f for f in families if f not in used), "other")
    else:
        fam = "direct_proof"
    cell = int(re.search(r"cell (\d+)", user_prompt).group(1))
    return {"target_cell": cell, "subgoal": "mock subgoal", "approach": f"mock {fam}", "approach_family": fam,
            "reason_for_choice": "mock: avoid families already rejected" if used else "mock: first natural approach",
            "proof_attempt": "(x-1)^2 >= 0 hence x^2 - 2x + 1 >= 0, i.e. x^2 + 1 >= 2x.", "claims_used": [],
            "sources_used": [], "code_used": [], "claimed_progress": "mock", "claimed_status": "CELL_SOLVED_CANDIDATE",
            "self_reported_gaps": [], "request_creative": False}, {"backend": "mock"}


BACKENDS = {"cli": call_cli, "api": call_api, "mock": call_mock}


# ----------------------------------------------------------------------------- validation (senza dipendenze)
def validate_attempt(data, schema):
    errs = []
    for k in schema["required"]:
        if k not in data:
            errs.append(f"campo mancante: {k}")
    for k in data:
        if k not in schema["properties"]:
            errs.append(f"campo non ammesso: {k}")
    props = schema["properties"]
    for k, v in data.items():
        spec = props.get(k)
        if not spec:
            continue
        if "enum" in spec and v not in spec["enum"]:
            errs.append(f"{k}: valore '{v}' non in enum")
        t = spec.get("type")
        if t == "array" and not isinstance(v, list):
            errs.append(f"{k}: atteso array")
        if t == "string" and not isinstance(v, str):
            errs.append(f"{k}: atteso string")
        if t == "integer" and not isinstance(v, int):
            errs.append(f"{k}: atteso integer")
        if t == "boolean" and not isinstance(v, bool):
            errs.append(f"{k}: atteso boolean")
    return errs


# ----------------------------------------------------------------------------- commands
def cmd_run(a):
    workdir = Path(a.workdir)
    (workdir / "attempts").mkdir(parents=True, exist_ok=True)
    ctx = load_context(workdir)
    state = ctx["state.json"]
    schema = json.loads(SCHEMA_PATH.read_text())
    system_prompt = PROMPT_PATH.read_text()

    stagnating, reason = detect_stagnation(ctx["history"])
    if stagnating:
        state["stagnation_count"] = int(state.get("stagnation_count", 0)) + 1
        (workdir / "state.json").write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n")
        print(f"[researcher] STAGNAZIONE: {reason} -> stagnation_count={state['stagnation_count']}", file=sys.stderr)

    user_prompt = build_user_prompt(ctx, stagnating, reason)
    if a.dry_run:
        print(user_prompt)
        return 0

    backend = a.backend or ("api" if os.environ.get("ANTHROPIC_API_KEY") else "cli")
    data, meta = BACKENDS[backend](system_prompt, user_prompt, schema, model=a.model, effort=a.effort)
    data.setdefault("request_creative", False)
    if stagnating:
        data["request_creative"] = True
    errs = validate_attempt(data, schema)
    if errs:
        print("[researcher] output non conforme allo schema: " + "; ".join(errs), file=sys.stderr)
        if a.strict:
            return 2

    n = next_attempt_number(workdir)
    attempt_id = f"attempt_{n:03d}"
    record = {"attempt_id": attempt_id, "problem_id": state.get("problem_id"), "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "meta": meta, "stagnation_detected": stagnating, "schema_errors": errs, **data}
    out = workdir / "attempts" / f"{attempt_id}.json"
    out.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    (workdir / "attempt.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")  # "ultimo tentativo" per il Referee
    print(json.dumps({"attempt_id": attempt_id, "target_cell": data.get("target_cell"), "approach_family": data.get("approach_family"),
                      "claimed_status": data.get("claimed_status"), "request_creative": data["request_creative"],
                      "file": str(out), "meta": meta}, ensure_ascii=False))
    return 0


def cmd_record(a):
    workdir = Path(a.workdir)
    rep = read_json(Path(a.report))
    if rep is None:
        print("report non leggibile", file=sys.stderr); return 2
    n = int(re.search(r"(\d+)", rep.get("attempt_id") or f"{next_attempt_number(workdir) - 1}").group(1))
    (workdir / "attempts" / f"referee_{n:03d}.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    (workdir / "referee_report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    # failed_attempts.md: appendice leggibile (il Researcher la rilegge)
    if rep.get("verdict") in ("REJECT", "COUNTEREXAMPLE_FOUND"):
        att = read_json(workdir / "attempts" / f"attempt_{n:03d}.json") or {}
        with open(workdir / "failed_attempts.md", "a") as f:
            f.write(f"- attempt_{n:03d} [{att.get('approach_family')}] {att.get('subgoal')}: "
                    f"{rep.get('verdict')} — {rep.get('fatal_error')}\n")
    print(f"registrato referee_{n:03d}.json ({rep.get('verdict')})")
    return 0


def cmd_history(a):
    for h in load_history(Path(a.workdir)):
        att, rep = h["attempt"] or {}, h["report"] or {}
        print(f"attempt_{h['n']:03d}  {att.get('approach_family'):<26} {att.get('claimed_status'):<26} "
              f"-> {rep.get('verdict', 'PENDING'):<16} {(rep.get('fatal_error') or '')[:70]}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--workdir", required=True)
    r.add_argument("--backend", choices=list(BACKENDS)); r.add_argument("--model"); r.add_argument("--effort")
    r.add_argument("--dry-run", action="store_true", help="stampa solo il prompt"); r.add_argument("--strict", action="store_true")
    rc = sub.add_parser("record"); rc.add_argument("--workdir", required=True); rc.add_argument("--report", required=True)
    h = sub.add_parser("history"); h.add_argument("--workdir", required=True)
    a = ap.parse_args()
    return {"run": cmd_run, "record": cmd_record, "history": cmd_history}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
