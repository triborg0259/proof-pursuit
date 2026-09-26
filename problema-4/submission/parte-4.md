# Problem 4 — Part 4 — submission (PARTIAL)

**Declared status: PARTIAL (strong).** Mathematics judged PASS by the independent mathematical judge for every size up to 13, with the exhaustiveness certificate written out; the evidence judge could not reproduce the runs only because the scripts, launched without arguments by the orchestrator, default to a size that exceeds the 10-minute limit (run them with the size as argument, as documented in section 3). The cell is therefore reported as partial, not solved. What follows is the intermediate progress actually established,
as judged by the automatic Referee (verdict `UNKNOWN_STATUS`: Provide the missing review or independently checked evidence).
The author's own declared status was `CELL_SOLVED_CANDIDATE`.

## 1. Result and scope
Complete proof of the statement for every 3 ≤ k ≤ 12 (the cell) and for k = 13, with an exhaustiveness certificate: finite set + proof (Lemma A, Corollary D), pruning rules each proved (Lemma B with all admissible M, R3, translation), node counts and wall clock per k, reruns reproducing the counts, zero stage-A survivors for k ≤ 12, one survivor at k = 13 decided by exhaustive residue search plus a hand proof of its 7-class forcing part (computer check that no part of size ≤ 6 forces it). Report for k = 9..13: nothing undecided. k = 14,15,16: runs launched (unconditional, and with the proved extra rules M4/M5) but unfinished at hand-in; reported as unfinished and not claimed. Non-vacuity demonstrated: the unmodified code at threshold k returns (k,…,k) with residues 0..k-1 at every k ≤ 12 (at threshold 12, 2 other tuples NON_DECISO by the node budget and 14 not reached by the wall-clock cap, reported). Source O'Bryant (k ≤ 20) tested: agreement for k ≤ 12; at k = 13 modulus-only rules (even with his items 4–5) leave one tuple that only the residue stage kills.

## 2. Proof
# Problem 4, cell 4 — proof for every k ≤ 12 (and k = 13), report for k = 9..16

## Statement proved

**Theorem.** Let $3\le k\le 12$ (and also $k=13$) and let $a_1 \pmod{m_1},\dots,a_k\pmod{m_k}$ be pairwise disjoint congruence classes ($m_i\ge1$). Then $\gcd(m_i,m_j)\ge k$ for some $i<j$.

A *counterexample of size $k$* is a pairwise disjoint family of $k$ classes with $g_{ij}:=\gcd(m_i,m_j)\le k-1$ for all $i<j$. We use only the definitions and the criterion $(*)$ of the problem statement: two classes meet iff $\gcd(m_i,m_j)\mid a_i-a_j$. **No minimality of $k$ is used** for $k\le13$. Put $L_k:=\operatorname{lcm}(1,2,\dots,k-1)$.

## Step 1. Three lemmas (all proved here)

**Lemma A (reduction to the gcd-lcm).** Let $a_1\pmod{m_1},\dots,a_k\pmod{m_k}$ be a counterexample of size $k\ge2$. Put $m_i':=\operatorname{lcm}\{g_{ij}: j\ne i\}$ and $a_i':=a_i \bmod m_i'$. Then
1. $2\le m_i'$, $m_i'\mid m_i$ and $m_i'\mid L_k$;
2. $\gcd(m_i',m_j')=g_{ij}$ for all $i\ne j$;
3. the classes $a_i'\pmod{m_i'}$ are pairwise disjoint (so they form a counterexample of size $k$ again);
4. **(R3)** every prime power $q$ dividing some $m_i'$ divides $m_j'$ for some $j\ne i$.

