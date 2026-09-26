# Problem 2 — Part 1 (C1) — submission draft

**Declared status: SOLVED (reviewed draft).** Both halves: $U(Q_3)=14$ and $U(Q_4)=34$, with value,
explicit labelling and complete hand proof; exact computations as confirmation.

## 1. Result and scope
$U(Q_3) = 14$ and $U(Q_4) = 34$.
Optimal labelling of $Q_4$ (increasing label order; two valleys, `0000` and `1111`):
`0000, 1111, 0111, 1101, 1110, 1011, 0001, 1000, 0010, 0100, 1001, 0110, 0011, 1010, 0101, 1100`.

For $Q_3$: optimal labelling (increasing label order; position $i$ of the string = coordinate $i$;
the convention is irrelevant because coordinate permutations are automorphisms of $Q_3$):
`000, 100, 010, 110, 101, 011, 001, 111`.

## 2. Proof
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

## 2b. Proof for $Q_4$

# $U(Q_4)=34$

**Conventions.** $V(Q_4)=\{0,1\}^4$, $u\sim v$ iff they differ in exactly one coordinate; $|V|=16$, $|E|=32$, every vertex has degree 4. In a 0/1 string the $i$-th character (from the left) is coordinate $i$; the convention is irrelevant for the count, since every coordinate permutation is an automorphism of $Q_4$ and automorphisms preserve the number of uphill paths (they map valleys to valleys and uphill paths to uphill paths bijectively when the labelling is transported). For a labelling $f$ orient each edge from the smaller to the larger label ($u\to v$ iff $uv\in E$, $f(u)<f(v)$); $\deg^-(v)=\#\{u:u\to v\}$, $\deg^+(v)=\#\{w: v\to w\}$, so $\deg^-(v)+\deg^+(v)=4$. Let $p(v)$ be the number of uphill paths whose last vertex is $v$.

## Preliminaries (verified claims, restated with proof for self-containedness)

**Lemma 1.** $p(v)=[v\text{ is a valley}]+\sum_{u\to v}p(u)$, and the total number of uphill paths is $\sum_v p(v)$.

*Proof.* An uphill path ending at $v$ either has length $1$ — then it is $(v)$ and $v$ is a valley, and conversely a valley $v$ gives exactly this path — or has length $\ge2$; deleting $v$ gives an uphill path ending at its penultimate vertex $u$, with $u\to v$, and conversely appending $v$ to an uphill path ending at $u$ with $u\to v$ gives an uphill path ending at $v$ (the increasing condition is exactly $f(u)<f(v)$). These maps are mutually inverse, and different $u$ give disjoint sets (they differ in the penultimate vertex). Each uphill path has a unique last vertex, hence the total is $\sum_v p(v)$. $\square$

**Lemma 2.** For every vertex $v$: $p(v)\ge1$ and $p(v)\ge\deg^-(v)$.

*Proof.* From $v$ repeatedly move to a neighbour with a smaller label while one exists; the labels strictly decrease, so the walk stops, at a vertex with no smaller neighbour, i.e. a valley $v_1$. The reversed walk is an uphill path ending at $v$, so $p(v)\ge1$. Applying this to every $u$ with $u\to v$ and using Lemma 1, $p(v)\ge\sum_{u\to v}p(u)\ge\sum_{u\to v}1=\deg^-(v)$. $\square$

**Corollary 3.** Total $\ \ge\sum_v\max(1,\deg^-(v))=\#\{\text{valleys}\}+|E|$.

*Proof.* Termwise from Lemma 2 and Lemma 1. Valleys are exactly the vertices with $\deg^-=0$, and $\sum_v\deg^-(v)=|E|$ because every edge has exactly one head. So $\sum_v\max(1,\deg^-(v))=\#\{v:\deg^-(v)=0\}+\sum_{v:\deg^-(v)\ge1}\deg^-(v)=\#\{\text{valleys}\}+|E|$. $\square$

The vertex with label $1$ is always a valley (all its neighbours have larger labels). Hence for $Q_4$: total $\ge 32+1=33$.

## Lower bound: no labelling of $Q_4$ has exactly 33 uphill paths, hence $U(Q_4)\ge34$

Suppose some labelling $f$ of $Q_4$ has total exactly $33$.

