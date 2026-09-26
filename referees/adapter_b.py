#!/usr/bin/env python3
"""adapter_b.py — ponte fra il Referee B e il contratto JSON del repo.

Cosa fa: legge una cartella di lavoro `runs/<problem_id>/` (attempt.json, state.json, problem.md),
la converte nel `ReviewInput` dei referee, chiama `referee_b.review_evidence` e riscrive la risposta
nel formato di `shared/schemas/referee_report.schema.json`, che l'orchestratore già legge.

Cosa NON fa:
- non giudica (il giudizio è tutto nel modello guidato da `prompts/b.md`);
- non esegue il codice contenuto nei tentativi: lo passa come artefatto da leggere;
- non emette mai ACCEPT, che resta una decisione umana;
- non popola `accepted_claims`, che nel contratto del repo significa "progresso verificato".

Comando:
  python -m referees.adapter_b run --workdir runs/p2_q3 [--backend mock|cli] [--rules FILE] [--out FILE]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from .contracts import Artifact, Candidate, Cell, Claim, ReviewInput, Rules, Source, VerifiedState
from .referee_b import review_evidence
from .trust import TrustedContext

ROOT = Path(__file__).resolve().parent.parent
RULES_DEFAULT = ROOT / "shared" / "competition_rules.example.json"
# Il claim bersaglio ha un id fisso: il contratto impone che il candidato dichiari il target esatto.
TARGET_CLAIM_ID = "main"
# Il Referee B da solo non può concludere: PASS significa "evidenze a posto", non "cella risolta".
VERDICT_BY_EVIDENCE = {"FAIL": "REJECT", "PARTIAL": "PARTIAL_PROGRESS", "PASS": "PARTIAL_PROGRESS"}


# =============================================================================== lettura della cartella
def read_json(path: Path):
    """Ritorna il JSON del file, None se manca. Coerente con researcher.py: i file di contesto sono facoltativi."""
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def extract_cell_statement(problem_text: str, number: int) -> str:
    """Estrae dal problem.md il testo della cella richiesta (riga che inizia con 'Cell N:').

    Perché: il contratto dei referee protegge il bersaglio esatto, quindi serve l'enunciato della
    SINGOLA cella e non tutto il problema. Se la riga manca, chi chiama deve passarlo esplicitamente.
    """
    match = re.search(rf"^Cell\s+{number}\s*:\s*(.+?)(?=\n\s*\n|\n#|\Z)", problem_text or "",
                      re.MULTILINE | re.DOTALL)
    return " ".join(match.group(1).split()) if match else ""


def resolve_statement(attempt, state, problem_text, override) -> str:
    """Sceglie l'enunciato del bersaglio: override esplicito, poi problem.md, poi current_blocker.
    Solleva un errore se nessuna fonte lo fornisce: meglio fermarsi che far giudicare un bersaglio inventato."""
    number = int(attempt.get("target_cell") or 1)
    for candidate in (override, extract_cell_statement(problem_text, number), (state or {}).get("current_blocker")):
        if candidate and candidate.strip():
            return candidate.strip()
    raise ValueError(f"Enunciato della cella {number} non trovato: usa --cell-statement")


# =============================================================================== costruzione del ReviewInput
def state_claims(state) -> list[Claim]:
    """I claim già verificati dall'orchestratore diventano il registro fidato `state.claims`."""
    return [Claim(id=f"vc_{i}", statement=text)
            for i, text in enumerate((state or {}).get("verified_claims") or [], start=1)]


def dependency_ids(attempt, verified: list[Claim]) -> tuple[list[str], list[Claim]]:
    """Traduce `claims_used` in id di claim.

    Un claim usato che coincide con un claim verificato punta a quello; uno che non coincide NON è
    verificato e viene registrato come claim del candidato (`dep_k`), così il Referee B ne valuta
    la provenienza invece di riceverlo come se fosse già acquisito.
    """
    by_text = {claim.statement: claim.id for claim in verified}
    ids, extra = [], []
    for k, text in enumerate((attempt.get("claims_used") or []), start=1):
        if text in by_text:
            ids.append(by_text[text])
        else:
            extra.append(Claim(id=f"dep_{k}", statement=text))
            ids.append(f"dep_{k}")
    return ids, extra


