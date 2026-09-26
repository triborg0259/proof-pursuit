"""Contract/merge/integration tests with simulated model and checker outputs.

These tests do not establish real mathematical soundness or prompt robustness.
"""
import asyncio
import json
import unittest
from pathlib import Path
from pydantic import ValidationError
from referees.contracts import (
    AgentEnvelope, Claim, EvidenceReport, Issue, MathReport, Provenance, ReviewInput,
)
from referees.merge import merge_reports
from referees.runner import review
from referees.trust import (
    CounterexampleRecord, HistoryEntry, OpenStatusRecord,
    TrustedContext, VerifiedRecord, submission_digest,
)


def job():
    return ReviewInput.model_validate_json(
        (Path(__file__).resolve().parents[1] / "examples/input.json").read_text())


def math_pass(ids=("main",)):
    return AgentEnvelope[MathReport](report=MathReport(
        mathematical_verdict="PASS", first_fatal_error=None,
        accepted_mathematical_claims=list(ids), unproved_claims=[],
        missing_cases=[], math_notes="Simulated reviewer for tests"), limitation=None)


def evidence_pass(ids=("main",)):
    return AgentEnvelope[EvidenceReport](report=EvidenceReport(
        evidence_verdict="PASS", source_issues=[], computation_issues=[], rule_violations=[],
        claim_provenance=[Provenance(
            claim_id=cid, categories=["PROVED_BY_US"], evidence_sufficient=True,
            permitted_by_rules=True, relies_on_external_result=False,
            uses_computation_as_proof=False, references=[], notes="Simulated test assessment") for cid in ids],
        reproducibility_notes="Simulated reviewer for tests"), limitation=None)


