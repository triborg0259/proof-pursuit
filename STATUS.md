# STATUS — Proof Pursuit

Tempo totale: 7 ore. Tempo rimanente: 5 ore (dichiarato alle ~11:45 del 2026-09-26 ⇒ fine ~16:45)
Ultimo aggiornamento: 2026-09-26, inizializzazione

Legenda stati: non iniziato · in analisi · in corso · parziale · bozza pronta · revisionato · bloccato

## Riepilogo colonne

| Problema | Titolo | Celle con evidenza | Stato complessivo |
|---|---|---|---|
| 1 | Angles between lines (Fejes Tóth), 32 pt | 2/6 | in corso (parti 1–2 revisionate e approvate) |
| 2 | Uphill paths on the hypercube, 32 pt | 3/6 | in corso (parti 1–3 approvate; parte 4 valore candidato) |
| 3 | Bulgarian solitaire, 32 pt | 1/6 | in corso (parte 1 approvata; parte 2 nel loop) |
| 4 | Disjoint classes / gcd of moduli, 32 pt | 3/6 | in corso (parti 1–3 approvate) |

## Problema 1 — Lines / somma di angoli

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | Prova: $S \le \frac{\pi}{2}\lfloor N^2/4\rfloor$ in $\mathbb{R}^2$ (1 pt, Judged) | revisionato | prova completa (semigiro casuale, argomento E) scritta a mano; Referee READY_FOR_HUMAN (A PASS, B PASS); approvata; submission/parte-1.md |
| 2 | Prova lemma di ortogonalità su catene di versori (2 pt, Judged) | revisionato | prova completa per induzione con proiezione (argomento F); Referee READY_FOR_HUMAN (A PASS, B PASS); approvata; submission/parte-2.md |
| 3 | $N=d+1$: $S\le(\binom{d+1}{2}-1)\pi/2$ (3 pt) | parziale |triage in note.md; dipende dal lemma P2; bozza parziale in inglese in submission/ (parziali.py) |
| 4 | 5 rette in $\mathbb{R}^3$ ($4\pi$), 6 in $\mathbb{R}^4$ ($13\pi/2$) (5 pt) | parziale |triage; possibile via P5 o calcolo rigoroso; bozza parziale in inglese in submission/ (parziali.py) |
| 5 | $N=d+2$: $S\le(\binom{d+2}{2}-2)\pi/2$ (8 pt) | parziale |triage; bozza parziale in inglese in submission/ (parziali.py) |
| 6 | Congettura completa, open (13 pt) | parziale |triage; solo ricerca controesempi / famiglie infinite; bozza parziale in inglese in submission/ (parziali.py) |

