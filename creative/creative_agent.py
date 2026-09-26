#!/usr/bin/env python3
"""creative_agent.py — agente Creative (Persona 3 del brief multi-agente di Proof Pursuit).

Cosa fa: legge una cartella di lavoro `runs/<problem_id>/` (stesso layout che usa il Researcher),
capisce COSA si sta ripetendo nei tentativi recenti, e scrive `creative_ideas.json` con proposte
SAFE/MEDIUM/WILD, ciascuna con un primo test concreto.
Cosa NON fa: non giudica se un tentativo è corretto (Referee), non decide se una cella è risolta,
non certifica nessuna matematica. Le sue idee sono direzioni da provare, non prove.

Comandi:
  run --workdir DIR [--backend rule_based|cli|api] [--model M] [--effort E] [--dry-run] [--auto]

--auto: non genera incondizionatamente, chiede prima ad activation.should_activate se ha senso
attivarsi ora (segnale di stagnazione del Researcher, tetto di attivazioni per cella, stato non
invariato dall'ultima attivazione) e registra ogni attivazione in runs/<problem>/creative/. Senza
--auto il comando genera e scrive sempre: è il modo in cui i test e un uso manuale restano semplici.

Backend: rule_based = deterministico, nessuna chiamata a modelli (funziona sempre, anche fuori dal
repo condiviso); cli/api = riusano call_cli/call_api di researcher/researcher.py (stesso "wrapper LLM"
del Researcher, per non duplicarne uno) — richiedono di essere eseguiti dalla radice del repo condiviso,
dove esistono researcher/ e shared/schemas/.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

from .activation import (
    STAGNATION_WINDOW,
    ActivationRecord,
    analyze_history,
    fingerprint,
    load_activation_history,
    next_activation_number,
    save_activation,
    should_activate,
)
from .schemas import APPROACH_FAMILIES, AttemptRecord, CreativeIdea, CreativeInput, CreativeOutput
from .validation import validate_output

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # radice del repo condiviso quando creative/ vi è stato integrato
PROMPT_PATH = HERE / "prompt.md"
SCHEMA_PATH = ROOT / "shared" / "schemas" / "creative_ideas.schema.json"

# File di contesto in Markdown, tutti facoltativi (stessa convenzione del Researcher: deve
# funzionare anche senza, con meno contesto invece di bloccarsi).
STATE_FILE = "state.json"
CONTEXT_TEXT_FILES = {"problem_text": "problem.md", "verified_claims_text": "verified_claims.md",
                      "failed_attempts_text": "failed_attempts.md"}


# =============================================================================== lettura/scrittura file
def read_text(path: Path):
    """Ritorna il testo del file, o None se manca: i file di contesto sono tutti facoltativi."""
    return path.read_text() if path.exists() else None


def read_json(path: Path):
    """Ritorna il JSON del file, o None se manca o è malformato (avvisa ma non blocca)."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as err:
        print(f"[creative] WARN {path.name} non è JSON valido ({err}); ignorato", file=sys.stderr)
        return None


def write_json(path: Path, data):
    """Scrive JSON leggibile (indentato, accenti non escapati) per revisione umana su GitHub."""
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


# =============================================================================== caricamento dello stato condiviso
def load_history(workdir: Path) -> list[AttemptRecord]:
    """Ricostruisce la storia strutturata: per ogni attempts/attempt_NNN.json cerca il referee_NNN.json
    gemello. Stessa logica di researcher.load_history, riletta qui per non dipendere da quel file."""
    history = []
    for attempt_path in sorted(glob.glob(str(workdir / "attempts" / "attempt_*.json"))):
        number = int(Path(attempt_path).stem.split("_")[1])
        report = read_json(workdir / "attempts" / f"referee_{number:03d}.json")
        history.append(AttemptRecord(number=number, attempt=read_json(Path(attempt_path)) or {}, referee_report=report))
    return history


def load_creative_input(workdir: Path) -> CreativeInput:
    """Legge tutto ciò che serve da una cartella `runs/<problem_id>/`. Il problem_id di default viene
    dal nome della cartella quando state.json manca ancora."""
    state = read_json(workdir / STATE_FILE) or {"problem_id": workdir.name}
    texts = {field: read_text(workdir / name) or "" for field, name in CONTEXT_TEXT_FILES.items()}
    return CreativeInput(
        problem_id=str(state.get("problem_id", workdir.name)),
        current_target=str(state.get("current_target", "")),
        current_blocker=str(state.get("current_blocker", "")),
        verified_claims=[str(c) for c in (state.get("verified_claims") or [])],
        stagnation_count=int(state.get("stagnation_count", 0)),
        cell_status=dict(state.get("cell_status") or {}),
        history=load_history(workdir),
        **texts,
    )


