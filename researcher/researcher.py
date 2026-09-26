#!/usr/bin/env python3
"""
researcher.py — agente Researcher (Persona 1 del brief multi-agente di Proof Pursuit).

Cosa fa: legge lo stato condiviso di una cartella di lavoro, costruisce un prompt, chiede al modello UN tentativo
strutturato (JSON conforme a shared/schemas/attempt.schema.json), lo salva e rileva la stagnazione.
Cosa NON fa: non giudica il tentativo (Referee), non inventa strategie nuove (Creative), non aggiorna
highest_verified_cell (Orchestrator). L'unico campo di state.json che tocca è stagnation_count.

Comandi:
  run     --workdir DIR [--backend cli|api|mock] [--model M] [--effort E] [--shell] [--dry-run] [--strict]
  record  --workdir DIR --report FILE     archivia il verdetto del Referee accanto al tentativo
  history --workdir DIR                   riepilogo tentativi/verdetti

Backend: cli = `claude -p` headless (abbonamento, nessuna chiave); api = SDK anthropic; mock = deterministico per i test.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA_PATH = ROOT / "shared" / "schemas" / "attempt.schema.json"
PROMPT_PATH = HERE / "researcher_prompt.md"

# File di contesto che il Researcher legge se esistono (il brief richiede che funzioni anche senza).
CONTEXT_FILES = ["problem.md", "state.json", "verified_claims.md", "failed_attempts.md",
                 "creative_ideas.json", "referee_report.json"]
# Regola del brief: tre tentativi consecutivi, stesso metodo, stesso motivo ⇒ stagnazione.
STAGNATION_WINDOW = 3

# Due modalità di shell per il backend CLI (scelte con --shell sandbox|full):
#  - sandbox: solo Python e lettura/scrittura dentro runs/<problema>/sandbox; niente rete, pip, git, rm.
#    Perché: calcoli ESATTI e riproducibili senza rischi per il repo.
#  - full: tutti gli strumenti di Claude Code (Bash libero, WebSearch, WebFetch), nessuna richiesta di permesso,
#    accesso al repo intero. Perché: il team vuole che il Researcher cerchi letteratura, installi pacchetti nel
#    venv e riusi gli esperimenti esistenti. Va lanciato da un terminale umano.
SHELL_MODES = {
    "sandbox": ["--tools", "Bash,Read,Write,Edit,Glob,Grep",
                "--allowedTools", "Bash(python3 *)", "Bash(python3:*)", "Bash(timeout *)", "Bash(ls *)", "Bash(ls)",
                "Bash(cat *)", "Bash(wc *)", "Bash(head *)", "Bash(tail *)", "Read", "Write", "Edit", "Glob", "Grep",
                "--disallowedTools", "Bash(curl *)", "Bash(wget *)", "Bash(pip *)", "Bash(rm *)", "Bash(git *)",
                "Bash(ssh *)", "WebFetch", "WebSearch",
                "--permission-mode", "dontAsk"],
    "full": ["--permission-mode", "bypassPermissions", "--add-dir", str(ROOT)],
}


# =============================================================================== lettura/scrittura file
def read_text(path: Path):
    """Ritorna il testo del file, oppure None se manca: i file di contesto sono tutti facoltativi."""
    return path.read_text() if path.exists() else None


def read_json(path: Path):
    """Ritorna il JSON del file, None se manca o è malformato (avvisa ma non blocca: meglio un tentativo
    con meno contesto che nessun tentativo)."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as err:
        print(f"[researcher] WARN {path.name} non è JSON valido ({err}); ignorato", file=sys.stderr)
        return None


def write_json(path: Path, data):
    """Scrive JSON leggibile (indentato, accenti non escapati) così i collaboratori possono leggerlo su GitHub."""
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def default_state(problem_id: str):
    """Stato minimo conforme a state.schema.json, usato quando state.json non esiste ancora."""
    return {"problem_id": problem_id, "highest_verified_cell": 0, "current_target": "cell_1",
            "current_blocker": "", "verified_claims": [], "failed_attempts": [], "stagnation_count": 0,
            "cell_status": {}}


