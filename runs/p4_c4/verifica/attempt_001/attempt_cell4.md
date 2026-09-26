# Problem 4, cell 4 — proof for every k ≤ 12 and report for k = 9..16

## Statement proved

**Theorem.** Let $3\le k\le 12$ (and also $k=13$) and let $a_1 \pmod{m_1},\dots,a_k\pmod{m_k}$ be pairwise disjoint congruence classes ($m_i\ge1$). Then $\gcd(m_i,m_j)\ge k$ for some $i<j$.

A *counterexample of size $k$* is a pairwise disjoint family of $k$ classes with $g_{ij}:=\gcd(m_i,m_j)\le k-1$ for all $i<j$. We use only the definitions and the criterion $(*)$ of the problem statement: two classes meet iff $\gcd(m_i,m_j)\mid a_i-a_j$. Nothing is assumed about smaller sizes (no minimality of $k$ is used anywhere). Put $L_k:=\operatorname{lcm}(1,2,\dots,k-1)$.

## Step 1. Three lemmas (all proved here)

**Lemma A (reduction to the gcd-lcm).** Let $a_1\pmod{m_1},\dots,a_k\pmod{m_k}$ be a counterexample of size $k\ge2$. Put $m_i':=\operatorname{lcm}\{g_{ij}: j\ne i\}$ and $a_i':=a_i \bmod m_i'$. Then

1. $2\le m_i'$, $m_i'\mid m_i$ and $m_i'\mid L_k$;
2. $\gcd(m_i',m_j')=g_{ij}$ for all $i\ne j$;
3. the classes $a_i'\pmod{m_i'}$ are pairwise disjoint (hence they form a counterexample of size $k$ again);
4. **(R3)** every prime power $q$ dividing some $m_i'$ divides $m_j'$ for some $j\ne i$.

*Proof.* If some $g_{ij}=1$ then $g_{ij}\mid a_i-a_j$ and the classes $i,j$ meet by $(*)$, contradicting disjointness; so every $g_{ij}\ge2$, hence $m_i'\ge2$. Each $g_{ij}$ divides $m_i$, so their lcm $m_i'$ divides $m_i$; each $g_{ij}\le k-1$ divides $L_k$, so $m_i'\mid L_k$. This is (1).
(2): $g_{ij}$ divides $m_i'$ and $m_j'$ (it is one of the numbers whose lcm defines each), so $g_{ij}\mid\gcd(m_i',m_j')$; conversely $\gcd(m_i',m_j')\mid\gcd(m_i,m_j)=g_{ij}$ because $m_i'\mid m_i$, $m_j'\mid m_j$.
(3): fix $i<j$. By (2) $\gcd(m_i',m_j')=g_{ij}$; since $g_{ij}\mid m_i'$ and $a_i'\equiv a_i\pmod{m_i'}$ we get $a_i'\equiv a_i\pmod{g_{ij}}$, likewise for $j$, so $a_i'-a_j'\equiv a_i-a_j\pmod{g_{ij}}$. The original classes are disjoint, so $g_{ij}\nmid a_i-a_j$ by $(*)$, hence $g_{ij}\nmid a_i'-a_j'$ and the reduced classes $i,j$ are disjoint by $(*)$.
(4): if $q=p^e$ divides $m_i'=\operatorname{lcm}_{j\ne i} g_{ij}$ then $e\le v_p(m_i')=\max_{j\ne i}v_p(g_{ij})$, so $q\mid g_{ij}$ for some $j\ne i$, and $g_{ij}\mid m_j'$ by (2). $\square$

**Lemma B (density criterion of Huhn–Megyesi type).** Let $a_i\pmod{m_i}$, $i\in I$ ($|I|\ge2$), be pairwise disjoint and let $M\ge1$ be a common multiple of all $g_{ij}$, $i<j$ in $I$. Then
$$\sum_{i\in I}\frac{1}{\gcd(m_i,M)}\le 1,\qquad\text{equivalently}\qquad \sum_{i\in I}\frac{M}{\gcd(m_i,M)}\le M.$$