*Proof.* If some $g_{ij}=1$ then $g_{ij}\mid a_i-a_j$ and classes $i,j$ meet by $(*)$, contradicting disjointness; so every $g_{ij}\ge2$, hence $m_i'\ge2$. Each $g_{ij}$ divides $m_i$, so their lcm $m_i'$ divides $m_i$; each $g_{ij}\le k-1$ divides $L_k$, so $m_i'\mid L_k$. This is (1).
(2): $g_{ij}$ divides $m_i'$ and $m_j'$ (it is one of the numbers whose lcm defines each), so $g_{ij}\mid\gcd(m_i',m_j')$; conversely $\gcd(m_i',m_j')\mid\gcd(m_i,m_j)=g_{ij}$ because $m_i'\mid m_i$, $m_j'\mid m_j$.
(3): fix $i<j$. By (2) $\gcd(m_i',m_j')=g_{ij}$; since $g_{ij}\mid m_i'$ and $a_i'\equiv a_i\pmod{m_i'}$ we get $a_i'\equiv a_i\pmod{g_{ij}}$, likewise for $j$, so $a_i'-a_j'\equiv a_i-a_j\pmod{g_{ij}}$. The original classes are disjoint, so $g_{ij}\nmid a_i-a_j$ by $(*)$, hence $g_{ij}\nmid a_i'-a_j'$ and the reduced classes $i,j$ are disjoint by $(*)$.
(4): if $q=p^e$ divides $m_i'=\operatorname{lcm}_{j\ne i} g_{ij}$ then $e\le v_p(m_i')=\max_{j\ne i}v_p(g_{ij})$, so $q\mid g_{ij}$ for some $j\ne i$, and $g_{ij}\mid m_j'$ by (2). $\square$

**Lemma B (density criterion, Huhn–Megyesi type).** Let $a_i\pmod{m_i}$, $i\in I$ ($|I|\ge2$), be pairwise disjoint and let $M\ge1$ be a common multiple of all $g_{ij}$, $i<j$ in $I$. Then $\sum_{i\in I} M/\gcd(m_i,M)\le M$.