def build_sources(attempt) -> list[Source]:
    """`sources_used` è una lista di riferimenti testuali: diventano Source legate al bersaglio.
    L'estratto resta vuoto perché il Researcher non consegna il testo della fonte; B lo segnalerà come MISSING."""
    return [Source(id=f"src_{i}", reference=reference, claim_ids=[TARGET_CLAIM_ID])
            for i, reference in enumerate(attempt.get("sources_used") or [], start=1)]


def build_artifacts(attempt) -> list[Artifact]:
    """Ogni voce di `code_used` diventa un artefatto CODE da LEGGERE, mai da eseguire.
    Scopo e livello di rigore dichiarato sono messi in testa: sono ciò che B deve confrontare col codice."""
    artifacts = []
    for i, item in enumerate(attempt.get("code_used") or [], start=1):
        header = (f"language: {item.get('language')}\n"
                  f"rigor dichiarato dal candidato: {item.get('rigor', 'non dichiarato')}\n"
                  f"scopo dichiarato: {item.get('purpose')}\n---\n")
        artifacts.append(Artifact(id=f"code_{i}", kind="CODE", content=header + (item.get("code") or ""),
                                  claim_ids=[TARGET_CLAIM_ID]))
    return artifacts


def build_candidate(attempt, statement: str, verified: list[Claim]) -> Candidate:
    """Assembla il Candidate: la prova, il claim bersaglio con le sue dipendenze, fonti e artefatti."""
    depends_on, extra = dependency_ids(attempt, verified)
    target = Claim(id=TARGET_CLAIM_ID, statement=statement, depends_on=depends_on)
    return Candidate(attempt_id=attempt.get("attempt_id") or "attempt_000",
                     proof=attempt.get("proof_attempt") or "(nessuna prova consegnata)",
                     method_tag=attempt.get("approach_family") or "other",
                     claims=[target] + extra, sources=build_sources(attempt),
                     artifacts=build_artifacts(attempt))


def load_rules(path: Path) -> Rules:
    """Carica le regole della gara. Non hanno un default implicito: HACKATHON_START.md chiede scelte esplicite."""
    data = read_json(path)
    if data is None:
        raise FileNotFoundError(f"File delle regole assente: {path}")
    return Rules(**data)


def build_review_input(workdir: Path, rules_path: Path = RULES_DEFAULT, statement: str | None = None) -> ReviewInput:
    """Converte una cartella `runs/<problem_id>/` nel ReviewInput dei referee."""
    attempt = read_json(workdir / "attempt.json")
    if attempt is None:
        raise FileNotFoundError(f"attempt.json assente in {workdir}")
    state = read_json(workdir / "state.json") or {}
    problem_text = (workdir / "problem.md").read_text(encoding="utf-8") if (workdir / "problem.md").exists() else ""
    target = resolve_statement(attempt, state, problem_text, statement)
    number = int(attempt.get("target_cell") or 1)
    verified = state_claims(state)
    return ReviewInput(
        problem_id=attempt.get("problem_id") or state.get("problem_id") or workdir.name,
        original_problem=problem_text or target,
        cell=Cell(id=f"cell_{number}", number=number, target_claim_id=TARGET_CLAIM_ID, statement=target),
        state=VerifiedState(highest_verified_cell=int(state.get("highest_verified_cell") or 0), claims=verified),
        candidate=build_candidate(attempt, target, verified),
        rules=load_rules(rules_path))


# =============================================================================== conversione del rapporto
def blocking_issues(report) -> list:
    """Tutte le segnalazioni che non sono puramente informative, nell'ordine in cui B le ha prodotte."""
    issues = report.source_issues + report.computation_issues + report.rule_violations
    return [issue for issue in issues if issue.severity != "INFO"]


def describe(issue) -> str:
    """Rende una Issue in una riga leggibile, con i claim coinvolti."""
    scope = f" [{', '.join(issue.claim_ids)}]" if issue.claim_ids else ""
    return f"{issue.code}{scope}: {issue.detail}"


