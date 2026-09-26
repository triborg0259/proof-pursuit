# Proof Pursuit — workspace di squadra

Gara di ricerca matematica assistita da AI (7 ore, 4 problemi × 6 parti). **Repo privato: non pubblicare.**

- `CLAUDE.md` — protocollo di lavoro (vale per umani e agenti).
- `STATUS.md` — stato di tutte le 24 parti, con evidenze. Aggiornarlo a ogni avanzamento.
- `problema-N/` — `enunciato.md` (testo ufficiale in LaTeX), `note.md` (triage, approcci, stato),
  `esperimenti/` (ricerca), `certificati/` (verifica), `submission/` (bozze consegna), `fonti/` (letteratura verificata).
- `tools/` — harness di ricerca numerica (`autoloop.py`, protocollo in `program.md`), `render.sh` (Markdown→HTML
  con formule), `HARNESS_RICERCA.md` (stato dell'arte sui loop AI per la matematica).

## Setup
```
python3 -m venv .venv && .venv/bin/pip install numpy mpmath
sh tools/render.sh        # opzionale: rende i .md in _html/ (serve pandoc); GitHub rende già il LaTeX
```

## Regole minime per collaborare
1. Un branch per persona/parte (`p3-c2-nome`), PR piccole verso `main`; `STATUS.md` si aggiorna nella stessa PR.
2. Distinguere sempre DIMOSTRATO / CITATO / VERIFICATO SU INTERVALLO FINITO / CONGETTURA.
3. Ogni esperimento: comando riproducibile, seed, tempi, nel README della cartella `esperimenti/`.
4. Nessuna submission alla piattaforma dal repo: le bozze restano in `submission/` per la revisione.
