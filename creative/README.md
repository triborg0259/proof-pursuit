# Creative Agent

Uno dei tre ruoli logici del sistema multi-agente di Proof Pursuit:

- **Researcher** (`researcher/`) — prova a risolvere la cella corrente.
- **Referee** (non ancora nel repo) — decide se un tentativo è davvero corretto.
- **Creative Agent** (questo modulo) — si accorge quando il Researcher è bloccato
  e propone direzioni genuinamente diverse. **Non certifica mai la correttezza
  e non dichiara mai una cella risolta.** Quello resta compito del Referee.

> Il Researcher si chiede: *"come lo risolvo?"*
> Il Referee si chiede: *"è davvero corretto?"*
> Il Creative Agent si chiede: *"stiamo cercando nel posto sbagliato?"*

## Contratto condiviso

Questo modulo legge/scrive esattamente il formato già concordato dal team in
`shared/schemas/` e usato da `researcher/researcher.py` — non un formato
inventato. Vive nella stessa cartella di lavoro del Researcher:

```
runs/<problem_id>/
  state.json                     scritto dall'Orchestrator/Researcher, letto da noi
  problem.md, verified_claims.md, failed_attempts.md   facoltativi, letti se presenti
  attempts/attempt_NNN.json + referee_NNN.json         storia strutturata, letta da noi
  creative_ideas.json            SCRITTO DA NOI (shared/schemas/creative_ideas.schema.json), letto dal Researcher
  creative/activation_NNN.json   storico delle NOSTRE attivazioni (cartella aggiuntiva, non nel contratto
                                 condiviso: nessun altro agente la legge, serve solo a noi per la prevenzione
                                 dei loop e il controllo di novità fra un'attivazione e l'altra)
```

## File

```
creative/
├── __init__.py       re-esporta l'API pubblica
├── schemas.py         CreativeInput/CreativeOutput/CreativeIdea/AttemptRecord (dataclass) + APPROACH_FAMILIES
├── activation.py      analyze_history (cosa si ripete) + should_activate (quando attivarsi) + storico persistente
├── validation.py       validate_output: errori strutturali vs avvisi di linguaggio da auto-certificazione
├── creative_agent.py    caricamento dello stato, generatore offline, backend cli/api, CLI
├── prompt.md            prompt fisso per il backend LLM (separato dal codice Python)
└── tests/               20 test, solo unittest della libreria standard
```

Deviazione deliberata dalla struttura suggerita in origine (`models.py`,
`prompts.py`, `stagnation.py`, `ranking.py`, `config.py` separati): il resto
del progetto condiviso tiene un file per agente (`researcher/researcher.py`
è ~450 righe, tutto dentro), quindi per coerenza stilistica teniamo due file
di logica (`creative_agent.py`, `activation.py`) più `validation.py` per un
controllo concettualmente distinto (onestà dell'output, non generazione),
invece di frammentare in molti micro-file da poche righe l'uno.

## Uso diretto (senza LLM, sempre disponibile)

```python
from creative import load_creative_input, generate_rule_based

state = load_creative_input(Path("runs/problem_1"))
output = generate_rule_based(state)   # nessuna chiamata a modelli, deterministico
output.to_dict()                      # conforme a creative_ideas.schema.json
```

`generate_rule_based` non è solo un doppio per i test: guarda quale
`approach_family` si ripete negli ultimi tentativi giudicati e in quale
motivo di rigetto (`activation.analyze_history`), ed evita esplicitamente
quella famiglia proponendo tre alternative (una per livello SAFE/MEDIUM/WILD).

## CLI

```bash
# dalla radice del repo condiviso
python3 -m creative.creative_agent run --workdir runs/problem_1
python3 -m creative.creative_agent run --workdir runs/problem_1 --dry-run   # stampa solo il prompt
python3 -m creative.creative_agent run --workdir runs/problem_1 --auto      # con attivazione automatica (sotto)
python3 -m creative.creative_agent run --workdir runs/problem_1 --backend cli --effort medium
```

Scrive sempre `creative_ideas.json` nella cartella di lavoro (tranne con
`--dry-run`, che stampa solo il prompt costruito).

### Backend

- `rule_based` (default): il generatore deterministico sopra. Funziona ovunque.
- `cli` / `api`: riusano `call_cli`/`call_api` di `researcher/researcher.py`
  (stesso wrapper LLM del Researcher, per non duplicarne uno, come richiesto
  dal brief originale) — richiedono di essere eseguiti dalla radice del repo
  condiviso, dove esistono `researcher/` e `shared/schemas/`. Se
  l'importazione fallisce (es. questa copia non è ancora dentro il repo
  condiviso), `generate()` ricade sul backend offline invece di crashare, e
  lo dice in `blocker_analysis`.
