#!/usr/bin/env python3
"""
bridge_referee.py — ponte fra il Researcher (nostro) e il Referee (pacchetto `referee/` di gabundos).

I due componenti sono nati con formati diversi: il Researcher scrive `attempt.json` (schema shared/attempt),
il Referee legge un `ReviewInput` (referee/schemas/input.schema.json) e produce un `ReviewPacket`.
Questo file fa solo traduzione e orchestrazione minima; non giudica nulla.

Comandi:
  to-review   --workdir DIR [--attempt FILE] [--out FILE]   attempt.json → review_input.json (input del Referee)
  from-packet --workdir DIR --packet FILE                   ReviewPacket → referee_report.json (+ record)
  review      --workdir DIR [--offline] [--model M]         to-review → Referee → from-packet, in un colpo
                                                            (--offline: solo controlli esatti, nessun modello)

Backend per `review`: la CLI `claude -p` (abbonamento, nessuna chiave API), adattata al protocollo JSONBackend
del Referee. Se esiste ANTHROPIC_API_KEY si può usare il loro ClaudeBackend con --backend api.
Come per il Researcher con shell: un run che lancia `claude -p` va avviato da un terminale umano.
"""
import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "referee"))   # il pacchetto `referees` vive in referee/ senza installazione
sys.path.insert(0, str(HERE))

from researcher import read_json, read_text, write_json, next_attempt_number, target_cell_from_state  # noqa: E402

# Regole della competizione: file condiviso e sostituibile. NON e' il regolamento ufficiale.
REGOLE_FILE = ROOT / "shared" / "competition_rules.example.json"
# Ultima spiaggia se anche il file manca, per non bloccare una revisione.
REGOLE_DEFAULT = {
    "allow_literature_as_proof": False,
    "allow_computation": True,
    "require_machine_verification": False,
    "additional_rules": ("Proof Pursuit: citing a published result for the statement to prove does not count; a proof "
                         "written out in full does. A computation supports a proof only if the code is included, runs "
                         "under 10 minutes on a laptop and is exact/interval or exhaustive over a finite set justified "
                         "by the argument."),
}


# =============================================================================== attempt → ReviewInput
def _ultimo_tentativo(workdir: Path, esplicito):
    """Il tentativo da giudicare: quello indicato, altrimenti l'ultimo salvato dal Researcher."""
    if esplicito:
        return read_json(Path(esplicito))
    numero = next_attempt_number(workdir) - 1
    return read_json(workdir / "attempts" / f"attempt_{numero:03d}.json")


def _claim_verificati(state):
    """I claim già verificati (stringhe in state.json) diventano claim con id stabile `verified_i`."""
    return [{"id": f"verified_{i + 1}", "statement": testo, "depends_on": []}
            for i, testo in enumerate(state.get("verified_claims", []))]


def _dipendenze(attempt, verificati):
    """Traduce `claims_used` in id di claim; ritorna (id delle dipendenze, claim extra da registrare).

    Un claim usato che coincide con uno verificato punta a quello. Uno che NON coincide non è
    verificato: diventa un claim del candidato (`dep_k`) invece di sparire in silenzio, così il
    Referee ne valuta la provenienza e può segnalarlo come UNVERIFIED.
    """
    per_testo = {c["statement"]: c["id"] for c in verificati}
    dipendenze, extra = [], []
    for k, testo in enumerate(attempt.get("claims_used", []), start=1):
        if testo in per_testo:
            dipendenze.append(per_testo[testo])
        else:
            extra.append({"id": f"dep_{k}", "statement": testo, "depends_on": []})
            dipendenze.append(f"dep_{k}")
    return dipendenze, extra


def _enunciato_cella(state, testo_problema, numero):
    """Enunciato esatto del bersaglio protetto, nell'ordine: `cell_statement` in state.json,
    riga `Cell N:` di problem.md, `current_blocker`.

    Senza nessuno dei tre ci si ferma invece di usare un segnaposto: il Referee protegge questo
    testo, e farlo giudicare su un bersaglio inventato produrrebbe un verdetto senza significato.
    """
    dal_problema = re.search(rf"^Cell\s+{numero}\s*:\s*(.+?)(?=\n\s*\n|\n#|\Z)", testo_problema or "",
                             re.MULTILINE | re.DOTALL)
    for fonte in (state.get("cell_statement"),
                  " ".join(dal_problema.group(1).split()) if dal_problema else None,
                  state.get("current_blocker")):
        if fonte and fonte.strip():
            return fonte.strip()
    raise ValueError(f"Enunciato della cella {numero} assente: aggiungi cell_statement a state.json")


def _regole(state):
    """Regole passate al Referee: quelle di state.json se presenti, altrimenti il file condiviso."""
    return state.get("rules") or read_json(REGOLE_FILE) or REGOLE_DEFAULT