**Step 1 (all inequalities are tight).** By Corollary 3, $33=\text{total}\ge\#\{\text{valleys}\}+32\ge 33$, so $\#\{\text{valleys}\}=1$ and $\sum_v p(v)=\sum_v\max(1,\deg^-(v))$. Since $p(v)\ge\max(1,\deg^-(v))$ holds for every $v$ (Lemma 2), equality of the sums forces equality for every term: $p(v)=\max(1,\deg^-(v))$ for all $v$. In particular, for every non-valley $v$ (i.e. $\deg^-(v)\ge1$): $p(v)=\deg^-(v)$.

**Step 2 (every in-neighbour of a non-valley has $p=1$, hence $\deg^-\le1$).** Let $v$ be a non-valley. By Lemma 1 (with $[v\text{ valley}]=0$) and Step 1,
$$\sum_{u\to v}p(u)=p(v)=\deg^-(v)=\sum_{u\to v}1 .$$
Each term satisfies $p(u)\ge1$ (Lemma 2), and there are $\deg^-(v)$ terms on each side, so $p(u)=1$ for every $u\to v$. By Lemma 2 again, $\deg^-(u)\le p(u)=1$.

**Step 3 (in-degrees lie in $\{0,1,4\}$).** Let $u$ be any vertex. If $\deg^+(u)\ge1$, pick $w$ with $u\to w$; then $w$ has an in-neighbour, so $w$ is not a valley, and Step 2 applied to $v=w$ gives $\deg^-(u)\le1$. If $\deg^+(u)=0$, then $\deg^-(u)=4-\deg^+(u)=4$. Hence $\deg^-(u)\in\{0,1,4\}$ for every vertex $u$.

**Step 4 (counting edges).** Let $s=\#\{u:\deg^-(u)=4\}$. The vertices with $\deg^-(u)=0$ are exactly the valleys, and there is exactly one (Step 1). The remaining $16-1-s=15-s$ vertices have $\deg^-(u)=1$. Summing in-degrees over all vertices, and using $\sum_u\deg^-(u)=|E|=32$:
$$4s+1\cdot(15-s)+0\cdot 1=32\quad\Longrightarrow\quad 3s=17,$$
which has no integer solution. Contradiction.

Therefore no labelling of $Q_4$ has exactly $33$ uphill paths; combined with total $\ge33$ (Corollary 3), every labelling has at least $34$ uphill paths: $U(Q_4)\ge34$.

(*Remark, not needed for the cell:* the same argument for $Q_d$, $d\ge2$, gives total $=|E|+1$ only if $(d-1)s=2^{d-1}(d-2)+1$ has an integer solution; for $d=3$ this is $2s=5$, recovering Proposition 4 of the $Q_3$ proof.)

## Upper bound: an explicit labelling with exactly 34 uphill paths

Labelling $f$, as the list of the 16 vertices in increasing label order (label $1$ first):

$$\texttt{0000},\ \texttt{1111},\ \texttt{0111},\ \texttt{1101},\ \texttt{1110},\ \texttt{1011},\ \texttt{0001},\ \texttt{1000},\ \texttt{0010},\ \texttt{0100},\ \texttt{1001},\ \texttt{0110},\ \texttt{0011},\ \texttt{1010},\ \texttt{0101},\ \texttt{1100}.$$

Structure: label $1$ = weight $0$; label $2$ = weight $4$; labels $3$–$6$ = the four vertices of weight $3$; labels $7$–$10$ = the four vertices of weight $1$; labels $11$–$16$ = the six vertices of weight $2$. (This is a bijection: the sixteen strings are pairwise distinct and are all of $\{0,1\}^4$.)

Computation of $p$ in increasing label order (Lemma 1). Neighbours of a vertex of weight $k$ have weights $k\pm1$.

