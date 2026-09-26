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


def _estratto_interno(riferimento, massimo=2500):
    """Se la fonte è un file del repo (es. problema-2/submission/parte-1.md) ne allega l'inizio: il giudice B non
    vede il repo e altrimenti segnala la fonte come non ispezionata."""
    m = re.search(r"[\w./-]+\.(?:md|py|txt)", riferimento or "")
    percorso = ROOT / m.group(0) if m else None
    return percorso.read_text(encoding="utf-8")[:massimo] if percorso and percorso.is_file() else ""


def _fonti(attempt):
    """Le fonti citate dal tentativo, legate al claim principale; quelle interne con estratto."""
    return [{"id": f"src_{i + 1}", "reference": rif, "claim_ids": ["main"], "submitted_excerpt": _estratto_interno(rif)}
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

    def __init__(self, model_a=None, model_b=None, timeout=300, log_dir=None):
        self.models = {"A": model_a, "B": model_b or model_a}
        self.timeout = timeout
        self.usage = []
        self.log_dir = Path(log_dir) if log_dir else None   # dove salvare gli output grezzi dei giudici

    def _salva_grezzo(self, role, tentativo, raw):
        """Conserva la risposta grezza del giudice: senza questo un ValidationError è indiagnosticabile.
        Al primo salvataggio di un run i grezzi del run precedente per quel giudice vengono tolti, così la cartella
        descrive sempre l'ultimo run (e il replay non pesca rapporti vecchi)."""
        if not self.log_dir:
            return
        if tentativo == 1:
            for vecchio in self.log_dir.glob(f"referee_raw_{role}_*.json"):
                vecchio.unlink()
        write_json(self.log_dir / f"referee_raw_{role}_{tentativo}.json", raw)

    @staticmethod
    def _normalizza(role, raw):
        """Rapporto E limitazione insieme: il contratto del Referee li vuole alternativi (limitazione = "non ho
        potuto giudicare"). Qui il giudice HA giudicato e aggiunge una riserva: il verdetto vale, la riserva
        finisce nelle note del rapporto. Senza questo passo un PASS motivato veniva buttato via."""
        if not isinstance(raw, dict) or raw.get("report") is None or raw.get("limitation") is None:
            return raw
        campo = "math_notes" if role == "A" else "reproducibility_notes"
        report = dict(raw["report"])
        report[campo] = f"{report.get(campo, '')}\n[limitation declared by the judge] {raw['limitation']}".strip()
        return {"report": report, "limitation": None}

    @staticmethod
    def _solo_claim_candidato(raw, payload):
        """Il prompt del giudice B gli chiede di classificare anche le dipendenze, ma il validatore del merge ammette in
        claim_provenance solo i claim del candidato: le voci sui claim già verificati (verified_i) vengono tolte. Si
        rimuove soltanto, mai si aggiunge: il verdetto resta quello del giudice."""
        report = (raw or {}).get("report") if isinstance(raw, dict) else None
        if not report or "claim_provenance" not in report:
            return raw
        candidati = {c["id"] for c in payload.get("submission", {}).get("candidate", {}).get("claims", [])}
        report = dict(report)
        report["claim_provenance"] = [v for v in report["claim_provenance"] if v.get("claim_id") in candidati]
        return {**raw, "report": report}

    @staticmethod
    def _valida(role, raw):
        """Applica le stesse regole pydantic del Referee (coerenza PASS/FAIL/PARTIAL). Ritorna il testo dell'errore o ''."""
        from referees.contracts import AgentEnvelope, MathReport, EvidenceReport
        envelope = AgentEnvelope[MathReport if role == "A" else EvidenceReport]
        try:
            envelope.model_validate(raw)
            return ""
        except Exception as err:
            return str(err)[:2000]

    def _comando(self, role, system, schema):
        cmd = ["claude", "-p", "--tools", "", "--no-session-persistence", "--output-format", "json",   # --tools è variadico:
               "--json-schema", json.dumps(schema), "--system-prompt", system]                        # mai ultimo prima del prompt
        cmd += ["--max-budget-usd", "8"]
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
        self.usage.append({"role": role, "cost_usd": out.get("total_cost_usd"), "model": list((out.get("modelUsage") or {}).keys()),
                           "usage": out.get("usage")})   # token (output = risposta + ragionamento)
        return out.get("structured_output") or json.loads(out["result"])

    async def generate(self, *, role, system, payload, schema):
        """Prima chiamata; se il rapporto viola le regole di coerenza del Referee, un solo ritentativo con l'errore
        esatto nel payload (il modello di solito corregge il campo incriminato). Poi si lascia decidere al Referee."""
        raw = self._normalizza(role, await asyncio.to_thread(self._chiama, role, system, payload, schema))
        raw = self._solo_claim_candidato(raw, payload)
        self._salva_grezzo(role, 1, raw)
        errore = self._valida(role, raw)
        if not errore:
            return raw
        print(f"[referee-cli] {role}: rapporto non valido, ritento una volta: {errore[:200]}", file=sys.stderr)
        payload_bis = {**payload, "previous_report_rejected_by_validator": raw, "validation_error": errore,
                       "instruction": "Return a report that satisfies the validator; keep your mathematical judgement."}
        raw = self._normalizza(role, await asyncio.to_thread(self._chiama, role, system, payload_bis, schema))
        raw = self._solo_claim_candidato(raw, payload)
        self._salva_grezzo(role, 2, raw)
        return raw

    async def close(self):
        return None


class ReplayBackend:
    """Restituisce l'ultimo rapporto grezzo salvato per ogni giudice (referee_raw_<ruolo>_<n>.json), applicando le stesse
    normalizzazioni del backend CLI. Perché: dopo una correzione del ponte si vuole ri-fondere i giudizi già pagati,
    non richiamare i modelli."""

    def __init__(self, log_dir):
        self.log_dir = Path(log_dir)
        self.usage = []

    def _ultimo_grezzo(self, role):
        """Il file più recente per data di modifica: un run può salvare solo _1 mentre resta un _2 del run prima."""
        file = sorted(self.log_dir.glob(f"referee_raw_{role}_*.json"), key=lambda f: f.stat().st_mtime)
        if not file:
            raise FileNotFoundError(f"nessun rapporto grezzo salvato per il giudice {role} in {self.log_dir}")
        return read_json(file[-1])

    async def generate(self, *, role, system, payload, schema):
        raw = CliBackend._normalizza(role, self._ultimo_grezzo(role))
        return CliBackend._solo_claim_candidato(raw, payload)

    async def close(self):
        return None


# =============================================================================== riesecuzione fidata del codice
def _cartella_verifica(workdir: Path, attempt):
    """Cartella pulita per rilanciare gli script: copia della sandbox del Researcher (gli script si importano
    a vicenda con i loro nomi veri) più un file code_i.py per ogni voce di code_used."""
    import shutil
    dest = workdir / "verifica" / attempt["attempt_id"]
    if dest.exists():
        shutil.rmtree(dest)
    sandbox = workdir / "sandbox"
    if sandbox.exists():
        shutil.copytree(sandbox, dest, ignore=shutil.ignore_patterns("__pycache__"))
    dest.mkdir(parents=True, exist_ok=True)
    for i, codice in enumerate(attempt.get("code_used", []), start=1):
        (dest / f"code_{i}.py").write_text(codice.get("code", ""), encoding="utf-8")
    return dest


def _osserva_script(cartella: Path, nome, timeout):
    """Esegue uno script e riassume l'esito in una riga: è ciò che il giudice B legge come osservazione fidata."""
    import time
    inizio = time.time()
    try:
        res = subprocess.run([sys.executable, nome], cwd=cartella, capture_output=True, text=True, timeout=timeout)
        esito = f"exit {res.returncode} in {time.time() - inizio:.1f}s"
        dettagli = f"stdout: {res.stdout.strip()[-700:]!r}; stderr: {res.stderr.strip()[-300:]!r}"
    except subprocess.TimeoutExpired:
        esito, dettagli = f"TIMEOUT after {timeout}s", "killed: exceeds the verification time limit"
    return f"orchestrator re-ran {nome} (python3, clean copy of the researcher sandbox): {esito}; {dettagli}"


def esegui_codice(workdir: Path, attempt, timeout=600):
    """Rilancia ogni script Python di code_used e ritorna le osservazioni. Perché: per il Referee i risultati
    riportati dal candidato non fanno fede; contano solo esecuzioni fatte dall'orchestratore (< 10 min ciascuna)."""
    cartella = _cartella_verifica(workdir, attempt)
    osservazioni = []
    for i, codice in enumerate(attempt.get("code_used", []), start=1):
        if codice.get("language", "").lower() != "python":
            osservazioni.append(f"code_{i}: not re-run (language {codice.get('language')!r} not supported by the orchestrator)")
            continue
        osservazioni.append(_osserva_script(cartella, f"code_{i}.py", timeout))
        print(f"[bridge] {osservazioni[-1][:160]}", file=sys.stderr)
    write_json(cartella / "osservazioni.json", osservazioni)
    return osservazioni


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


async def _esegui_review(job_dict, backend, timeout, osservazioni=()):
    """Chiama il Referee del collega e restituisce il pacchetto come dizionario. Le osservazioni (nostre esecuzioni
    del codice) entrano nel TrustedContext: solo l'orchestratore può fornirle, mai il Researcher."""
    from referees.contracts import ReviewInput
    from referees.hackathon import prepare_review
    from referees.trust import TrustedContext
    fidato = TrustedContext(evidence_observations=tuple(osservazioni))
    packet = await prepare_review(ReviewInput.model_validate(job_dict), backend, [], timeout=timeout, trusted=fidato)
    return json.loads(packet.model_dump_json())


def _scegli_backend(args):
    """offline → nessun modello; api → ClaudeBackend del collega (serve chiave); altrimenti la CLI."""
    if args.offline:
        return None
    if args.replay:
        return ReplayBackend(Path(args.workdir) / "attempts")
    if args.backend == "api":
        from referees.provider import ClaudeBackend
        return ClaudeBackend(args.model or "claude-opus-5", args.model_b)
    return CliBackend(args.model, args.model_b, timeout=args.timeout, log_dir=Path(args.workdir) / "attempts")


def cmd_review(args):
    workdir = Path(args.workdir)
    attempt = _ultimo_tentativo(workdir, args.attempt)
    if attempt is None:
        print("nessun tentativo da giudicare", file=sys.stderr)
        return 2
    job = costruisci_review_input(workdir, attempt)
    backend = _scegli_backend(args)
    osservazioni = esegui_codice(workdir, attempt) if args.run_code else []
    packet = asyncio.run(_esegui_review(job, backend, args.timeout, osservazioni))
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
    rv.add_argument("--replay", action="store_true",
                    help="ri-fonde gli ultimi rapporti grezzi salvati dei due giudici, senza chiamare i modelli")
    rv.add_argument("--run-code", action="store_true",
                    help="rilancia gli script di code_used e passa gli esiti al Referee come osservazioni fidate")
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
