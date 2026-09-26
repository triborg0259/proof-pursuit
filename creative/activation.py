"""activation.py — quando attivare il Creative Agent, e come evitare che si attivi a vuoto o in loop.

Il Researcher (researcher.py) già rileva la stagnazione e la scrive in state.json (`stagnation_count`)
e nel singolo tentativo (`request_creative`): questo modulo NON duplica quella regola, la legge e basta.
Il suo lavoro è tutto ciò che viene dopo:
1. capire COSA si sta ripetendo (`analyze_history`, usato anche dal generatore di idee);
2. decidere se ha senso attivarsi ORA (`should_activate`): non due volte sullo stesso stato invariato,
   non oltre un tetto di attivazioni per cella;
3. tenere uno storico persistente delle attivazioni (`runs/<problem_id>/creative/activation_NNN.json`),
   che serve sia per il punto 2 sia come materiale per il controllo di novità fra un'attivazione e l'altra.

Nessuna dipendenza da researcher.py: questo file legge solo lo stato già caricato da creative_agent.py
(CreativeInput), non tocca file del Researcher.
"""
import glob
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .schemas import CreativeInput

# Stessa soglia che il contratto condiviso assegna all'Orchestrator (shared/README.md: "l'Orchestrator
# chiama il Creative quando stagnation_count >= 3 o quando vede request_creative"): non ne inventiamo una
# seconda, la rendiamo solo configurabile qui in un unico punto.
STAGNATION_THRESHOLD = 3
STAGNATION_WINDOW = 3  # finestra di tentativi recenti considerata da analyze_history, stessa di researcher.py

# Prevenzione loop: quante volte il Creative Agent può attivarsi sulla STESSA cella prima di fermarsi
# e lasciare la decisione a un umano (non ha senso generare idee all'infinito se nessuna sblocca nulla).
MAX_ACTIVATIONS_PER_CELL = 5


# =============================================================================== confronto testuale (Jaccard)
def _words(text: str) -> set[str]:
    """Parole significative di un testo, per confrontare due errori fatali (stessa idea di researcher.py)."""
    stop = {"the", "a", "an", "of", "to", "is", "in", "and", "not", "that"}
    return set(re.findall(r"[a-z0-9]+", (text or "").lower())) - stop


def similar(text_a: str, text_b: str, threshold: float = 0.5) -> bool:
    """Vero se due testi condividono almeno metà delle parole (indice di Jaccard). Stessa soglia usata
    da researcher.py per la regola di stagnazione: qui serve anche a confrontare idee fra attivazioni."""
    words_a, words_b = _words(text_a), _words(text_b)
    if not words_a or not words_b:
        return False
    return len(words_a & words_b) / len(words_a | words_b) >= threshold


# =============================================================================== diagnosi di stagnazione
def analyze_history(state: CreativeInput, window: int = STAGNATION_WINDOW) -> dict:
    """Analisi deterministica e pura (nessuna chiamata a modelli) degli ultimi `window` tentativi già
    giudicati: quale approach_family si ripete e quale errore fatale si ripete con parole simili.
    Non decide SE attivarsi (lo fa should_activate, leggendo il segnale già dato dal Researcher):
    qui si assume di essere già stati chiamati e si cerca COSA sta bloccando la ricerca."""
    from collections import Counter  # import locale: usato solo qui, tiene l'intestazione del file corta

    judged = [h for h in state.history if h.referee_report]
    recent = judged[-window:]
    families = [h.approach_family for h in recent if h.approach_family]
    family_counts = Counter(families)
    repeated_family = family_counts.most_common(1)[0][0] if family_counts and len(recent) >= window and len(set(families)) == 1 else None

    errors = [h.fatal_error for h in recent if h.fatal_error]
    repeated_error = errors[-1] if errors and all(similar(errors[0], e) for e in errors[1:]) and len(errors) >= 2 else None

    families_ever_tried = {h.approach_family for h in judged if h.approach_family}
    return {
        "families_seen_recently": dict(family_counts),
        "repeated_family": repeated_family,
        "repeated_fatal_error": repeated_error,
        "families_ever_tried": sorted(families_ever_tried),
        "consecutive_rejects": sum(1 for h in reversed(judged) if h.verdict == "REJECT") if judged and judged[-1].verdict == "REJECT" else 0,
    }


