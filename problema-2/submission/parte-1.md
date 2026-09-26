# Problema 2 — Parte 1 (C1) — bozza di consegna

**Stato dichiarato: PARZIALE.** Risolta la metà $U(Q_3)$ con valore, etichettatura esplicita e prova completa
(a mano + calcolo esaustivo). La metà $U(Q_4)$ NON è ancora trattata.

## 1. Risultato e ambito
$U(Q_3) = 14$. Etichettatura ottima (ordine crescente di etichetta; posizione $i$ della stringa = coordinata $i$;
la convenzione è irrilevante perché le permutazioni di coordinate sono automorfismi di $Q_3$):
`000, 100, 010, 110, 101, 011, 001, 111`.

## 2. Dimostrazione
## Result

$$U(Q_3) = 14.$$

An optimal labelling, as the list of the 8 vertices in increasing label order (string position $i$ = coordinate $i$; the convention is irrelevant for the count since $\mathrm{Aut}(Q_3)$ contains all coordinate permutations):

$$\texttt{000},\ \texttt{100},\ \texttt{010},\ \texttt{110},\ \texttt{101},\ \texttt{011},\ \texttt{001},\ \texttt{111}$$

i.e. $f(000)=1,\ f(100)=2,\ f(010)=3,\ f(110)=4,\ f(101)=5,\ f(011)=6,\ f(001)=7,\ f(111)=8$.

## Notation and the counting identity

For a labelling $f$ of a graph $G$, orient every edge from the smaller to the larger label; this gives an acyclic orientation. Write $u \to v$ if $uv\in E$ and $f(u)<f(v)$, and $\deg^-(v)=\#\{u: u\to v\}$. Let $p(v)$ be the number of uphill paths whose last vertex is $v$.

**Lemma 1 (recursion).** $p(v) = [\,v \text{ is a valley}\,] + \sum_{u\to v} p(u)$, and the total number of uphill paths is $\sum_v p(v)$.

*Proof.* An uphill path ending at $v$ has $k=1$ (then it is $(v)$ and $v$ must be a valley; conversely a valley gives exactly this one path) or $k\ge2$; in the latter case deleting $v$ gives an uphill path ending at $v_{k-1}$ with $v_{k-1}\to v$, and conversely appending $v$ to any uphill path ending at some $u$ with $u\to v$ gives an uphill path ending at $v$ (the label condition $f(u)<f(v)$ is exactly $u\to v$). These correspondences are bijective, and the sets for different $u$ are disjoint (they differ in the penultimate vertex). Every uphill path has a unique last vertex, hence the total is $\sum_v p(v)$. $\square$

## Upper bound: the labelling above has exactly 14 uphill paths

Neighbours in $Q_3$: flip one coordinate. Compute $p$ in increasing label order using Lemma 1:

| vertex | label | lower neighbours | $p$ |
|---|---|---|---|
| 000 | 1 | none (valley) | 1 |
| 100 | 2 | 000 | 1 |
| 010 | 3 | 000 | 1 |
| 110 | 4 | 100, 010 | 1+1 = 2 |
| 101 | 5 | 100 (001 has label 7, 111 has 8) | 1 |
| 011 | 6 | 010 (001 has 7, 111 has 8) | 1 |
| 001 | 7 | 000, 101, 011 | 1+1+1 = 3 |
| 111 | 8 | 110, 101, 011 | 2+1+1 = 4 |

Only 000 is a valley (every other vertex has a lower neighbour, as the table shows). Total $=1+1+1+2+1+1+3+4 = 14$. Hence $U(Q_3)\le 14$.

## Lower bound (hand proof): no labelling of $Q_3$ has $\le 13$ uphill paths

**Lemma 2.** For every labelling of any graph and every vertex $v$: $p(v)\ge 1$, and $p(v)\ge \deg^-(v)$.

*Proof.* Starting from $v$, repeatedly move to a neighbour with smaller label while one exists; labels strictly decrease so this stops, at a valley $v_1$. Reversing the walk gives an uphill path ending at $v$, so $p(v)\ge1$. Applying this to each $u$ with $u\to v$ gives $p(u)\ge1$, so by Lemma 1 $p(v)\ge\sum_{u\to v}p(u)\ge\deg^-(v)$. $\square$

**Corollary 3.** Total $\ \ge \sum_v \max(1,\deg^-(v)) = \#\{\text{valleys}\} + \sum_{v \text{ not valley}}\deg^-(v) = \#\{\text{valleys}\} + |E|$, since valleys are exactly the vertices with $\deg^-=0$ and $\sum_v\deg^-(v)=|E|$ (each edge has exactly one head). For $Q_3$, $|E|=12$ and the vertex with label 1 is always a valley, so the total is $\ge 13$.

**Proposition 4.** The total is never exactly 13 for $Q_3$; hence $U(Q_3)\ge 14$.

*Proof.* Suppose a labelling has total 13. Then every inequality in Corollary 3 is an equality: (a) there is exactly one valley, and (b) for every non-valley $v$, $p(v)=\deg^-(v)$, i.e. $\sum_{u\to v}p(u)=\deg^-(v)$ with each $p(u)\ge1$, so $p(u)=1$ for every $u\to v$. By Lemma 2, $p(u)=1$ forces $\deg^-(u)\le1$.

