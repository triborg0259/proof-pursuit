"""Test software di Referee A con backend simulati.

ATTENZIONE SULL'AMBITO: questi test verificano il SOFTWARE (ruolo, isolamento
dell'input, schema di uscita, gestione degli errori, compatibilita' con chi
consuma review_math). Un backend simulato restituisce risposte decise da noi:
NON dimostra nulla sulla capacita' matematica del modello reale.
La valutazione matematica vive in tests/test_a_eval_offline.py (casi e attese)
e nello strumento live tools/eval_referee_a.py.

Esecuzione: python -m unittest tests.test_a_contract -v
"""
import asyncio
import copy
import json
import unittest
from pathlib import Path

from pydantic import ValidationError

from referees.contracts import AgentEnvelope, MathReport, ReviewInput
from referees.hackathon import prepare_review
from referees.referee_a import review_math
from referees.trust import TrustedContext

ROOT = Path(__file__).resolve().parents[1]


def job():
    """Job di riferimento: la disuguaglianza x^2+1 >= 2x usata dagli esempi."""
    return ReviewInput.model_validate_json((ROOT / "examples/input.json").read_text())


def math_report(verdict="PASS", **overrides):
    """Costruisce il dizionario di un MathReport valido, con campi sovrascrivibili."""
    report = {"mathematical_verdict": verdict, "first_fatal_error": None,
              "accepted_mathematical_claims": ["main"], "unproved_claims": [],
              "missing_cases": [], "math_notes": "Backend simulato: nessun giudizio reale"}
    report.update(overrides)
    return {"report": report, "limitation": None}


class RecordingBackend:
    """Backend che registra cosa gli viene passato e restituisce una risposta fissa."""

    def __init__(self, response=None):
        self.response = response if response is not None else math_report()
        self.calls = []

    async def generate(self, *, role, system, payload, schema):
        self.calls.append({"role": role, "system": system,
                           "payload": copy.deepcopy(payload), "schema": schema})
        return self.response


class FailingBackend:
    """Backend che solleva l'eccezione richiesta, per simulare un guasto operativo."""

    def __init__(self, exc):
        self.exc = exc

    async def generate(self, **kwargs):
        raise self.exc


async def run_a(backend, trusted=None, timeout=5, target=None):
    """Invoca review_math sul job indicato con il backend fornito."""
    return await review_math(target or job(), backend, trusted or TrustedContext(), timeout)


class RoleAndPayloadTests(unittest.IsolatedAsyncioTestCase):
    """A deve ricevere il proprio ruolo, il proprio prompt e nulla che non gli spetti."""

    async def test_uses_role_a_and_the_a_prompt(self):
        backend = RecordingBackend()
        await run_a(backend)
        call = backend.calls[0]
        self.assertEqual(call["role"], "A")
        self.assertIn("Referee A", call["system"])
        # Il prompt inviato deve essere esattamente il file di A, non quello di B.
        expected = (ROOT / "referees/prompts/a.md").read_text()
        self.assertEqual(call["system"], expected)

    async def test_requests_the_math_envelope_schema(self):
        backend = RecordingBackend()
        await run_a(backend)
        schema = backend.calls[0]["schema"]
        self.assertEqual(set(schema["properties"]), {"report", "limitation"})
        # Lo schema deve descrivere MathReport, non EvidenceReport.
        self.assertIn("MathReport", json.dumps(schema))
        self.assertNotIn("EvidenceReport", json.dumps(schema))

    async def test_contest_rules_are_withheld_from_a(self):
        # Le regole di gara competono a B: A giudica solo la matematica.
        backend = RecordingBackend()
        await run_a(backend)
        self.assertNotIn("rules", backend.calls[0]["payload"]["submission"])

    async def test_payload_carries_nothing_beyond_submission_and_observations(self):
        # Nessun rapporto di B, nessuno storico di conversazione, nessun verdetto altrui.
        backend = RecordingBackend()
        await run_a(backend)
        payload = backend.calls[0]["payload"]
        self.assertEqual(set(payload), {"submission", "trusted_observations"})
        serialized = json.dumps(payload).lower()
        for forbidden in ("evidence_verdict", "evidence_report", "final_verdict",
                          "review_status", "claim_provenance"):
            self.assertNotIn(forbidden, serialized)

    async def test_trusted_observations_are_forwarded(self):
        # Le osservazioni dei checker arrivano dall'orchestratore, non dal candidato.
        trusted = TrustedContext(evidence_observations=("checker: 3 casi su 3 coincidono",))
        backend = RecordingBackend()
        await run_a(backend, trusted=trusted)
        self.assertEqual(backend.calls[0]["payload"]["trusted_observations"],
                         ["checker: 3 casi su 3 coincidono"])


class InputIntegrityTests(unittest.IsolatedAsyncioTestCase):
    """L'input non deve essere modificato da A, ne' direttamente ne' per riferimento."""

    async def test_job_is_not_mutated(self):
        target = job()
        before = target.model_dump_json()
        await run_a(RecordingBackend(), target=target)
        self.assertEqual(target.model_dump_json(), before)

    async def test_backend_cannot_corrupt_the_job_through_the_payload(self):
        # Il payload e' una copia JSON: toccarlo non deve riflettersi sul job.
        class MutatingBackend(RecordingBackend):
            async def generate(self, *, role, system, payload, schema):
                payload["submission"]["candidate"]["proof"] = "sostituito"
                return await super().generate(role=role, system=system,
                                              payload=payload, schema=schema)

        target = job()
        original_proof = target.candidate.proof
        await run_a(MutatingBackend(), target=target)
        self.assertEqual(target.candidate.proof, original_proof)

    async def test_verified_state_is_not_advanced_by_a(self):
        # A e' consultivo: non tocca highest_verified_cell.
        target = job()
        await run_a(RecordingBackend(), target=target)
        self.assertEqual(target.state.highest_verified_cell, 0)


