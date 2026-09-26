# Problema 3 — Parte 1 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 1 (C1) — Cyclic partitions and cycles

**Punteggio:** 1 point · **Valutazione:** Judged

First, the long-run behaviour: which partitions repeat under the shift, and how they fall into cycles.
Let $n = T_k$. Prove that for every partition $\lambda$ of $n$ there is an $i$ with $B^i(\lambda) = \delta_k$,
and that $\delta_k$ is the only cyclic partition of $n$. Then let $n$ be arbitrary of rank $k$, say
$n = T_{k-1} + r$ with $1 \le r \le k$: determine all cyclic partitions of $n$, and determine the number of
distinct cycles of $B$ on the partitions of $n$. Prove both.

**Cosa consegniamo.** Descrizione completa della struttura (dimostrazione in corso di stesura dal Researcher): partizioni cicliche = scala $\delta_{k-1}$ più $r$ carte extra su $r$ delle $k$ posizioni $0,\dots,k-1$; i cicli corrispondono alle collane binarie con $k$ perle di cui $r$ nere; numero di cicli $\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d}$.

## 2. Dimostrazione
**Rappresentazione.** Una partizione di $n=T_{k-1}+r$ si scrive come diagramma di Young; l'operazione $B$ sposta ogni cella lungo una diagonale. Le partizioni della forma $\delta_{k-1}$ + indicatore $\varepsilon\in\{0,1\}^k$ (una carta extra in posizione $i$ significa parte $i+1$ invece di $i$, con posizione $0$ = nuova parte 1) sono chiuse sotto $B$, che agisce su $\varepsilon$ come rotazione ciclica in $\mathbb Z_k$; quindi sono tutte cicliche e i cicli sono le orbite della rotazione, cioè le collane, contate dal lemma di Burnside. **Da completare:** (i) che ogni partizione entra in questo insieme (potenziale = somma degli scarti dalla scala, strettamente decrescente fuori dall'insieme); (ii) che nessun'altra partizione è ciclica (segue da (i)). Per $n=T_k$ ($r=k$ oppure $r=0$) l'unica collana è tutta nera/bianca: unica ciclica $\delta_k$.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Researcher attempt_001, code_1 (python, exact): Sanity check (not part of the proof): exact brute-force enumeration of all partitions of n for n = 1..60, computing the 
- Researcher attempt_002, code_1 (python, exact): Exact brute-force check for n=1..40: cyclic partitions equal S_{k,r}; number of cycles equals the necklace formula; for 

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); solo abstract letto.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); solo abstract letto.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); solo abstract letto.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); solo abstract letto.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); solo abstract letto.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); solo abstract letto.
Brandt (1982) caratterizza le partizioni cicliche (citato nei survey Drensky [1503.00885] e Meštrović [2607.17194]); riproduciamo l'argomento per esteso, come ammesso dalle regole.

## 5. Limiti e parti irrisolte
Stesura completa dei punti (i)–(ii).
