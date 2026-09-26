"""Test 1 dallo spec: generazione di base.

Input: una cartella di lavoro con solo state.json, nessun tentativo ancora fatto (fixture toy_x2,
identica a quella usata da tests/test_researcher.py nel repo condiviso, per interoperabilità diretta).
Atteso: l'output è valido, ha >= 3 idee, e sono presenti SAFE/MEDIUM/WILD.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from creative import generate_rule_based, load_creative_input  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


class TestBasicGeneration(unittest.TestCase):
    def test_basic_generation_has_safe_medium_wild(self):
        state = load_creative_input(FIXTURES / "toy_x2")
        output = generate_rule_based(state)

        self.assertEqual(len(output.ideas), 3)
        risks = {idea.risk for idea in output.ideas}
        self.assertEqual(risks, {"SAFE", "MEDIUM", "WILD"})
        for idea in output.ideas:
            self.assertTrue(idea.first_test, f"idea {idea.id} senza first_test")
            self.assertTrue(idea.approach_family, f"idea {idea.id} senza approach_family")
        self.assertTrue(output.blocker_analysis)

    def test_output_round_trips_through_json(self):
        state = load_creative_input(FIXTURES / "toy_x2")
        output = generate_rule_based(state)

        # Deve essere serializzabile in JSON puro: è il contratto che legge il Researcher
        # (shared/schemas/creative_ideas.schema.json → creative_ideas.json).
        dumped = json.dumps(output.to_dict())
        reloaded = json.loads(dumped)
        self.assertIn("ideas", reloaded)
        self.assertIn("blocker_analysis", reloaded)
        self.assertIn("avoid", reloaded)
        self.assertEqual(len(reloaded["ideas"]), 3)


if __name__ == "__main__":
    unittest.main()
