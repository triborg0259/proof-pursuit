"""Test dell'attivazione automatica: quando should_activate dice sì/no, e la prevenzione dei loop
(tetto di attivazioni per cella, nessuna riattivazione su stato invariato). Stati costruiti direttamente
come oggetti Python (non da fixture su disco): should_activate è una funzione pura su CreativeInput,
non serve passare dal filesystem per testarla.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from creative import CreativeInput, fingerprint, should_activate  # noqa: E402
from creative.activation import ActivationRecord, load_activation_history, save_activation  # noqa: E402
from creative.schemas import AttemptRecord  # noqa: E402


def _state(stagnation_count=0, request_creative=False, target="cell_2"):
    attempt = AttemptRecord(number=1, attempt={"approach_family": "induction", "request_creative": request_creative},
                            referee_report={"verdict": "REJECT"})
    return CreativeInput(current_target=target, stagnation_count=stagnation_count, history=[attempt])


class TestShouldActivate(unittest.TestCase):
    def test_no_signal_means_no_activation(self):
        activate, reason = should_activate(_state(), activation_log=[])
        self.assertFalse(activate)
        self.assertIn("nessun segnale", reason)

    def test_request_creative_flag_triggers_activation(self):
        activate, _ = should_activate(_state(request_creative=True), activation_log=[])
        self.assertTrue(activate)

    def test_stagnation_count_threshold_triggers_activation(self):
        activate, _ = should_activate(_state(stagnation_count=3), activation_log=[])
        self.assertTrue(activate)

    def test_max_activations_per_cell_blocks_further_activation(self):
        state = _state(stagnation_count=3)
        log = [ActivationRecord(number=i, target=state.current_target, reason="x", state_fingerprint=f"fp{i}")
               for i in range(1, 6)]  # 5 = MAX_ACTIVATIONS_PER_CELL di default
        activate, reason = should_activate(state, activation_log=log)
        self.assertFalse(activate)
        self.assertIn("limite", reason)

    def test_unchanged_state_blocks_reactivation(self):
        state = _state(stagnation_count=3)
        log = [ActivationRecord(number=1, target=state.current_target, reason="x", state_fingerprint=fingerprint(state))]
        activate, reason = should_activate(state, activation_log=log)
        self.assertFalse(activate)
        self.assertIn("invariato", reason)

    def test_changed_state_after_previous_activation_is_allowed(self):
        state = _state(stagnation_count=3)
        log = [ActivationRecord(number=1, target=state.current_target, reason="x", state_fingerprint="stato-diverso")]
        activate, _ = should_activate(state, activation_log=log)
        self.assertTrue(activate)


class TestActivationHistoryPersistence(unittest.TestCase):
    def test_save_and_reload_round_trips(self):
        with tempfile.TemporaryDirectory() as d:
            workdir = Path(d)
            record = ActivationRecord(number=1, target="cell_2", reason="test", state_fingerprint="fp1",
                                      ideas_summary=[{"id": "idea_safe", "risk": "SAFE"}])
            save_activation(workdir, record)
            reloaded = load_activation_history(workdir)
            self.assertEqual(len(reloaded), 1)
            self.assertEqual(reloaded[0].target, "cell_2")
            self.assertEqual(reloaded[0].ideas_summary[0]["id"], "idea_safe")


if __name__ == "__main__":
    unittest.main()