# =============================================================================== contesto e storia
def load_history(workdir: Path):
    """Ricostruisce la storia strutturata: per ogni attempts/attempt_NNN.json cerca il referee_NNN.json gemello.
    Serve sia per il prompt (cosa è già stato provato) sia per la rilevazione della stagnazione."""
    history = []
    for attempt_path in sorted(glob.glob(str(workdir / "attempts" / "attempt_*.json"))):
        number = int(Path(attempt_path).stem.split("_")[1])
        report = read_json(workdir / "attempts" / f"referee_{number:03d}.json")
        history.append({"n": number, "attempt": read_json(Path(attempt_path)), "report": report})
    return history


def load_context(workdir: Path):
    """Carica tutti i file di contesto in un dizionario; i .json come oggetti, i .md come testo."""
    context = {}
    for name in CONTEXT_FILES:
        path = workdir / name
        context[name] = read_json(path) if name.endswith(".json") else read_text(path)
    if context["state.json"] is None:
        context["state.json"] = default_state(workdir.name)
    context["history"] = load_history(workdir)
    context["literature"] = read_json(workdir / "literature.json") or []  # prodotto da literature.py (arXiv)
    return context


def next_attempt_number(workdir: Path):
    """Numero progressivo del prossimo tentativo (1 se la cartella è vuota)."""
    numbers = [int(Path(p).stem.split("_")[1]) for p in glob.glob(str(workdir / "attempts" / "attempt_*.json"))]
    return max(numbers, default=0) + 1


def target_cell_from_state(state):
    """Estrae il numero di cella da current_target (es. 'cell_3' → 3); in mancanza, la cella dopo l'ultima verificata."""
    match = re.search(r"(\d+)", str(state.get("current_target", "")))
    return int(match.group(1)) if match else state.get("highest_verified_cell", 0) + 1


# =============================================================================== stagnazione
def _words(text):
    """Insieme di parole significative di un testo, per confrontare due motivi di rigetto."""
    stop = {"the", "a", "an", "of", "to", "is", "in", "and", "not", "that"}
    return set(re.findall(r"[a-z0-9]+", (text or "").lower())) - stop


def similar(text_a, text_b, threshold=0.5):
    """Vero se due testi condividono almeno metà delle parole (indice di Jaccard).
    Perché: il brief chiede 'stesso motivo di fallimento' e i Referee riformulano; un confronto esatto non basterebbe."""
    words_a, words_b = _words(text_a), _words(text_b)
    if not words_a or not words_b:
        return False
    return len(words_a & words_b) / len(words_a | words_b) >= threshold


def detect_stagnation(history, window=STAGNATION_WINDOW):
    """Applica la regola del brief agli ultimi `window` tentativi giudicati:
    tutti REJECT, nessun claim accettato, stessa approach_family, motivi di rigetto simili.
    Ritorna (stagna?, spiegazione)."""
    recent = [h for h in history if h["attempt"] and h["report"]][-window:]
    if len(recent) < window:
        return False, ""
    all_rejected = all(h["report"].get("verdict") == "REJECT" for h in recent)
    nothing_accepted = not any(h["report"].get("accepted_claims") for h in recent)
    families = {h["attempt"].get("approach_family") for h in recent}
    errors = [h["report"].get("fatal_error") or "" for h in recent]
    same_reason = all(similar(errors[0], e) for e in errors[1:])
    if all_rejected and nothing_accepted and len(families) == 1 and same_reason:
        return True, f"{window} REJECT consecutivi con approach_family={families.pop()} e motivo simile: {errors[-1][:120]}"
    return False, ""


# =============================================================================== costruzione del prompt
def _json_block(title, data):
    """Sezione Markdown con un blocco JSON: il modello legge meglio lo stato se è delimitato e indentato."""
    return f"# {title}\n```json\n{json.dumps(data, indent=1, ensure_ascii=False)}\n```"


def _history_section(history):
    """Riassunto degli ultimi 6 tentativi in una riga ciascuno: famiglia, sotto-obiettivo, verdetto, errore fatale."""
    lines = []
    for h in [h for h in history if h["attempt"]][-6:]:
        attempt, report = h["attempt"], h["report"] or {}
        lines.append(f"- attempt_{h['n']:03d}: family={attempt.get('approach_family')} | subgoal={attempt.get('subgoal')} | "
                     f"verdict={report.get('verdict', 'PENDING')} | fatal_error={report.get('fatal_error')}")
    return "# RECENT ATTEMPT HISTORY (structured)\n" + "\n".join(lines) if lines else ""