def supported_claims(report) -> list[str]:
    """Claim per cui B ritiene le evidenze sufficienti e ammesse dalle regole.

    NON finiscono in `accepted_claims`: in `shared/` quel campo significa progresso verificato, che
    richiede anche la revisione matematica e l'approvazione umana. Restano un suggerimento.
    """
    return sorted(p.claim_id for p in report.claim_provenance
                  if p.evidence_sufficient and p.permitted_by_rules
                  and not {"EXPERIMENTAL_ONLY", "UNVERIFIED"}.intersection(p.categories))


def unavailable_report(job: ReviewInput, limitation: str) -> dict:
    """Rapporto per il caso "B non è riuscito a valutare": è UNKNOWN_STATUS, mai un REJECT.
    Un errore operativo o un timeout non sono un difetto matematico del tentativo."""
    return {"attempt_id": job.candidate.attempt_id, "verdict": "UNKNOWN_STATUS",
            "highest_verified_cell": job.state.highest_verified_cell, "accepted_claims": [],
            "fatal_error": None, "citation_issue": False, "computation_issue": False,
            "next_blocker": f"Referee B non ha potuto valutare: {limitation}",
            "reasoning_summary": "Nessuna revisione delle evidenze eseguita.",
            "referee_role": "B", "evidence_verdict": None, "limitation": limitation,
            "accept_requires_human": True}


def to_referee_report(envelope, job: ReviewInput) -> dict:
    """Traduce AgentEnvelope[EvidenceReport] nel formato di shared/schemas/referee_report.schema.json.

    `verdict` non vale mai ACCEPT: B copre solo la dimensione evidenze e l'approvazione è umana.
    `highest_verified_cell` è una fotografia dello stato, mai incrementata qui.
    """
    if envelope.report is None:
        return unavailable_report(job, envelope.limitation or "motivo non riportato")
    report = envelope.report
    blocking = blocking_issues(report)
    fatal = next((i for i in blocking if i.severity == "FATAL"), None)
    return {
        "attempt_id": job.candidate.attempt_id,
        "verdict": VERDICT_BY_EVIDENCE[report.evidence_verdict],
        "highest_verified_cell": job.state.highest_verified_cell,
        "accepted_claims": [],
        "fatal_error": describe(fatal) if fatal else None,
        "citation_issue": any(i.severity != "INFO" for i in report.source_issues),
        "computation_issue": any(i.severity != "INFO" for i in report.computation_issues),
        "next_blocker": describe(blocking[0]) if blocking else
                        "Nessun blocco sulle evidenze: restano la revisione matematica e l'approvazione umana.",
        "reasoning_summary": report.reproducibility_notes,
        # Campi extra (lo schema ammette additionalProperties) per non perdere il dettaglio di B.
        "referee_role": "B",
        "evidence_verdict": report.evidence_verdict,
        "evidence_supported_claims": supported_claims(report),
        "source_issues": [describe(i) for i in report.source_issues],
        "computation_issues": [describe(i) for i in report.computation_issues],
        "rule_violations": [describe(i) for i in report.rule_violations],
        "claim_provenance": [p.model_dump(mode="json") for p in report.claim_provenance],
        "accept_requires_human": True,
    }


# =============================================================================== backend
class MockBackend:
    """Backend deterministico per i test: restituisce risposte preparate, nessuna chiamata a pagamento."""

    def __init__(self, response):
        self.response = response
        self.seen: list[dict] = []

    async def generate(self, *, role, system, payload, schema):
        """Registra ciò che riceve (serve a verificare che il payload sia corretto) e ritorna la risposta fissa."""
        self.seen.append({"role": role, "system": system, "payload": payload, "schema": schema})
        return self.response(payload) if callable(self.response) else self.response