| vertex | label | lower neighbours | $p$ |
|---|---|---|---|
| 0000 | 1 | none (its neighbours are the weight-1 vertices, labels 7–10) — **valley** | 1 |
| 1111 | 2 | none (its neighbours are the weight-3 vertices, labels 3–6) — **valley** | 1 |
| 0111 | 3 | 1111 (label 2); the other neighbours 0011, 0101, 0110 have labels 13, 15, 12 | 1 |
| 1101 | 4 | 1111; others 0101, 1001, 1100 have labels 15, 11, 16 | 1 |
| 1110 | 5 | 1111; others 0110, 1010, 1100 have labels 12, 14, 16 | 1 |
| 1011 | 6 | 1111; others 0011, 1001, 1010 have labels 13, 11, 14 | 1 |
| 0001 | 7 | 0000 (label 1); others 1001, 0101, 0011 have labels 11, 15, 13 | 1 |
| 1000 | 8 | 0000; others 1100, 1010, 1001 have labels 16, 14, 11 | 1 |
| 0010 | 9 | 0000; others 1010, 0110, 0011 have labels 14, 12, 13 | 1 |
| 0100 | 10 | 0000; others 1100, 0110, 0101 have labels 16, 12, 15 | 1 |
| 1001 | 11 | 0001, 1000 (weight 1) and 1101, 1011 (weight 3): all four lower, each with $p=1$ | 4 |
| 0110 | 12 | 0010, 0100, 1110, 0111 | 4 |
| 0011 | 13 | 0001, 0010, 1011, 0111 | 4 |
| 1010 | 14 | 1000, 0010, 1110, 1011 | 4 |
| 0101 | 15 | 0001, 0100, 1101, 0111 | 4 |
| 1100 | 16 | 1000, 0100, 1110, 1101 | 4 |

Every weight-2 vertex has exactly two weight-1 and two weight-3 neighbours, all with labels $\le10<11$, so all four neighbours are lower and each has $p=1$, giving $p=4$. The valleys are exactly 0000 and 1111 (every other vertex has a lower neighbour, as the table shows). Total
$$\sum_v p(v)=1+1+4\cdot1+4\cdot1+6\cdot4=34 .$$
Hence $U(Q_4)\le34$.

## Conclusion

$$U(Q_4)=34,$$ attained by the labelling above. (For comparison $U(Q_3)=14=|E|+2$ and $U(Q_4)=34=|E|+2$.)

## Computational checks (exact integer arithmetic; independent of the proof)

1. `verifica_etichettatura_q4.py` checks the submitted labelling: bijection, valleys, per-vertex $p$ (the table above), and the total by two independent methods — the DP of Lemma 1 in label order and an explicit recursive DFS enumerating every uphill path from every valley. Output: both totals $=34$, valleys $\{0000,1111\}$. Wall-clock 0.02 s (Python 3.14.7, macOS).