def _shell_section(shell_dir, mode):
    """Istruzioni per l'uso della shell. Le regole di rigore (script salvati, insieme finito dichiarato, float solo
    per esplorare) valgono in entrambe le modalità; in `full` si aggiungono rete e repo, con l'obbligo di citare
    con precisione ciò che si legge online e di non presentare come letta una fonte non letta."""
    rigor = ("Save every script you rely on as a file in the working directory and copy it into `code_used` with "
             "`rigor` set honestly; state the finite set the computation covers and its wall-clock time. "
             "Floating point is exploration only. Keep each computation under 10 minutes.")
    if mode == "sandbox":
        return ("# SANDBOX SHELL AVAILABLE\nYou may run `python3` only (no network, no pip, no other commands) in the "
                f"current directory for exploration and EXACT computations. {rigor} Working directory: {shell_dir}")
    return ("# FULL SHELL AVAILABLE\nYou have a full shell, network access (WebSearch, WebFetch, curl) and the whole "
            f"repository at {ROOT}: read the problem folders, reuse tools/ and the .venv (numpy, mpmath); install "
            "packages in .venv only. Use the network to check literature: record exact references and quote the "
            f"statement you rely on; never present an unread source as read. {rigor} Working directory: {shell_dir}")


def build_user_prompt(context, stagnating, reason, shell_dir=None, shell_mode="sandbox"):
    """Assembla il prompt utente dalle sezioni disponibili. L'ordine va dal più stabile (problema) al più
    volatile (task), così la parte iniziale resta uguale fra iterazioni e si presta alla cache."""
    state = context["state.json"]
    verified = context["verified_claims.md"] or "\n".join(f"- {c}" for c in state.get("verified_claims", [])) or "(none)"
    sections = [
        "# PROBLEM\n" + (context["problem.md"] or "(problem.md mancante: usa solo state.json)"),
        _json_block("SHARED STATE (state.json)", state),
        "# VERIFIED CLAIMS (usable as hypotheses)\n" + verified,
        "# FAILED ATTEMPTS (do not repeat without a stated change)\n" + (context["failed_attempts.md"] or "(none recorded)"),
        _history_section(context["history"]),
    ]
    if context.get("literature"):
        from literature import sezione_prompt  # stesso pacchetto; import locale per non legare i test a arXiv
        sections.append(sezione_prompt(context["literature"]))
    if context["referee_report.json"]:
        sections.append(_json_block("LAST REFEREE REPORT", context["referee_report.json"]))
    if context["creative_ideas.json"]:
        sections.append(_json_block("CREATIVE IDEAS (the system asked for new directions; prefer these)", context["creative_ideas.json"]))
    if stagnating:
        sections.append(f"# STAGNATION DETECTED\n{reason}\nYou MUST change approach_family. If no creative ideas are listed, "
                        "pick a different family yourself and explain why it escapes the repeated fatal error.")
    if shell_dir:
        sections.append(_shell_section(shell_dir, shell_mode))
    blocker = state.get("current_blocker") or "(none stated: choose the first natural subgoal of the cell)"
    sections.append(f"# TASK\nTarget: {state.get('current_target')} (cell {target_cell_from_state(state)}). "
                    f"Blocker: {blocker}.\nProduce ONE attempt as JSON per the schema.")
    return "\n\n".join(s for s in sections if s)


# =============================================================================== backend: CLI
def _cli_command(system_prompt, user_prompt, schema, model, effort, shell, max_turns, max_budget_usd, shell_mode):
    """Costruisce la riga di comando di `claude -p`. Senza shell nessuno strumento; con shell applica la modalità
    scelta (vedi SHELL_MODES). In headless nessuno risponde ai prompt di permesso, per questo ogni modalità
    fissa a priori cosa è concesso."""
    cli_schema = {k: v for k, v in schema.items() if k not in ("$schema", "title")}  # il validatore CLI rifiuta $schema 2020-12
    cmd = ["claude", "-p", "--no-session-persistence", "--output-format", "json",
           "--json-schema", json.dumps(cli_schema), "--system-prompt", system_prompt,
           "--max-budget-usd", str(max_budget_usd)]
    if shell:
        cmd += [*SHELL_MODES[shell_mode], "--max-turns", str(max_turns)]
    else:
        cmd += ["--tools", ""]
    if model:
        cmd += ["--model", model]
    if effort:
        cmd += ["--effort", effort]
    return cmd + [user_prompt]


