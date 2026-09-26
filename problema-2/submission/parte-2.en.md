# Problem 2 — Part 2 (C2) — submission draft

**Declared status: REVIEWED (ready for submission).** Value $U(Q_5)=88$ with an explicit labelling; lower bound by
reduction to a finite statement (★) refuted by exhaustive enumeration (three concordant implementations, one independent
per method). Automatic Referee: **READY_FOR_HUMAN** (judge A, mathematics: PASS on both directions in three independent
runs; judge B, evidence: PASS, with INFO notes only, after the trusted re-execution of the code by the
orchestrator). Human review of the reduction: done lemma by lemma (STATUS.md). Final approval remains human.

## 1. Result and scope
$U(Q_5) = 88 = |E(Q_5)| + 8$. Optimal labelling (increasing label order; position $i$ of the string =
coordinate $i$; the convention is irrelevant because coordinate permutations are automorphisms of $Q_5$), with 8 valleys:
`00000, 11110, 11001, 10101, 01101, 10011, 01011, 00111` are labels 1–8 (the valleys), followed by the leaves and the
peaks as in the complete list in §2 (upper bound table). The complete 32-element list is produced and
verified by `certificati/costruzione_88.py` and `certificati/verifica_dfs_88.py`.

## 2. Proof
*(Text of the Researcher's attempt `runs/p2_q5/attempts/attempt_001.json`, re-read lemma by lemma by the team; the
computational verifications were re-executed by the orchestrator in `runs/p2_q5/verifica/attempt_001/`.)*


# $U(Q_5) = 88$

**Conventions.** $V(Q_5)=\{0,1\}^5$, $u\sim v$ iff they differ in exactly one coordinate; $|V|=32$, $|E|=80$, every vertex has degree $5$. In a 0/1 string the $i$-th character from the left is coordinate $i$ (irrelevant for the count: coordinate permutations are automorphisms). For a labelling $f$, orient each edge from the smaller to the larger label ($u\to v$ iff $uv\in E$, $f(u)<f(v)$); $\deg^-(v)=\#\{u:u\to v\}$, $\deg^+(v)=\#\{w:v\to w\}$, $\deg^-(v)+\deg^+(v)=5$. Let $p(v)$ be the number of uphill paths whose last vertex is $v$. A *valley* is a vertex with $\deg^-=0$; a *peak* is a vertex with $\deg^+=0$. The vertex with label $1$ is a valley, so $v:=\#\text{valleys}\ge1$.

## 0. Preliminaries (restated with proof for self-containedness)

**Lemma 1 (recursion).** $p(v)=[v\text{ valley}]+\sum_{u\to v}p(u)$ and the total number of uphill paths is $T=\sum_v p(v)$.

*Proof.* An uphill path ending at $v$ has length $1$ — then it is $(v)$ and $v$ is a valley; conversely a valley gives exactly this path — or length $\ge2$; deleting $v$ gives an uphill path ending at its penultimate vertex $u$ with $u\to v$; conversely appending $v$ to an uphill path ending at $u$ with $u\to v$ gives an uphill path ending at $v$ (the increasing condition is exactly $f(u)<f(v)$). These maps are mutually inverse and different $u$ give disjoint sets. Every uphill path has a unique last vertex. $\square$

**Lemma 2.** For every vertex $v$: $p(v)\ge1$, and $p(v)\ge\deg^-(v)$.

*Proof.* From $v$ move repeatedly to a neighbour with smaller label while one exists; labels strictly decrease, so this stops at a valley; the reversed walk is an uphill path ending at $v$. Hence $p(v)\ge1$ for all $v$, and by Lemma 1, $p(v)\ge\sum_{u\to v}p(u)\ge\deg^-(v)$. $\square$

## 1. The excess identity

Define the **excess** $X:=\sum_{(u\to w)\in E}\bigl(p(u)-1\bigr)$ (sum over all $80$ oriented edges). By Lemma 2 every term is $\ge0$.

**Lemma 3.** $T=|E|+v+X = 80+v+X$.

