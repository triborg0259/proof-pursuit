# Problema 3 — Parte 3 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 3 (C3) — A general upper bound

**Punteggio:** 3 points · **Valutazione:** Judged

Now the numbers strictly between two consecutive triangular numbers. Prove that for every $k \ge 4$ and every
non-triangular $n$ with $T_{k-1} < n < T_k$,
$$
D_B(n) \le k^2 - 2k - 1,
$$
and determine $D_B(T_k - 1)$ exactly. Determine also, for that $n$, which partitions attain the maximum.

**Cosa consegniamo.** Nessuna prova. Piano: tabella esatta di $D_B(n)$ per $n\le60$ con partizioni estremali, poi formula e prova.

## 2. Dimostrazione
Calcolo esatto sul grafo funzionale delle partizioni (interi, nessun errore numerico), con due implementazioni (partizioni come tuple; carte in posizione sul diagramma). Congettura da confermare: $D_B(T_k-1)$ e le estremali esplicite in $k$. Non eseguito nel tempo di gara.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Nessun codice ancora.

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); solo abstract letto.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); solo abstract letto.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); solo abstract letto.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); solo abstract letto.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); solo abstract letto.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); solo abstract letto.
Griggs–Ho (1998) probabilmente contengono il bound $k^2-2k-1$: da verificare, non letto.

## 5. Limiti e parti irrisolte
Tutto tranne il piano.