def _cli_meta(output, started, shell, shell_mode):
    """Metadati del run (modello, costo, tempo, turni, permessi negati) salvati nel tentativo per la tracciabilità."""
    return {"backend": "cli", "model": list((output.get("modelUsage") or {}).keys()), "cost_usd": output.get("total_cost_usd"),
            "seconds": round(time.time() - started, 1), "session_id": output.get("session_id"),
            "num_turns": output.get("num_turns"), "shell": shell_mode if shell else None,
            "permission_denials": len(output.get("permission_denials") or [])}


def call_cli(system_prompt, user_prompt, schema, model=None, effort=None, shell=None,
             max_turns=150, max_budget_usd=15.0, timeout=3600, shell_mode="sandbox"):
    """Chiama Claude Code headless e ritorna (attempt, meta). L'output è strutturato dallo schema (--json-schema).
    NOTA: con shell attiva va lanciato da un terminale umano; un agente che lancia un altro agente con permessi
    pre-autorizzati viene bloccato dal classificatore di sicurezza."""
    cmd = _cli_command(system_prompt, user_prompt, schema, model, effort, shell, max_turns, max_budget_usd, shell_mode)
    started = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                            stdin=subprocess.DEVNULL, cwd=str(shell) if shell else None)
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI exit {result.returncode}: {result.stderr[:500]}")
    output = json.loads(result.stdout)
    if output.get("is_error"):
        raise RuntimeError(f"claude CLI error: {output.get('result')}")
    attempt = output.get("structured_output") or json.loads(output["result"])
    return attempt, _cli_meta(output, started, shell, shell_mode)


# =============================================================================== backend: SDK
def call_api(system_prompt, user_prompt, schema, model=None, effort=None, **_):
    """Chiama l'API con l'SDK anthropic (richiede credenziali). Streaming perché l'output può essere lungo;
    fallbacks "default" perché un rifiuto dei classificatori non deve fermare il loop. NON testato: manca la chiave."""
    import anthropic  # importato qui: dipendenza necessaria solo a questo backend
    client = anthropic.Anthropic()
    output_config = {"format": {"type": "json_schema", "schema": schema}}
    if effort:
        output_config["effort"] = effort
    started = time.time()
    with client.messages.stream(
        model=model or "claude-opus-5", max_tokens=64000, system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}], output_config=output_config,
        extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"}, extra_body={"fallbacks": "default"},
    ) as stream:
        response = stream.get_final_message()
    if response.stop_reason == "refusal":
        raise RuntimeError(f"refusal: {getattr(response, 'stop_details', None)}")
    text = next(block.text for block in response.content if block.type == "text")
    meta = {"backend": "api", "model": [response.model], "seconds": round(time.time() - started, 1),
            "usage": {"in": response.usage.input_tokens, "out": response.usage.output_tokens}}
    return json.loads(text), meta


# =============================================================================== backend: mock
def _mock_family(user_prompt):
    """Sceglie la famiglia di approccio come farebbe un Researcher sensato: segue le idee creative se presenti,
    altrimenti dopo un REJECT evita le famiglie già usate. Serve a testare il loop senza chiamare modelli."""
    families = ["direct_proof", "induction", "contradiction", "algebraic_reformulation", "extremal"]
    used = re.findall(r"family=(\w+)", user_prompt)
    if "# CREATIVE IDEAS" in user_prompt:
        idea = re.search(r'"approach_family":\s*"(\w+)"', user_prompt.split("# CREATIVE IDEAS")[-1])
        if idea:
            return idea.group(1)
    rejected = "# STAGNATION DETECTED" in user_prompt or ("# LAST REFEREE REPORT" in user_prompt and '"REJECT"' in user_prompt)
    if rejected:
        return next((f for f in families if f not in used), "other")
    return "direct_proof"