# La diagnosi di stagnazione (analyze_history) e la decisione se attivarsi (should_activate) vivono in
# activation.py: sono importate in cima al file, non ridefinite qui.


# =============================================================================== costruzione del prompt (backend LLM)
def _json_block(title: str, data) -> str:
    """Sezione Markdown con un blocco JSON, come in researcher.py: il modello legge meglio uno stato delimitato."""
    return f"# {title}\n```json\n{json.dumps(data, indent=1, ensure_ascii=False)}\n```"


def build_prompt(state: CreativeInput, analysis: dict) -> str:
    """Assembla il prompt: istruzioni fisse da prompt.md + stato corrente serializzato."""
    template = PROMPT_PATH.read_text(encoding="utf-8")
    history_lines = [f"- attempt_{h.number:03d}: family={h.approach_family} | verdict={h.verdict} | "
                     f"fatal_error={h.fatal_error}" for h in state.history[-6:]]
    payload = {
        "problem_id": state.problem_id, "current_target": state.current_target,
        "current_blocker": state.current_blocker, "verified_claims": state.verified_claims,
        "stagnation_count": state.stagnation_count, "cell_status": state.cell_status,
        "stagnation_analysis": analysis,
    }
    sections = [template, _json_block("CURRENT STATE", payload)]
    if history_lines:
        sections.append("# RECENT ATTEMPT HISTORY\n" + "\n".join(history_lines))
    if state.problem_text:
        sections.append("# PROBLEM\n" + state.problem_text)
    if state.failed_attempts_text:
        sections.append("# FAILED ATTEMPTS (Markdown log)\n" + state.failed_attempts_text)
    return "\n\n".join(sections)


# =============================================================================== generatore offline (backend rule_based)
_RISK_FAMILY_PREFERENCE = {
    "SAFE": ["special_case", "stronger_or_weaker_lemma", "case_analysis"],
    "MEDIUM": ["algebraic_reformulation", "matrix_formulation", "equivalent_statement", "reduction"],
    "WILD": ["counterexample_search", "probabilistic", "projective_spherical", "graph_formulation"],
}


def _pick_family(risk: str, exclude: set[str]) -> str:
    """Sceglie una approach_family per il livello di rischio dato, evitando quelle in `exclude`
    (la famiglia ripetuta e, quando possibile, tutte quelle già tentate)."""
    preferred = _RISK_FAMILY_PREFERENCE[risk]
    for family in preferred:
        if family not in exclude:
            return family
    for family in APPROACH_FAMILIES:
        if family not in exclude:
            return family
    return "other"  # tutte le famiglie sono già state tentate: caso limite, ma il codice non deve rompersi


def _idea_for(risk: str, family: str, state: CreativeInput, analysis: dict) -> CreativeIdea:
    """Costruisce un'idea concreta per il livello di rischio e la famiglia scelti, agganciata al
    blocco effettivo (current_blocker / repeated_fatal_error), non un consiglio generico."""
    target = state.current_target or "(cella non specificata)"
    blocker = state.current_blocker or analysis.get("repeated_fatal_error") or "(nessun blocco indicato)"
    method = family.replace("_", " ")
    why_different = f"Non è '{analysis['repeated_family']}': cambia esattamente il metodo che si ripeteva." \
        if analysis.get("repeated_family") else "Non ripete un metodo già scartato in questa run."
    return CreativeIdea(
        id=f"idea_{risk.lower()}", risk=risk, method=method, approach_family=family,
        why_different=why_different,
        why_it_might_work=f"Attacca '{target}' da un angolo che non ha ereditato l'ostacolo riportato "
                          f"({blocker[:160]}), perché non si basa sullo stesso passaggio.",
        first_test=f"Applicare '{method}' al caso più piccolo non ancora chiuso di '{target}' e verificare "
                   f"a mano se l'ostacolo ('{blocker[:120]}') si ripresenta.",
        expected_gain="Risolve un caso speciale, oppure isola con precisione dove sta l'ostacolo.",
        main_risk="Può ridursi a un problema altrettanto difficile: trattare il primo test come filtro rapido, non come prova.",
    )


