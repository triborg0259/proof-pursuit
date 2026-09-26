# Proof Pursuit — sistema multi-agente per ricerca matematica verificata

Gara di ricerca matematica assistita da AI: 7 ore, 4 problemi × 6 celle di difficoltà crescente (1/2/3/5/8/13 punti).
Contano solo prove e certificati verificabili. **Nulla viene inviato alla piattaforma dal repo**: le consegne restano
bozze in `problema-N/submission/` finché un umano non le approva.

Questo README spiega l'intera pipeline: dai documenti con i problemi formalizzati, al loop fra gli agenti, a come e
perché ogni agente decide, fino all'output strutturato (consegne + rapporto LaTeX) da caricare sulla piattaforma.

---

## 1. Mappa del repo

```
CLAUDE.md            protocollo di lavoro (vale per umani e agenti): cosa è una prova, cosa no
STATUS.md            stato delle 24 celle con evidenze; registro delle decisioni
problema-N/          enunciato.md (testo ufficiale in LaTeX) · note.md (triage, approcci) · fonti/ (letteratura letta,
                     arxiv.json) · esperimenti/ (ricerca) · certificati/ (verifica, separata) · submission/ (bozze)
shared/schemas/      il CONTRATTO fra gli agenti: state · attempt · referee_report · creative_ideas (JSON Schema)
researcher/          Researcher (researcher.py), ricerca arXiv (literature.py), ponte verso il Referee
                     (bridge_referee.py), ciclo end-to-end (loop.py)
referee/             Referee (gabundos): due giudici modello in parallelo + controlli esatti + merge deterministico
creative/            Creative (Marco Renzi): analizza la storia dei tentativi e propone direzioni nuove
runs/                una cartella per cella (pN_cK): problem.md, state.json, attempts/, referee_report.json,
                     creative_ideas.json, loop_log.jsonl (la traccia delle decisioni), verifica/ (riesecuzioni)
tools/               prepara_runs.py · lancia_loop.sh · cerca_letteratura.sh · build_report.py · run_tests.sh ·
                     autoloop.py (harness numerico) · render.sh
report/              rapporto LaTeX generato (proof_pursuit.tex) con prove, decisioni, codice e citazioni
tests/               test del Researcher, del ponte, del loop e del Referee B (tutti senza modelli)
SPIEGAZIONE_SEMPLICE.md   i quattro problemi e il metodo spiegati con metafore
```

---

## 2. La pipeline completa

```
   TESTO UFFICIALE                 FORMALIZZAZIONE                   CARTELLE DI LAVORO (una per cella)
 ┌──────────────────┐   a mano   ┌──────────────────────┐  prepara_runs.py  ┌──────────────────────────────┐
 │ enunciato incol- │ ─────────► │ problema-N/          │ ────────────────► │ runs/pN_cK/                   │
 │ lato dalla piat- │            │   enunciato.md (LaTeX│                   │   problem.md   (enunciato +   │
 │ taforma          │            │   fedele)            │                   │                 cella bersagl.)│
 └──────────────────┘            │   note.md (triage)   │                   │   state.json   (contratto)    │
                                 │ runs/celle.json      │                   │   literature.json (arXiv)     │
                                 │   (24 enunciati di   │                   └──────────────┬───────────────┘
   ARXIV (API pubblica)          │    cella, testuali)  │                                  │
 ┌──────────────────┐            └──────────────────────┘                                  │
 │ cerca_letteratura│ ──► problema-N/fonti/arxiv.json ──(filtro pertinenza)────────────────┘
 └──────────────────┘                                                                      │
                                                                                           ▼
                                                                    researcher/loop.py  (§3: il ciclo)
                                                                                           │
                    ┌──────────────────────────────────────────────────────────────────────┤
                    ▼                                                                      ▼
   REVISIONE UMANA (CLAUDE.md §Revisione)                                  TRACCIA runs/pN_cK/loop_log.jsonl
   problema-N/submission/parte-K.md  ◄── bozza scritta a mano dal tentativo     + attempts/ + referee_*.json
   STATUS.md aggiornato con evidenze          approvato (READY_FOR_HUMAN)       + creative_ideas.json + verifica/
                    │                                                                      │
                    └──────────────────────────► tools/build_report.py ◄───────────────────┘
                                                          │
                                                          ▼
                                     report/proof_pursuit.tex   (§6: output strutturato)
```

Punti fermi della pipeline:
- **L'enunciato è protetto.** Il testo della cella entra in `state.json` come `cell_statement` e il Referee giudica
  *quel* testo: nessun agente può riformulare il bersaglio.