*Proof.* Put $d_i=\gcd(m_i,M)$. For $0\le t<M/d_i$ the integers $a_i+tm_i$ are pairwise incongruent modulo $M$: if $a_i+tm_i\equiv a_i+t'm_i\pmod M$ then $M\mid (t-t')m_i$, so $(M/d_i)\mid (t-t')(m_i/d_i)$, and since $\gcd(M/d_i,m_i/d_i)=1$ we get $(M/d_i)\mid t-t'$, forcing $t=t'$. So the class $i$ contains representatives of exactly $M/d_i$ distinct residues modulo $M$ (in fact exactly these: every element $a_i+tm_i$ is congruent mod $M$ to one with $0\le t<M/d_i$). Suppose $\sum_i M/d_i>M$. By pigeonhole two of the listed integers, necessarily from different indices $i\ne j$ (within one index they are pairwise incongruent), are congruent modulo $M$: $a_i+tm_i\equiv a_j+sm_j\pmod M$. Then $a_i-a_j=sm_j-tm_i+uM$ for some integer $u$. Since $g_{ij}$ divides $m_i$, $m_j$ and $M$, it divides $a_i-a_j$, so classes $i$ and $j$ meet by $(*)$ — a contradiction. $\square$

*Remark.* With $M=\operatorname{lcm}(m_i)$ Lemma B is the trivial bound $\sum 1/m_i\le1$; the strength lies in the freedom to take small $M$ and sub-families $I$ (the sub-family criterion is not implied by the full-family one).

**Lemma C (translation).** If $a_i\pmod{m_i}$ are pairwise disjoint then so are $a_i-a_1\pmod{m_i}$ (same moduli, same gcds). *Proof:* $(a_i-a_1)-(a_j-a_1)=a_i-a_j$, so $(*)$ gives the same verdict for every pair. $\square$

## Step 2. The finite set and the pruning rules (certificate items 1–2)

**Corollary D (finite set).** If a counterexample of size $k$ exists, then there is a counterexample $a_i\pmod{m_i}$ of size $k$ whose moduli, listed in non-decreasing order, form a $k$-tuple $(m_1\le\dots\le m_k)$ with

- **(R1)** $m_i\mid L_k$, $m_i\ge2$, and $2\le\gcd(m_i,m_j)\le k-1$ for all $i<j$;
- **(R2)** for every sub-multiset $I$ of the indices with $|I|\ge2$ and every divisor $M$ of $L_k$ that is a multiple of $\operatorname{lcm}\{g_{ij}:i<j\in I\}$: $\sum_{i\in I} M/\gcd(m_i,M)\le M$;
- **(R3)** every prime power dividing some $m_i$ divides some other $m_j$;
- **(R5)** there exist residues $a_1=0,a_2,\dots,a_k$ with $g_{ij}\nmid a_i-a_j$ for all $i<j$.

*Proof.* Apply Lemma A to the given counterexample: the reduced family is a counterexample of size $k$ with (R1) (Lemma A (1),(2) and $g_{ij}\le k-1$) and (R3) (Lemma A (4)). (R2) is Lemma B applied to every sub-family of the reduced family, which is pairwise disjoint (Lemma A (3)). (R5) follows from Lemma C and $(*)$. Sorting the indices does not affect any of the properties. $\square$

Hence: **if for a given $k$ no non-decreasing tuple of divisors of $L_k$ satisfies (R1)–(R3) and (R5), then the Theorem holds for that $k$.** Everything the search discards is discarded by one of the rules (R1), (R2), (R3), (R5), each proved above; there is no other rule in the code.

**Enumeration (file `ricerca_moduli_hm.py`, stage A).** Vertices are the divisors $\ge2$ of $L_k$ in increasing order. A depth-first search builds non-decreasing tuples; a candidate $m$ is appended to the partial tuple $T$ only if (R1) holds for $m$ against every element of $T$, and (R2) holds for the *prefix* $T\cup\{m\}$ and every divisor $M$ of $L_k$ that is a multiple of $\operatorname{lcm}$ of the gcds of $T\cup\{m\}$ (the sums $\sum M/\gcd(m_i,M)$ are maintained incrementally for all divisors $M$ of $L_k$, in exact integer arithmetic). At a full tuple (leaf) the code applies (R3) and then (R2) for *every* sub-multiset $I$ with $|I|\ge2$ and every admissible $M$ (function `tutti_i_sottoinsiemi_passano`). Tuples passing everything are the **stage-A survivors** and are printed in full.

**Residue decision (file `decidi_residui.py`, stage B).** For each stage-A survivor, exhaustive backtracking over $a_1=0$, $a_i\in\{0,\dots,m_i-1\}$ in index order, extending only when $g_{ij}\nmid a_i-a_j$ for all earlier $j$. It returns a witness family (re-verified independently by the direct criterion $(*)$ on all pairs, function `verifica_diretta`) or `INFATTIBILE` after exhausting the tree (or `NON_DECISO` if a node budget is exceeded — this never happened in the runs below at thresholds $k-1$). The node budget never cut a search at threshold $k-1$; the budget exists so that the non-vacuity runs at threshold $k$ terminate in bounded time and report honestly.

The whole computation uses only Python integers (`math.gcd`, `math.lcm`, `//`, `%`); no floating point anywhere.

## Step 3. Results (certificate items 3–5)

Environment: Apple M4, Python 3.14.7 (`.venv`), all runs single-threaded. Command: `python ricerca_moduli_hm.py ricerca 3 4 5 6 7 8 9 10 11 12` (threshold $k-1$).

| $k$ | $L_k$ | candidates | nodes | leaves (passed R1+prefix-R2) | stage-A survivors | wall clock |
|---|---|---|---|---|---|---|
| 3 | 2 | 1 | 3 | 0 | 0 | 0.00 s |
| 4 | 6 | 3 | 10 | 0 | 0 | 0.00 s |
| 5 | 12 | 5 | 26 | 0 | 0 | 0.00 s |
| 6 | 60 | 11 | 103 | 0 | 0 | 0.00 s |
| 7 | 60 | 11 | 218 | 0 | 0 | 0.00 s |
| 8 | 420 | 23 | 1023 | 0 | 0 | 0.01 s |
| 9 | 840 | 31 | 3632 | 0 | 0 | 0.05 s |
| 10 | 2520 | 47 | 14907 | 0 | 0 | 0.32 s |
| 11 | 2520 | 47 | 41768 | 128 | 0 | 1.03 s |
| 12 | 27720 | 95 | 280931 | 110 | 0 | 14.9 s |
| 13 | 27720 | 95 | 1224204 | 3889 | **1** | 79.7 s |

"Nodes" counts every call of `estendi` (root included); "leaves" counts full $k$-tuples reaching the leaf test; at $k=11,12$ all leaves were removed by (R3) or subset-(R2). **Rerun** (`run2_k3_12.txt`): identical counts for every $k\le12$ (the diff of the two outputs contains only the timing fields).

**Conclusion for $k\le12$: no stage-A survivor, so by Corollary D no counterexample of size $k$ exists for any $3\le k\le12$.** (The sizes $3\le k\le 8$ are re-proved here independently of cells 1–3.)

### $k=13$: exactly one object left by stage A, decided in stage B

Stage A leaves exactly one tuple: $(10,10,10,10,10,12,12,12,12,24,36,40,45)$. Stage B (`parte_minima.py`, which calls `cerca_residui` with no budget cut) exhausts the residue tree in 154 235 nodes (4.6 s): **no residues exist**, so this tuple is not the modulus tuple of a disjoint family and $k=13$ is closed as well. The smallest part that already forces the decision has 7 classes: the script tests every sub-multiset in order of increasing size and reports the minimal residue-infeasible ones; every sub-multiset of size $\le6$ admits residues (all were tested, exhaustively), and the smallest infeasible parts are, e.g., $(10,10,10,10,10,12,45)$. Hand proof for this part: five pairwise disjoint classes modulo $10$ have pairwise gcd $10$, hence five residues pairwise distinct mod $10$. If they cover all five residues mod $5$, then the class with modulus $45$ (gcd $5$ with each of them) shares its residue mod $5$ with one of them, and they meet by $(*)$. Otherwise two of the five agree mod $5$, hence (being distinct mod $10$) have different parities; then the class with modulus $12$ (gcd $2$ with each) agrees mod $2$ with one of them and they meet by $(*)$. So no residues exist for this 7-tuple, and a fortiori for the 13-tuple. The full list of minimal infeasible parts (36 index sets, sizes 7, 9, 10) is in `k13_sopravvissuto.txt`.

### Report for $k=9,\dots,16$: what the method leaves undecided

- $k=9,10,11,12$: **nothing.** Stage A has zero survivors (table above), so nothing reaches stage B; proved by Corollary D + the exhaustive stage-A run.
- $k=13$: stage A leaves exactly the tuple $(10,10,10,10,10,12,12,12,12,24,36,40,45)$; stage B decides it (infeasible), with the 7-class forcing part proved by hand above. So the full method (A+B) leaves **nothing** undecided at $k=13$, and the Theorem holds at $k=13$ too. Note that O'Bryant's modulus-only method (see below) would *not* close $k=13$ with our rule set without residues: this tuple passes (R1)–(R3).
- $k=14,15,16$: see the status recorded in `run_k13_16.txt` at the time of hand-in (each size was given a 600 s limit). Whatever is not listed there as finished with its survivor list is **unfinished and not claimed**; an unfinished size is reported as such, with the counts reached, and no statement is made about it.

### Non-vacuity (the machinery, unmodified, at threshold $k$)

Command: `python decidi_residui.py nonvacuita 2000000 3 ... 11` runs the same two stages with threshold $k$ instead of $k-1$ (the only change is the parameter). At every $k\in\{3,\dots,12\}$ stage A returns the tuple $(k,\dots,k)$ among its survivors (files `nonvacuita_k3_12.txt`), and stage B finds the witness $0,1,\dots,k-1\pmod k$, re-verified by $(*)$ (files `nonvacuita_residui_k3_11.txt`, `nonvacuita_residui_k12.txt`). Other stage-A survivors at threshold $k$ (e.g. $(6,6,6,12,15,20)$ at $k=6$, two tuples at $k=10$, 57 tuples at $k=12$) are individually decided by stage B where it finished; they show that stage A is not vacuous and that stage B is genuinely needed.

## Step 4. Comparison with sources (tested)

O'Bryant, *On Z.-W. Sun's disjoint congruence classes conjecture*, arXiv:math/0604347v2 (2006), read in full, proves the statement for $k\le20$ and that a minimal counterexample has $k\notin\{24,30\}$. His method is modulus-only: Lemma 6 (items 1–8, several of which use *minimality of $k$* and *minimality of $\sum m_i$*), the criterion of Lemma 5 (= our Lemma B, which he states with the Huhn–Megyesi reference and proves), and a Mathematica search `Grow` for $k\le19$ that applies Lemma 5 only with $M=\operatorname{lcm}$ of the gcds of each subset (a week of CPU in 2006). Our method differs: (i) no minimality assumption (Lemma A replaces his items 1, 3 without it); (ii) Lemma B is applied with *all* divisors $M$ of $L_k$ that are multiples of the gcd-lcm, which is strictly stronger pruning; (iii) a residue stage B decides survivors. **Tested agreement:** for $k\le12$ both his claim and our run give "no counterexample". At $k=13$ we find that the modulus-only rules (R1)–(R3) do *not* suffice (one tuple survives); O'Bryant reports none surviving his tests at $k=13$, and this is consistent only if one of his minimality items (4, 5 or 6) kills that tuple: indeed item 5 requires at least three multiples of $k-1=12$ among the moduli, and $(10,10,10,10,10,12,12,12,12,24,36,40,45)$ has four multiples of 12, so item 5 passes; item 4 (no prime power) passes; item 6 does not apply. His `LemmaTest` uses only $M=\operatorname{lcm}$ of gcds of a subset; our (R2) with all $M$ is stronger, so our stage-A survivors are a subset of what his subset test would leave. We therefore cannot reproduce from his paper a modulus-only refutation of this tuple, and we did not test his code; we rely on nothing from his paper, and the discrepancy (if any) does not affect our claims, which are decided by our own stage B. Fornal–Sun, arXiv:2607.24655 (read), is asymptotic and gives nothing at these sizes.

## Scope and honesty

Claimed: the Theorem for $3\le k\le 12$ (cell 4) and additionally $k=13$; the report for $k=9..13$ (nothing undecided); $k=14,15,16$ reported exactly as the run file shows (unfinished sizes are not claimed). Everything rests on Lemmas A, B, C (proved above), Corollary D, and the exhaustive runs whose code, counts, rerun and survivor lists are included.
