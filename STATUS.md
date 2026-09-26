# STATUS — Proof Pursuit

Tempo totale: 7 ore. Tempo rimanente: (da indicare)
Ultimo aggiornamento: 2026-09-26, inizializzazione

Legenda stati: non iniziato · in analisi · in corso · parziale · bozza pronta · revisionato · bloccato

## Riepilogo colonne

| Problema | Titolo | Celle con evidenza | Stato complessivo |
|---|---|---|---|
| 1 | Angles between lines (Fejes Tóth), 32 pt | 0/6 | in corso (tutte le 6 parti ricevute) |
| 2 | Uphill paths on the hypercube, 32 pt | 0/6 | in analisi (tutte le 6 parti ricevute) |
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
| 1 | $U(Q_3)$, $U(Q_4)$ + etichettature (1 pt, checked) | in analisi | $Q_3$ brute-force fattibile; $Q_4$ serve B&B |
| 2 | $U(Q_5)$ (2 pt, checked) | in analisi | harness discreto |
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
- 2026-09-26: letteratura P1 (Bilyk–Matzke, letta): solo il piano è risolto; P3/P5/P6 e '6 in R^4' aperti al 2018. Fonti in problema-1/fonti/.
- 2026-09-26: ricerca web sui harness (tools/HARNESS_RICERCA.md): evolutivo solo per costruzioni; Lean non fattibile; LLM-giudice solo come critico.
- 2026-09-26: autoresearch di Karpathy NON integrato come repo (dominio ML/GPU); adottato solo il pattern in tools/autoloop.py.
