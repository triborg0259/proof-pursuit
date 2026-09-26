"""Controlli offline sulla batteria di valutazione di Referee A.

AMBITO: qui si verifica che la BATTERIA sia costruita bene (input validi,
attese non visibili al modello, conteggi corretti). Non si verifica, e non si
puo' verificare offline, quanto il modello sia bravo in matematica: quello
richiede l'esecuzione live di tools/eval_referee_a.py.

Esecuzione: python -m unittest tests.test_a_eval_offline -v
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval_referee_a import (  # noqa: E402
    CASES, EvalCase, build_job, classify, injection_leaked, run_case, summarize,
)
from referees.contracts import MathReport, ReviewInput  # noqa: E402


def case_by_id(case_id):
    return next(c for c in CASES if c.case_id == case_id)


def report(verdict="PASS", **overrides):
    """MathReport valido, usato per esercitare la classificazione.

    Per FAIL il contratto pretende un Issue di severita' FATAL: lo aggiunge qui,
    cosi' i test sulla classificazione non devono ripeterlo ogni volta.
    """
    data = {"mathematical_verdict": verdict, "first_fatal_error": None,
            "accepted_mathematical_claims": ["main"], "unproved_claims": [],
            "missing_cases": [], "math_notes": "sintetico"}
    if verdict == "FAIL":
        data["first_fatal_error"] = {"code": "INVALID_INFERENCE",
                                     "detail": "Passo non giustificato",
                                     "severity": "FATAL", "claim_ids": ["main"]}
        data["accepted_mathematical_claims"] = []
    data.update(overrides)
    return MathReport.model_validate(data)


class CaseWellFormednessTests(unittest.TestCase):
    """Ogni caso deve essere un ReviewInput accettato dal contratto stretto."""

    def test_every_case_builds_a_valid_review_input(self):
        for case in CASES:
            with self.subTest(case=case.case_id):
                self.assertIsInstance(build_job(case), ReviewInput)

    def test_target_claim_matches_the_cell_statement(self):
        # Il contratto pretende che il claim protetto sia dichiarato alla lettera.
        for case in CASES:
            with self.subTest(case=case.case_id):
                job = build_job(case)
                target = next(c for c in job.candidate.claims
                              if c.id == job.cell.target_claim_id)
                self.assertEqual(target.statement, job.cell.statement)

    def test_expected_verdict_is_in_the_acceptable_set(self):
        for case in CASES:
            with self.subTest(case=case.case_id):
                self.assertIn(case.expected, case.acceptable)


class LabelLeakageTests(unittest.TestCase):
    """L'esito atteso non deve mai raggiungere il modello, nemmeno di sbieco."""

    def payload_of(self, case):
        return build_job(case).model_dump_json()

    def test_case_identifiers_are_neutral(self):
        # ID come "division_zero" rivelerebbero la risposta: servono ID muti.
        for case in CASES:
            with self.subTest(case=case.case_id):
                self.assertRegex(case.case_id, r"^case_\d{2}$")

    def test_expected_verdict_never_appears_in_the_payload(self):
        # Criterio preciso: l'esito ATTESO del caso non deve comparire.
        # Il caso con iniezione contiene di proposito la parola "FAIL" nel testo
        # della prova: e' l'esca che A deve ignorare, non l'etichetta attesa,
        # che li' vale PASS.
        for case in CASES:
            with self.subTest(case=case.case_id):
                self.assertNotIn(case.expected, self.payload_of(case))

    def test_verdict_words_are_absent_from_the_metadata(self):
        # Nei campi strutturali non ci deve essere alcun verdetto, mai.
        for case in CASES:
            with self.subTest(case=case.case_id):
                job = build_job(case)
                metadata = " ".join([job.problem_id, job.original_problem,
                                     job.candidate.attempt_id,
                                     job.candidate.method_tag, job.cell.id,
                                     job.cell.statement,
                                     job.rules.additional_rules])
                for word in ("PASS", "PARTIAL", "FAIL", "expected", "atteso"):
                    self.assertNotIn(word, metadata)

    def test_internal_annotations_never_appear_in_the_payload(self):
        # probe e rationale sono note nostre: restano nella tabella locale.
        for case in CASES:
            with self.subTest(case=case.case_id):
                payload = self.payload_of(case).lower()
                for fragment in case.probe.lower().split():
                    if len(fragment) > 6:
                        self.assertNotIn(fragment, payload)
                self.assertNotIn(case.rationale.lower()[:30], payload)

    def test_no_case_identifier_hints_at_the_defect(self):
        # Nessuna parola rivelatrice negli identificatori inviati.
        revealing = re.compile(r"zero|circular|inject|wrong|bad|correct|fail|pass",
                               re.IGNORECASE)
        for case in CASES:
            with self.subTest(case=case.case_id):
                job = build_job(case)
                for value in (job.problem_id, job.candidate.attempt_id,
                              job.candidate.method_tag, job.cell.id):
                    self.assertIsNone(revealing.search(value))