def _artefatti(attempt):
    """Ogni voce di code_used diventa un artefatto CODE legato al claim principale."""
    artefatti = []
    for i, codice in enumerate(attempt.get("code_used", [])):
        testo = f"# {codice.get('purpose', '')}\n# rigor: {codice.get('rigor', '?')}\n{codice.get('code', '')}"
        artefatti.append({"id": f"code_{i + 1}", "kind": "CODE", "content": testo, "claim_ids": ["main"]})
    return artefatti


def _fonti(attempt):
    """Le fonti citate dal tentativo, legate al claim principale."""
    return [{"id": f"src_{i + 1}", "reference": rif, "claim_ids": ["main"], "submitted_excerpt": ""}
            for i, rif in enumerate(attempt.get("sources_used", []))]


def costruisci_review_input(workdir: Path, attempt):
    """Assembla il ReviewInput del Referee dal nostro contesto (attempt.json + state.json + problem.md)."""
    state = read_json(workdir / "state.json") or {}
    testo_problema = read_text(workdir / "problem.md")
    numero_cella = target_cell_from_state(state)
    enunciato = _enunciato_cella(state, testo_problema, numero_cella)
    verificati = _claim_verificati(state)
    dipendenze, extra = _dipendenze(attempt, verificati)
    return {
        "problem_id": state.get("problem_id", workdir.name),
        "original_problem": testo_problema or enunciato,
        "cell": {"id": f"cell_{numero_cella}", "number": numero_cella, "target_claim_id": "main", "statement": enunciato},
        "state": {"highest_verified_cell": int(state.get("highest_verified_cell", 0)), "claims": verificati},
        "candidate": {
            "attempt_id": attempt["attempt_id"],
            "proof": attempt["proof_attempt"],
            "method_tag": attempt.get("approach_family", "other"),
            "claims": [{"id": "main", "statement": enunciato, "depends_on": dipendenze}] + extra,
            "sources": _fonti(attempt),
            "artifacts": _artefatti(attempt),
        },
        "rules": _regole(state),
    }


# =============================================================================== ReviewPacket → referee_report
def _errore_fatale(report):
    """Il primo errore fatale segnalato dal giudice matematico; se assente, il blocker per un REJECT."""
    fatale = (report.get("math_review") or {}).get("first_fatal_error")
    if fatale:
        return fatale.get("detail")
    return report.get("blocking_issue") if report.get("final_verdict") == "REJECT" else None


def converti_packet(packet, attempt_id):
    """Traduce il ReviewPacket nel nostro referee_report.schema.json. `review_status` viene conservato perché
    READY_FOR_HUMAN non è un ACCEPT: l'approvazione resta umana (regola del pacchetto Referee)."""
    report = packet["report"]
    evidenze = report.get("evidence_review") or {}
    matematica = report.get("math_review") or {}
    return {
        "attempt_id": attempt_id,
        "verdict": report["final_verdict"],
        "review_status": packet["review_status"],
        "highest_verified_cell": int(report.get("highest_verified_cell", 0)),
        "accepted_claims": list(report.get("accepted_progress", [])),
        "proposed_claim_ids": list(packet.get("proposed_claim_ids", [])),
        "fatal_error": _errore_fatale(report),
        "citation_issue": bool(evidenze.get("source_issues") or evidenze.get("rule_violations")),
        "computation_issue": bool(evidenze.get("computation_issues") or packet.get("check_errors")),
        "next_blocker": report.get("next_required_step", ""),
        "reasoning_summary": (f"review_status={packet['review_status']}; math={matematica.get('verdict')}; "
                              f"evidence={evidenze.get('verdict')}; {report.get('blocking_issue', '')}"),
        "stagnation_signal": bool(report.get("stagnation_signal", False)),
    }


def registra_report(workdir: Path, report):
    """Archivia il verdetto come fa `researcher.py record`: gemello del tentativo + copia corrente + failed_attempts."""
    numero = int(re.search(r"(\d+)", report["attempt_id"]).group(1))
    write_json(workdir / "attempts" / f"referee_{numero:03d}.json", report)
    write_json(workdir / "referee_report.json", report)
    if report["verdict"] in ("REJECT", "COUNTEREXAMPLE_FOUND"):
        from researcher import append_failed_attempt
        append_failed_attempt(workdir, numero, report)


