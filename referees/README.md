# referees — Referee B (evidenze, fonti, calcolo, regole)

Il Referee B controlla **provenienza, applicabilità delle fonti, evidenze computazionali,
riproducibilità e rispetto delle regole**. Non rifà la dimostrazione: quella è la dimensione
del Referee A, che qui non c'è (lo aggiungerà l'integratore).

## Cosa contiene

| File | Origine | Modificabile |
|---|---|---|
| `contracts.py`, `agent_common.py`, `provider.py`, `trust.py` | copiati **senza modifiche** dal progetto dei referee | no — sono condivisi con A e con l'integratore |
| `referee_b.py`, `prompts/b.md` | copiati senza modifiche | sì, sono i file di proprietà di B |
| `adapter_b.py` | **nostro** | sì |

`adapter_b.py` è l'unico pezzo scritto qui. Fa solo conversione, in due direzioni:

- `runs/<problem_id>/` (`attempt.json` + `state.json` + `problem.md`) → `ReviewInput` dei referee;
- `EvidenceReport` → JSON conforme a `shared/schemas/referee_report.schema.json`.

## Garanzie

- **Mai ACCEPT.** `evidence_verdict` PASS diventa `PARTIAL_PROGRESS`, non ACCEPT: B copre una sola
  dimensione e l'approvazione finale è umana. Ogni rapporto porta `accept_requires_human: true`.
- **`accepted_claims` sempre vuoto.** In `shared/` quel campo significa *progresso verificato*, e solo
  l'orchestratore può popolarlo dopo una verifica reale. Le valutazioni positive di B stanno nel campo
  separato `evidence_supported_claims`, che è un suggerimento.
- **`highest_verified_cell` è una fotografia**, mai incrementata qui.
- **Il codice dei tentativi non viene eseguito.** `code_used` viaggia come artefatto `CODE` da leggere.
- **Un errore operativo non è un rigetto.** Timeout, output malformato o rifiuto del modello producono
  `UNKNOWN_STATUS` con `limitation`, mai `REJECT`.
- **Nessun log del candidato è un'osservazione fidata.** `TrustedContext` viene passato vuoto: non
  abbiamo eseguito verifiche indipendenti.

## Regole della competizione

`ReviewInput` richiede scelte esplicite, senza default impliciti. Il file
`shared/competition_rules.example.json` contiene i **vincoli interni del team** ricavati da `CLAUDE.md`,
non il regolamento ufficiale: va sostituito col regolamento vero appena disponibile. Finché resta
quello, `additional_rules` lo dichiara al modello, che deve segnalare come `MISSING` ciò che dipende
dalle regole reali.

## Come l'orchestratore chiama il componente

```python
import asyncio, json
from pathlib import Path
from referees.adapter_b import ClaudeCliBackend, review_attempt

workdir = Path("runs/p2_q3")

# Il backend è sostituibile: qualsiasi oggetto con
#   async def generate(self, *, role, system, payload, schema) -> dict
# va bene (vedi il protocollo JSONBackend in provider.py).
backend = ClaudeCliBackend(model="claude-opus-5")          # abbonamento, nessuna chiave API
# backend = ClaudeBackend(model_a=..., model_b=...)        # SDK anthropic, richiede ANTHROPIC_API_KEY

report = asyncio.run(review_attempt(workdir, backend, timeout=120))

# Il rapporto è già conforme a shared/schemas/referee_report.schema.json.
(workdir / "referee_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))

# L'orchestratore decide; il Referee B non tocca lo stato condiviso.
if report["verdict"] == "REJECT":
    print("blocco sulle evidenze:", report["fatal_error"])
```

Per archiviare il verdetto accanto al tentativo si usa il comando già esistente del Researcher
(richiede che `runs/<problem_id>/attempts/` esista):

```bash
python researcher/researcher.py record --workdir runs/p2_q3 --report runs/p2_q3/referee_report.json
```

### Da riga di comando

```bash
# revisione reale (consuma budget)
python -m referees.adapter_b run --workdir runs/p2_q3 --out runs/p2_q3/referee_report.json

# prova a costo zero, con una risposta simulata
python -m referees.adapter_b run --workdir runs/p2_q3 --backend mock \
  --mock-response tests/fixtures/referee_b/mock_response.json
```

Se `problem.md` non contiene una riga `Cell N:` con l'enunciato della cella, va passato a mano con
`--cell-statement`: il contratto protegge il bersaglio esatto e l'adattatore si rifiuta di inventarlo.

## Test

```bash
python -m pytest tests/ -q          # oppure: python tests/test_b_referee.py
```

Tutti con backend mock: **nessuna chiamata a pagamento**. Verificano il contratto e la conversione,
non la qualità del giudizio del modello, che richiede il test avversariale a pagamento
(`adversarial_eval.py`, non integrato qui).

## Dipendenze

`pydantic >= 2` (usato dai contratti). `anthropic` serve **solo** a `ClaudeBackend` in `provider.py`;
`ClaudeCliBackend` usa la CLI `claude` e non lo richiede. I test non richiedono nessuno dei due.