def call_mock(system_prompt, user_prompt, schema, model=None, effort=None, **_):
    """Backend deterministico per i test: nessuna chiamata, risposta sempre conforme allo schema."""
    family = _mock_family(user_prompt)
    cell = int(re.search(r"cell (\d+)", user_prompt).group(1))
    attempt = {"target_cell": cell, "subgoal": "mock subgoal", "approach": f"mock {family}", "approach_family": family,
               "reason_for_choice": "mock: avoid families already rejected" if "family=" in user_prompt else "mock: first natural approach",
               "literature_position": "none found" if "# LITERATURE" not in user_prompt else "mock: cites the listed abstracts",
               "proof_attempt": "(x-1)^2 >= 0 hence x^2 - 2x + 1 >= 0, i.e. x^2 + 1 >= 2x.", "claims_used": [],
               "sources_used": [], "code_used": [], "claimed_progress": "mock", "claimed_status": "CELL_SOLVED_CANDIDATE",
               "self_reported_gaps": [], "request_creative": False}
    return attempt, {"backend": "mock"}


BACKENDS = {"cli": call_cli, "api": call_api, "mock": call_mock}


# =============================================================================== validazione (senza dipendenze)
_TYPE_CHECKS = {"array": list, "string": str, "integer": int, "boolean": bool}


def validate_attempt(data, schema):
    """Controllo leggero dello schema (campi obbligatori, campi extra, tipi, enum). Perché non jsonschema:
    evita una dipendenza per un controllo che sta in dieci righe; il Referee farà comunque il controllo vero."""
    errors = [f"campo mancante: {k}" for k in schema["required"] if k not in data]
    errors += [f"campo non ammesso: {k}" for k in data if k not in schema["properties"]]
    for key, value in data.items():
        spec = schema["properties"].get(key, {})
        if "enum" in spec and value not in spec["enum"]:
            errors.append(f"{key}: valore '{value}' non in enum")
        expected = _TYPE_CHECKS.get(spec.get("type"))
        if expected and not isinstance(value, expected):
            errors.append(f"{key}: atteso {spec['type']}")
    return errors


# =============================================================================== comando run
def bump_stagnation(workdir: Path, state, reason):
    """Incrementa stagnation_count in state.json (unico campo che il Researcher può toccare) e lo segnala."""
    state["stagnation_count"] = int(state.get("stagnation_count", 0)) + 1
    write_json(workdir / "state.json", state)
    print(f"[researcher] STAGNAZIONE: {reason} -> stagnation_count={state['stagnation_count']}", file=sys.stderr)


def save_attempt(workdir: Path, state, data, meta, stagnating, schema_errors):
    """Salva il tentativo numerato in attempts/ e una copia come attempt.json (l'input del Referee)."""
    attempt_id = f"attempt_{next_attempt_number(workdir):03d}"
    record = {"attempt_id": attempt_id, "problem_id": state.get("problem_id"), "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
              "meta": meta, "stagnation_detected": stagnating, "schema_errors": schema_errors, **data}
    write_json(workdir / "attempts" / f"{attempt_id}.json", record)
    write_json(workdir / "attempt.json", record)
    return attempt_id, workdir / "attempts" / f"{attempt_id}.json"


