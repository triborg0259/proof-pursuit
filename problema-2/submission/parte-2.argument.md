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


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.
- **attempt_001** — Researcher: family `case_analysis`, subgoal: Determine U(Q_5) exactly: prove the lower bound U(Q_5) >= 88 by a hand case analysis of the "excess" plus a small exact finite check, and exhibit an explicit labelling with exactly 88 uphill paths.; declared `CELL_SOLVED_CANDIDATE`.
  - Why this approach: No previous attempt for this cell. The verified claims (total ≥ |E| + #valleys, and the parity argument that killed |E|+1 for Q_4/Q_5) suggested pushing the same equality analysis further: quantify the slack ("excess") vertex by vertex. The key new observation is that in a 5-regular graph any slack is at least 3 and the remaining cases are a tiny combinatorial statement about independent sets and induced forests of Q_5 that can be checked exactly in under a second, with the reduction proved by hand.
  - Position w.r.t. the literature: none found. No LITERATURE section was supplied. I searched the web for "uphill paths" hypercube labelling valley minimum (WebSearch, 2026-09-26): only IMO 2022 Problem 6 material (Nordic squares, answer 2n^2-2n+1: AoPS wiki https://artofproblemsolving.com/wiki/index.php/2022_IMO_Problems/Problem_6, Evan Chen's notes https://web.evanchen.cc/exams/IMO-2022-notes.pdf, D. Grozev's blog https://dgrozev.wordpress.com/2022/07/16/three-graph-problems-on-imo-2022-problem-6/) and unrelated hypercube papers (arXiv 2404.18014 on layered subgraphs, 2310.18163 open problems). None treats the hypercube version. The repo notes (problema-2/note.md, item F) record an earlier arXiv search with the same conclusion. My approach follows the IMO 2022 lower-bound idea (p(v) ≥ max(1, deg^-(v))) and departs from it by quantifying the excess per vertex, which is what the hypercube (regular of odd degree 5) makes decisive.
  - Referee: `UNKNOWN_STATUS` / `READY_FOR_HUMAN`; next: Human reviews the exact target, proof and evidence, then approves explicit claims

## 6b. Tokens used by the agents
- Token counts not recorded for this run (older harness version; only cost and turns were logged).
- Token counts not recorded for this run (older harness version; only cost and turns were logged).

## 7. arXiv literature consulted
- arXiv:1412.3893v1 — *The competition between simple and complex evolutionary trajectories in asexual populations* (Ian E. Ochs, Michael M. Desai, 2014), found by query `uphill paths`; abstract read, full text not relied upon.

## 8. Code

**attempt_001 / code_1** (python, rigor `exact`): Exact count of uphill paths of a labelling of Q_d via the recursion p(v) = [valley] + sum of p over lower neighbours (shared module).

```python
"""Conteggio esatto dei cammini in salita di una etichettatura di Q_d.

Vertici = interi 0..2^d-1 (bit i = coordinata i); vicini = XOR con un bit.
p(v) = [v valle] + somma p(u) sui vicini u con etichetta minore; totale = somma p(v).
Aritmetica intera: risultato esatto.
"""


def vicini(v, d):
    """Restituisce i d vicini di v in Q_d."""
    return [v ^ (1 << i) for i in range(d)]


def conta_cammini(ordine, d):
    """ordine = lista dei vertici in ordine crescente di etichetta. Ritorna (totale, p, valli)."""
    etichetta = {v: i for i, v in enumerate(ordine)}
    assert sorted(ordine) == list(range(1 << d)), "non e' una biiezione"
    p = {}
    valli = []
    for v in ordine:
        minori = [u for u in vicini(v, d) if etichetta[u] < etichetta[v]]
        if not minori:
            valli.append(v)
            p[v] = 1
        else:
            p[v] = sum(p[u] for u in minori)
    return sum(p.values()), p, valli


def stringa(v, d):
    """Vertice intero -> stringa 0/1, coordinata 1 a sinistra."""
    return "".join(str((v >> i) & 1) for i in range(d))


def da_stringa(s):
    """Stringa 0/1 -> vertice intero (coordinata 1 a sinistra)."""
    return sum(int(c) << i for i, c in enumerate(s))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_1.py (python3, clean copy of the researcher sandbox): exit 0 in 0.0s; stdout: ''; stderr: ''`

**attempt_001 / code_2** (python, rigor `exact`): Certificate 1 for the lower bound: enumerate all independent 12-sets of Q_5 containing vertex 0 (1377 sets, symmetry reduction by XOR translations) and, for each vertex u outside, test that Q_5 - (I ∪ {u}) has a cycle (edges = vertices - components criterion). Covers all 27540 pairs (I,u); output 0 acyclic complements; 0.24 s.

```python
"""Certificato per il bound inferiore U(Q_5) >= 88 (implementazione 1: backtracking).

Enunciato verificato (Lemma computazionale):
  per ogni insieme indipendente I di Q_5 con |I| = 12 e per ogni vertice u di Q_5,
  il sottografo indotto da V meno (I u {u}) contiene un ciclo.
Riduzione: le traslazioni x -> x XOR t sono automorfismi di Q_5, quindi basta considerare
gli I che contengono il vertice 0 (ogni I non vuoto si trasla a contenerne uno).
Aciclicita' decisa con conteggio esatto: componenti + spigoli (un grafo e' una foresta sse
spigoli = vertici - componenti). Tutto intero: rigore = exact.
"""
import time
from conta_cammini import vicini

D = 5
N = 1 << D
ADJ = [set(vicini(v, D)) for v in range(N)]


def e_foresta(S):
    """True sse il sottografo indotto da S e' aciclico (spigoli = |S| - componenti)."""
    S = set(S)
    spigoli = sum(len(ADJ[v] & S) for v in S) // 2
    visti, comp = set(), 0
    for s in S:
        if s in visti:
            continue
        comp += 1
        pila, visti = [s], visti | {s}
        while pila:
            v = pila.pop()
            for w in ADJ[v] & S:
                if w not in visti:
                    visti.add(w)
                    pila.append(w)
    return spigoli == len(S) - comp


def indipendenti_con_zero(k):
    """Genera tutti gli insiemi indipendenti di taglia k contenenti 0 (vertici in ordine crescente)."""
    def ric(I, prossimo, vietati):
        if len(I) == k:
            yield list(I)
            return
        for v in range(prossimo, N):
            if v not in vietati and N - v >= k - len(I):
                yield from ric(I + [v], v + 1, vietati | ADJ[v] | {v})
    yield from ric([0], 1, ADJ[0] | {0})


if __name__ == "__main__":
    inizio = time.time()
    n_insiemi, n_test, violazioni = 0, 0, []
    for I in indipendenti_con_zero(12):
        n_insiemi += 1
        for u in range(N):
            if u in I:
                continue
            n_test += 1
            if e_foresta(set(range(N)) - set(I) - {u}):
                violazioni.append((I, u))
    print(f"insiemi indipendenti di taglia 12 contenenti 0: {n_insiemi}")
    print(f"coppie (I,u) esaminate: {n_test}; complementi aciclici trovati: {len(violazioni)}")
    print(f"tempo {time.time()-inizio:.2f}s")

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_2.py (python3, clean copy of the researcher sandbox): exit 0 in 0.5s; stdout: 'insiemi indipendenti di taglia 12 contenenti 0: 1377\ncoppie (I,u) esaminate: 27540; complementi aciclici trovati: 0\ntempo 0.44s'; stderr: ''`

**attempt_001 / code_3** (python, rigor `exact`): Certificate 2 for the lower bound, independent method and no symmetry reduction: all independent 12-sets as A ∪ B (A ⊆ even class over all 2^16 bitmasks, B ⊆ odd vertices not adjacent to A), acyclicity by union-find. Covers all 3672 independent 12-sets and 73440 pairs (I,u); 0 acyclic complements; 0.39 s.

```python
"""Certificato per il bound inferiore U(Q_5) >= 88 (implementazione 2, metodo diverso).

Stesso enunciato di verifica_q5_indipendenti.py, ma senza usare la simmetria:
ogni insieme indipendente e' A u B con A sottoinsieme dei vertici di peso pari e
B sottoinsieme dei vertici di peso dispari NON adiacenti ad A. Si scorrono tutti i 2^16
sottoinsiemi A (bitmask), poi tutti i B di taglia 12-|A| tra i dispari disponibili.
Aciclicita' con union-find (metodo diverso dal conteggio componenti). Rigore = exact.
"""
import itertools
import time

D = 5
N = 1 << D
PARI = [v for v in range(N) if bin(v).count("1") % 2 == 0]
DISPARI = [v for v in range(N) if bin(v).count("1") % 2 == 1]
SPIGOLI = [(v, v ^ (1 << i)) for v in range(N) for i in range(D) if v < v ^ (1 << i)]


def maschera_vicini(v):
    """Bitmask dei vicini di v."""
    return sum(1 << (v ^ (1 << i)) for i in range(D))


VIC = [maschera_vicini(v) for v in range(N)]


def ha_ciclo(maschera_vertici):
    """True sse il sottografo indotto dai vertici nella bitmask contiene un ciclo (union-find)."""
    padre = list(range(N))

    def trova(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for a, b in SPIGOLI:
        if (maschera_vertici >> a) & 1 and (maschera_vertici >> b) & 1:
            ra, rb = trova(a), trova(b)
            if ra == rb:
                return True
            padre[ra] = rb
    return False


def insiemi_indipendenti_12():
    """Genera le bitmask di tutti gli insiemi indipendenti di taglia 12."""
    for bits in range(1 << 16):
        A = [PARI[i] for i in range(16) if (bits >> i) & 1]
        if len(A) > 12:
            continue
        vietati = 0
        for a in A:
            vietati |= VIC[a]
        disponibili = [w for w in DISPARI if not (vietati >> w) & 1]
        for B in itertools.combinations(disponibili, 12 - len(A)):
            m = 0
            for x in A + list(B):
                m |= 1 << x
            yield m


if __name__ == "__main__":
    inizio = time.time()
    tutti = (1 << N) - 1
    n_insiemi, n_test, aciclici = 0, 0, 0
    for I in insiemi_indipendenti_12():
        n_insiemi += 1
        for u in range(N):
            if (I >> u) & 1:
                continue
            n_test += 1
            if not ha_ciclo(tutti & ~I & ~(1 << u)):
                aciclici += 1
    print(f"insiemi indipendenti di taglia 12 (tutti, senza simmetria): {n_insiemi}")
    print(f"coppie (I,u) esaminate: {n_test}; complementi aciclici: {aciclici}")
    print(f"tempo {time.time()-inizio:.2f}s")

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_3.py (python3, clean copy of the researcher sandbox): exit 0 in 0.8s; stdout: 'insiemi indipendenti di taglia 12 (tutti, senza simmetria): 3672\ncoppie (I,u) esaminate: 73440; complementi aciclici: 0\ntempo 0.77s'; stderr: ''`

**attempt_001 / code_4** (python, rigor `exact`): Builds the 88-path labelling (peaks = even vertices minus 00000, 11110) and counts exactly with the recursion: prints 88, the 8 valleys and the 32-vertex order.

```python
"""Costruzione esplicita con 88 cammini in salita su Q_5 e verifica esatta.

Idea: picchi = tutti i vertici di peso pari tranne 00000 e 11110 (14 picchi, indipendenti);
il complemento (2 pari + 16 dispari) e' una foresta con 10 spigoli e 8 componenti:
etichettiamo prima le 8 radici (valli), poi le foglie, poi i picchi. Ogni non-picco ha p = 1,
ogni picco ha p = 5: totale 18 + 14*5 = 88.
"""
from conta_cammini import conta_cammini, stringa, da_stringa

D = 5
N = 1 << D
peso = lambda v: bin(v).count("1")
radici = [da_stringa("00000"), da_stringa("11110")]
dispari = [v for v in range(N) if peso(v) % 2 == 1]
foglie = [v for v in dispari if any(v ^ r in [1 << i for i in range(D)] for r in radici)]
isolati = [v for v in dispari if v not in foglie]
picchi = [v for v in range(N) if peso(v) % 2 == 0 and v not in radici]
ordine = radici + isolati + foglie + picchi

if __name__ == "__main__":
    tot, p, valli = conta_cammini(ordine, D)
    print("totale cammini:", tot)
    print("valli:", [stringa(v, D) for v in valli])
    print("ordine:", ",".join(stringa(v, D) for v in ordine))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_4.py (python3, clean copy of the researcher sandbox): exit 0 in 0.0s; stdout: "totale cammini: 88\nvalli: ['00000', '11110', '11001', '10101', '01101', '10011', '01011', '00111']\nordine: 00000,11110,11001,10101,01101,10011,01011,00111,10000,01000,00100,11100,00010,11010,101`

**attempt_001 / code_5** (python, rigor `exact`): Independent verification of the submitted labelling by explicit DFS enumeration of every uphill path from each valley (string-based, no shared code): prints 88.

```python
"""Verifica indipendente dell'etichettatura a 88 cammini: enumerazione esplicita per DFS.

Metodo diverso dalla ricorsione p(v): da ogni valle si esplorano tutti i cammini con etichette
crescenti e si contano uno a uno. Controlla anche che l'input sia una biiezione.
"""
ORDINE = ("00000,11110,11001,10101,01101,10011,01011,00111,10000,01000,00100,11100,00010,11010,"
          "10110,01110,00001,11111,11000,10100,01100,10010,01010,00110,10001,01001,00101,11101,"
          "00011,11011,10111,01111").split(",")
D = 5


def vicini(s):
    """Vicini della stringa s: cambia un carattere."""
    return [s[:i] + ("1" if s[i] == "0" else "0") + s[i + 1:] for i in range(D)]


def conta_da(s, etichetta):
    """Numero di cammini in salita che iniziano in s (s incluso come cammino di lunghezza 1)."""
    return 1 + sum(conta_da(w, etichetta) for w in vicini(s) if etichetta[w] > etichetta[s])


if __name__ == "__main__":
    assert len(set(ORDINE)) == 32 and all(len(s) == 5 and set(s) <= {"0", "1"} for s in ORDINE)
    etichetta = {s: i + 1 for i, s in enumerate(ORDINE)}
    valli = [s for s in ORDINE if all(etichetta[w] > etichetta[s] for w in vicini(s))]
    totale = sum(conta_da(s, etichetta) for s in valli)
    print("valli:", valli)
    print("cammini in salita (DFS esplicita):", totale)

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_5.py (python3, clean copy of the researcher sandbox): exit 0 in 0.0s; stdout: "valli: ['00000', '11110', '11001', '10101', '01101', '10011', '01011', '00111']\ncammini in salita (DFS esplicita): 88"; stderr: ''`

**attempt_001 / code_6** (python, rigor `exact`): Sanity check (evidence only, not part of the proof) of the identity T = 80 + #valleys + X and of X ∈ {0} ∪ [3,∞) on 200000 random labellings of Q_5 (all asserts passed; smallest positive X observed: 14).

```python
"""Controllo di sanita' (solo evidenza) dell'identita' usata nella prova:
totale = |E| + #valli + X, X = somma sugli spigoli u->w di (p(u)-1), e X in {0} u [3, inf).
Etichettature casuali di Q_5 con aritmetica esatta.
"""
import random
from conta_cammini import conta_cammini, vicini

D, N = 5, 32
rng = random.Random(1)
valori_x = set()
for _ in range(200000):
    ordine = list(range(N))
    rng.shuffle(ordine)
    tot, p, valli = conta_cammini(ordine, D)
    et = {v: i for i, v in enumerate(ordine)}
    x = sum(p[u] - 1 for u in range(N) for w in vicini(u, D) if et[u] < et[w])
    assert tot == 80 + len(valli) + x
    valori_x.add(x)
print("identita' verificata su 200000 etichettature casuali; min X>0 osservato:", min(v for v in valori_x if v > 0))
print("valori di X osservati sotto 10:", sorted(v for v in valori_x if v < 10))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_6.py (python3, clean copy of the researcher sandbox): exit 0 in 13.4s; stdout: "identita' verificata su 200000 etichettature casuali; min X>0 osservato: 14\nvalori di X osservati sotto 10: []"; stderr: ''`

**attempt_001 / code_7** (python, rigor `float_exploration_only`): Simulated annealing over labellings (exploration only): best value found 88 in every seed run (seeds 0-5 in a first run, seeds 0-3 in a second run; 200k swap moves per seed, exact scoring). Not a proof.

```python
"""Ricerca locale (simulated annealing) sul numero di cammini in salita di Q_5.

Esplorazione: trova etichettature con pochi cammini. NON e' una prova (minimo locale possibile).
Stato = permutazione dei 32 vertici; mossa = scambio di due etichette; punteggio esatto (interi).
"""
import random
import sys
import time
from conta_cammini import conta_cammini, stringa

D = 5
N = 1 << D


def ricottura(seed, passi=200000, t0=2.0, t1=0.05):
    """Un run di annealing con seed fissato; ritorna (miglior_valore, miglior_ordine)."""
    rng = random.Random(seed)
    ordine = list(range(N))
    rng.shuffle(ordine)
    val = conta_cammini(ordine, D)[0]
    migliore, miglior_ordine = val, ordine[:]
    for k in range(passi):
        t = t0 * (t1 / t0) ** (k / passi)
        i, j = rng.randrange(N), rng.randrange(N)
        ordine[i], ordine[j] = ordine[j], ordine[i]
        nuovo = conta_cammini(ordine, D)[0]
        if nuovo <= val or rng.random() < 2.718 ** ((val - nuovo) / t):
            val = nuovo
            if val < migliore:
                migliore, miglior_ordine = val, ordine[:]
        else:
            ordine[i], ordine[j] = ordine[j], ordine[i]
    return migliore, miglior_ordine


if __name__ == "__main__":
    semi = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    inizio = time.time()
    globale = None
    for seed in range(semi):
        v, o = ricottura(seed)
        print(f"seed {seed}: {v}", flush=True)
        if globale is None or v < globale[0]:
            globale = (v, o)
    v, o = globale
    tot, p, valli = conta_cammini(o, D)
    print("migliore:", v, "valli:", [stringa(x, D) for x in valli])
    print("ordine:", ",".join(stringa(x, D) for x in o))
    print(f"tempo {time.time()-inizio:.1f}s")

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_7.py (python3, clean copy of the researcher sandbox): exit 0 in 60.5s; stdout: "seed 0: 88\nseed 1: 88\nseed 2: 88\nseed 3: 88\nseed 4: 88\nseed 5: 88\nseed 6: 88\nseed 7: 88\nmigliore: 88 valli: ['01001', '11100', '11010', '11111', '10011']\nordine: 01001,11100,01000,11010,`


---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c2.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