*Proof.* By Lemma 1, $T=\sum_v p(v)=v+\sum_{w}\sum_{u\to w}p(u)=v+\sum_{(u\to w)\in E}\bigl(1+(p(u)-1)\bigr)=v+|E|+X$, since each edge is counted once, at its head. $\square$

Grouping the terms of $X$ by tail: $X=\sum_u \deg^+(u)\,(p(u)-1)$. Call $u$ **heavy** if $\deg^+(u)\ge1$ and $p(u)\ge2$; let $H$ be the set of heavy vertices and $c(u):=\deg^+(u)(p(u)-1)$ its contribution, so $X=\sum_{u\in H}c(u)$. Vertices with $p=1$ are called **light**.

**Lemma 4 (structure of light vertices).** If $p(u)=1$ then either $u$ is a valley or $\deg^-(u)=1$ and its unique in-neighbour is light. Consequently, for any set $L$ of light vertices, the subgraph of $Q_5$ induced by $L$ is acyclic.

*Proof.* By Lemma 2, $\deg^-(u)\le p(u)=1$. If $\deg^-(u)=1$ with in-neighbour $u'$, Lemma 1 gives $1=p(u)=p(u')$. For the second claim: a cycle inside $L$ contains a vertex of maximal label, which has two in-neighbours on the cycle, contradicting $\deg^-\le1$. $\square$