def generate_rule_based(state: CreativeInput) -> CreativeOutput:
    """Backend di default: nessuna chiamata a modelli, sempre disponibile e testabile offline.
    Non è solo un doppio per i test: è una strategia minima ma reale (guarda cosa si ripete e
    propone tre famiglie diverse, una per livello di rischio)."""
    analysis = analyze_history(state)
    exclude = {analysis["repeated_family"]} if analysis["repeated_family"] else set()
    exclude |= set(analysis["families_ever_tried"]) if len(analysis["families_ever_tried"]) < len(APPROACH_FAMILIES) else set()

    ideas = []
    for risk in ("SAFE", "MEDIUM", "WILD"):
        family = _pick_family(risk, exclude)
        ideas.append(_idea_for(risk, family, state, analysis))
        exclude.add(family)  # non riproporre la stessa famiglia in due idee diverse

    avoid = []
    if analysis["repeated_family"]:
        avoid.append(f"altri tentativi con approach_family='{analysis['repeated_family']}' senza un cambiamento reale")
    if analysis["repeated_fatal_error"]:
        avoid.append(f"ripetere un argomento che il Referee ha già respinto per lo stesso motivo: "
                     f"\"{analysis['repeated_fatal_error'][:200]}\"")

    if analysis["repeated_family"]:
        blocker_analysis = (f"Gli ultimi {STAGNATION_WINDOW} tentativi giudicati usano tutti "
                            f"approach_family='{analysis['repeated_family']}' ed è per questo che la ricerca è bloccata.")
    else:
        blocker_analysis = f"Nessuna famiglia singola domina gli ultimi tentativi; propongo comunque direzioni " \
                           f"diverse per: {state.current_blocker or state.current_target or '(stato non specificato)'}."

    repetition_patterns = [f"approach_family ripetuta: {analysis['repeated_family']}"] if analysis["repeated_family"] else []
    if analysis["repeated_fatal_error"]:
        repetition_patterns.append(f"stesso errore fatale (parole simili): {analysis['repeated_fatal_error'][:120]}")

    return CreativeOutput(blocker_analysis=blocker_analysis, avoid=avoid, ideas=ideas, repetition_patterns=repetition_patterns)


# =============================================================================== backend LLM (riuso di researcher.py)
def _idea_from_dict(d: dict) -> CreativeIdea:
    """Legge un'idea proposta dal modello, con default onesti per campi mancanti (mai far crashare
    l'orchestratore per un campo assente: meglio un'idea incompleta di nessuna idea)."""
    return CreativeIdea(
        id=str(d.get("id", "idea")), risk=str(d.get("risk", "MEDIUM")).upper(),
        method=str(d.get("method", "")), why_different=str(d.get("why_different", "")),
        why_it_might_work=str(d.get("why_it_might_work", "")), first_test=str(d.get("first_test", "")),
        expected_gain=str(d.get("expected_gain", "")), main_risk=str(d.get("main_risk", "")),
        approach_family=str(d.get("approach_family", "")),
    )


def _parse_llm_output(raw: str, state: CreativeInput) -> CreativeOutput:
    """Converte la risposta JSON del modello in CreativeOutput, poi la fa passare da validate_output.
    Su qualunque errore di parsing O su un errore strutturale (id duplicati, risk non valido, campo
    obbligatorio vuoto) ricade sul generatore offline: mai scrivere un creative_ideas.json che non
    rispetta lo schema condiviso. I soli warning (es. copertura SAFE/MEDIUM/WILD incompleta, linguaggio
    da auto-certificazione) restano visibili in cima a blocker_analysis invece di bloccare l'output."""
    try:
        data = json.loads(raw)
        ideas = [_idea_from_dict(idea) for idea in data["ideas"]]
        if not ideas:
            raise ValueError("il modello non ha proposto nessuna idea")
        output = CreativeOutput(blocker_analysis=str(data.get("blocker_analysis", "")),
                                avoid=[str(x) for x in (data.get("avoid") or [])], ideas=ideas,
                                repetition_patterns=[str(x) for x in (data.get("repetition_patterns") or [])])
        errors, warnings = validate_output(output)
        if errors:
            raise ValueError("output non conforme: " + "; ".join(errors))
        if warnings:
            output.blocker_analysis = f"[AVVISI: {'; '.join(warnings)}] {output.blocker_analysis}"
        return output
    except Exception as err:  # qualunque cosa vada storta (parsing o validazione): mai bloccare il loop
        fallback = generate_rule_based(state)
        fallback.blocker_analysis = f"[risposta del modello non accettata ({err}); uso il generatore " \
                                    f"offline] {fallback.blocker_analysis}"
        return fallback