class ClaudeCliBackend:
    """Backend che usa `claude -p` headless, come il Researcher: sfrutta l'abbonamento, nessuna chiave API.

    Nessuno strumento è concesso al modello (`--tools ""`): B deve giudicare i materiali consegnati,
    non navigare né eseguire codice. NON verificato con una chiamata reale: richiede un run a pagamento.
    """

    def __init__(self, model: str | None = None, max_budget_usd: float = 2.0, timeout: float = 300):
        self.model, self.max_budget_usd, self.timeout = model, max_budget_usd, timeout
        self.usage: list[dict] = []

    def _command(self, system: str, payload: dict, schema: dict) -> list[str]:
        """Riga di comando della CLI. `$schema` e `title` vanno rimossi: il validatore della CLI li rifiuta."""
        clean = {k: v for k, v in schema.items() if k not in ("$schema", "title")}
        return ["claude", "-p", "--no-session-persistence", "--output-format", "json",
                "--json-schema", json.dumps(clean), "--system-prompt", system, "--tools", "",
                "--max-budget-usd", str(self.max_budget_usd)] + \
               (["--model", self.model] if self.model else []) + \
               [json.dumps(payload, ensure_ascii=False)]

    def _run(self, system, payload, schema) -> dict:
        """Esecuzione sincrona della CLI; gli errori risalgono e diventano una `limitation`, non un REJECT."""
        started = time.time()
        result = subprocess.run(self._command(system, payload, schema), capture_output=True,
                                text=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI exit {result.returncode}: {result.stderr[:300]}")
        output = json.loads(result.stdout)
        if output.get("is_error"):
            raise RuntimeError(f"claude CLI error: {output.get('result')}")
        self.usage.append({"cost_usd": output.get("total_cost_usd"), "seconds": round(time.time() - started, 1)})
        return output.get("structured_output") or json.loads(output["result"])

    async def generate(self, *, role, system, payload, schema):
        """Interfaccia JSONBackend: la CLI è sincrona, quindi gira in un thread separato."""
        return await asyncio.to_thread(self._run, system, payload, schema)


# =============================================================================== uso da orchestratore
async def review_attempt(workdir: Path, backend, rules_path: Path = RULES_DEFAULT,
                         statement: str | None = None, timeout: float = 120) -> dict:
    """Punto d'ingresso per l'orchestratore: cartella di lavoro -> rapporto JSON pronto da salvare.

    `TrustedContext()` è vuoto di proposito: non abbiamo eseguito verifiche indipendenti, e un log
    prodotto dal candidato non va mai presentato come un'osservazione fidata.
    """
    job = build_review_input(Path(workdir), rules_path, statement)
    envelope = await review_evidence(job, backend, TrustedContext(), timeout)
    return to_referee_report(envelope, job)


# =============================================================================== CLI
def cmd_run(args) -> int:
    """Esegue la revisione delle evidenze e scrive il rapporto (su file con --out, altrimenti su stdout)."""
    backend = MockBackend(json.loads(Path(args.mock_response).read_text(encoding="utf-8"))) \
        if args.backend == "mock" else ClaudeCliBackend(args.model, timeout=args.timeout)
    report = asyncio.run(review_attempt(Path(args.workdir), backend, Path(args.rules), args.cell_statement,
                                        timeout=args.timeout))
    text = json.dumps(report, indent=1, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"[referee_b] {report['verdict']} -> {args.out}", file=sys.stderr)
    else:
        print(text, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Definisce il sottocomando `run`; tenuto separato da main per leggibilità."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--workdir", required=True, help="cartella runs/<problem_id> con attempt.json")
    run.add_argument("--backend", choices=["mock", "cli"], default="cli")
    run.add_argument("--mock-response", help="file JSON con la risposta simulata (solo --backend mock)")
    run.add_argument("--rules", default=str(RULES_DEFAULT), help="regole della gara (JSON conforme a Rules)")
    run.add_argument("--cell-statement", help="enunciato esatto della cella, se problem.md non lo contiene")
    run.add_argument("--model", help="modello per il backend cli")
    run.add_argument("--timeout", type=float, default=120)
    run.add_argument("--out", help="file di destinazione del rapporto")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.backend == "mock" and not args.mock_response:
        print("--backend mock richiede --mock-response", file=sys.stderr)
        return 2
    return cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