# =============================================================================== impronta dello stato
def fingerprint(state: CreativeInput) -> str:
    """Riassunto deterministico dello stato rilevante (cella corrente + storia dei verdetti): due
    attivazioni con la stessa impronta vedono esattamente le stesse informazioni, quindi la seconda
    non produrrebbe niente di nuovo. Non serve crittograficamente forte: solo stabile e riproducibile."""
    payload = {"target": state.current_target,
              "history": [(h.number, h.approach_family, h.verdict, h.fatal_error) for h in state.history]}
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


# =============================================================================== storico delle attivazioni
@dataclass
class ActivationRecord:
    """Una riga di storico: cosa è stato proposto, per quale cella, con quale impronta di stato.
    Persistita in runs/<problem_id>/creative/activation_NNN.json (cartella nuova, non in conflitto con
    nessun file del contratto condiviso: Researcher e Referee non la leggono, è solo memoria del Creative)."""
    number: int
    target: str
    reason: str
    state_fingerprint: str
    ts: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))
    ideas_summary: list = field(default_factory=list)  # [{"id":..,"risk":..,"approach_family":..,"first_test":..}]

    def to_dict(self) -> dict:
        return asdict(self)


def _activations_dir(workdir: Path) -> Path:
    return workdir / "creative"


def load_activation_history(workdir: Path) -> list[ActivationRecord]:
    """Tutte le attivazioni passate per questa cartella di lavoro, in ordine."""
    records = []
    for path in sorted(glob.glob(str(_activations_dir(workdir) / "activation_*.json"))):
        data = json.loads(Path(path).read_text())
        records.append(ActivationRecord(**data))
    return records


def save_activation(workdir: Path, record: ActivationRecord) -> Path:
    """Scrive una nuova riga di storico. Non sovrascrive mai le precedenti (numerazione progressiva)."""
    _activations_dir(workdir).mkdir(parents=True, exist_ok=True)
    path = _activations_dir(workdir) / f"activation_{record.number:03d}.json"
    path.write_text(json.dumps(record.to_dict(), indent=1, ensure_ascii=False) + "\n")
    return path


def next_activation_number(workdir: Path) -> int:
    numbers = [int(Path(p).stem.split("_")[1]) for p in glob.glob(str(_activations_dir(workdir) / "activation_*.json"))]
    return max(numbers, default=0) + 1


# =============================================================================== la decisione vera e propria
def should_activate(state: CreativeInput, activation_log: list[ActivationRecord],
                    max_per_cell: int = MAX_ACTIVATIONS_PER_CELL,
                    stagnation_threshold: int = STAGNATION_THRESHOLD) -> tuple[bool, str]:
    """Decide se il Creative Agent deve generare idee ORA per questo stato.
    Tre motivi per rifiutare, in ordine: (1) il Researcher non ha ancora segnalato stagnazione;
    (2) la cella ha già raggiunto il tetto di attivazioni; (3) lo stato è identico all'ultima
    attivazione (nessun tentativo o verdetto nuovo da quando abbiamo già proposto idee)."""
    last_attempt_flagged = bool(state.history[-1].attempt.get("request_creative")) if state.history else False
    if state.stagnation_count < stagnation_threshold and not last_attempt_flagged:
        return False, "nessun segnale di stagnazione dal Researcher (stagnation_count e request_creative assenti)"

    same_cell = [a for a in activation_log if a.target == state.current_target]
    if len(same_cell) >= max_per_cell:
        return False, f"raggiunto il limite di {max_per_cell} attivazioni per '{state.current_target}': serve intervento umano"

    current_fp = fingerprint(state)
    if same_cell and same_cell[-1].state_fingerprint == current_fp:
        return False, "stato invariato dall'ultima attivazione: nessun nuovo tentativo o verdetto da analizzare"

    return True, "stagnazione confermata dal Researcher, stato cambiato, sotto il limite di attivazioni"
