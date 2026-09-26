# researcher/ — Persona 1: Researcher / autoresearch agent

Produce il miglior tentativo successivo per la cella target, leggendo lo stato condiviso. **Non giudica** (Referee),
**non inventa idee nuove quando stagna** (Creative), **non aggiorna `highest_verified_cell`** (Orchestrator).

## File
- `researcher_prompt.md` — system prompt: regole di onestà, un solo sotto-obiettivo, uso del feedback, formato JSON.
- `researcher.py` — agente a riga di comando, nessuna dipendenza oltre Python 3 (SDK `anthropic` solo per `--backend api`).
- `sample_output.json` — output reale (backend CLI, Claude Fable 5.1) sul problema giocattolo $x^2+1\ge 2x$.

## Uso
```
python3 researcher/researcher.py run     --workdir runs/problem_1 [--backend cli|api|mock] [--model M] [--effort low|medium|high|xhigh|max]
python3 researcher/researcher.py record  --workdir runs/problem_1 --report referee_report.json   # archivia il verdetto (lo chiama l'Orchestrator)
python3 researcher/researcher.py history --workdir runs/problem_1
python3 researcher/researcher.py run --workdir ... --dry-run     # stampa solo il prompt costruito
```
Backend: `cli` = `claude -p` headless (abbonamento Claude Code, nessuna chiave; default se `ANTHROPIC_API_KEY` non c'è);
`api` = SDK Anthropic (`pip install anthropic`, modello di default `claude-opus-5`, con `fallbacks: "default"`; **non testato**: nessuna chiave disponibile);
`mock` = deterministico, per i test.

## Cosa legge (tutti facoltativi tranne il problema)
`problem.md`, `state.json`, `verified_claims.md`, `failed_attempts.md`, `creative_ideas.json`, `referee_report.json`,
più la storia strutturata `attempts/attempt_NNN.json` + `attempts/referee_NNN.json`.

## Cosa scrive
- `attempts/attempt_NNN.json` (schema `shared/schemas/attempt.schema.json` + `attempt_id`, `ts`, `meta`, `schema_errors`)
- `attempt.json` = copia dell'ultimo tentativo (input del Referee)
- `state.json`: SOLO `stagnation_count` (+1 quando rileva stagnazione); `record` appende a `failed_attempts.md`.

## Stagnazione (regola del brief)
Tre tentativi consecutivi con la stessa `approach_family`, tutti REJECT senza claim accettati, e `fatal_error`
simili (Jaccard sulle parole ≥ 0.5) ⇒ `stagnation_count += 1`, `request_creative: true` nel tentativo, e il prompt
impone un cambio di famiglia. L'Orchestrator chiama il Creative quando `stagnation_count >= 3` o quando vede
`request_creative`.

## Test
```
python3 tests/test_researcher.py          # 4 test, backend mock, ~1 s
```
Run reali (CLI, effort medium): `runs/toy_x2` (17 s, $0.48, prova completa del giocattolo);
`runs/toy_fail` (tentativo → REJECT iniettato → secondo tentativo che corregge esattamente l'errore segnalato, 30 s, $0.25).
Costo indicativo su problemi veri con effort high/xhigh: 1–5 $ e 1–5 min per tentativo.

## Shell (`--shell sandbox|full`, solo backend cli)
```
python3 researcher/researcher.py run --workdir runs/X --backend cli --shell sandbox --effort high --strict
python3 researcher/researcher.py run --workdir runs/X --backend cli --shell full    --effort high --strict
```
- `sandbox`: Bash limitato a `python3` (più ls/cat/head/tail/wc), Read/Write/Edit, dentro `runs/X/sandbox/`;
  niente rete, pip, git, rm. `--permission-mode dontAsk`: ogni chiamata fuori allowlist è negata, non chiesta
  (`meta.permission_denials` le conta).
- `full`: tutti gli strumenti di Claude Code, Bash libero, rete (WebSearch, WebFetch, curl), accesso all'intero repo
  (`--add-dir`), `--permission-mode bypassPermissions`. Il prompt obbliga a citare con precisione ciò che si legge
  online, a installare pacchetti solo nel `.venv`, e alle stesse regole di rigore del sandbox.
La cartella di lavoro del modello è sempre `runs/X/sandbox/`. Limiti: `--max-turns` (150) e `--max-budget-usd` (15).
**Va lanciato da un terminale umano** (in Claude Code: prefisso `!`): un agente che lancia un altro agente con
permessi pre-autorizzati viene bloccato dal classificatore di sicurezza di Claude Code, anche in `--dry-run`.

## Ponte con il Referee (`bridge_referee.py`)
Il Referee del team (pacchetto `referee/`, di gabundos) legge un `ReviewInput` e produce un `ReviewPacket`;
il ponte traduce nei due sensi e archivia il verdetto come `researcher.py record`:
```
.venv/bin/python researcher/bridge_referee.py review --workdir runs/X            # Referee via CLI claude (abbonamento)
.venv/bin/python researcher/bridge_referee.py review --workdir runs/X --offline  # solo controlli esatti, nessun modello
.venv/bin/python researcher/bridge_referee.py to-review --workdir runs/X         # scrive solo review_input.json
.venv/bin/python researcher/bridge_referee.py from-packet --workdir runs/X --packet packet.json
```
Mappatura: `final_verdict`→`verdict`, `first_fatal_error.detail`→`fatal_error`, `next_required_step`→`next_blocker`;
`review_status` è conservato: **READY_FOR_HUMAN non è ACCEPT**, l'approvazione resta umana (`python -m referees approve`).
L'enunciato protetto della cella è `cell_statement` in state.json (se manca, `current_blocker`).
Il backend CLI (`CliBackend`) implementa il loro protocollo `JSONBackend` con `claude -p --json-schema`; il loro
`ClaudeBackend` (SDK, chiave API) usa `tool_choice` forzato, che su Claude Fable 5.1 restituisce 400: usare Opus.
Test: `.venv/bin/python tests/test_bridge_referee.py` (offline).

## Ciclo end-to-end (`loop.py`)
Researcher → Referee → decisione → (REJECT) Researcher rilegge `fatal_error` → … fino a READY_FOR_HUMAN.
```
python3 researcher/loop.py --workdir runs/X --max-iter 4 --researcher-backend cli --shell full --effort high --referee cli \
    --literature "frase esatta 1" --literature "frase esatta 2" [--creative-cmd "python3 creative/creative.py --workdir {workdir}"]
python3 researcher/loop.py --workdir runs/X --researcher-backend mock --referee mock --mock-rejects 2   # test senza modelli
```
Regole di arresto: READY_FOR_HUMAN/ACCEPT (approvazione umana), COUNTEREXAMPLE_FOUND, KNOWN_OPEN, UNKNOWN_STATUS, `--max-iter`.
PARTIAL_PROGRESS: i claim accettati entrano in `state.verified_claims`. Creative: punto d'aggancio `--creative-cmd`
(deve scrivere `{workdir}/creative_ideas.json`), chiamato su `request_creative`, `stagnation_signal` o aumento di
`stagnation_count`; se assente, avviso e si prosegue. Traccia per iterazione in `loop_log.jsonl`.
Test: `.venv/bin/python tests/test_loop.py`.

## Letteratura (`literature.py`, arXiv)
Ricerca deterministica sull'API pubblica di arXiv (frasi esatte per query multi-parola; sintassi nativa `ti:`, `au:`
passata com'è), salvata in `literature.json` e iniettata nel prompt come sezione LITERATURE con gli abstract.
Il tentativo deve contenere `literature_position`: cosa dà lo stato dell'arte per la cella e perché l'approccio lo segue,
lo adatta o se ne discosta, con id arXiv. Gli abstract non sono prove: un risultato preso da un paper è CITED, non
provato, salvo riproduzione completa (possibile con shell `full` scaricando il PDF). Esito onesto quando non c'è nulla:
`literature.json = []` e `literature_position = "none found"` (è il caso del problema 2, inedito).

## Limiti noti
- La similarità dei `fatal_error` è lessicale: un Referee che riformula lo stesso errore con parole diverse può
  ritardare la rilevazione della stagnazione (il Researcher può comunque impostare `request_creative` da solo).
- Senza `--shell` il Researcher non esegue codice: allega i calcoli in `code_used` e spetta al Referee eseguirli.
- Il run reale con `--shell` su `runs/p2_q3` (U(Q_3) per enumerazione esaustiva) non è ancora stato eseguito: farlo da terminale.