def call_llm_backend(backend: str, state: CreativeInput, model, effort) -> tuple[CreativeOutput, dict]:
    """Chiama il backend `cli` o `api` riusando il wrapper già scritto dal Researcher (stesso schema-in
    JSON-out), invece di duplicare la costruzione del comando/della chiamata SDK. Se researcher.py non è
    raggiungibile (es. questa copia non è ancora dentro il repo condiviso), ricade sul backend offline."""
    try:
        sys.path.insert(0, str(ROOT))
        from researcher.researcher import call_api, call_cli  # import tardivo: solo quando serve davvero
    except ImportError as err:
        fallback = generate_rule_based(state)
        fallback.blocker_analysis = f"[backend '{backend}' non disponibile ({err}): eseguire da dentro il " \
                                    f"repo condiviso, dove esiste researcher/researcher.py] {fallback.blocker_analysis}"
        return fallback, {"backend": "rule_based_fallback"}

    analysis = analyze_history(state)
    prompt = build_prompt(state, analysis)
    schema = json.loads(SCHEMA_PATH.read_text()) if SCHEMA_PATH.exists() else {"required": [], "properties": {}}
    caller = call_cli if backend == "cli" else call_api
    raw_output, meta = caller("Sei il Creative Agent. Rispondi SOLO con il JSON richiesto.", prompt, schema,
                              model=model, effort=effort)
    raw_text = raw_output if isinstance(raw_output, str) else json.dumps(raw_output)
    return _parse_llm_output(raw_text, state), meta


# =============================================================================== comando run
def _generate(args, state: CreativeInput) -> tuple[CreativeOutput, dict]:
    """Sceglie il backend e produce l'output; fattorizzato fuori da cmd_run così --auto e la chiamata
    diretta condividono lo stesso percorso invece di divergere silenziosamente."""
    if args.backend in ("cli", "api"):
        return call_llm_backend(args.backend, state, args.model, args.effort)
    return generate_rule_based(state), {"backend": "rule_based"}


def cmd_run(args) -> int:
    """Un'esecuzione. Senza --auto: genera e scrive sempre (comportamento diretto, usato dai test e da
    una chiamata manuale). Con --auto: prima chiede ad activation.should_activate se ha senso attivarsi
    ORA (rispetta il segnale di stagnazione del Researcher, il tetto di attivazioni per cella, e non
    rigenera su uno stato invariato), e in caso positivo registra l'attivazione nello storico — questo
    è il punto in cui un futuro Orchestrator può limitarsi a chiamare `run --auto` a ogni iterazione
    senza dover reimplementare la logica di quando conviene farlo (Creative Agent resta comunque
    chiamabile direttamente, come richiesto: --auto è un livello in più, non l'unico modo di usarlo)."""
    workdir = Path(args.workdir)
    state = load_creative_input(workdir)

    if args.dry_run:
        print(build_prompt(state, analyze_history(state)))
        return 0

    if args.auto:
        activation_log = load_activation_history(workdir)
        activate, reason = should_activate(state, activation_log)
        if not activate:
            print(json.dumps({"activated": False, "reason": reason}, ensure_ascii=False))
            return 0

    output, meta = _generate(args, state)
    write_json(workdir / "creative_ideas.json", output.to_dict())

    if args.auto:
        record = ActivationRecord(
            number=next_activation_number(workdir), target=state.current_target, reason=reason,
            state_fingerprint=fingerprint(state),
            ideas_summary=[{"id": i.id, "risk": i.risk, "approach_family": i.approach_family,
                           "first_test": i.first_test} for i in output.ideas])
        save_activation(workdir, record)

    print(json.dumps({"ideas": len(output.ideas), "avoid": len(output.avoid), "meta": meta}, ensure_ascii=False))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--workdir", required=True)
    run.add_argument("--backend", choices=["rule_based", "cli", "api"], default="rule_based")
    run.add_argument("--model")
    run.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    run.add_argument("--dry-run", action="store_true", help="stampa solo il prompt costruito")
    run.add_argument("--auto", action="store_true",
                     help="attiva solo se should_activate lo conferma, e registra l'attivazione nello storico")
    return parser


def main():
    args = build_parser().parse_args()
    return {"run": cmd_run}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