2. `q4_branch_and_bound.py T` is an exact, symmetry-reduced search for labellings with $<T$ uphill paths. Vertices are placed in increasing label order; when $v$ is placed all its lower neighbours are already placed, so $p(v)$ is fixed at that moment (Lemma 1). *Symmetry reduction:* at each node only one candidate per orbit of the pointwise stabiliser (inside $\mathrm{Aut}(Q_4)$, order $384$, generated explicitly as coordinate permutation followed by XOR with a mask) of the already-placed set is tried; this is sound because if $g$ fixes the placed vertices pointwise and $g(v)=v'$, then $f\mapsto f\circ g^{-1}$ maps labellings with prefix $(\dots,v)$ bijectively onto labellings with prefix $(\dots,v')$ and preserves the number of uphill paths. *Lower bound at a node* (placed set $S$, unplaced set $U$, $a(v)=\sum_{u\in N(v)\cap S}p(u)$, $d(v)$ = number of in-neighbours of $v$ inside $U$ in the final orientation, so $\sum_{v\in U}d(v)=E(U)$, the number of edges inside $U$): for $v\in U$ all $S$-neighbours are lower and all unplaced in-neighbours have $p\ge1$, so $p(v)\ge\max(1,a(v)+d(v))$; minimising $\sum_{v\in U}\max(1,a(v)+d(v))$ over nonnegative $d$ with $\sum d=E(U)$ gives $\sum_{v\in U,a(v)\ge1}a(v)+\max(\#\{v\in U:a(v)=0\},E(U))$, so $\text{LB}=\sum_{v\in S}p(v)+\sum_{v\in U,a(v)\ge1}a(v)+\max(\#\{a=0\},E(U))$ is a valid lower bound for every completion; a node is pruned iff $\text{LB}\ge T$. Results: $T=34$: **0 labellings found**, 47 978 nodes, 0.3 s. $T=35$: 19 525 440 labellings with exactly 34 reached by the reduced search, 54 814 700 nodes, 156.8 s (shows the pruning is not over-aggressive at the optimum). Sanity check on $Q_3$ (same code with `D = 3`): $T=13$: 0 found; $T=14$: 0 found (83 nodes); $T=15$: 148 found, and $148\cdot48=7104$ is exactly the known number of optimal labellings of $Q_3$ ($|\mathrm{Aut}(Q_3)|=48$). This search is a confirmation only; the proof of $U(Q_4)\ge34$ is the hand argument above.

3. `q4_ricerca_locale.py` (simulated annealing, 12 seeds, 200 000 steps each, 12.8 s) found the value 34 in every run and never below; heuristic only, proves nothing, used to find the incumbent.

## 3. Verification: instructions, dependencies, timings
Three independent programs, standard Python 3 only (exact integers), each enumerating all $8!=40320$ labellings:
- `problema-2/certificati/q3_esaustivo.py` — explicit DFS of the paths + dynamic programming of Lemma 1,
  with an equality `assert` on every labelling. Measured time: 0.37 s.
- `problema-2/certificati/q3_verifica_indipendente.py` — written separately, different method: explicit
  level-by-level construction of all increasing sequences starting from the valleys. Measured time: 0.20 s.
- `problema-2/certificati/verifica_etichettatura_q3.py` — checks only the submitted labelling (bijection,
  valleys, $p(v)$ per vertex, total 14).
Command: `python3 problema-2/certificati/q3_verifica_indipendente.py` (and analogous). Python 3.14.7, macOS.
All report: minimum 14, 7104 optimal labellings, distribution with no values 13 and 15.

For $Q_4$ (the lower-bound proof is by hand; the computation is confirmation only):
- `verifica_etichettatura_q4.py` (Researcher, two methods) and `q4_verifica_etichettatura_indipendente.py` (written separately,
  explicit construction of the paths): both 34 paths, valleys `0000` and `1111`, bijection verified.
- `q4_branch_and_bound.py SOGLIA`: exact branch-and-bound with symmetry reduction (384 automorphisms); with threshold 34
  no labelling below 34 (47978 nodes, 0.3 s); with threshold 35 it finds labellings with 34 (54.8M nodes, 157 s).
  The soundness of the reduction is argued in the script but the cell does not depend on it.
- `q4_ricerca_locale.py`: simulated annealing, exploration only (12 seeds, best value 34 in every run).

## 4. Sources and contribution
No external sources used. The lower-bound argument generalises the idea of IMO 2022 P6 (every vertex is the end
of at least one path; $p(v)\ge\deg^-(v)$), adding the obstruction specific to $Q_3$ (Proposition 4).
Proof produced by the automatic Researcher (Claude Fable 5.1, run `runs/p2_q3/attempts/attempt_001.json`) and
reviewed by hand step by step; independent numerical verification written separately.

## 5. Limits and unresolved parts
- No unresolved part for C1.
- $U(Q_3)=|E|+2$ and $U(Q_4)=|E|+2$. The parity argument for $Q_4$ (Steps 3–4) generalises: the total $|E|+1$ is
  impossible on $Q_d$ when $(d-1)\nmid 2^{d-1}(d-2)+1$, i.e. for every $d$ from 3 to 10 at least. Hence $U(Q_d)\ge|E|+2$
  in that range: a weak bound compared with the known 2368 for $Q_9$, but free.
- The optimum of $Q_4$ has TWO valleys and attains exactly $|E|+\#\text{valleys}$: for large cubes it is worth looking for
  labellings with few valleys in which almost all vertices have $p(v)=\max(1,\deg^-(v))$.


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.
- **attempt_001** — Researcher: family `exact_computation`, subgoal: Determine U(Q_3) exactly (value + explicit optimal labelling in the required format), with certainty via exhaustive exact enumeration of all 8! labellings, plus an independent hand proof of the lower bound.; declared `CELL_SOLVED_CANDIDATE`.
  - Why this approach: No prior attempts exist. The cell explicitly allows exhaustive exact computation with code and stated finite set; 8! = 40320 labellings is tiny (0.36 s). To make the result robust against a coding bug, two genuinely different counting routines are cross-checked on every labelling, and the lower bound is also proved by hand so the value does not rest on the code alone.
  - Referee: `(nessun verdetto)` / `None`
- **attempt_001** — Researcher: family `direct_proof`, subgoal: Determine U(Q_4) exactly: prove the lower bound U(Q_4) >= 34 by hand and exhibit an explicit labelling with exactly 34 uphill paths (route (b) of the cell), with an independent exact computer confirmation.; declared `CELL_SOLVED_CANDIDATE`.
  - Why this approach: No failed attempts recorded. Simulated annealing (12 seeds) never went below 34 = |E| + 2, while the verified bound gives 33; the gap of 1 suggested a tightness analysis of the verified bound |E| + #valleys, exactly as Proposition 4 did for Q_3. The tightness analysis turned out to close with a pure counting argument (no case analysis), so I chose route (b) (hand proof + explicit labelling), and added a symmetry-reduced exact search only as an independent check, not as the proof.
  - Referee: `(nessun verdetto)` / `None`

## 7. arXiv literature consulted
- arXiv:1412.3893v1 — *The competition between simple and complex evolutionary trajectories in asexual populations* (Ian E. Ochs, Michael M. Desai, 2014), found by query `uphill paths`; abstract read, full text not relied upon.

## 8. Code

**attempt_001 / code_1** (python, rigor `exact`): Exhaustive exact enumeration of all 8! = 40320 labellings of Q_3; two independent counts (explicit DFS path enumeration and DP p(v)) asserted equal on every labelling; reports minimum, distribution and an optimal labelling in submission format. Wall-clock 0.36 s. Saved as runs/p2_q3/sandbox/q3_esaustivo.py and problema-2/certificati/q3_esaustivo.py.

```python
"""
Calcolo esatto di U(Q_3) per enumerazione esaustiva di tutte le 8! = 40320 etichettature.

Due conteggi indipendenti per ogni etichettatura:
  1. DFS: enumera esplicitamente ogni cammino in salita (v_1,...,v_k) partendo da ogni valle.
  2. DP:  p(v) = [v valle] + somma_{u vicino, f(u)<f(v)} p(u);  totale = somma_v p(v).
Aritmetica: solo interi Python (esatta). Insieme coperto: TUTTE le biiezioni V(Q_3) -> {1..8}.
"""
from itertools import permutations
from collections import Counter
import time

D = 3
VERTICI = list(range(2 ** D))                      # vertice = intero, bit i = coordinata i
VICINI = [[v ^ (1 << i) for i in range(D)] for v in VERTICI]


def stringa(v):
    """Vertice intero -> stringa 0/1 di lunghezza D (bit 0 a sinistra)."""
    return "".join(str((v >> i) & 1) for i in range(D))


def valli(etichetta):
    """Vertici con tutti i vicini di etichetta maggiore."""
    return [v for v in VERTICI if all(etichetta[w] > etichetta[v] for w in VICINI[v])]


def conta_dfs(etichetta):
    """Conteggio 1: enumera esplicitamente ogni cammino in salita."""
    def cammini_da(v):
        # il cammino che termina in v conta 1, piu' tutte le estensioni ai vicini maggiori
        return 1 + sum(cammini_da(w) for w in VICINI[v] if etichetta[w] > etichetta[v])
    return sum(cammini_da(v) for v in valli(etichetta))


def conta_dp(etichetta):
    """Conteggio 2: programmazione dinamica in ordine crescente di etichetta."""
    ordine = sorted(VERTICI, key=lambda v: etichetta[v])
    p = {}
    for v in ordine:
        minori = [w for w in VICINI[v] if etichetta[w] < etichetta[v]]
        p[v] = (1 if not minori else 0) + sum(p[w] for w in minori)
    return sum(p.values())


def esplora_tutte():
    """Enumera tutte le 8! etichettature; restituisce (minimo, distribuzione, ottime)."""
    distribuzione = Counter()
    ottime = []
    minimo = None
    for perm in permutations(range(1, 2 ** D + 1)):
        etichetta = list(perm)                     # etichetta[v] = f(v)
        n_dfs = conta_dfs(etichetta)
        n_dp = conta_dp(etichetta)
        assert n_dfs == n_dp, (etichetta, n_dfs, n_dp)
        distribuzione[n_dfs] += 1
        if minimo is None or n_dfs < minimo:
            minimo, ottime = n_dfs, [etichetta]
        elif n_dfs == minimo:
            ottime.append(etichetta)
    return minimo, distribuzione, ottime


def lista_ordinata(etichetta):
    """Formato di consegna: vertici in ordine crescente di etichetta, come stringhe 0/1."""
    return [stringa(v) for v in sorted(VERTICI, key=lambda v: etichetta[v])]


if __name__ == "__main__":
    inizio = time.time()
    minimo, distribuzione, ottime = esplora_tutte()
    print(f"etichettature esaminate: {sum(distribuzione.values())}")
    print(f"U(Q_3) = {minimo}; etichettature ottime: {len(ottime)}")
    print("distribuzione (cammini -> numero etichettature):", sorted(distribuzione.items()))
    print("prima etichettatura ottima (ordine crescente di etichetta):", lista_ordinata(ottime[0]))
    print(f"tempo: {time.time() - inizio:.2f} s")

```

**attempt_001 / code_2** (python, rigor `exact`): Independent check of the single submitted labelling (bijection check, valleys, per-vertex p, total = 14). Saved as runs/p2_q3/sandbox/verifica_etichettatura_q3.py and problema-2/certificati/. Runs instantly.

```python
"""
Verifica indipendente della singola etichettatura consegnata per Q_3:
stampa valli, p(v) per ogni vertice e il totale dei cammini in salita (interi esatti).
"""
D = 3
CONSEGNA = ['000', '100', '010', '110', '101', '011', '001', '111']   # ordine crescente di etichetta


def vicini(s):
    """Stringhe 0/1 che differiscono da s in esattamente una coordinata."""
    return [s[:i] + ('1' if s[i] == '0' else '0') + s[i + 1:] for i in range(D)]


def verifica(consegna):
    """Calcola p(v) in ordine di etichetta e restituisce (valli, p, totale)."""
    assert sorted(consegna) == sorted(format(k, f'0{D}b') for k in range(2 ** D)), "non e' una biiezione"
    etichetta = {s: k + 1 for k, s in enumerate(consegna)}
    p, valli = {}, []
    for s in consegna:
        minori = [w for w in vicini(s) if etichetta[w] < etichetta[s]]
        if not minori:
            valli.append(s)
        p[s] = (1 if not minori else 0) + sum(p[w] for w in minori)
    return valli, p, sum(p.values())


if __name__ == "__main__":
    valli, p, totale = verifica(CONSEGNA)
    print("valli:", valli)
    for s in CONSEGNA:
        print(f"  {s}  etichetta {CONSEGNA.index(s)+1}  p = {p[s]}")
    print("cammini in salita totali:", totale)

```

**attempt_001 / code_1** (python, rigor `exact`): Exact verification of the submitted labelling of Q_4: bijection check, valleys, per-vertex p(v) table, total computed by two independent methods (DP of Lemma 1 in label order; explicit DFS enumeration of all uphill paths from every valley). Output: both totals 34, valleys {0000,1111}. Wall-clock 0.02 s. File: runs/p2_q4/sandbox/verifica_etichettatura_q4.py

```python
"""Verifica ESATTA (interi Python) dell'etichettatura candidata di Q_4 con 34 cammini in salita.
Due metodi indipendenti: (i) DP di Lemma 1 in ordine di etichetta; (ii) enumerazione esplicita
(DFS) di tutti i cammini in salita da ogni valle. Stampa la tabella p(v) per la consegna."""
D = 4
N = 1 << D
# Convenzione: carattere i-esimo della stringa (da sinistra) = coordinata i; bit i dell'intero.
ETICHETTATURA = ['0000', '1111', '0111', '1101', '1110', '1011', '0001', '1000',
                 '0010', '0100', '1001', '0110', '0011', '1010', '0101', '1100']


def da_stringa(s):
    """Converte la stringa 0/1 (carattere i = coordinata i) nell'intero con bit i = coordinata i."""
    return sum(int(c) << i for i, c in enumerate(s))


def vicini(v):
    """I d vicini di v in Q_d: si cambia esattamente una coordinata."""
    return [v ^ (1 << i) for i in range(D)]


def conta_con_dp(ordine, etichetta):
    """Metodo (i): p(v) = [v valle] + somma p(u) sui vicini u con etichetta minore."""
    p = {}
    righe = []
    for v in ordine:
        minori = [u for u in vicini(v) if etichetta[u] < etichetta[v]]
        p[v] = 1 if not minori else sum(p[u] for u in minori)
        righe.append((format(v, f'0{D}b')[::-1], etichetta[v], [format(u, f'0{D}b')[::-1] for u in minori], p[v]))
    return sum(p.values()), righe


def conta_con_dfs(etichetta):
    """Metodo (ii): enumera esplicitamente ogni cammino in salita partendo da ogni valle."""
    def estendi(v):
        totale = 1  # il cammino che termina qui
        for w in vicini(v):
            if etichetta[w] > etichetta[v]:
                totale += estendi(w)
        return totale
    valli = [v for v in range(N) if all(etichetta[w] > etichetta[v] for w in vicini(v))]
    return sum(estendi(v) for v in valli), valli


def main():
    ordine = [da_stringa(s) for s in ETICHETTATURA]
    assert sorted(ordine) == list(range(N)), "non e' una biiezione"
    etichetta = {v: i + 1 for i, v in enumerate(ordine)}
    totale_dp, righe = conta_con_dp(ordine, etichetta)
    totale_dfs, valli = conta_con_dfs(etichetta)
    for stringa, lab, minori, p in righe:
        print(f"{stringa}  etichetta {lab:2d}  vicini minori {minori}  p = {p}")
    print("valli:", [format(v, f'0{D}b')[::-1] for v in valli])
    print("totale (DP di Lemma 1):", totale_dp)
    print("totale (DFS esplicita):", totale_dfs)
    assert totale_dp == totale_dfs == 34


if __name__ == "__main__":
    main()

```

**attempt_001 / code_2** (python, rigor `exact`): Independent exact confirmation of the lower bound: symmetry-reduced branch-and-bound over all labellings of Q_4 placed in increasing label order (one candidate per orbit of the pointwise stabiliser of the placed set inside Aut(Q_4), order 384; provable lower bound LB = sum_{placed} p + sum_{unplaced, a>=1} a(v) + max(#{a=0}, E(U))). Covers ALL 16! labellings up to the stated symmetry reduction. Results: threshold 34 -> 0 labellings with <34 paths, 47978 nodes, 0.3 s; threshold 35 -> 19525440 labellings with 34 reached, 54814700 nodes, 156.8 s. Sanity on Q_3 (D=3): none <14; 148 representatives with 14 (148*48 = 7104 = known count). Python 3.14.7. File: runs/p2_q4/sandbox/q4_branch_and_bound.py

```python
"""Branch-and-bound ESATTO (interi) su Q_4: cerca un'etichettatura con < SOGLIA cammini in salita.
Si piazzano i vertici in ordine crescente di etichetta; p(v) e' determinato al piazzamento (Lemma 1).
Riduzione per simmetria: a ogni nodo si prova un solo candidato per orbita dello stabilizzatore
puntuale (in Aut(Q_4), ordine 384) dell'insieme gia' piazzato. Bound inferiore dimostrato nel testo.
Conferma indipendente della prova a mano; NON e' la prova principale."""
import sys, time
from itertools import permutations

D = 4
N = 1 << D
VICINI = [[v ^ (1 << i) for i in range(D)] for v in range(N)]


def automorfismi():
    """Tutti i 384 automorfismi di Q_4 come tuple immagine: v -> perm(coordinate) XOR maschera."""
    gruppo = []
    for perm in permutations(range(D)):
        for maschera in range(N):
            immagine = tuple(sum(((v >> i) & 1) << perm[i] for i in range(D)) ^ maschera for v in range(N))
            gruppo.append(immagine)
    return gruppo


GRUPPO = automorfismi()


def bound_inferiore(p, piazzati, non_piazzati):
    """Bound: per v non piazzato p(v) >= max(1, a(v) + d(v)), a(v) = somma p sui vicini piazzati,
    d(v) = archi entranti da vertici non piazzati (somma dei d(v) = archi interni E(U)).
    Minimizzando sui d(v) a somma fissata: somma_{a>=1} a(v) + max(|U0|, E(U)), U0 = {a(v)=0}."""
    totale = sum(p[v] for v in piazzati)
    zeri, archi_interni = 0, 0
    for v in non_piazzati:
        a = sum(p[u] for u in VICINI[v] if u in piazzati)
        if a == 0:
            zeri += 1
        else:
            totale += a
        archi_interni += sum(1 for u in VICINI[v] if u not in piazzati)
    return totale + max(zeri, archi_interni // 2)


def rappresentanti(non_piazzati, stabilizzatore):
    """Un candidato per orbita dello stabilizzatore sui vertici non piazzati."""
    visti, scelti = set(), []
    for v in sorted(non_piazzati):
        if v in visti:
            continue
        scelti.append(v)
        visti.update(g[v] for g in stabilizzatore)
    return scelti


class Ricerca:
    def __init__(self, soglia):
        self.soglia = soglia
        self.nodi = 0
        self.trovate = []

    def esplora(self, ordine, p, piazzati, stabilizzatore):
        """Espande un nodo: prova ogni rappresentante d'orbita come prossimo vertice."""
        self.nodi += 1
        non_piazzati = [v for v in range(N) if v not in piazzati]
        if not non_piazzati:
            self.trovate.append(list(ordine))
            return
        if bound_inferiore(p, piazzati, non_piazzati) >= self.soglia:
            return
        for v in rappresentanti(non_piazzati, stabilizzatore):
            minori = [u for u in VICINI[v] if u in piazzati]
            p[v] = 1 if not minori else sum(p[u] for u in minori)
            piazzati.add(v)
            ordine.append(v)
            self.esplora(ordine, p, piazzati, [g for g in stabilizzatore if g[v] == v])
            ordine.pop()
            piazzati.discard(v)
            del p[v]


def main():
    soglia = int(sys.argv[1]) if len(sys.argv) > 1 else 34
    inizio = time.time()
    ricerca = Ricerca(soglia)
    ricerca.esplora([], {}, set(), GRUPPO)
    print(f"soglia {soglia}: etichettature con < {soglia} cammini trovate: {len(ricerca.trovate)}")
    for ordine in ricerca.trovate[:5]:
        print("  ", [format(v, f'0{D}b')[::-1] for v in ordine])
    print(f"nodi visitati: {ricerca.nodi}; tempo: {time.time() - inizio:.1f} s")


if __name__ == "__main__":
    main()

```

**attempt_001 / code_3** (python, rigor `float_exploration_only`): Heuristic simulated annealing to find an incumbent labelling (upper bound candidate). 12 seeds x 200000 steps, 12.8 s: best value 34 in every run. Proves nothing; the raw labelling found was normalised by XOR with its first vertex (an automorphism) to obtain the submitted one. File: runs/p2_q4/sandbox/q4_ricerca_locale.py

```python
"""Ricerca locale (simulated annealing) di etichettature di Q_4 con pochi cammini in salita.
Serve solo a trovare un buon candidato (upper bound): NON dimostra nulla.
Aritmetica: interi esatti (il conteggio), float solo nella regola di accettazione di SA."""
import random, sys, math

D = 4
N = 1 << D
VICINI = [[v ^ (1 << i) for i in range(D)] for v in range(N)]


def conta_cammini(ordine):
    """Numero di cammini in salita dell'etichettatura data come lista di vertici
    in ordine crescente di etichetta (Lemma 1: p(v) = [valle] + somma p(u) sui vicini minori)."""
    etichetta = [0] * N
    for pos, v in enumerate(ordine):
        etichetta[v] = pos
    p = [0] * N
    totale = 0
    for v in ordine:
        minori = [u for u in VICINI[v] if etichetta[u] < etichetta[v]]
        p[v] = 1 if not minori else sum(p[u] for u in minori)
        totale += p[v]
    return totale


def ricottura(seme, passi=200000):
    """Una corsa di simulated annealing con mosse di scambio e di spostamento."""
    rng = random.Random(seme)
    ordine = list(range(N))
    rng.shuffle(ordine)
    valore = conta_cammini(ordine)
    migliore, migliore_ordine = valore, ordine[:]
    for passo in range(passi):
        temperatura = 2.0 * (1 - passo / passi) + 0.05
        nuovo = ordine[:]
        i, j = rng.randrange(N), rng.randrange(N)
        if rng.random() < 0.5:
            nuovo[i], nuovo[j] = nuovo[j], nuovo[i]
        else:
            nuovo.insert(j, nuovo.pop(i))
        nuovo_valore = conta_cammini(nuovo)
        if nuovo_valore <= valore or rng.random() < math.exp((valore - nuovo_valore) / temperatura):
            ordine, valore = nuovo, nuovo_valore
            if valore < migliore:
                migliore, migliore_ordine = valore, ordine[:]
    return migliore, migliore_ordine


def main():
    corse = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    globale, globale_ordine = None, None
    for seme in range(corse):
        valore, ordine = ricottura(seme)
        if globale is None or valore < globale:
            globale, globale_ordine = valore, ordine
        print(f"seme {seme}: {valore} (migliore finora {globale})", flush=True)
    stringhe = [format(v, f"0{D}b") for v in globale_ordine]
    print("MIGLIORE:", globale, stringhe)


if __name__ == "__main__":
    main()

```


---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c1.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