def cmd_run(args):
    """Un'iterazione del loop: contesto → stagnazione? → prompt → modello → validazione → salvataggio."""
    workdir = Path(args.workdir)
    (workdir / "attempts").mkdir(parents=True, exist_ok=True)
    context = load_context(workdir)
    state = context["state.json"]

    stagnating, reason = detect_stagnation(context["history"])
    if stagnating:
        bump_stagnation(workdir, state, reason)

    shell_dir = None
    if args.shell:
        shell_dir = (workdir / "sandbox").resolve()  # cartella di lavoro del modello, anche in modalità full
        shell_dir.mkdir(exist_ok=True)
    user_prompt = build_user_prompt(context, stagnating, reason, shell_dir, args.shell or "sandbox")
    if args.dry_run:
        print(user_prompt)
        return 0

    # Senza chiave API il default è la CLI (abbonamento); il mock si sceglie solo esplicitamente.
    backend = args.backend or ("api" if os.environ.get("ANTHROPIC_API_KEY") else "cli")
    schema = json.loads(SCHEMA_PATH.read_text())
    data, meta = BACKENDS[backend](PROMPT_PATH.read_text(), user_prompt, schema, model=args.model, effort=args.effort,
                                   shell=shell_dir, max_turns=args.max_turns, max_budget_usd=args.max_budget_usd,
                                   shell_mode=args.shell or "sandbox")
    data.setdefault("request_creative", False)
    if stagnating:
        data["request_creative"] = True  # la richiesta al Creative parte anche se il modello non l'ha impostata
    schema_errors = validate_attempt(data, schema)
    if schema_errors:
        print("[researcher] output non conforme allo schema: " + "; ".join(schema_errors), file=sys.stderr)
        if args.strict:
            return 2

    attempt_id, path = save_attempt(workdir, state, data, meta, stagnating, schema_errors)
    print(json.dumps({"attempt_id": attempt_id, "target_cell": data.get("target_cell"),
                      "approach_family": data.get("approach_family"), "claimed_status": data.get("claimed_status"),
                      "request_creative": data["request_creative"], "file": str(path), "meta": meta}, ensure_ascii=False))
    return 0


# =============================================================================== comandi record e history
def append_failed_attempt(workdir: Path, number, report):
    """Aggiunge una riga leggibile a failed_attempts.md, così il prossimo prompt mostra cosa è già fallito e perché."""
    attempt = read_json(workdir / "attempts" / f"attempt_{number:03d}.json") or {}
    with open(workdir / "failed_attempts.md", "a") as f:
        f.write(f"- attempt_{number:03d} [{attempt.get('approach_family')}] {attempt.get('subgoal')}: "
                f"{report.get('verdict')} — {report.get('fatal_error')}\n")


def cmd_record(args):
    """Archivia il verdetto del Referee come referee_NNN.json (gemello del tentativo) e come referee_report.json."""
    workdir = Path(args.workdir)
    report = read_json(Path(args.report))
    if report is None:
        print("report non leggibile", file=sys.stderr)
        return 2
    match = re.search(r"(\d+)", report.get("attempt_id") or "")
    number = int(match.group(1)) if match else next_attempt_number(workdir) - 1  # senza id: l'ultimo tentativo
    write_json(workdir / "attempts" / f"referee_{number:03d}.json", report)
    write_json(workdir / "referee_report.json", report)
    if report.get("verdict") in ("REJECT", "COUNTEREXAMPLE_FOUND"):
        append_failed_attempt(workdir, number, report)
    print(f"registrato referee_{number:03d}.json ({report.get('verdict')})")
    return 0


def cmd_history(args):
    """Stampa una riga per tentativo: famiglia, stato dichiarato, verdetto, inizio dell'errore fatale."""
    for h in load_history(Path(args.workdir)):
        attempt, report = h["attempt"] or {}, h["report"] or {}
        print(f"attempt_{h['n']:03d}  {attempt.get('approach_family'):<26} {attempt.get('claimed_status'):<26} "
              f"-> {report.get('verdict', 'PENDING'):<16} {(report.get('fatal_error') or '')[:70]}")
    return 0


# =============================================================================== CLI
def build_parser():
    """Definisce i tre sottocomandi; tenuto separato da main per leggibilità."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--workdir", required=True)
    run.add_argument("--backend", choices=list(BACKENDS))
    run.add_argument("--model")
    run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    run.add_argument("--shell", choices=list(SHELL_MODES),
                     help="sandbox = solo python3 in <workdir>/sandbox; full = tutti gli strumenti, rete inclusa (solo backend cli)")
    run.add_argument("--max-turns", type=int, default=150)
    run.add_argument("--max-budget-usd", type=float, default=15.0)
    run.add_argument("--dry-run", action="store_true", help="stampa solo il prompt costruito")
    run.add_argument("--strict", action="store_true", help="esci con errore se l'output viola lo schema")
    record = sub.add_parser("record")
    record.add_argument("--workdir", required=True)
    record.add_argument("--report", required=True)
    history = sub.add_parser("history")
    history.add_argument("--workdir", required=True)
    return parser


def main():
    args = build_parser().parse_args()
    return {"run": cmd_run, "record": cmd_record, "history": cmd_history}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