def certificate(j, ids=("main",), kind="LEAN"):
    # TEST DOUBLE ONLY: a real orchestrator must run a real independent checker.
    return TrustedContext(records=tuple(VerifiedRecord(
        submission_digest(j), cid, kind, "TEST-ONLY: synthetic checker evidence") for cid in ids))


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.j, self.a, self.b = job(), math_pass(), evidence_pass()

    def test_two_passes_do_not_certify(self):
        r = merge_reports(self.j, self.a, self.b)
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")
        self.assertEqual(r.accepted_progress, [])

    def test_checked_pass_accepts_but_does_not_advance_state(self):
        before = self.j.model_dump_json()
        r = merge_reports(self.j, self.a, self.b, certificate(self.j))
        self.assertEqual(r.final_verdict, "ACCEPT")
        self.assertEqual(r.highest_verified_cell, 0)
        self.assertEqual(self.j.model_dump_json(), before)

    def test_stale_certificate_cannot_be_reused(self):
        trusted = certificate(self.j)
        self.j.candidate.proof += " A new unverified sentence."
        self.assertEqual(merge_reports(self.j, self.a, self.b, trusted).final_verdict, "UNKNOWN_STATUS")

    def test_math_fail_has_precedence_over_certificates(self):
        self.a.report.mathematical_verdict = "FAIL"
        self.a.report.first_fatal_error = Issue(code="INVALID_INFERENCE", detail="Step 2 divides by zero",
                                               severity="FATAL", claim_ids=["main"])
        r = merge_reports(self.j, self.a, self.b, certificate(self.j))
        self.assertEqual(r.final_verdict, "REJECT")
        self.assertIn("Referee A", r.blocking_issue)
        self.assertEqual(r.accepted_progress, [])

    def test_evidence_fail_has_precedence(self):
        self.b.report.evidence_verdict = "FAIL"
        self.b.report.rule_violations = [Issue(code="FORBIDDEN_SOURCE", detail="Forbidden essential source",
                                               severity="FATAL", claim_ids=["main"])]
        r = merge_reports(self.j, self.a, self.b, certificate(self.j))
        self.assertEqual(r.final_verdict, "REJECT")
        self.assertIn("Referee B", r.blocking_issue)

    def test_pass_and_missing_evidence_not_accept(self):
        self.b.report.evidence_verdict = "PARTIAL"
        self.b.report.computation_issues = [Issue(code="NOT_EXECUTED", detail="No authentic execution",
                                                  severity="MISSING", claim_ids=["main"])]
        r = merge_reports(self.j, self.a, self.b, certificate(self.j))
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")

    def test_human_review_does_not_satisfy_machine_policy(self):
        r = merge_reports(self.j, self.a, self.b, certificate(self.j, kind="HUMAN_REVIEW"))
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")

    def test_explicit_human_review_policy(self):
        self.j.rules.require_machine_verification = False
        r = merge_reports(self.j, self.a, self.b, certificate(self.j, kind="HUMAN_REVIEW"))
        self.assertEqual(r.final_verdict, "ACCEPT")

    def test_unverified_dependency_blocks_target(self):
        self.j.candidate.claims.append(Claim(id="lemma", statement="An intermediate lemma"))
        self.j.candidate.claims[0].depends_on = ["lemma"]
        r = merge_reports(self.j, math_pass(("main", "lemma")), evidence_pass(("main", "lemma")), certificate(self.j))
        self.assertNotEqual(r.final_verdict, "ACCEPT")

    def test_circular_dependencies_do_not_certify(self):
        self.j.candidate.claims.append(Claim(id="lemma", statement="Lemma", depends_on=["main"]))
        self.j.candidate.claims[0].depends_on = ["lemma"]
        ids = ("main", "lemma")
        r = merge_reports(self.j, math_pass(ids), evidence_pass(ids), certificate(self.j, ids))
        self.assertEqual(r.accepted_progress, [])

    def test_partial_retains_only_checked_lemma(self):
        self.j.candidate.claims.append(Claim(id="lemma", statement="Reusable lemma"))
        self.a.report.mathematical_verdict = "PARTIAL"
        self.a.report.accepted_mathematical_claims = ["lemma"]
        self.a.report.unproved_claims = ["main"]
        r = merge_reports(self.j, self.a, evidence_pass(("main", "lemma")), certificate(self.j, ("lemma",)))
        self.assertEqual(r.final_verdict, "PARTIAL_PROGRESS")
        self.assertEqual([c.id for c in r.accepted_progress], ["lemma"])

    def test_fatal_rejection_can_retain_independent_checked_lemma(self):
        self.j.candidate.claims.append(Claim(id="lemma", statement="Independent lemma"))
        self.a.report.mathematical_verdict = "FAIL"
        self.a.report.accepted_mathematical_claims = ["lemma"]
        self.a.report.first_fatal_error = Issue(code="GAP", detail="Target gap", severity="FATAL", claim_ids=["main"])
        r = merge_reports(self.j, self.a, evidence_pass(("main", "lemma")), certificate(self.j, ("lemma",)))
        self.assertEqual(r.final_verdict, "REJECT")
        self.assertEqual([c.id for c in r.accepted_progress], ["lemma"])

    def test_invented_claim_id_never_accepted(self):
        self.a.report.accepted_mathematical_claims = ["invented"]
        self.assertEqual(merge_reports(self.j, self.a, self.b).final_verdict, "UNKNOWN_STATUS")

    def test_provenance_missing_for_target_invalidates_pass(self):
        self.b.report.claim_provenance = []
        self.assertEqual(merge_reports(self.j, self.a, self.b, certificate(self.j)).final_verdict, "UNKNOWN_STATUS")

    def test_numerical_examples_cannot_certify(self):
        self.b.report.evidence_verdict = "PARTIAL"
        self.b.report.claim_provenance[0].categories = ["EXPERIMENTAL_ONLY"]
        self.b.report.claim_provenance[0].evidence_sufficient = False
        self.assertEqual(merge_reports(self.j, self.a, self.b, certificate(self.j)).accepted_progress, [])

    def test_known_result_independently_proved_is_not_forbidden_citation(self):
        self.b.report.claim_provenance[0].categories = ["KNOWN_IN_LITERATURE", "PROVED_BY_US"]
        self.assertEqual(merge_reports(self.j, self.a, self.b, certificate(self.j)).final_verdict, "ACCEPT")

    def test_forbidden_external_dependency_blocked_even_if_b_misses_rule(self):
        self.b.report.claim_provenance[0].relies_on_external_result = True
        self.assertNotEqual(merge_reports(self.j, self.a, self.b, certificate(self.j)).final_verdict, "ACCEPT")

    def test_missing_reviewer_does_not_mean_false(self):
        absent = AgentEnvelope[MathReport](report=None, limitation="Timeout")
        self.assertEqual(merge_reports(self.j, absent, self.b).final_verdict, "UNKNOWN_STATUS")

    def test_verified_counterexample_identifies_scope(self):
        trusted = TrustedContext(counterexamples=(CounterexampleRecord(
            submission_digest(self.j), "main", "TEST-ONLY counterexample"),))
        r = merge_reports(self.j, self.a, self.b, trusted)
        self.assertEqual(r.final_verdict, "COUNTEREXAMPLE_FOUND")
        self.assertIn("main", r.blocking_issue)

    def test_stale_counterexample_ignored(self):
        trusted = TrustedContext(counterexamples=(CounterexampleRecord("stale", "main", "test"),))
        self.assertNotEqual(merge_reports(self.j, self.a, self.b, trusted).final_verdict, "COUNTEREXAMPLE_FOUND")

    def test_conflicting_certificates_block_progress(self):
        checked = certificate(self.j)
        trusted = TrustedContext(records=checked.records, counterexamples=(CounterexampleRecord(
            submission_digest(self.j), "main", "TEST counterexample"),))
        r = merge_reports(self.j, self.a, self.b, trusted)
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")
        self.assertEqual(r.accepted_progress, [])

    def test_known_open_requires_separate_trusted_record(self):
        absent = AgentEnvelope[MathReport](report=None, limitation="Cannot assess")
        self.assertEqual(merge_reports(self.j, absent, self.b).final_verdict, "UNKNOWN_STATUS")
        trusted = TrustedContext(open_status=OpenStatusRecord(
            submission_digest(self.j), "main", "TEST-ONLY exact-question source", "2026-09-26"))
        self.assertEqual(merge_reports(self.j, absent, self.b, trusted).final_verdict, "KNOWN_OPEN")

    def test_stagnation_needs_three_distinct_attempts_in_same_cell(self):
        self.assertFalse(merge_reports(self.j, self.a, self.b).stagnation_signal)
        history = tuple(HistoryEntry(self.j.problem_id, self.j.cell.id, f"old_{i}", "method", "gap", ()) for i in range(2))
        self.assertTrue(merge_reports(self.j, self.a, self.b, TrustedContext(history=history)).stagnation_signal)
        duplicates = (history[0], history[0])
        self.assertFalse(merge_reports(self.j, self.a, self.b, TrustedContext(history=duplicates)).stagnation_signal)

    def test_unknown_input_keys_rejected(self):
        data = self.j.model_dump()
        data["trusted_records"] = [{"verified": True}]
        with self.assertRaises(ValidationError):
            ReviewInput.model_validate(data)

    def test_inconsistent_pass_schema_rejected(self):
        data = self.a.model_dump()
        data["report"]["unproved_claims"] = ["main"]
        with self.assertRaises(ValidationError):
            AgentEnvelope[MathReport].model_validate(data)

    def test_exact_target_cannot_be_replaced(self):
        data = self.j.model_dump()
        data["candidate"]["claims"][0]["statement"] = "True"
        with self.assertRaises(ValidationError):
            ReviewInput.model_validate(data)


class RunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_independent_payloads_and_parallel_execution(self):
        class Backend:
            def __init__(self):
                self.seen = {}
                self.both_started = asyncio.Event()

            async def generate(self, *, role, system, payload, schema):
                self.seen[role] = payload
                if len(self.seen) == 2:
                    self.both_started.set()
                await asyncio.wait_for(self.both_started.wait(), 0.5)
                return (math_pass() if role == "A" else evidence_pass()).model_dump()

        backend = Backend()
        j = job()
        result = await review(j, backend)
        self.assertEqual(result.final_verdict, "UNKNOWN_STATUS")
        self.assertEqual(set(backend.seen), {"A", "B"})
        self.assertNotIn("rules", backend.seen["A"]["submission"])
        self.assertIn("rules", backend.seen["B"]["submission"])
        backend.seen["A"]["submission"]["candidate"]["proof"] = "mutated"
        self.assertNotEqual(backend.seen["B"]["submission"]["candidate"]["proof"], "mutated")
        self.assertNotEqual(j.candidate.proof, "mutated")

    async def test_invalid_json_fail_closed(self):
        class Backend:
            async def generate(self, **kwargs):
                return {"final_verdict": "ACCEPT", "highest_verified_cell": 999}
        r = await review(job(), Backend())
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")
        self.assertEqual(r.highest_verified_cell, 0)

    async def test_timeout_is_not_math_fail(self):
        class Backend:
            async def generate(self, **kwargs):
                await asyncio.sleep(0.1)
        r = await review(job(), Backend(), timeout=0.001)
        self.assertEqual(r.final_verdict, "UNKNOWN_STATUS")
        self.assertIn("TimeoutError", r.blocking_issue)


if __name__ == "__main__":
    unittest.main()