class OutcomeTests(unittest.IsolatedAsyncioTestCase):
    """Verdetti validi restituiti, guasti operativi trasformati in astensione."""

    async def test_valid_report_is_returned(self):
        out = await run_a(RecordingBackend())
        self.assertIsNone(out.limitation)
        self.assertEqual(out.report.mathematical_verdict, "PASS")
        self.assertEqual(out.report.accepted_mathematical_claims, ["main"])

    async def test_each_allowed_verdict_survives_the_round_trip(self):
        fatal = {"code": "INVALID_INFERENCE", "detail": "Passo 3 divide per zero",
                 "severity": "FATAL", "claim_ids": ["main"]}
        cases = {
            "PASS": math_report("PASS"),
            "PARTIAL": math_report("PARTIAL", unproved_claims=["main"],
                                   accepted_mathematical_claims=["main2"]),
            "FAIL": math_report("FAIL", first_fatal_error=fatal),
        }
        for verdict, response in cases.items():
            with self.subTest(verdict=verdict):
                target = job()
                if verdict == "PARTIAL":
                    # PARTIAL richiede un claim riutilizzabile diverso dal target.
                    target.candidate.claims.append(
                        target.candidate.claims[0].model_copy(update={"id": "main2"}))
                out = await run_a(RecordingBackend(response), target=target)
                self.assertEqual(out.report.mathematical_verdict, verdict)

    async def test_timeout_is_an_abstention_not_a_mathematical_fail(self):
        class SlowBackend:
            async def generate(self, **kwargs):
                await asyncio.sleep(1)

        out = await review_math(job(), SlowBackend(), TrustedContext(), timeout=0.01)
        self.assertIsNone(out.report)
        self.assertIn("TimeoutError", out.limitation)

    async def test_backend_error_is_an_abstention(self):
        out = await run_a(FailingBackend(ConnectionError("rete assente")))
        self.assertIsNone(out.report)
        self.assertIn("ConnectionError", out.limitation)

    async def test_malformed_output_is_an_abstention(self):
        # Un JSON che non rispetta lo schema non significa "prova sbagliata".
        out = await run_a(RecordingBackend({"verdict": "ACCEPT", "highest_verified_cell": 99}))
        self.assertIsNone(out.report)
        self.assertIn("ValidationError", out.limitation)

    async def test_unknown_verdict_is_rejected(self):
        out = await run_a(RecordingBackend(math_report("ACCEPT")))
        self.assertIsNone(out.report)
        self.assertIsNotNone(out.limitation)

    async def test_extra_fields_are_rejected(self):
        # extra="forbid": A non puo' inventare campi fuori contratto.
        out = await run_a(RecordingBackend(math_report(confidence=0.99)))
        self.assertIsNone(out.report)
        self.assertIsNotNone(out.limitation)


class ContractInvariantTests(unittest.TestCase):
    """Invarianti del validatore che il prompt di A deve rispettare per non astenersi."""

    def envelope(self, **overrides):
        return AgentEnvelope[MathReport].model_validate(math_report(**overrides))

    def test_fail_requires_severity_fatal(self):
        # Severita' diversa da FATAL fa fallire la validazione: il rapporto va perso.
        soft = {"code": "MISSING_LEMMA", "detail": "Lemma non dimostrato",
                "severity": "MISSING", "claim_ids": ["main"]}
        with self.assertRaises(ValidationError):
            self.envelope(mathematical_verdict="FAIL", first_fatal_error=soft)

    def test_pass_cannot_carry_open_obligations(self):
        with self.assertRaises(ValidationError):
            self.envelope(mathematical_verdict="PASS", missing_cases=["x = 0"])

    def test_partial_requires_a_reusable_claim(self):
        with self.assertRaises(ValidationError):
            self.envelope(mathematical_verdict="PARTIAL", accepted_mathematical_claims=[])

    def test_claim_cannot_be_accepted_and_unproved(self):
        with self.assertRaises(ValidationError):
            self.envelope(mathematical_verdict="PARTIAL", unproved_claims=["main"])


class ConsumerCompatibilityTests(unittest.IsolatedAsyncioTestCase):
    """Chi consuma review_math deve continuare a funzionare senza modifiche."""

    async def test_prepare_review_embeds_the_a_envelope(self):
        class BothRoles:
            """Risponde ad A con MathReport e a B con un EvidenceReport minimo."""

            async def generate(self, *, role, system, payload, schema):
                if role == "A":
                    return math_report()
                return {"report": {"evidence_verdict": "PARTIAL", "source_issues": [],
                                   "computation_issues": [], "rule_violations": [],
                                   "claim_provenance": [], "reproducibility_notes": "simulato"},
                        "limitation": None}

        packet = await prepare_review(job(), BothRoles(), timeout=5)
        self.assertEqual(packet.math.report.mathematical_verdict, "PASS")
        # Due PASS simulati non bastano a certificare: l'ACCEPT resta umano.
        self.assertNotEqual(packet.report.final_verdict, "ACCEPT")

    async def test_offline_mode_yields_an_explicit_limitation(self):
        packet = await prepare_review(job())
        self.assertIsNone(packet.math.report)
        self.assertIn("Offline", packet.math.limitation)


if __name__ == "__main__":
    unittest.main()
