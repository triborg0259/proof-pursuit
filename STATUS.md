# STATUS — Proof Pursuit

Tempo totale: 7 ore. Tempo rimanente: 5 ore (dichiarato alle ~11:45 del 2026-09-26 ⇒ fine ~16:45)
Ultimo aggiornamento: 2026-09-26, inizializzazione

Legenda stati: non iniziato · in analisi · in corso · parziale · bozza pronta · revisionato · bloccato

## Riepilogo colonne

| Problema | Titolo | Celle con evidenza | Stato complessivo |
|---|---|---|---|
| 1 | Angles between lines (Fejes Tóth), 32 pt | 0/6 | in corso (tutte le 6 parti ricevute) |
| 2 | Uphill paths on the hypercube, 32 pt | 1/6 | in corso (C1 revisionata) |
| 3 | Bulgarian solitaire, 32 pt | 0/6 | in analisi (tutte le 6 parti ricevute) |
| 4 | Disjoint classes / gcd of moduli, 32 pt | 0/6 | in analisi (tutte le 6 parti ricevute) |

## Problema 1 — Lines / somma di angoli

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | Prova: $S \le \frac{\pi}{2}\lfloor N^2/4\rfloor$ in $\mathbb{R}^2$ (1 pt, Judged) | in corso | E1: max numerico = target per N≤10; prova via argomento di Crofton abbozzata (note.md, E), da scrivere e revisionare; definizione di $S$ confermata dal preambolo |
| 2 | Prova lemma di ortogonalità su catene di versori (2 pt, Judged) | in corso | prova per induzione abbozzata (note.md, F); casi m=2,3 verificati a mano |
| 3 | $N=d+1$: $S\le(\binom{d+1}{2}-1)\pi/2$ (3 pt) | in analisi | triage in note.md; dipende dal lemma P2 |
| 4 | 5 rette in $\mathbb{R}^3$ ($4\pi$), 6 in $\mathbb{R}^4$ ($13\pi/2$) (5 pt) | in analisi | triage; possibile via P5 o calcolo rigoroso |
| 5 | $N=d+2$: $S\le(\binom{d+2}{2}-2)\pi/2$ (8 pt) | in analisi | triage |
| 6 | Congettura completa, open (13 pt) | in analisi | triage; solo ricerca controesempi / famiglie infinite |

## Problema 2 — Uphill paths on the hypercube

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | $U(Q_3)$, $U(Q_4)$ + etichettature (1 pt, checked) | revisionato | $U(Q_3)=14$, $U(Q_4)=34$: prove a mano rilette passo per passo + verifiche esatte indipendenti; bozza in submission/parte-1.md |
| 2 | $U(Q_5)$ (2 pt, checked) | bozza pronta | $U(Q_5)=88$: riduzione a (★) riletta a mano + 3 enumerazioni concordi; etichettatura verificata; verdetto Referee automatico in corso |
| 3 | $U(Q_6)$ (3 pt, checked) | in analisi | |
| 4 | $U(Q_7)$, $U(Q_8)$ (5 pt, checked) | in analisi | |
| 5 | Migliorare $2368\le U(Q_9)\le2400$ (8 pt) | in analisi | via realistica: etichettatura $\le2399$ |
| 6 | $U(Q_9)$ esatto con prove (13 pt, open) | in analisi | |

## Problema 3 — Bulgarian solitaire

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | Cicliche e numero di cicli, prove (1 pt) | in analisi | struttura nota (collane), prova da scrivere |
| 2 | $D_B(T_k)$ esatto (2 pt) | in analisi | atteso $k^2-k$ (Igusa/Etienne, da verificare) |
| 3 | Bound $k^2-2k-1$ e $D_B(T_k-1)$ (3 pt) | in analisi | |
| 4 | $D_B(T_{k-1}+1)$ (5 pt) | in analisi | |
| 5 | $D_B(T_{k-1}+2)$ (8 pt) | in analisi | |
| 6 | $D_B(n)$ per ogni $n$ (13 pt, open) | in analisi | |

