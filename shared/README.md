# shared — contratto JSON fra Researcher, Referee, Creative, Orchestrator

Concordare questi formati PRIMA di lavorare separati; non cambiarli in corsa. Schemi in `schemas/`:

| File | Chi scrive | Chi legge |
|---|---|---|
| `state.schema.json` → `state.json` | Orchestrator (dopo il Referee); il Researcher tocca solo `stagnation_count` | tutti |
| `attempt.schema.json` → `attempts/attempt_NNN.json` | Researcher | Referee, Creative |
| `referee_report.schema.json` → `referee_report.json` (+ copia `attempts/referee_NNN.json`) | Referee | Orchestrator, Researcher, Creative |
| `creative_ideas.schema.json` → `creative_ideas.json` | Creative | Researcher |

File di contesto in Markdown (facoltativi, il Researcher funziona anche senza): `problem.md`, `verified_claims.md`, `failed_attempts.md`.

Layout di una cartella di lavoro (una per problema):
```
runs/<problem_id>/
  problem.md  state.json  verified_claims.md  failed_attempts.md  creative_ideas.json  referee_report.json
  attempts/attempt_001.json  attempts/referee_001.json  ...
```
Stati di cella ammessi: SOLVED · SOLVED_BY_COMPUTATION · PARTIAL_PROGRESS · UNRESOLVED · KNOWN_OPEN · FALSE.
Verdetti del Referee: ACCEPT · PARTIAL_PROGRESS · REJECT · COUNTEREXAMPLE_FOUND · KNOWN_OPEN · UNKNOWN_STATUS.