# =============================================================================== backend CLI per il Referee
class CliBackend:
    """Adatta `claude -p --json-schema` al protocollo JSONBackend del Referee (generate(role, system, payload, schema)).
    Ogni richiesta è indipendente, senza strumenti; il modello A e B possono differire."""

    def __init__(self, model_a=None, model_b=None, timeout=300):
        self.models = {"A": model_a, "B": model_b or model_a}
        self.timeout = timeout
        self.usage = []

    def _comando(self, role, system, schema):
        cmd = ["claude", "-p", "--no-session-persistence", "--output-format", "json", "--tools", "",
               "--json-schema", json.dumps(schema), "--system-prompt", system]
        if self.models[role]:
            cmd += ["--model", self.models[role]]
        return cmd

    def _chiama(self, role, system, payload, schema):
        """Chiamata sincrona: eseguita in un thread da `generate` così i due giudici girano in parallelo."""
        res = subprocess.run(self._comando(role, system, schema) + [json.dumps(payload, ensure_ascii=False)],
                             capture_output=True, text=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
        if res.returncode != 0:
            raise ValueError(f"claude CLI exit {res.returncode}: {res.stderr[:300]}")
        out = json.loads(res.stdout)
        if out.get("is_error"):
            raise ValueError(f"claude CLI error: {out.get('result')}")
        self.usage.append({"role": role, "cost_usd": out.get("total_cost_usd"), "model": list((out.get("modelUsage") or {}).keys())})
        return out.get("structured_output") or json.loads(out["result"])

    async def generate(self, *, role, system, payload, schema):
        return await asyncio.to_thread(self._chiama, role, system, payload, schema)

    async def close(self):
        return None


# =============================================================================== comandi
def cmd_to_review(args):
    workdir = Path(args.workdir)
    attempt = _ultimo_tentativo(workdir, args.attempt)
    if attempt is None:
        print("nessun tentativo da giudicare", file=sys.stderr)
        return 2
    job = costruisci_review_input(workdir, attempt)
    from referees.contracts import ReviewInput
    ReviewInput.model_validate(job)  # fallisce subito se il formato non è quello atteso dal Referee
    out = Path(args.out) if args.out else workdir / "review_input.json"
    write_json(out, job)
    print(f"scritto {out} (attempt {attempt['attempt_id']})")
    return 0


def cmd_from_packet(args):
    workdir = Path(args.workdir)
    packet = read_json(Path(args.packet))
    report = converti_packet(packet, packet["job"]["candidate"]["attempt_id"])
    registra_report(workdir, report)
    print(json.dumps({k: report[k] for k in ("attempt_id", "verdict", "review_status", "fatal_error", "next_blocker")},
                     ensure_ascii=False))
    return 0


async def _esegui_review(job_dict, backend, timeout):
    """Chiama il Referee del collega e restituisce il pacchetto come dizionario."""
    from referees.contracts import ReviewInput
    from referees.hackathon import prepare_review
    packet = await prepare_review(ReviewInput.model_validate(job_dict), backend, [], timeout=timeout)
    return json.loads(packet.model_dump_json())


def _scegli_backend(args):
    """offline → nessun modello; api → ClaudeBackend del collega (serve chiave); altrimenti la CLI."""
    if args.offline:
        return None
    if args.backend == "api":
        from referees.provider import ClaudeBackend
        return ClaudeBackend(args.model or "claude-opus-5", args.model_b)
    return CliBackend(args.model, args.model_b, timeout=args.timeout)


def cmd_review(args):
    workdir = Path(args.workdir)
    attempt = _ultimo_tentativo(workdir, args.attempt)
    if attempt is None:
        print("nessun tentativo da giudicare", file=sys.stderr)
        return 2
    job = costruisci_review_input(workdir, attempt)
    backend = _scegli_backend(args)
    packet = asyncio.run(_esegui_review(job, backend, args.timeout))
    write_json(workdir / "attempts" / f"packet_{attempt['attempt_id'].split('_')[1]}.json", packet)
    report = converti_packet(packet, attempt["attempt_id"])
    if backend is not None:
        report["usage"] = getattr(backend, "usage", [])
    registra_report(workdir, report)
    print(json.dumps({k: report.get(k) for k in ("attempt_id", "verdict", "review_status", "fatal_error", "next_blocker", "usage")},
                     ensure_ascii=False))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    tr = sub.add_parser("to-review")
    tr.add_argument("--workdir", required=True)
    tr.add_argument("--attempt")
    tr.add_argument("--out")
    fp = sub.add_parser("from-packet")
    fp.add_argument("--workdir", required=True)
    fp.add_argument("--packet", required=True)
    rv = sub.add_parser("review")
    rv.add_argument("--workdir", required=True)
    rv.add_argument("--attempt")
    rv.add_argument("--offline", action="store_true", help="solo controlli esatti, nessun modello")
    rv.add_argument("--backend", choices=["cli", "api"], default="cli")
    rv.add_argument("--model")
    rv.add_argument("--model-b")
    rv.add_argument("--timeout", type=float, default=300)
    return parser


def main():
    args = build_parser().parse_args()
    return {"to-review": cmd_to_review, "from-packet": cmd_from_packet, "review": cmd_review}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