- **La letteratura è deterministica.** `literature.py` interroga arXiv (frase esatta, id reali, abstract letti) prima
  del tentativo; il Researcher deve dichiarare in `literature_position` se segue, adatta o si stacca dallo stato
  dell'arte e perché. Un risultato preso da un paper è CITATO, non dimostrato.
- **Nessun agente dichiara mai "risolto".** Il Referee arriva al massimo a `READY_FOR_HUMAN`; `ACCEPT` è una firma umana.

---

## 3. Il ciclo di una cella, iterazione per iterazione

```
                         ┌─────────────────────────── ITERAZIONE i ────────────────────────────┐
                         │                                                                      │
   state.json ──────────►│  ① RESEARCHER  (researcher.py run --shell full)                       │
   referee_report.json ─►│     legge: enunciato, claim verificati, ultimo verdetto, tentativi     │
   failed_attempts.md ──►│     falliti, idee del Creative, abstract arXiv                         │
   creative_ideas.json ─►│     sceglie UN sotto-obiettivo e UNA famiglia di approccio            │
   literature.json ─────►│     lavora in una shell reale (python, rete) e scrive                 │
                         │     attempts/attempt_i.json: proof_attempt, code_used, claims_used,   │
                         │     reason_for_choice, literature_position, claimed_status, gaps      │
                         │                              │                                        │
                         │  ② PONTE (bridge_referee.py) │  attempt → ReviewInput del Referee     │
                         │     - claim usati ma non verificati → claim `dep_k` (il Referee li    │
                         │       vede e può marcarli UNVERIFIED, non spariscono)                  │
                         │     - RILANCIA ogni script di code_used in una copia pulita della     │
                         │       sandbox: exit code e stdout diventano `trusted_observations`     │
                         │       (i risultati riportati dal candidato non fanno fede)             │
                         │                              │                                        │
                         │  ③ REFEREE (referee/)        ▼                                        │
                         │     ┌──────────────────┐  ┌──────────────────────┐                    │
                         │     │ Giudice A        │  │ Giudice B            │  indipendenti,     │
                         │     │ MATEMATICA:      │  │ EVIDENZE: fonti,     │  stessa submission,│
                         │     │ primo passo non  │  │ codice, esaustività, │  nessuno vede      │
                         │     │ giustificato     │  │ regole di gara       │  l'altro           │
                         │     └────────┬─────────┘  └──────────┬───────────┘                    │
                         │              └──────── merge deterministico ───────┘                   │
                         │                 (pydantic strict: PASS/PARTIAL/FAIL coerenti)          │
                         │                              │                                        │
                         │  ④ DECISIONE (loop.py)       ▼   referee_report.json                   │
                         │     READY_FOR_HUMAN ─────► STOP: bozza di consegna + revisione umana   │
                         │     COUNTEREXAMPLE_FOUND ─► STOP: l'enunciato della cella è falso      │
                         │     KNOWN_OPEN / UNKNOWN ─► STOP: a mano                               │
                         │     PARTIAL_PROGRESS ────► i claim accettati entrano in                │
                         │                            state.verified_claims → iterazione i+1      │
                         │     REJECT ──────────────► failed_attempts.md (famiglia + errore)      │
                         │                            stagnazione? ──sì──► ⑤ CREATIVE             │
                         │                                          └─no──► iterazione i+1        │
                         │                                                                      │
                         │  ⑤ CREATIVE (creative/)  legge TUTTA la storia (attempts + verdetti)   │
                         │     scrive creative_ideas.json: blocker_analysis, avoid[], ideas[]     │
                         │     (SAFE / RISKY, why_different, why_it_might_work)                   │
                         │     → il Researcher della prossima iterazione DEVE preferirle          │
                         └──────────────────────────────────────────────────────────────────────┘
```

Ogni iterazione lascia una riga in `runs/pN_cK/loop_log.jsonl` con: famiglia e sotto-obiettivo scelti dal Researcher
e **perché** (`researcher_reason`, `literature_position`), verdetto e **errore fatale** del Referee (`fatal_error`,
`next_blocker`), se e **perché** è entrato il Creative (`creative`, `creative_analysis`). È questa traccia che finisce
nella consegna e nel rapporto LaTeX (§6).

---

## 4. Chi decide cosa, quando e perché