Let $x$ be the vertex with label 8. All 3 neighbours of $x$ are lower, so $\deg^-(x)=3$ and by (b) every $a\in N(x)$ has $\deg^-(a)\le1$.

Let $y$ be the vertex with label 7. At most one neighbour of $y$ (namely $x$) is higher, so $\deg^-(y)\ge2$. If $y\in N(x)$ we would have $\deg^-(y)\le1$, a contradiction; so $y\notin N(x)$, $y\ne x$, hence $y$ is the antipode $\bar x$ of $x$ (in $Q_3$ the only vertex at distance 3). Then $N(y)$ is the set of the 3 vertices at distance 2 from $x$, all lower than $y$, so $\deg^-(y)=3$ and by (b) every $b\in N(y)$ has $\deg^-(b)\le1$.

$N(x)\cup N(y)$ is the set $S$ of the 6 vertices other than $x,y$. Count edges inside $S$: $Q_3$ has 12 edges, 3 are incident to $x$, 3 to $y$, and $xy$ is not an edge, so exactly $12-6=6$ edges have both ends in $S$. Each such edge is oriented towards its higher endpoint, which lies in $S$, so $\sum_{s\in S}\deg^-(s)\ge 6$. But each $s\in S$ has $\deg^-(s)\le1$, so $\sum_{s\in S}\deg^-(s)\le6$; therefore $\deg^-(s)=1$ for every $s\in S$. Thus no vertex of $S$ is a valley; $x$ and $y$ are not valleys either ($\deg^-\ge2$). So the labelling has no valley, contradicting the fact that the vertex with label 1 is a valley (all its neighbours have larger labels). $\square$

Combining: $U(Q_3)=14$, attained by the labelling above.

## Independent confirmation: exhaustive exact computation

Script `q3_esaustivo.py` (saved in `runs/p2_q3/sandbox/` and copied to `problema-2/certificati/`) enumerates **all** $8!=40320$ bijections $V(Q_3)\to\{1,\dots,8\}$ (`itertools.permutations`), with vertices encoded as integers $0..7$ (bit $i$ = coordinate $i$) and adjacency = XOR with a single bit. For each labelling it computes the number of uphill paths in two independent ways — (i) an explicit recursive DFS that enumerates every uphill path from every valley, (ii) the DP of Lemma 1 processed in increasing label order — and `assert`s that the two agree. All arithmetic is Python integers (exact; rigor = `exact`).

Output (Python 3.14.7, wall-clock 0.36 s):

```
etichettature esaminate: 40320
U(Q_3) = 14; etichettature ottime: 7104
distribuzione (cammini -> numero etichettature): [(14, 7104), (16, 14112), (17, 6720), (18, 4704), (19, 576), (20, 3648), (21, 1920), (22, 480), (23, 192), (24, 768), (26, 96)]
prima etichettatura ottima (ordine crescente di etichetta): ['000', '100', '010', '110', '101', '011', '001', '111']
```

The distribution confirms Proposition 4 (no labelling with 13, and also none with 15) and Corollary 3 (none below 13). Reproduce with `.venv/bin/python problema-2/certificati/q3_esaustivo.py`. A second script `verifica_etichettatura_q3.py` checks only the submitted labelling (bijection check, valleys, per-vertex $p$, total 14) and prints the table above.

## 3. Verifica: istruzioni, dipendenze, tempi
Tre programmi indipendenti, solo Python 3 standard (interi esatti), ciascuno enumera tutte le $8!=40320$ etichettature:
- `problema-2/certificati/q3_esaustivo.py` — DFS esplicita dei cammini + programmazione dinamica di Lemma 1,
  con `assert` di uguaglianza su ogni etichettatura. Tempo misurato: 0.37 s.
- `problema-2/certificati/q3_verifica_indipendente.py` — scritto separatamente, metodo diverso: costruzione
  esplicita livello per livello di tutte le sequenze crescenti a partire dalle valli. Tempo misurato: 0.20 s.
- `problema-2/certificati/verifica_etichettatura_q3.py` — controlla la sola etichettatura consegnata (biiezione,
  valli, $p(v)$ per vertice, totale 14).
Comando: `python3 problema-2/certificati/q3_verifica_indipendente.py` (e analoghi). Python 3.14.7, macOS.
Tutti riportano: minimo 14, 7104 etichettature ottime, distribuzione senza valori 13 e 15.

## 4. Fonti e contributo
Nessuna fonte esterna usata. L'argomento del lower bound generalizza l'idea di IMO 2022 P6 (ogni vertice è fine
di almeno un cammino; $p(v)\ge\deg^-(v)$), aggiungendo l'ostruzione specifica di $Q_3$ (Proposizione 4).
Prova prodotta dal Researcher automatico (Claude Fable 5.1, run `runs/p2_q3/attempts/attempt_001.json`) e
revisionata a mano passo per passo; verifica numerica indipendente scritta a parte.

## 5. Limiti e parti irrisolte
- $U(Q_4)$ non determinato: $16!$ etichettature non sono enumerabili direttamente; serve riduzione per simmetria
  ($|\mathrm{Aut}(Q_4)|=384$) o branch-and-bound con il bound $|E|+\#\text{valli}$ e l'ostruzione sui vertici alti.
- Osservazione utile: $U(Q_3)=|E|+2$, non $|E|+1$; l'eccesso nasce dal vertice massimo e dal suo antipodo.