*Proof.* Put $d_i=\gcd(m_i,M)$. For $0\le t<M/d_i$ the integers $a_i+tm_i$ are pairwise incongruent modulo $M$: if $a_i+tm_i\equiv a_i+t'm_i\pmod M$ then $M\mid (t-t')m_i$, so $(M/d_i)\mid (t-t')(m_i/d_i)$, and since $\gcd(M/d_i,m_i/d_i)=1$ we get $(M/d_i)\mid t-t'$, forcing $t=t'$. Suppose $\sum_i M/d_i>M$. By pigeonhole two of the listed integers, necessarily from different indices $i\ne j$ (within one index they are pairwise incongruent), are congruent modulo $M$: $a_i+tm_i\equiv a_j+sm_j\pmod M$. Then $a_i-a_j=sm_j-tm_i+uM$ for an integer $u$. Since $g_{ij}$ divides $m_i$, $m_j$ and $M$, it divides $a_i-a_j$, so classes $i$ and $j$ meet by $(*)$ — contradiction. $\square$

*Remark.* With $M=\operatorname{lcm}(m_i)$ this is the trivial bound $\sum 1/m_i\le1$; the strength lies in small $M$ and sub-families $I$ (the sub-family criterion is not implied by the full-family one; e.g. $(6,6,6,6,12,15,20)$ passes the full-family test and fails on the sub-family without $20$ with $M=12$).

**Lemma C (translation).** If $a_i\pmod{m_i}$ are pairwise disjoint then so are $a_i-a_1\pmod{m_i}$ (same moduli). *Proof:* $(a_i-a_1)-(a_j-a_1)=a_i-a_j$, so $(*)$ gives the same verdict for every pair. $\square$

## Step 2. The finite set and the pruning rules (certificate items 1–2)

**Corollary D.** If a counterexample of size $k$ exists, then there is one whose moduli, in non-decreasing order, form a $k$-tuple $(m_1\le\dots\le m_k)$ with
- **(R1)** $m_i\mid L_k$, $m_i\ge2$, and $2\le\gcd(m_i,m_j)\le k-1$ for all $i<j$;
- **(R2)** for every sub-multiset $I$ of indices with $|I|\ge2$ and every divisor $M$ of $L_k$ that is a multiple of $\operatorname{lcm}\{g_{ij}:i<j\in I\}$: $\sum_{i\in I} M/\gcd(m_i,M)\le M$;
- **(R3)** every prime power dividing some $m_i$ divides some other $m_j$;
- **(R5)** there exist residues $a_1=0,a_2,\dots,a_k$ with $g_{ij}\nmid a_i-a_j$ for all $i<j$.

*Proof.* Apply Lemma A: the reduced family is a counterexample of size $k$ with (R1) (Lemma A (1),(2) and $g_{ij}\le k-1$) and (R3) (Lemma A (4)). (R2) is Lemma B applied to every sub-family of the reduced family, which is pairwise disjoint (Lemma A (3)). (R5) is Lemma C plus $(*)$. Sorting indices affects nothing. $\square$

Hence **if for a given $k$ no non-decreasing tuple of divisors of $L_k$ satisfies (R1)–(R3) and (R5), the Theorem holds for that $k$.** Everything the search discards is discarded by one of (R1), (R2), (R3), (R5); there is no other rule in the code (the optional flags M4/M5 are off in all runs used for the claims).

**Finite set enumerated (item 1):** $S_k=\{(m_1\le\dots\le m_k): m_i\mid L_k,\ m_i\ge2,\ 2\le\gcd(m_i,m_j)\le k-1\}$; by Corollary D nothing outside $S_k$ can be (the modulus tuple of a reduced) counterexample.

**Stage A (`ricerca_moduli_hm.py`).** Depth-first construction of non-decreasing tuples over the divisors $\ge2$ of $L_k$. A candidate $m$ is appended to the partial tuple $T$ only if (R1) holds against every element of $T$ and (R2) holds for the *prefix* $T\cup\{m\}$ with every divisor $M$ of $L_k$ that is a multiple of the lcm of the gcds of $T\cup\{m\}$ (sums $\sum M/\gcd(m_i,M)$ are maintained incrementally for all divisors $M$, exact integers). At a full tuple (leaf) the code applies (R3) and then (R2) for *every* sub-multiset $I$, $|I|\ge2$, with every admissible $M$. Tuples passing everything are the **stage-A survivors**, printed in full.

**Stage B (`decidi_residui.py`).** For each survivor: exhaustive backtracking over $a_1=0$, $a_i\in\{0,\dots,m_i-1\}$ in index order, extending only if $g_{ij}\nmid a_i-a_j$ for all earlier $j$. Returns a witness (re-verified by the direct criterion $(*)$ on all pairs) or `INFATTIBILE` after exhausting the tree (or `NON_DECISO` if a node budget is hit — this never occurred at threshold $k-1$; it occurred twice in the non-vacuity run at threshold 12, see below).

Only Python integer arithmetic (`math.gcd`, `math.lcm`, `//`, `%`) is used; no floating point.

## Step 3. Results (certificate items 3–5)

Apple M4, Python 3.14.7, single thread. Command `python ricerca_moduli_hm.py ricerca 3 ... 13` (threshold $k-1$):

| $k$ | $L_k$ | candidates | nodes | leaves | stage-A survivors | wall clock |
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
| 13 | 27720 | 95 | 1224204 | 3889 | **1** | 79.7 s / 93.8 s |

"Nodes" = calls of `estendi` (root included); "leaves" = full tuples reaching the leaf test (at $k=11,12$ all leaves were removed by (R3) or by sub-multiset (R2)). **Reruns:** `run2_k3_12.txt` reproduces every count for $k\le12$ (diff contains only timing fields); $k=13$ was run twice (old and time-limited version of the script) with identical counts 1224204 / 3889 / 1.

**Conclusion for $k\le12$: zero stage-A survivors, so by Corollary D no counterexample of size $k$ exists for $3\le k\le12$.** (Sizes $3\le k\le8$ are re-proved here independently of cells 1–3.)

### $k=13$: exactly one object left by stage A, decided in stage B

Stage A leaves exactly one tuple: $(10,10,10,10,10,12,12,12,12,24,36,40,45)$. Stage B (`parte_minima.py`, no budget cut) exhausts the residue tree in 154 235 nodes (4.6 s): **no residues exist**. The smallest part forcing the decision has 7 classes: the script tests every sub-multiset in order of increasing size; every sub-multiset of size $\le6$ admits residues (all tested exhaustively), and the smallest infeasible parts are e.g. $(10,10,10,10,10,12,45)$ (full list of the 36 minimal infeasible index sets, sizes 7, 9, 10, in `k13_sopravvissuto.txt`). **Hand proof for this part:** five pairwise disjoint classes modulo $10$ have pairwise gcd $10$, hence residues pairwise distinct mod $10$. If they cover all five residues mod $5$, the class with modulus $45$ (gcd $5$ with each) agrees mod $5$ with one of them and they meet by $(*)$. Otherwise two of the five agree mod $5$ and, being distinct mod $10$, have different parities; the class with modulus $12$ (gcd $2$ with each) then agrees mod $2$ with one of them and they meet by $(*)$. So this 7-tuple, hence the 13-tuple, is not the modulus tuple of a disjoint family, and the Theorem holds at $k=13$.

### Report for $k=9,\dots,16$: what the method leaves undecided

- $k=9,10,11,12$: **nothing** — stage A has zero survivors (table), proved by Corollary D + the exhaustive run.
- $k=13$: stage A leaves exactly the tuple above; stage B decides it (infeasible), with the 7-class forcing part proved by hand. Nothing undecided; $k=13$ holds. Modulus-only rules (R1)–(R3) do *not* close $k=13$, and neither does adding the two extra rules (M4) "no prime-power modulus" and (M5) "at least three multiples of $k-1$" (run with flags: 669 090 nodes, 3812 leaves, the same single survivor, 56 s); residues are needed.
- $k=14,15,16$: **unfinished at the time of hand-in, not claimed.** Two runs were launched (600 s per size): the unconditional method, and the method plus (M4)/(M5), both of which are proved under explicit hypotheses — (M4) needs the statement at sizes $\le\lceil k/2\rceil\le8$ (proved above): if $m_1=p^r$ then $p\mid$ every $m_j$, some $\lceil k/p\rceil$ residues agree mod $p$, dividing by $p$ gives a disjoint family of that size with gcds $g_{ij}/p$, so some $g_{ij}\ge p\lceil k/p\rceil\ge k$; (M5) needs size $k-1$ settled: otherwise drop one multiple of $k-1$ (if any) and the remaining $k-1$ classes have all gcds $\le k-2$, a counterexample of size $k-1$. At hand-in both files (`run_k13_16_incond.txt`, `run_k13_16_m45.txt`) contain only the finished $k=13$ lines; $k=14$ was still running in both modes. Whatever they show later (finished with survivor list, or `NON_TERMINATA` with counts reached) is the exact report for those sizes; no claim is made here for $k\ge14$.

### Non-vacuity (unmodified machinery at threshold $k$)

`python decidi_residui.py nonvacuita ...` runs both stages with threshold $k$ instead of $k-1$ (the only change is the parameter). For every $k\in\{3,\dots,12\}$ stage A returns $(k,\dots,k)$ among its survivors and stage B returns the witness $0,1,\dots,k-1\pmod k$, re-verified by $(*)$ (files `nonvacuita_k3_12.txt`, `nonvacuita_residui_k3_11.txt`, `nonvacuita_residui_k12.txt`). Stage A also returns other tuples at threshold $k$ (e.g. $(6,6,6,12,15,20)$ at $k=6$, two at $k=10$, 57 at $k=12$), each passed to stage B: for $k\le11$ all decided (feasible or infeasible). At $k=12$ (57 survivors, node budget $3\cdot10^6$, 590 s wall-clock cap): 21 feasible (incl. $(12^{12})$ with witness $0..11$), 20 infeasible, **2 NON_DECISO by the node budget** — $(12,12,12,12,12,12,12,12,12,24,30,40)$ and $(12,12,12,12,12,12,12,12,36,40,56,315)$ — and the remaining 14 not reached before the wall-clock cap. This concerns only the non-vacuity demonstration at threshold 12 (not the proof, at threshold 11) and is reported as such; it shows the method is not vacuous and that stage B is genuinely needed.

## Step 4. Comparison with sources (tested)

O'Bryant, arXiv:math/0604347v2 (read in full) proves $k\le20$ with a modulus-only method (Lemma 5 = our Lemma B; Lemma 6 items using minimality of $k$ and of $\sum m_i$; a week-long Mathematica search applying Lemma 5 with $M=\operatorname{lcm}$ of the gcds of each subset). Tested agreement for $k\le12$: both give no counterexample. At $k=13$ our modulus-only rules, even with his items 4 and 5 added, leave one tuple; we did not run his code and cannot reproduce from his paper a modulus-only refutation; our own stage B decides it, so our claims do not rest on him. Fornal–Sun arXiv:2607.24655 (read) is asymptotic and gives nothing at these sizes.

## Scope and honesty

Claimed: the Theorem for $3\le k\le12$ (the cell) and additionally $k=13$; the report "nothing undecided" for $k=9..13$; $k=14,15,16$ reported as unfinished and not claimed. Everything rests on Lemmas A, B, C, Corollary D, and the exhaustive runs whose code, counts, reruns and survivor lists are included.

## 3. Verification: instructions, dependencies, timings
Python 3 standard library. Scripts (re-run by the orchestrator, see `runs/p4_c4/verifica/`):
- code_1 (python, rigor `exact`): Stage A (certificate): enumerate non-decreasing k-tuples of divisors of L_k with pairwise gcd in [2,k-1]; prune by Lemma B on every prefix with every admissible divisor M of L_k; at leaves apply (R3) and Lemma B on every sub-multiset; print node/leaf counts, survivors, wall clock. Mode 'nonvacuita' uses threshold k. Exact integer arithmetic. Runs: k=3..12 in 16 s total (counts in the table), k=13 in 80 s, reruns identical. File runs/p4_c4/sandbox/ricerca_moduli_hm.py (the on-disk version additionally has a 600 s time limit with count snapshot and optional flags --senza-potenze (M4) / --tre-multipli (M5), off by default; counts unchanged, checked for k=9,10,11,13).
- code_2 (python, rigor `exact`): Stage B: for each stage-A survivor, exhaustive backtracking on residues (a_1 = 0 by Lemma C), witness re-verified by criterion (*). Used for the non-vacuity runs (threshold k): every k in 3..12 returns the witness 0..k-1 (mod k). File runs/p4_c4/sandbox/decidi_residui.py.
- code_3 (python, rigor `exact`): Decision of the unique k=13 stage-A survivor (10,10,10,10,10,12,12,12,12,24,36,40,45): exhaustive residue search (INFATTIBILE, 154235 nodes, 4.6 s) and enumeration of all minimal residue-infeasible sub-multisets (smallest has 7 classes; all sub-multisets of size <= 6 are feasible). Output in runs/p4_c4/sandbox/k13_sopravvissuto.txt. Command: python parte_minima.py 10 10 10 10 10 12 12 12 12 24 36 40 45 (23 s).

## 4. Sources and contribution
- Problem statement of Problema 4 (definitions and criterion (*)), problema-4/enunciato.md
- K. O'Bryant, On Z.-W. Sun's disjoint congruence classes conjecture, arXiv:math/0604347v2 (2006), read in full (PDF): Theorem 3 (k ≤ 20; minimal counterexample has k ∉ {24,30}), Lemma 5 (density criterion, attributed to Huhn–Megyesi), Lemma 6 items 1–8, Mathematica 'Grow' search — used for comparison and for the statement/proof idea of Lemma B and rules M4/M5 (all reproved above); nothing relied upon
- J. Fornal, Y.-C. Sun, On the problem of large gcd for disjoint residue classes, arXiv:2607.24655v1, read (intro + Lemma 4.1): asymptotic only; context and pointer to O'Bryant
- A. P. Huhn, L. Megyesi, On disjoint residue classes, Discrete Math. 41 (1982) — cited by O'Bryant as origin of the density criterion; NOT read by us
- Approved submission problema-4/submission/parte-3.en.md (cell 3 method), read; not relied upon (cell 4 re-proves k ≤ 8)
- Position with respect to the literature: Fornal–Sun arXiv:2607.24655 (read in full via the PDF): asymptotic bound max gcd ≫ k·exp(−(2+o(1))√(log k/log log k)); their Lemma 4.1 is asymptotic and gives nothing at fixed small k; they cite O'Bryant for k ≤ 20. O'Bryant, arXiv:math/0604347v2 (read in full): proves the statement for k ≤ 20 and that a minimal counterexample has k ∉ {24,30}, using a modulus-only method: Lemma 5 (= our Lemma B, stated with the Huhn–Megyesi reference), Lemma 6 (items 1–8, several requiring minimality of k and of Σm_i) and a week-long Mathematica search 'Grow' for k ≤ 19 applying Lemma 5 only with M = lcm of the gcds of each subset. Our method ADAPTS his: (i) Lemma A gives his items 1 and 3 without any minimality assumption; (ii) Lemma B is applied with ALL divisors M of L_k that are multiples of the gcd-lcm (strictly stronger pruning; his whole k ≤ 19 search is replaced by seconds); (iii) we add a residue stage, which is needed: at k = 13 the modulus-only rules (R1)–(R3) leave one tuple, and so do the rules with his items 4–5 added (tested: 669 090 nodes, same single survivor). Tested agreement with O'Bryant: k ≤ 12 both give 'no counterexample'; at k = 13 we could not reproduce a modulus-only refutation of (10,10,10,10,10,12,12,12,12,24,36,40,45) from his paper (we did not run his code), but our stage B decides it, so nothing we claim depends on him. Abstracts 2603.26043, 1511.04293 (disjoint covering systems) and 2608.15873 (group form, tuple (6,6,6,10,15)) are not relevant to this cell.

## 5. Limits and unresolved parts
Referee's blocking point: —
Next step required: Provide the missing review or independently checked evidence
Gaps declared by the author:
- k = 14, 15, 16: the cell asks for a report on these sizes; the searches (unconditional and with M4/M5, 600 s per size) had not finished when this attempt was written (only the k = 13 lines are in run_k13_16_incond.txt / run_k13_16_m45.txt); the report for them is 'unfinished, no claim'. The Referee should read the final files from disk.
- Non-vacuity at threshold 12: of the 57 stage-A survivors, 21 feasible, 20 infeasible, 2 NON_DECISO (node budget 3e6) and 14 not reached within the 590 s cap. This affects only the non-vacuity demonstration, not the proof (which is at threshold 11).
- The exhaustiveness rests on the correctness of ~100 lines of Python in stage A (enumeration invariant argued in prose only); there is no second, independently written implementation in this attempt (required for cell 5, not for cell 4).
- The k = 13 'no smaller part forces the decision' claim is by exhaustive computation over all sub-multisets of size <= 6 (each found feasible), not by hand; the hand proof covers only the 7-class part.
- The comparison with O'Bryant is by reading his paper, not by running his Mathematica code.
- The code_used text of ricerca_moduli_hm.py is the version that produced the tabulated counts; the on-disk file was later extended with a time limit and optional flags (default off) and re-checked to give identical counts for k = 9, 10, 11, 13.
