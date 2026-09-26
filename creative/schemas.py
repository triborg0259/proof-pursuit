"""Strutture dati del Creative Agent.

Allineate al contratto reale del progetto condiviso (vedi
`shared-proof-pursuit/shared/schemas/*.json` nel repo di squadra): non sono
un'invenzione nostra, replicano i campi che Researcher e Referee già usano,
così Creative si inserisce senza bisogno che gli altri due cambino nulla.

Nessuna dipendenza esterna: solo dataclass della libreria standard, come
richiesto dalle regole di clean code del team ("niente file/requirements
nuovi per dipendenze già installate altrove").
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

# Stesso vocabolario di shared/schemas/attempt.schema.json (campo approach_family)
# e di creative_ideas.schema.json (campo approach_family delle idee). Un'unica lista
# qui evita che le due parti del sistema divergano silenziosamente.
APPROACH_FAMILIES = [
    "direct_proof", "contradiction", "induction", "extremal", "symmetry",
    "algebraic_reformulation", "matrix_formulation", "graph_formulation",
    "projective_spherical", "probabilistic", "exact_computation", "special_case",
    "equivalent_statement", "counterexample_search", "stronger_or_weaker_lemma",
    "reduction", "case_analysis", "other",
]

# Verdetti del Referee, da shared/schemas/referee_report.schema.json.
REFEREE_VERDICTS = ["ACCEPT", "PARTIAL_PROGRESS", "REJECT", "COUNTEREXAMPLE_FOUND", "KNOWN_OPEN", "UNKNOWN_STATUS"]


@dataclass
class AttemptRecord:
    """Un tentativo del Researcher, con il verdetto del Referee se già arrivato
    (None finché il Referee non ha ancora giudicato). Corrisponde alla coppia
    `attempts/attempt_NNN.json` + `attempts/referee_NNN.json` di una run reale."""
    number: int
    attempt: dict[str, Any] = field(default_factory=dict)
    referee_report: Optional[dict[str, Any]] = None

    @property
    def approach_family(self) -> str:
        return str(self.attempt.get("approach_family", ""))

    @property
    def verdict(self) -> str:
        return str((self.referee_report or {}).get("verdict", ""))

    @property
    def fatal_error(self) -> str:
        return str((self.referee_report or {}).get("fatal_error") or "")


@dataclass
class CreativeInput:
    """Tutto ciò che il Creative Agent legge per una cartella `runs/<problem_id>/`.
    Rispecchia state.schema.json più la storia strutturata dei tentativi; i tre
    file di contesto in Markdown sono facoltativi, esattamente come per il
    Researcher (deve funzionare anche senza)."""
    problem_id: str = ""
    current_target: str = ""
    current_blocker: str = ""
    verified_claims: list[str] = field(default_factory=list)
    stagnation_count: int = 0
    cell_status: dict[str, str] = field(default_factory=dict)
    history: list[AttemptRecord] = field(default_factory=list)
    problem_text: str = ""
    verified_claims_text: str = ""
    failed_attempts_text: str = ""


@dataclass
class CreativeIdea:
    """Una proposta di strategia. Campi obbligatori e nomi identici a
    creative_ideas.schema.json → properties.ideas.items; `approach_family`
    è l'unico campo opzionale previsto dallo schema di squadra."""
    id: str
    risk: str  # "SAFE" | "MEDIUM" | "WILD"
    method: str
    why_different: str
    why_it_might_work: str
    first_test: str
    expected_gain: str
    main_risk: str
    approach_family: str = ""


@dataclass
class CreativeOutput:
    """Corrisponde esattamente a creative_ideas.schema.json: blocker_analysis,
    avoid, ideas sono gli unici campi richiesti. `repetition_patterns` è un
    campo extra facoltativo (lo schema condiviso ha additionalProperties:
    true) tenuto solo per leggibilità umana della revisione, non letto dal
    Researcher."""
    blocker_analysis: str
    avoid: list[str]
    ideas: list[CreativeIdea]
    repetition_patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