| Momento | Chi | Decisione | Su che base | Dove resta scritto |
|---|---|---|---|---|
| prima del loop | umano | formalizza l'enunciato, fissa la cella e le regole | testo ufficiale, `CLAUDE.md` | `problema-N/enunciato.md`, `runs/celle.json`, `shared/competition_rules.example.json` |
| inizio iterazione | Researcher | UN sotto-obiettivo, UNA famiglia (`approach_family`) | stato, ultimo `fatal_error`, tentativi falliti, idee del Creative, abstract arXiv | `attempt_i.json: subgoal, reason_for_choice, literature_position` |
| durante il tentativo | Researcher | quali calcoli fare e con che rigore (`exact` / `interval` / `float_exploration_only`) | regole di gara (< 10 min, insieme finito giustificato) | `attempt_i.json: code_used[]`, `sandbox/` |
| fine tentativo | Researcher | `claimed_status` onesto e `self_reported_gaps` | ciò che ha davvero giustificato | `attempt_i.json` |
| ponte | orchestratore | rilanciare il codice; registrare claim non verificati come `dep_k` | il Referee giudica solo osservazioni fidate | `verifica/attempt_i/osservazioni.json`, `review_input.json` |
| giudizio | Referee A | PASS / PARTIAL / FAIL matematico, **primo** errore fatale | solo la prova, come un referee di rivista | `attempts/packet_i.json: math_review` |
| giudizio | Referee B | PASS / PARTIAL / FAIL su evidenze; provenienza di ogni claim | fonti, osservazioni fidate, regole | `attempts/packet_i.json: evidence_review` |
| merge | Referee (codice) | verdetto finale, `review_status`, claim accettati, `stagnation_signal` | regole deterministiche, nessun modello | `referee_report.json` |
| decisione | loop.py | fermarsi / continuare / integrare claim / chiamare il Creative | tabella in §3 | `loop_log.jsonl` |
| stagnazione | Creative | analisi del blocco, cosa evitare, 2–4 direzioni nuove | tutta la storia dei tentativi | `creative_ideas.json`, `creative/activation_*.json` |
| dopo lo STOP | umano | scrivere la bozza di consegna, revisione critica, `STATUS.md` | protocollo `CLAUDE.md` | `problema-N/submission/parte-K.md` |

### Perché e quando entra il Creative

Il Creative **non** gira a ogni iterazione: costerebbe e disperderebbe. Entra solo quando il ciclo sta girando a vuoto,
e il loop lo riconosce con tre segnali indipendenti, ognuno sufficiente (`loop.py: serve_creative`):

1. **il Researcher lo chiede** (`request_creative: true`): ritiene di aver esaurito le vie naturali;
2. **il Referee lo segnala** (`stagnation_signal`): stesso errore fatale che si ripete;
3. **il contatore di stagnazione sale** (`state.stagnation_count`): il Researcher stesso rileva, prima di tentare,
   che gli ultimi tentativi hanno stessa famiglia e stesso motivo di rigetto (similarità lessicale del `fatal_error`).

