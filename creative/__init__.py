"""Modulo Creative Agent. Vedi README.md per ruolo, integrazione, contratto condiviso."""
from .activation import (
    STAGNATION_THRESHOLD,
    ActivationRecord,
    analyze_history,
    fingerprint,
    load_activation_history,
    should_activate,
)
from .creative_agent import build_prompt, generate_rule_based, load_creative_input, load_history
from .schemas import (
    APPROACH_FAMILIES,
    AttemptRecord,
    CreativeIdea,
    CreativeInput,
    CreativeOutput,
)
from .validation import validate_output

__all__ = [
    "load_creative_input",
    "load_history",
    "analyze_history",
    "generate_rule_based",
    "build_prompt",
    "should_activate",
    "fingerprint",
    "load_activation_history",
    "ActivationRecord",
    "STAGNATION_THRESHOLD",
    "validate_output",
    "CreativeInput",
    "CreativeOutput",
    "CreativeIdea",
    "AttemptRecord",
    "APPROACH_FAMILIES",
]
