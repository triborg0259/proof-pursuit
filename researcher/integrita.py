"""Perimetro di verifica: i file che il Researcher NON deve poter modificare mentre lavora.

Perché: con `--shell full` il Researcher vede tutto il repo (serve per riusare tools/ e leggere i problemi).
Se potesse ritoccare il Referee, i suoi prompt, gli schemi o l'enunciato della cella, il verdetto non varrebbe
più nulla (è la falla documentata in autoresearch #599: l'agente che riscrive il valutatore). Qui si prende
un'impronta dei file protetti prima del tentativo e la si confronta dopo: ogni differenza ferma il loop.

Uso da codice:  prima = impronta(workdir); ...; modificati = differenze(prima, impronta(workdir))
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Cartelle e file del repo che costituiscono il verificatore. Relativi a ROOT.
PERIMETRO_REPO = ["referee", "shared/schemas", "researcher/bridge_referee.py", "researcher/loop.py",
                  "researcher/integrita.py", "researcher/researcher.py", "CLAUDE.md"]
# File della cartella di lavoro che appartengono all'orchestratore, non al Researcher.
PERIMETRO_RUN = ["problem.md", "state.json", "referee_report.json", "approval.json", "literature.json"]
IGNORA = {"__pycache__", ".pytest_cache"}


def _file_sotto(percorso):
    """Tutti i file regolari sotto un percorso (o il percorso stesso se è un file), saltando le cache."""
    if percorso.is_file():
        return [percorso]
    if not percorso.is_dir():
        return []
    return [f for f in sorted(percorso.rglob("*")) if f.is_file() and not (IGNORA & set(f.parts))]


def _sha256(percorso):
    """Impronta del contenuto, letta a blocchi per non caricare file grandi in memoria."""
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 16), b""):
            h.update(blocco)
    return h.hexdigest()


def _sha256_state(percorso):
    """state.json senza `stagnation_count`: è l'unico campo che il Researcher ha il diritto di toccare, quindi
    un suo cambiamento non è una violazione. Se il file non è JSON valido si torna all'impronta grezza."""
    try:
        stato = json.loads(percorso.read_text(encoding="utf-8"))
        stato.pop("stagnation_count", None)
        return hashlib.sha256(json.dumps(stato, sort_keys=True).encode()).hexdigest()
    except (ValueError, AttributeError):
        return _sha256(percorso)


def impronta(workdir, root=ROOT):
    """Mappa {percorso: sha256} di tutto il perimetro (repo + file dell'orchestratore nel workdir)."""
    workdir = Path(workdir)
    percorsi = [root / p for p in PERIMETRO_REPO] + [workdir / p for p in PERIMETRO_RUN]
    risultato = {}
    for base in percorsi:
        for f in _file_sotto(base):
            risultato[str(f)] = _sha256_state(f) if f.name == "state.json" else _sha256(f)
    return risultato


def differenze(prima, dopo):
    """Percorsi modificati, cancellati o aggiunti tra due impronte, in ordine alfabetico."""
    cambiati = {p for p in prima if p in dopo and prima[p] != dopo[p]}
    cancellati = set(prima) - set(dopo)
    aggiunti = set(dopo) - set(prima)
    return sorted(cambiati | cancellati | aggiunti)