## Problema 2 — Uphill paths on the hypercube

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | $U(Q_3)$, $U(Q_4)$ + etichettature (1 pt, checked) | revisionato | $U(Q_3)=14$, $U(Q_4)=34$: prove a mano rilette passo per passo + verifiche esatte indipendenti; bozza in submission/parte-1.md |
| 2 | $U(Q_5)$ (2 pt, checked) | revisionato | $U(Q_5)=88$: riduzione a (★) riletta a mano lemma per lemma + 3 enumerazioni concordi (una indipendente per metodo); etichettatura verificata; Referee automatico READY_FOR_HUMAN (giudice A PASS in 3 run, giudice B PASS con sole note INFO, codice rieseguito dall'orchestratore); bozza in submission/parte-2.md |
| 3 | $U(Q_6)$ (3 pt, checked) | revisionato | loop p2_c3 attempt_001: Referee READY_FOR_HUMAN (A PASS, B PASS); approvata da Thomas Tumini (human); submission/parte-3.en.md |
| 4 | $U(Q_7)$, $U(Q_8)$ (5 pt, checked) | parziale | valori candidati 464 = |E|+16 e 1040 = |E|+16 (Hamming) per costruzione a stelle; bound inferiore non dimostrato; submission/parte-4.md |
| 5 | Migliorare $2368\le U(Q_9)\le2400$ (8 pt) | parziale |la costruzione a stelle con un codice (8,20,3) dà esattamente 2400: il bound noto è questa famiglia; per scendere serve una foresta non a stelle; bozza parziale in inglese in submission/ (parziali.py) |
| 6 | $U(Q_9)$ esatto con prove (13 pt, open) | parziale | bozza parziale in inglese in submission/ (parziali.py) |

## Problema 3 — Bulgarian solitaire

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | Cicliche e numero di cicli, prove (1 pt) | revisionato | loop p3_c1 attempt_002: Referee READY_FOR_HUMAN (A PASS, B PASS); approvata da Thomas Tumini (human); submission/parte-1.en.md |
| 2 | $D_B(T_k)$ esatto (2 pt) | parziale |atteso $k^2-k$ (Igusa/Etienne, da verificare); bozza parziale in inglese in submission/ (parziali.py) |
| 3 | Bound $k^2-2k-1$ e $D_B(T_k-1)$ (3 pt) | parziale | bozza parziale in inglese in submission/ (parziali.py) |
| 4 | $D_B(T_{k-1}+1)$ (5 pt) | parziale | bozza parziale in inglese in submission/ (parziali.py) |
| 5 | $D_B(T_{k-1}+2)$ (8 pt) | parziale | bozza parziale in inglese in submission/ (parziali.py) |
| 6 | $D_B(n)$ per ogni $n$ (13 pt, open) | parziale | bozza parziale in inglese in submission/ (parziali.py) |

## Problema 4 — Disjoint congruence classes, large gcd

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | $k=3$ (1 pt) | revisionato | prova completa (parità); Referee READY_FOR_HUMAN (A PASS, B PASS); approvata; submission/parte-1.md |
| 2 | $k=4$ (2 pt) | revisionato | prova completa (clique per primo, casi su $|T|$); Referee READY_FOR_HUMAN (A PASS, B PASS); approvata; submission/parte-2.md |
| 3 | $k\le8$ (3 pt) | revisionato | loop p4_c3 attempt_001: Referee READY_FOR_HUMAN (A PASS, B PASS); approvata da Thomas Tumini (human); submission/parte-3.en.md |
| 4 | $k\le12$ + report 9–16 (5 pt) | parziale | bozza parziale in inglese in submission/ (parziali.py) |
| 5 | boundary certificato + $k=24,30$ (8 pt) | parziale |richiede 2 implementazioni indipendenti; bozza parziale in inglese in submission/ (parziali.py) |
| 6 | oltre (13 pt, open) | parziale | bozza parziale in inglese in submission/ (parziali.py) |

## Registro decisioni e ostacoli
- 2026-09-26 ~15:20: PRIMO END-TO-END REALE CHIUSO: `runs/p2_q5` → READY_FOR_HUMAN. Quarto ostacolo di contratto nel pacchetto Referee: il prompt di B gli chiede di classificare anche le dipendenze, ma `_validate_ids` ammette in `claim_provenance` solo i claim del candidato ("B references unregistered provenance"). Fix nel ponte: le voci sui claim già verificati vengono tolte (mai aggiunto nulla); `review --replay` ri-fonde i grezzi salvati senza richiamare i modelli. Da segnalare a gabundos insieme al `limitation`+report. Costo totale dei 3 run del Referee su Q5: ≈ $7.
- 2026-09-26 ~15:00: INTEGRAZIONE COMPLETA su main. Mergiati `feature/referee-a` (prompt del giudice A + regole di campo, 2 suite) e `feature/referee-b` (Referee B consolidato nel ponte: claim `dep_k`, enunciato da problem.md, regole da file, UTF-8); conflitti solo in .gitignore/STATUS (uniti). Creative di Marco collegato al loop come default (`--creative cli|rule_based|none`). Tre bug reali trovati dai run: (1) `--tools ""` è variadico e ingoiava il prompt se ultimo (fix: subito dopo -p); (2) il giudice A allegava una `limitation` a un PASS valido e il contratto scartava il rapporto (fix: la riserva va nelle note); (3) il giudice B esigeva riesecuzioni fidate e le regole ufficiali (fix: il ponte rilancia `code_used` in una copia pulita → trusted_observations; `rules` di ogni run = paragrafo 'What to hand in' dell'enunciato). Tutte le suite verdi: 26 test nostri, 94 Referee, 20 Creative (`tools/run_tests.sh`). Cartelle `runs/pN_cK` per tutte le 24 celle con letteratura arXiv filtrata (`tools/prepara_runs.py`), lanciatore `tools/lancia_loop.sh`, rapporto LaTeX `tools/build_report.py` → `report/proof_pursuit.tex`, README di architettura, SPIEGAZIONE_SEMPLICE.md. Rami remoti integrati da cancellare (permesso negato all'agente).
- 2026-09-26 ~14:40: arXiv per P4 trova Fornal–Sun [2607.24655] (lug. 2026): $\max\gcd\gg k\exp(-(2+o(1))\sqrt{\log k/\log\log k})$, migliora il bound citato nell'enunciato di C6(b). Riprodurre la prova per esteso varrebbe (regola: 'whatever its source'). Per P1: Lim–McCann [2007.08698] non copre $N=d+1,d+2$.
- 2026-09-26 ~14:30: Referee B consolidato su `feature/referee-b` DENTRO `bridge_referee.py`, senza creare un secondo ponte: la prima versione (pacchetto `referees/` + `adapter_b.py`) duplicava `referee/referees/` ed è stata cancellata. Tre migliorie portate nel ponte: (1) un `claims_used` senza riscontro diventa un claim `dep_k` del candidato invece di sparire, così il Referee ne valuta la provenienza; (2) l'enunciato della cella si cerca anche nella riga `Cell N:` di `problem.md` e in mancanza totale ci si ferma invece di usare un segnaposto; (3) le regole vengono da `shared/competition_rules.example.json` (segnaposto, NON il regolamento ufficiale) invece che da un dizionario nel codice. 15 test in `tests/test_b_referee.py` coprono i sette casi di CLAUDE_CODE_B.md con backend simulato, nessuna chiamata a pagamento: 21 test nel progetto, 50 nel pacchetto `referee/` (intatto). Corretto un bug di encoding in `researcher.py`: lettura/scrittura senza `encoding="utf-8"` corrompeva i caratteri non-ASCII su Windows (cp1252). Invariante confermato dai test: nessuna combinazione di verdetti dei modelli produce ACCEPT, che resta un'approvazione umana firmata.
- 2026-09-26 ~13:55 CHECKPOINT (pre-compact): primo loop reale su Q5: Researcher ok (88), Referee fallito per ValidationError su entrambi i giudici → backend CLI ora salva output grezzi e ritenta una volta con l'errore; re-run del Referee in corso. Prossimo: merge dei branch dei collaboratori, test, conflitti, loop end-to-end per parte.
- 2026-09-26 ~13:35: ciclo end-to-end `researcher/loop.py` (test mock verdi) + ricerca arXiv `literature.py` con campo `literature_position` obbligatorio nel tentativo. Creative NON collegato per scelta: arriva dal team; il loop ha il punto d'aggancio `--creative-cmd`. arXiv non ha letteratura sul problema 2 (ricerca fatta, esito vuoto).
- 2026-09-26 ~13:15: integrato il Referee di gabundos (branch gabundos-patch-1, zip) in `referee/`; ponte `researcher/bridge_referee.py` testato offline. Il branch NON è stato mergiato (base vecchia, cancellerebbe runs/).
- 2026-09-26: MVP Researcher (Persona 1 del brief) costruito e testato: `researcher/`, schemi in `shared/schemas/`, 4 test mock + 2 run reali via CLI. Repo reso privato.
- 2026-09-26: letteratura P1 (Bilyk–Matzke, letta): solo il piano è risolto; P3/P5/P6 e '6 in R^4' aperti al 2018. Fonti in problema-1/fonti/.
- 2026-09-26: ricerca web sui harness (tools/HARNESS_RICERCA.md): evolutivo solo per costruzioni; Lean non fattibile; LLM-giudice solo come critico.
- 2026-09-26: autoresearch di Karpathy NON integrato come repo (dominio ML/GPU); adottato solo il pattern in tools/autoloop.py.