**Lemma 5 (every heavy vertex costs at least 3).** For every heavy $u$, $c(u)\ge3$. Moreover, writing $i=\deg^-(u)$ (so $\deg^+(u)=5-i$, $1\le i\le4$ since $\deg^+\ge1$ and $p\ge2$ excludes valleys):
- if $i=1$: $p(u)=p(u')\ge2$ for the in-neighbour $u'$, which is then itself heavy ($\deg^+(u')\ge1$ because $u'\to u$), and $c(u)=4(p(u)-1)\ge4$;
- if $i=2$: $c(u)=3(p(u)-1)\ge3$, with equality iff $p(u)=2$ iff both in-neighbours are light;
- if $i=3$: $c(u)=2(p(u)-1)\ge4$ (as $p(u)\ge3$), with equality iff all three in-neighbours are light;
- if $i=4$: $c(u)=p(u)-1\ge3$, with equality iff all four in-neighbours are light.

*Proof.* Direct from Lemma 2 ($p(u)\ge i$) and Lemma 1 ($p(u)=\sum_{u'\to u}p(u')$ with each $p(u')\ge1$; equality $p(u)=i$ iff every in-neighbour has $p=1$). Note also: if an in-neighbour $u'$ of a heavy $u$ has $p(u')\ge2$ then $u'$ is heavy (it has $\deg^+\ge1$). $\square$

**Corollary 6.** $X\in\{0\}\cup[3,\infty)$, and $X\le 7$ forces $|H|\le2$.

**Lemma 7 (in-degree count).** Let $P$ be the set of peaks, $q=|P|$, $s_H=\sum_{u\in H}\deg^-(u)$. If every non-heavy non-peak vertex is light (which holds automatically for every vertex with $\deg^+\ge1$ that is not heavy, by definition of heavy), then
$$4q=48+v+|H|-s_H .$$

*Proof.* Peaks have $\deg^-=5$; no peak is heavy (heavy needs $\deg^+\ge1$) and no valley is heavy. The vertices outside $P\cup H$ are light: valleys ($\deg^-=0$, $v$ of them) and light non-valleys ($\deg^-=1$ by Lemma 4, $32-q-|H|-v$ of them). Summing in-degrees, $80=\sum_u\deg^-(u)=5q+s_H+(32-q-|H|-v)$, i.e. $4q=48+v+|H|-s_H$. $\square$

Also note: **peaks form an independent set** (if two peaks were adjacent, the one with the smaller label would have $\deg^+\ge1$).

## 2. Case analysis: every labelling with $T\le87$ has one of four structures

Assume $T\le87$, i.e. (Lemma 3) $v+X\le7$ with $v\ge1$, so $X\le6$. By Corollary 6, $X\in\{0,3,4,5,6\}$ and $|H|\le2$.

**Case $|H|=2$.** Then $X\ge6$, so $X=6$, $v=1$, and both heavy vertices have $c=3$; by Lemma 5 each has $(\deg^-,p)\in\{(2,2),(4,4)\}$, so $s_H\in\{4,6,8\}$ and Lemma 7 gives $4q=48+1+2-s_H\in\{47,45,43\}$, none divisible by $4$. **Impossible.**

**Case $|H|=0$.** Then $X=0$, $T=80+v$, and Lemma 7 gives $4q=48+v$, so $v\equiv0\pmod 4$; with $T\le87$ this forces $v=4$, $q=13$, $T=84$. Every non-peak vertex is light; so $F:=V\setminus P$ (19 vertices) induces an acyclic subgraph (Lemma 4), and $P$ is an independent set of size $13$. **(Structure A.)**

**Case $|H|=1$, $H=\{u\}$.** Then $X=c(u)\le6$. By Lemma 5, if some in-neighbour of $u$ had $p\ge2$ it would be heavy, contradicting $|H|=1$; hence all in-neighbours of $u$ are light and $p(u)=\deg^-(u)=:i$; $i=1$ is excluded (it needs a heavy in-neighbour). So $(i,c(u))\in\{(2,3),(3,4),(4,3)\}$, and Lemma 7 with $|H|=1$, $s_H=i$ gives $4q=49+v-i$:
- $i=2$: $4q=47+v$, $v\equiv1\pmod4$, and $v+X=v+3\le7$ gives $v=1$, $q=12$, $T=84$. **(Structure B.)**
- $i=3$: $4q=46+v$, $v\equiv2\pmod4$, $v+4\le7$ gives $v=2$, $q=12$, $T=86$. **(Structure C.)**
- $i=4$: $4q=45+v$, $v\equiv3\pmod4$, $v+3\le7$ gives $v=3$, $q=12$, $T=86$. **(Structure D.)**

In each of B, C, D: the out-neighbours $w$ of $u$ satisfy $p(w)\ge p(u)\ge2$ (Lemma 1), so if such a $w$ had $\deg^+(w)\ge1$ it would be heavy; hence **all out-neighbours of $u$ are peaks**. The in-neighbours of $u$ are non-peaks. All vertices other than $u$ and the peaks are light, so by Lemma 4 the set $L:=V\setminus(P\cup\{u\})$ induces an acyclic subgraph; $P$ is an independent set of size $12$ and $u\notin P$.

**Summary.** If $T\le 87$ then there exist an independent set $I\subseteq V(Q_5)$ and a vertex $u\notin I$ such that $V\setminus(I\cup\{u\})$ induces an acyclic subgraph, where either $|I|=12$ (structures B, C, D with $I=P$), or $|I|=13$ and $V\setminus I$ is acyclic (structure A) — in which case, choosing any $u_0\in I$ and $I'=I\setminus\{u_0\}$, the pair $(I',u_0)$ has $|I'|=12$, $I'$ independent, $u_0\notin I'$, and $V\setminus(I'\cup\{u_0\})=V\setminus I$ acyclic. So in all cases:

> **(★)** there is an independent set $I$ of $Q_5$ with $|I|=12$ and a vertex $u\notin I$ such that $Q_5-(I\cup\{u\})$ is a forest.

## 3. Exact finite verification: (★) never holds in $Q_5$

**Reduction.** The maps $x\mapsto x\oplus t$ are automorphisms of $Q_5$ and act transitively on vertices, and (★) is invariant under automorphisms. Hence it suffices to check all independent $12$-sets $I$ containing the vertex $00000$ and all $u\notin I$.

**Computation 1** (`verifica_q5_indipendenti.py`, exact integer arithmetic): backtracking enumerates all independent sets of size $12$ containing $0$ in increasing vertex order (a vertex may be added iff it is neither in the set nor adjacent to it), and for each of the $20$ vertices $u\notin I$ tests acyclicity of the induced subgraph on the $19$ remaining vertices by the exact criterion *#edges = #vertices − #components*. Output: `insiemi indipendenti di taglia 12 contenenti 0: 1377; coppie (I,u) esaminate: 27540; complementi aciclici trovati: 0; tempo 0.24s`.

**Computation 2** (`verifica_q5_bipartita.py`, independent method, no symmetry reduction): every independent set is $A\cup B$ with $A$ a subset of the 16 even-weight vertices and $B$ a subset of the odd-weight vertices not adjacent to $A$; the script scans all $2^{16}$ bitmasks $A$, all $B$ of size $12-|A|$, and tests acyclicity by union–find over the edge list. Output: `insiemi indipendenti di taglia 12 (tutti): 3672; coppie (I,u) esaminate: 73440; complementi aciclici: 0; tempo 0.39s`. Consistency: $3672\cdot 12/32=1377$, as vertex-transitivity predicts.

Hence (★) is false, so no labelling of $Q_5$ has $T\le87$:
$$U(Q_5)\ge 88.$$

(The counts also make the impossibility of the $X=0$, $v=4$ structure transparent by hand: an independent $12$- or $13$-set turns out to lie in one parity class except for a few mixed sets, and any three even vertices contain two at distance $2$, which share two odd neighbours and thus close a $4$-cycle in the complement; but the proof relies only on the exhaustive check above.)

## 4. Upper bound: a labelling with exactly 88 uphill paths

Let $R=\{00000,11110\}$ and let $P$ be the $14$ even-weight vertices other than $R$. $P$ is independent (even-weight vertices are pairwise non-adjacent). The complement $F=R\cup\{\text{16 odd vertices}\}$ induces exactly the $10$ edges from $R$ to the odd vertices (the two vertices of $R$ are at distance $4$, so their neighbourhoods $\{10000,01000,00100,00010,00001\}$ and $\{01110,10110,11010,11100,11111\}$ are disjoint): $F$ is a forest with $18$ vertices, $10$ edges and $8$ components, namely the two stars centred at $R$ and the $6$ isolated odd vertices $11001,10101,01101,10011,01011,00111$.

Labelling (increasing label order; coordinate 1 on the left):

```
00000,11110,11001,10101,01101,10011,01011,00111,
10000,01000,00100,11100,00010,11010,10110,01110,00001,11111,
11000,10100,01100,10010,01010,00110,10001,01001,00101,11101,00011,11011,10111,01111
```

i.e. labels $1$–$2$: the star centres; $3$–$8$: the six isolated odd vertices; $9$–$18$: the ten star leaves; $19$–$32$: the fourteen peaks $P$.

*Count.* The $8$ vertices with labels $1$–$8$ have all neighbours higher (their $F$-neighbours, if any, are leaves labelled $9$–$18$; their other neighbours are in $P$): they are valleys, $p=1$. Each leaf (labels $9$–$18$) has exactly one lower neighbour, its star centre, so $p=1$. Each peak has all $5$ neighbours lower, all in $F$ with $p=1$, so $p=5$. Total $T=18\cdot1+14\cdot5=88$. Verified exactly by two independent scripts: `costruzione_88.py` (recursion of Lemma 1) and `verifica_dfs_88.py` (explicit DFS enumeration of all uphill paths from the $8$ valleys), both printing $88$ and the same $8$ valleys.

## 5. Conclusion

$U(Q_5)=88=|E|+8$, attained by the labelling in §4. Consistency checks (not part of the proof): the same Lemmas 3–7 for $Q_4$ give $c(u)\ge2$ and $3q=16+v$, reproducing $U(Q_4)=34$ with $v=2$; for $Q_3$ they reproduce $U(Q_3)=14$. The identity $T=80+v+X$ and the fact $X\in\{0\}\cup[3,\infty)$ were also sanity-checked on $200{,}000$ random labellings of $Q_5$ (`sanity_eccesso.py`; the smallest positive $X$ seen was $14$). Simulated annealing over labellings (`ricottura_q5.py`, 200k swap moves per seed, exact scoring) never went below $88$ in any seed run so far (evidence only).


## 3. Verification: instructions, dependencies, timings
Dependencies: standard Python 3, no packages. All scripts use exact integer arithmetic.
```
cd problema-2/certificati
python3 costruzione_88.py                 # costruisce l'etichettatura e conta 88 cammini (< 0.1 s)
python3 verifica_dfs_88.py                # conteggio indipendente per DFS esplicita (< 0.1 s)
python3 verifica_q5_indipendenti.py       # (★) confutata: 1377 insiemi con 0, 27540 coppie, 0 aciclici (0.47 s)
python3 verifica_q5_bipartita.py          # (★) confutata senza riduzione per simmetria: 3672 / 73440 / 0 (0.71 s)
python3 q5_stella_verifica_indipendente.py  # (★) confutata con metodo diverso (potatura delle foglie): 3672 / 73440 / 0 (0.40 s)
```
Timings measured on a laptop (trusted re-execution by the orchestrator, 2026-09-26). Code of the attempt:
- `code_1` (python, rigour `exact`): Exact count of uphill paths of a labelling of Q_d via the recursion p(v) = [valley] + sum of p over lower neighbours (shared module).
- `code_2` (python, rigour `exact`): Certificate 1 for the lower bound: enumerate all independent 12-sets of Q_5 containing vertex 0 (1377 sets, symmetry reduction by XOR translations) and, for eac
- `code_3` (python, rigour `exact`): Certificate 2 for the lower bound, independent method and no symmetry reduction: all independent 12-sets as A ∪ B (A ⊆ even class over all 2^16 bitmasks, B ⊆ od
- `code_4` (python, rigour `exact`): Builds the 88-path labelling (peaks = even vertices minus 00000, 11110) and counts exactly with the recursion: prints 88, the 8 valleys and the 32-vertex order.
- `code_5` (python, rigour `exact`): Independent verification of the submitted labelling by explicit DFS enumeration of every uphill path from each valley (string-based, no shared code): prints 88.
- `code_6` (python, rigour `exact`): Sanity check (evidence only, not part of the proof) of the identity T = 80 + #valleys + X and of X ∈ {0} ∪ [3,∞) on 200000 random labellings of Q_5 (all asserts
- `code_7` (python, rigour `float_exploration_only`): Simulated annealing over labellings (exploration only): best value found 88 in every seed run (seeds 0-5 in a first run, seeds 0-3 in a second run; 200k swap mo

## 4. Sources and contribution
- Counting lemma $p(v)=[\text{valle}]+\sum_{u\to v}p(u)$ and bound $\#\ge|E|+\#\text{valli}$: ours (part 1, re-proved here).
- Context: IMO 2022 P6 (grid), cited only as context; no result taken from the literature.
- Deterministic arXiv search (`runs/p2_q5/literature.json`, `problema-2/fonti/arxiv.json`): no work on uphill paths
  on the hypercube; the problem appears to be new. Contribution entirely ours.

## 5. Limits and unresolved parts
- Gaps declared by the Researcher in the attempt:
- The lower bound is computer-assisted at one point: statement (★) (no independent 12-set I and vertex u with Q_5 − (I ∪ {u}) acyclic) is proved by exhaustive enumeration, not by hand. The reduction to (★) is fully by hand; the enumeration is exact, covers the whole finite set (all 3672 independent 12-sets × 20 outside vertices), runs in < 1 s and was done by two methods. A hand proof of (★) was only sketched (parity-class argument), not written out.
- In Lemma 7 / §2 I use that every non-peak, non-heavy vertex is light; this is immediate from the definitions (a vertex with deg^+ ≥ 1 and p ≥ 2 is heavy by definition) but the Referee should check that no case escapes: valleys (p=1), peaks (deg^+=0), heavy, light — these four classes cover V.
- The step 'out-neighbours of the unique heavy vertex u are peaks' (needed for nothing in the final finite check, since (★) only uses I independent of size 12 and u ∉ I) is included for completeness; the final reduction deliberately uses only the weaker necessary conditions, so any slip there does not affect the proof.
- Simulated annealing results are exploration only and play no role in the proof; the second SA run (20 seeds) was still running when this report was written (4 seeds completed, all at 88).
- Judge B classified all observations on sources and computations as INFO (context sources not loaded and not
  needed; Python version not recorded: 3.14, standard library; reproduced timings 0.44–0.71 s). In the first two runs
  the only MISSING point concerned the official rules, later passed verbatim from the preamble of the problem statement.
- The cell is "checked instantly" on the value: the residual risk is an error in the reduction to (★); for this reason the reduction
  was re-read by hand and (★) refuted by three different programs.