- Qualunque cosa arrivi da `cli`/`api` passa da `validation.validate_output`
  prima di essere scritta: un output strutturalmente rotto (id duplicati,
  `risk` non valido, campo obbligatorio vuoto) fa ricadere sul backend
  offline invece di scrivere un `creative_ideas.json` non conforme allo
  schema condiviso.

## Attivazione automatica (`--auto`) e prevenzione dei loop

Senza `--auto`, il comando genera e scrive sempre — è il comportamento
diretto usato dai test e da un uso manuale (**il Creative Agent resta
chiamabile direttamente anche se esiste orchestrazione automatica**, come
richiesto). Con `--auto`, prima chiede a `activation.should_activate` se ha
senso attivarsi ORA:

1. **Segnale di stagnazione**: rifiuta se il Researcher non ha ancora
   segnalato stagnazione (`state.json.stagnation_count >= 3`, la stessa
   soglia che `shared/README.md` assegna all'Orchestrator — non ne
   inventiamo una seconda) né impostato `request_creative: true` sull'ultimo
   tentativo.
2. **Tetto per cella**: rifiuta se questa cella ha già raggiunto
   `MAX_ACTIVATIONS_PER_CELL` (5 di default, in `activation.py`) — a quel
   punto serve una decisione umana, non altre idee automatiche.
3. **Stato invariato**: rifiuta se l'impronta dello stato (`activation.fingerprint`,
   cella + intera storia di tentativi/verdetti) è identica all'ultima
   attivazione registrata — nessun tentativo o verdetto nuovo da analizzare,
   quindi nessuna idea nuova da generare.

Ogni attivazione accettata viene registrata in
`runs/<problem_id>/creative/activation_NNN.json` (numero, cella, motivo,
impronta di stato, riassunto delle idee proposte): è lo storico che rende
possibili i punti 2 e 3, ed è materiale riusabile per un controllo di novità
fra un'attivazione e l'altra.

## Onestà dell'output (`validation.py`)

`validate_output(output)` ritorna `(errors, warnings)`:
- **errors** (id duplicati, `risk` non in SAFE/MEDIUM/WILD, campo
  obbligatorio vuoto, `approach_family` fuori dal vocabolario condiviso):
  fanno ricadere sul generatore offline quando arrivano da un backend LLM.
- **warnings** (copertura SAFE/MEDIUM/WILD incompleta, linguaggio che suona
  come un'auto-certificazione — es. "this proves the cell is solved" senza
  una parola di riserva vicino come "if"/"would"/"assuming") restano
  visibili in cima a `blocker_analysis` invece di bloccare la scrittura: il
  controllo è euristico, non una garanzia semantica, e va letto da un umano
  in revisione. Frasi condizionali ("se questo lemma si dimostra, questo
  ridurrebbe la cella a...") restano esplicitamente ammesse, come richiesto.

## Verificato per davvero, non solo nei test

Oltre ai 20 test unitari, questo modulo è stato fatto girare contro il vero
`researcher/researcher.py` (non un doppio): 3 tentativi "induction" respinti
→ il Researcher reale rileva la stagnazione da solo → questo Creative Agent
genera `creative_ideas.json` → il tentativo successivo del Researcher adotta
`approach_family` dalla nostra prima idea. Una seconda chiamata con `--auto`
sullo stesso stato si rifiuta correttamente citando "stato invariato".

## Test

```bash
cd proof-pursuit   # o dalla radice del repo condiviso, dopo l'integrazione
python3 -m unittest discover -s creative/tests -p "test_*.py" -v
```

20 test, solo `unittest` della libreria standard, nessuna chiamata di rete
o a modelli, ~3 millisecondi in totale:
- `test_basic.py` — generazione di base (>=3 idee, SAFE/MEDIUM/WILD presenti).
- `test_repetition.py` — anti-ripetizione (non ripropone la famiglia che si
  ripeteva) e creatività guidata dal Referee (evita l'argomento già segnalato
  come insufficiente).
- `test_activation.py` — quando `should_activate` dice sì/no, tetto per
  cella, nessuna riattivazione su stato invariato, persistenza dello storico.
- `test_validation.py` — errori strutturali vs avvisi di onestà, incluso che
  una frase condizionale non venga segnalata mentre una categorica sì.

## Cosa NON fa (esplicito, per costruzione)

- Non decide se un tentativo è corretto (compito del Referee).
- Non dichiara mai una cella risolta, né in codice né nel testo generato
  (schermato da `validation.py`, per quanto un controllo euristico può fare).
- Non costruisce un Referee finto: il confine per quando arriverà è
  `shared/schemas/referee_report.schema.json`, già esistente e già letto
  passivamente da `state.json`/`referee_report.json` se presenti — nessuna
  modifica necessaria qui quando il Referee sarà aggiunto da un compagno.
- Nessun database, vector store, frontend, o processo in background.