Quando entra, legge *tutta* la storia (non solo l'ultimo tentativo), scrive perché il blocco si ripete
(`blocker_analysis`), cosa non ripetere (`avoid`) e direzioni davvero diverse con rischio dichiarato (`ideas`). Il
Researcher dell'iterazione successiva vede queste idee nel prompt e deve dire quale segue e perché. Il Creative
**non certifica nulla e non dichiara mai una cella risolta**: quello resta compito del Referee, poi dell'umano.

### Perché due giudici e un merge senza modello

Un solo modello che dice "corretto" non è una prova. Il Referee separa due domande che vengono confuse volentieri:
*è vero?* (A: logica, casi mancanti, target mismatch, bound superiore spacciato per valore esatto) ed *è
dimostrato con ciò che è stato mostrato?* (B: fonti recuperate o no, calcoli riprodotti o no, esaustivo o campionato,
float o esatto). Nessun giudice vede l'altro. Il merge è codice deterministico con regole di coerenza: un PASS con
un errore fatale è rifiutato dal validatore; un giudice che non può giudicare restituisce una `limitation`, che non è
mai un FAIL. Se un giudice allega una riserva a un rapporto valido, il ponte la sposta nelle note invece di perdere
il giudizio (era il caso reale di U(Q₅): un PASS motivato scartato per un campo di troppo). Analogamente, se B classifica
anche i claim già verificati, il ponte tiene solo quelli del candidato, come vuole il validatore del merge. Le
normalizzazioni tolgono soltanto, non aggiungono mai. `bridge_referee.py review --replay` ri-fonde gli ultimi rapporti
grezzi salvati senza richiamare i modelli: utile dopo una correzione del ponte.

---

## 5. I contratti (shared/schemas)

- `state.schema.json` — `current_target`, `cell_statement` (protetto), `verified_claims[]`, `failed_attempts[]`,
  `stagnation_count`, `cell_status` con stati ammessi SOLVED · SOLVED_BY_COMPUTATION · PARTIAL_PROGRESS · UNRESOLVED ·
  KNOWN_OPEN · FALSE. Il Researcher tocca solo `stagnation_count`; `highest_verified_cell` lo muove solo il Referee.
- `attempt.schema.json` — tutti i campi obbligatori (`literature_position` compreso); `claimed_status` ∈
  CELL_SOLVED_CANDIDATE · LEMMA_CANDIDATE · NUMERICAL_EVIDENCE_ONLY · LITERATURE_ONLY · COUNTEREXAMPLE_CANDIDATE · NO_PROGRESS.
- `referee_report.schema.json` — `verdict`, `review_status` (READY_FOR_HUMAN ≠ ACCEPT), `fatal_error`, `next_blocker`,
  `accepted_claims`, `stagnation_signal`.
- `creative_ideas.schema.json` — `blocker_analysis`, `avoid[]`, `ideas[]` con rischio e motivazioni.

---

## 6. Output strutturato per la piattaforma

Per ogni cella la piattaforma riceve una consegna scritta. Qui il percorso è:

1. **STOP del loop con READY_FOR_HUMAN** ⇒ un umano scrive `problema-N/submission/parte-K.md` seguendo `CLAUDE.md`:
   risultato e ambito · dimostrazione completa (o certificato + giustificazione) · istruzioni di verifica con tempi
   misurati · fonti (distinguendo risultati esistenti e contributo nostro) · limiti.
2. **Revisione critica umana** (ipotesi mancanti, circolarità, discrepanze codice/enunciato) ⇒ `STATUS.md` passa a
   `revisionato`. Un verdetto READY_FOR_HUMAN senza revisione resta `bozza pronta`.
3. **Rapporto LaTeX** `tools/build_report.py` ⇒ `report/proof_pursuit.tex`, per ogni problema e cella:
   enunciato ufficiale · stato · consegna (prova) · **decisioni degli agenti** iterazione per iterazione (famiglia,
   motivo, verdetto, errore fatale, intervento del Creative e sua analisi) · **codice** su cui la prova poggia,
   con l'esito della riesecuzione fidata e il verdetto del Referee · **citazioni arXiv** trovate dalla ricerca
   deterministica e usate dal Researcher, con la posizione dichiarata rispetto allo stato dell'arte.

Regola d'oro (CLAUDE.md): DIMOSTRATO / CITATO (con fonte) / VERIFICATO SU INTERVALLO FINITO / CONGETTURA sono
quattro cose diverse e la consegna le tiene separate.

---

## 7. Come si usa

```
python3 -m venv .venv && .venv/bin/pip install numpy mpmath pydantic     # ambiente
tools/run_tests.sh                                                        # tutte le suite, senza modelli
tools/cerca_letteratura.sh                                                # arXiv → problema-N/fonti/arxiv.json
.venv/bin/python tools/prepara_runs.py p1 p2                              # cartelle runs/pN_cK
tools/lancia_loop.sh p1 2                # loop reale su tutte le celle di P1, 2 iterazioni, in parallelo
tools/lancia_loop.sh p2 2 3 4 5 6        # P2, solo celle 3–6 (1–2 già chiuse)
.venv/bin/python researcher/loop.py --workdir runs/p1_c1 --max-iter 3 --researcher-backend cli --shell full \
      --referee cli --creative cli      # una cella sola, a mano
.venv/bin/python tools/build_report.py   # → report/proof_pursuit.tex (+ HTML di anteprima se c'è pandoc)
```
Note operative: il Researcher con shell `full` gira con permessi pre-autorizzati e va avviato da un terminale umano
(in Claude Code: prefisso `!`). Backend: `claude -p --json-schema` con abbonamento; nessuna chiave API necessaria.
Test del ciclo senza modelli: `--researcher-backend mock --referee mock --creative rule_based`.

## 8. Regole minime per collaborare
1. Branch per persona/parte, PR piccole verso `main`; `STATUS.md` si aggiorna nella stessa PR.
2. Clean code: funzioni piccole, commenti in italiano che dicono cosa e perché, nessuna dipendenza duplicata.
3. Ogni esperimento: comando riproducibile, seed, tempi. Ogni certificato: separato dalla ricerca.
4. Nessuna submission alla piattaforma dal repo.
