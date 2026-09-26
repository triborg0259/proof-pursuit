"""Test 2 e Test 3 dallo spec.

Test 2 — anti-ripetizione: fixture toy_fail, tre tentativi "induction" di fila, tutti REJECT con lo
stesso errore fatale (stessa fixture concettuale usata da tests/test_researcher.py nel repo condiviso
per il test di stagnazione). Atteso: nessuna idea riproduce approach_family='induction'.

Test 3 — creatività guidata dal Referee: fixture moment_bound, il Referee ha già segnalato che "il
second-moment bound è insufficiente". Atteso: la lista avoid lo riporta esplicitamente e nessuna idea
ripropone quella stessa approach_family nuda.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from creative import analyze_history, generate_rule_based, load_creative_input  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


class TestRepetitionAvoidance(unittest.TestCase):
    def test_repeated_family_detected(self):
        state = load_creative_input(FIXTURES / "toy_fail")
        analysis = analyze_history(state)
        self.assertEqual(analysis["repeated_family"], "induction")
        self.assertIsNotNone(analysis["repeated_fatal_error"])

    def test_no_bare_induction_idea_proposed(self):
        state = load_creative_input(FIXTURES / "toy_fail")
        output = generate_rule_based(state)

        self.assertTrue(any("induction" in a.lower() for a in output.avoid))
        families = [idea.approach_family for idea in output.ideas]
        self.assertNotIn("induction", families)


class TestRefereeGuidedCreativity(unittest.TestCase):
    def test_avoids_repeating_the_named_weak_bound(self):
        state = load_creative_input(FIXTURES / "moment_bound")
        output = generate_rule_based(state)

        avoid_text = " ".join(output.avoid).lower()
        self.assertIn("second-moment", avoid_text)
        families = [idea.approach_family for idea in output.ideas]
        self.assertNotIn("algebraic_reformulation", families)  # è la famiglia già tentata due volte


if __name__ == "__main__":
    unittest.main()