## Problema 4 — Disjoint congruence classes, large gcd

| Parte | Richiesta | Stato | Evidenza |
|---|---|---|---|
| 1 | $k=3$ (1 pt) | in analisi | prova a mano abbozzata (parità) |
| 2 | $k=4$ (2 pt) | in analisi | schema "clique per primo" abbozzato |
| 3 | $k\le8$ (3 pt) | in analisi | riduzione a insieme finito abbozzata (note.md) |
| 4 | $k\le12$ + report 9–16 (5 pt) | in analisi | |
| 5 | boundary certificato + $k=24,30$ (8 pt) | in analisi | richiede 2 implementazioni indipendenti |
| 6 | oltre (13 pt, open) | in analisi | |

## Registro decisioni e ostacoli
- 2026-09-26 ~14:30: Referee B consolidato su `feature/referee-b` DENTRO `bridge_referee.py`, senza creare un secondo ponte: la prima versione (pacchetto `referees/` + `adapter_b.py`) duplicava `referee/referees/` ed è stata cancellata. Tre migliorie portate nel ponte: (1) un `claims_used` senza riscontro diventa un claim `dep_k` del candidato invece di sparire, così il Referee ne valuta la provenienza; (2) l'enunciato della cella si cerca anche nella riga `Cell N:` di `problem.md` e in mancanza totale ci si ferma invece di usare un segnaposto; (3) le regole vengono da `shared/competition_rules.example.json` (segnaposto, NON il regolamento ufficiale) invece che da un dizionario nel codice. 15 test in `tests/test_b_referee.py` coprono i sette casi di CLAUDE_CODE_B.md con backend simulato, nessuna chiamata a pagamento: 21 test nel progetto, 50 nel pacchetto `referee/` (intatto). Corretto un bug di encoding in `researcher.py`: lettura/scrittura senza `encoding="utf-8"` corrompeva i caratteri non-ASCII su Windows (cp1252). Invariante confermato dai test: nessuna combinazione di verdetti dei modelli produce ACCEPT, che resta un'approvazione umana firmata.
- 2026-09-26 ~13:55 CHECKPOINT (pre-compact): primo loop reale su Q5: Researcher ok (88), Referee fallito per ValidationError su entrambi i giudici → backend CLI ora salva output grezzi e ritenta una volta con l'errore; re-run del Referee in corso. Prossimo: merge dei branch dei collaboratori, test, conflitti, loop end-to-end per parte.
- 2026-09-26 ~13:35: ciclo end-to-end `researcher/loop.py` (test mock verdi) + ricerca arXiv `literature.py` con campo `literature_position` obbligatorio nel tentativo. Creative NON collegato per scelta: arriva dal team; il loop ha il punto d'aggancio `--creative-cmd`. arXiv non ha letteratura sul problema 2 (ricerca fatta, esito vuoto).
- 2026-09-26 ~13:15: integrato il Referee di gabundos (branch gabundos-patch-1, zip) in `referee/`; ponte `researcher/bridge_referee.py` testato offline. Il branch NON è stato mergiato (base vecchia, cancellerebbe runs/).
- 2026-09-26: MVP Researcher (Persona 1 del brief) costruito e testato: `researcher/`, schemi in `shared/schemas/`, 4 test mock + 2 run reali via CLI. Repo reso privato.
- 2026-09-26: letteratura P1 (Bilyk–Matzke, letta): solo il piano è risolto; P3/P5/P6 e '6 in R^4' aperti al 2018. Fonti in problema-1/fonti/.
- 2026-09-26: ricerca web sui harness (tools/HARNESS_RICERCA.md): evolutivo solo per costruzioni; Lean non fattibile; LLM-giudice solo come critico.
- 2026-09-26: autoresearch di Karpathy NON integrato come repo (dominio ML/GPU); adottato solo il pattern in tools/autoloop.py.