class CoverageTests(unittest.TestCase):
    """La batteria deve coprire tutte le categorie richieste dall'incarico."""

    def test_required_defect_families_are_present(self):
        probes = " ".join(c.probe for c in CASES)
        required = ["quadrato non negativo", "caso limite", "divisione",
                    "quantificatori", "esempi numerici", "lemma indispensabile",
                    "circolare", "induzione", "limite superiore",
                    "risultato parziale", "istruzioni ostili"]
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, probes)

    def test_suite_is_balanced_between_correct_and_defective(self):
        # Un referee che rifiuta tutto non deve poter sembrare bravo.
        correct = [c for c in CASES if c.expected == "PASS"]
        self.assertGreaterEqual(len(correct), 2)
        self.assertGreater(len(CASES) - len(correct), len(correct))

    def test_every_case_documents_its_reason(self):
        for case in CASES:
            with self.subTest(case=case.case_id):
                self.assertGreater(len(case.rationale), 30)


class ClassificationTests(unittest.TestCase):
    """La classificazione deve isolare i due errori che contano."""

    def test_accepting_a_wrong_proof_is_flagged(self):
        self.assertEqual(
            classify(case_by_id("case_03"), "PASS", report("PASS")),
            "wrong_proof_accepted")

    def test_rejecting_a_correct_proof_is_flagged(self):
        self.assertEqual(
            classify(case_by_id("case_01"), "FAIL", report("FAIL")),
            "correct_proof_rejected")

    def test_partial_on_a_correct_proof_counts_as_rejection(self):
        # Non dare PASS a una prova corretta e' comunque un errore, non una sfumatura.
        self.assertEqual(
            classify(case_by_id("case_01"), "PARTIAL", report("PARTIAL")),
            "correct_proof_rejected")

    def test_exact_match_is_recognised(self):
        self.assertEqual(
            classify(case_by_id("case_10"), "PARTIAL", report("PARTIAL")),
            "exact")

    def test_defensible_alternative_is_separated_from_exact(self):
        case = EvalCase(case_id="case_99", target="t", proof="p", expected="FAIL",
                        acceptable=("FAIL", "PARTIAL"), probe="x",
                        rationale="motivazione sufficientemente lunga per il test")
        self.assertEqual(classify(case, "PARTIAL", report("PARTIAL")), "defensible")

    def test_abstention_is_not_counted_as_a_verdict(self):
        self.assertEqual(classify(case_by_id("case_01"), None, None), "abstention")


class InjectionDetectionTests(unittest.TestCase):
    """L'iniezione del caso 11 chiede un claim inventato: va rilevato se compare."""

    def test_leak_detected_when_injected_claim_is_listed(self):
        leaked = report("PASS", accepted_mathematical_claims=["main", "bonus_claim"])
        self.assertTrue(injection_leaked(leaked))

    def test_clean_report_is_not_flagged(self):
        self.assertFalse(injection_leaked(report("PASS")))

    def test_absent_report_is_not_flagged(self):
        self.assertFalse(injection_leaked(None))


class SummaryTests(unittest.IsolatedAsyncioTestCase):
    """Il riepilogo deve contare le categorie senza mescolarle."""

    def test_counts_are_separated_by_category(self):
        rows = [{"outcome": "wrong_proof_accepted", "injection_leaked": False},
                {"outcome": "wrong_proof_accepted", "injection_leaked": True},
                {"outcome": "exact", "injection_leaked": False},
                {"outcome": "abstention", "injection_leaked": False}]
        summary = summarize(rows)
        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["wrong_proof_accepted"], 2)
        self.assertEqual(summary["exact"], 1)
        self.assertEqual(summary["abstention"], 1)
        self.assertEqual(summary["injection_leaks"], 1)

    async def test_run_case_reports_an_abstention_on_backend_failure(self):
        class Broken:
            async def generate(self, **kwargs):
                raise RuntimeError("guasto simulato")

        row = await run_case(case_by_id("case_01"), Broken(), timeout=5)
        self.assertEqual(row["actual"], "UNAVAILABLE")
        self.assertEqual(row["outcome"], "abstention")
        self.assertIn("RuntimeError", row["limitation"])

    async def test_run_case_records_the_blocker_for_manual_review(self):
        class Fails:
            async def generate(self, **kwargs):
                return {"report": {"mathematical_verdict": "FAIL",
                                   "first_fatal_error": {
                                       "code": "DOMAIN_ERROR",
                                       "detail": "Divisione per a-b, che vale 0",
                                       "severity": "FATAL", "claim_ids": ["main"]},
                                   "accepted_mathematical_claims": [],
                                   "unproved_claims": [], "missing_cases": [],
                                   "math_notes": "simulato"}, "limitation": None}

        row = await run_case(case_by_id("case_03"), Fails(), timeout=5)
        self.assertEqual(row["outcome"], "exact")
        self.assertEqual(row["first_fatal_error"]["code"], "DOMAIN_ERROR")
        # Il motivo resta leggibile: la qualita' del blocker si giudica a mano.
        self.assertIn("a-b", row["first_fatal_error"]["detail"])


if __name__ == "__main__":
    unittest.main()
