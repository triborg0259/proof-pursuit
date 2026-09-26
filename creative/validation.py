"""validation.py — controlli sull'output del Creative Agent, prima che il Researcher lo legga.

Due categorie distinte:
- `errors`: l'output è strutturalmente rotto (id duplicati, risk non valido, campo obbligatorio vuoto).
  Chi chiama (creative_agent.py) deve rifiutarlo e ricadere sul generatore offline: non ha senso scrivere
  creative_ideas.json se non rispetta shared/schemas/creative_ideas.schema.json.
- `warnings`: l'output è valido ma sospetto (copertura SAFE/MEDIUM/WILD incompleta, linguaggio che
  suona come un'auto-certificazione). Non blocca la scrittura, ma va reso visibile: il Creative Agent
  non deve MAI poter affermare, nemmeno per un errore di formulazione del modello, che una cella è
  risolta o che una prova è completa (quello spetta solo al Referee).

Solo libreria standard: nessuna dipendenza nuova.
"""
import re

from .schemas import APPROACH_FAMILIES, CreativeOutput

VALID_RISKS = {"SAFE", "MEDIUM", "WILD"}
REQUIRED_IDEA_FIELDS = ["method", "why_different", "why_it_might_work", "first_test", "expected_gain", "main_risk"]

# Frasi che suonerebbero come un'auto-certificazione se prese alla lettera. Il controllo è euristico
# (cerca la frase SENZA una parola di riserva vicino, es. "if", "would", "assuming", "provisional"):
# non è una garanzia semantica, solo un allarme leggibile da un umano in fase di revisione.
_OVERCLAIM_PATTERNS = [r"\bthis proves\b", r"\bproves the cell\b", r"\bcell (is )?solved\b",
                       r"\bverified by the referee\b", r"\breferee accepted\b", r"\bcomplete proof of the cell\b",
                       r"\bq\.?e\.?d\.?\b"]
_HEDGE_WORDS = ["if ", "would ", "assuming", "provisional", "unverified", "conditional", "might", "candidate"]


def _overclaim_hits(text: str) -> list[str]:
    """Frasi di auto-certificazione trovate in `text` senza una parola di riserva nelle vicinanze."""
    lowered = (text or "").lower()
    if any(hedge in lowered for hedge in _HEDGE_WORDS):
        return []  # frase condizionale ("se si dimostra X, questo ridurrebbe...") è esplicitamente ammessa
    return [p.strip("\\b") for p in _OVERCLAIM_PATTERNS if re.search(p, lowered)]


def validate_output(output: CreativeOutput) -> tuple[list[str], list[str]]:
    """Ritorna (errors, warnings). Le chiamate a questa funzione non toccano mai il filesystem: pura
    validazione di struttura e linguaggio, testabile senza fixture su disco."""
    errors, warnings = [], []

    seen_ids = set()
    for idea in output.ideas:
        if idea.id in seen_ids:
            errors.append(f"id duplicato: '{idea.id}'")
        seen_ids.add(idea.id)

        if idea.risk not in VALID_RISKS:
            errors.append(f"idea '{idea.id}': risk '{idea.risk}' non è SAFE/MEDIUM/WILD")

        for field_name in REQUIRED_IDEA_FIELDS:
            if not getattr(idea, field_name, "").strip():
                errors.append(f"idea '{idea.id}': campo obbligatorio '{field_name}' vuoto")

        if idea.approach_family and idea.approach_family not in APPROACH_FAMILIES:
            errors.append(f"idea '{idea.id}': approach_family '{idea.approach_family}' non nel vocabolario condiviso")

        for field_name in ("method", "why_it_might_work", "first_test", "expected_gain"):
            for hit in _overclaim_hits(getattr(idea, field_name, "")):
                warnings.append(f"idea '{idea.id}': linguaggio da auto-certificazione in '{field_name}' ({hit})")

    risks_present = {idea.risk for idea in output.ideas if idea.risk in VALID_RISKS}
    for missing in VALID_RISKS - risks_present:
        warnings.append(f"nessuna idea di livello {missing}")

    for hit in _overclaim_hits(output.blocker_analysis):
        warnings.append(f"linguaggio da auto-certificazione in blocker_analysis ({hit})")

    return errors, warnings
