"""Test della validazione: errori strutturali vs avvisi di linguaggio da auto-certificazione.
Il Creative Agent non deve MAI poter scrivere che una cella è risolta: questo è il test che lo controlla.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from creative import CreativeIdea, CreativeOutput, generate_rule_based, load_creative_input  # noqa: E402
from creative.validation import validate_output  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def _idea(**overrides):
    base = dict(id="idea_1", risk="SAFE", method="m", why_different="d", why_it_might_work="w",
               first_test="t", expected_gain="g", main_risk="r", approach_family="special_case")
    base.update(overrides)
    return CreativeIdea(**base)


class TestValidateOutputStructural(unittest.TestCase):
    def test_our_own_generator_never_fails_its_own_validation(self):
        state = load_creative_input(FIXTURES / "toy_fail")
        output = generate_rule_based(state)
        errors, warnings = validate_output(output)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_duplicate_ids_is_an_error(self):
        output = CreativeOutput("x", [], [_idea(id="dup"), _idea(id="dup")])
        errors, _ = validate_output(output)
        self.assertTrue(any("duplicato" in e for e in errors))

    def test_bad_risk_value_is_an_error(self):
        output = CreativeOutput("x", [], [_idea(risk="HIGH")])
        errors, _ = validate_output(output)
        self.assertTrue(any("risk" in e for e in errors))

    def test_empty_required_field_is_an_error(self):
        output = CreativeOutput("x", [], [_idea(first_test="")])
        errors, _ = validate_output(output)
        self.assertTrue(any("first_test" in e for e in errors))

    def test_unknown_approach_family_is_an_error(self):
        output = CreativeOutput("x", [], [_idea(approach_family="not_a_real_family")])
        errors, _ = validate_output(output)
        self.assertTrue(any("approach_family" in e for e in errors))


class TestValidateOutputHonesty(unittest.TestCase):
    def test_missing_risk_tier_is_a_warning(self):
        output = CreativeOutput("x", [], [_idea(id="a", risk="SAFE"), _idea(id="b", risk="MEDIUM")])
        _, warnings = validate_output(output)
        self.assertTrue(any("WILD" in w for w in warnings))

    def test_unconditional_solved_claim_is_flagged(self):
        output = CreativeOutput("x", [], [_idea(why_it_might_work="This proves the cell is solved.")])
        _, warnings = validate_output(output)
        self.assertTrue(any("auto-certificazione" in w for w in warnings))

    def test_conditional_phrasing_is_not_flagged(self):
        """Il brief lo richiede esplicitamente: 'if Lemma X can be established, this would reduce Cell N...'
        deve restare ammesso, solo l'affermazione categorica va segnalata."""
        output = CreativeOutput("x", [], [_idea(
            why_it_might_work="If this lemma can be established, this would reduce the cell to a simpler claim.")])
        _, warnings = validate_output(output)
        self.assertFalse(any("auto-certificazione" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
