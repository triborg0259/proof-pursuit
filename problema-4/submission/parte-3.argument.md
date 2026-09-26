Problem 4 — Part 3 — submission

Declared status: SOLVED (approved). Complete proof; automatic Referee READY_FOR_HUMAN (judge A, mathematics: PASS;
judge B, evidence: PASS; code re-run by the orchestrator); human approval recorded in runs/p4_c3/approval.json.

1. Result and scope

Complete proof of the cell-3 statement for every k in {3,...,8}: (i) Lemma 1 reduces any size-k counterexample (all gcds ≤ 7) to a family with moduli dividing 420, identical pairwise gcds, still pairwise disjoint — full proof given; (ii) exhaustive enumeration of all k-cliques of the compatibility graph on the 1343 reduced classes finds no clique for k=3..8, with exhaustiveness certificate: finite set + proof (Corollary 2), no pruning beyond the definition, node counts (7118 / 20241 / 56208 / 234719 / 806717 / 3523544), wall clock (2.5 s total, Apple M4, Python 3.14.7), rerun reproducing all counts exactly, zero survivors; (iii) the unmodified machinery with threshold k recovers the trivial partition (non-vacuity); (iv) an independent second implementation agrees; (v) hand proofs for k=3 and k=4 included so the cell does not depend on cells 1–2.

2. Proof

Statement proved

Theorem. Let $3 \le k \le 8$ and let $a_1 \pmod{m_1},\dots,a_k \pmod{m_k}$ be pairwise disjoint congruence classes ($m_i\ge 1$). Then $\gcd(m_i,m_j)\ge k$ for some $i<j$.

Throughout, a counterexample of size $k$ is a pairwise disjoint family of $k$ classes with $\gcd(m_i,m_j)\le k-1$ for all $i<j$. We use only the definitions and the criterion $(*)$ from the problem statement: two classes meet iff $\gcd(m_i,m_j)\mid a_i-a_j$.

Step 0. Two preliminary facts

(P1) In a pairwise disjoint family with $k\ge2$, every $m_i\ge 2$. Indeed, if $m_i=1$ then $\gcd(m_i,m_j)=1\mid a_i-a_j$ for any $j\neq i$, so the classes $i,j$ meet by $(*)$.

(P2) Every integer $g$ with $1\le g\le 7$ divides $N:=420=2^2\cdot3\cdot5\cdot7$. (Check: $420=1\cdot420=2\cdot210=3\cdot140=4\cdot105=5\cdot84=6\cdot70=7\cdot60$.)

Step 1. Reduction lemma (the finite set)

Lemma 1. Let $a_1 \pmod{m_1},\dots,a_k \pmod{m_k}$ ($k\ge2$) be pairwise disjoint with $g_{ij}:=\gcd(m_i,m_j)\le 7$ for all $i<j$. Put $m_i':=\gcd(m_i,N)$ with $N=420$ and $a_i':=a_i \bmod m_i'$ (so $0\le a_i'<m_i'$). Then:

1. $m_i' \mid 420$ and $m_i'\ge 2$;
2. $\gcd(m_i',m_j')=g_{ij}$ for all $i<j$;
3. the classes $a_1' \pmod{m_1'},\dots,a_k'\pmod{m_k'}$ are pairwise disjoint;
4. the $k$ pairs $(a_i',m_i')$ are pairwise distinct.

Proof. (2): $\gcd(m_i',m_j')=\gcd(\gcd(m_i,N),\gcd(m_j,N))=\gcd(m_i,m_j,N)=\gcd(g_{ij},N)$. Since $1\le g_{ij}\le 7$, (P2) gives $g_{ij}\mid N$, hence $\gcd(g_{ij},N)=g_{ij}$.

(1): $m_i'\mid N$ by definition. For any $j\ne i$, $g_{ij}\mid m_i$ and $g_{ij}\mid N$, so $g_{ij}\mid m_i'$; by (P1) applied to the original family, $g_{ij}\ge 2$ — more precisely, disjointness of classes $i,j$ and $(*)$ give $g_{ij}\nmid a_i-a_j$, which is impossible for $g_{ij}=1$; hence $g_{ij}\ge2$ and $m_i'\ge g_{ij}\ge2$.

(3): Fix $i<j$. By (2), $\gcd(m_i',m_j')=g_{ij}$. Since $g_{ij}\mid m_i'$ and $g_{ij}\mid m_j'$ (shown in (1)), and $a_i'\equiv a_i \pmod{m_i'}$, $a_j'\equiv a_j\pmod{m_j'}$, we get $a_i'-a_j'\equiv a_i-a_j \pmod{g_{ij}}$. The original classes are disjoint, so by $()$ $g_{ij}\nmid a_i-a_j$, hence $g_{ij}\nmid a_i'-a_j'$, and by $()$ again the reduced classes $i,j$ are disjoint.

(4): Two equal pairs would be the same nonempty class, contradicting (3). $\square$

Corollary 2. If a counterexample of size $k$ exists with $3\le k\le8$, then there exist $k$ pairwise distinct pairs $(a_i,m_i)$ with $m_i\mid 420$, $m_i\ge2$, $0\le a_i<m_i$, such that for every $i<j$: $\gcd(m_i,m_j)\le k-1$ and $\gcd(m_i,m_j)\nmid a_i-a_j$.

Proof. In a counterexample of size $k\le 8$ all $g_{ij}\le k-1\le 7$, so Lemma 1 applies; its conclusions (1)–(4) together with the preserved gcds (2) give exactly the listed properties. $\square$

Step 2. The finite search and its certificate

Finite set (certificate item 1). Let $V=\{(a,m): m\mid 420,\ m\ge2,\ 0\le a<m\}$. Then $|V|=\sigma(420)-1=1344-1=1343$ (the script prints vertici=1343). For each $k\in\{3,\dots,8\}$ let $G_k$ be the graph on $V$ with an edge between $(a,m)$ and $(a',m')$ iff
$$\gcd(m,m')\le k-1\quad\text{and}\quad \gcd(m,m')\nmid (a-a').$$
By Corollary 2, a counterexample of size $k$ yields a $k$-clique in $G_k$; so if $G_k$ has no $k$-clique, the Theorem holds for that $k$. Nothing outside $V$ needs to be examined: Lemma 1 maps every counterexample into $V$.

Algorithm. Vertices are indexed $0,\dots,1342$ in a fixed order (moduli increasing, residues increasing). adj[i] is the bitset of indices $j>i$ adjacent to $i$ in $G_k$, computed directly from the definition with exact integer arithmetic (math.gcd, %). The recursion ricorsione(parziale, candidati) starts with the empty tuple and the candidate set $=V$; it iterates over candidates $j$ in increasing order and recurses with parziale+[j] and candidati & adj[j].

Correctness (every $k$-clique is found). By induction on the length of parziale: the invariant is that candidati equals the set of indices greater than the last element of parziale (all of $V$ if it is empty) that are adjacent to every element of parziale. Initially true. If it holds for parziale and $j$ is a candidate, then candidati & adj[j] is the set of indices that are $>j$ (since adj[j] only contains indices $>j$), adjacent to every element of parziale (since they are in candidati) and adjacent to $j$; this is the invariant for parziale+[j]. Therefore every increasing tuple $(v_1<\dots<v_k)$ of pairwise adjacent vertices is visited (each $v_{t+1}$ lies in the candidate set of the prefix $(v_1,\dots,v_t)$), and it is visited exactly once (a tuple is reached only through its unique chain of prefixes). Every $k$-clique of $G_k$ is exactly one such tuple. Whenever len(parziale)==k the tuple is recorded as a survivor.

Pruning rules (certificate item 2). None beyond the definition: a partial tuple is extended only by vertices adjacent (in $G_k$) to all its members. A set containing a non-adjacent pair contains either two classes that meet or a pair with gcd $\ge k$, so it is not (a reduction of) a counterexample; hence nothing that can be completed to a counterexample is discarded. No symmetry reduction, no ordering heuristic beyond the fixed vertex order, no extra rules.

Node counts and wall clock (certificate item 3). A node is one recursive call with nonempty parziale, i.e. the number of nonempty pairwise-adjacent increasing tuples of length $\le k$ (so it equals $\sum_{t=1}^{k}\#\{t\text{-cliques of }G_k\}$; e.g. for $k=3$: $7118 = 1343 + 5775 + 0$, i.e. $G_3$ has 5775 edges and no triangle). Run 1 (run1.txt), Apple M4, Python 3.14.7, exact integer arithmetic:

- $k$ · gcd threshold $\le k-1$ · vertices · nodes · survivors · time
- 3 · 2 · 1343 · 7118 · 0 · 0.10 s
- 4 · 3 · 1343 · 20241 · 0 · 0.11 s
- 5 · 4 · 1343 · 56208 · 0 · 0.12 s
- 6 · 5 · 1343 · 234719 · 0 · 0.20 s
- 7 · 6 · 1343 · 806717 · 0 · 0.46 s
- 8 · 7 · 1343 · 3523544 · 0 · 1.51 s
Total wall clock of the whole certificate run: 2.5 s (far below the 10-minute limit). Command: .venv/bin/python runs/p4_c3/sandbox/ricerca_clique_420.py certificato.

Rerun (certificate item 4). A second run (run2.txt) reproduced every node count and survivor count exactly (verified by diff after stripping the timing field: IDENTICI); times were 0.10/0.11/0.12/0.20/0.43/1.50 s.

Survivors (certificate item 5). None at any $k\in\{3,\dots,8\}$, so there is nothing to decide.

Conclusion of Step 2. For each $k\in\{3,\dots,8\}$, $G_k$ has no $k$-clique; by Corollary 2 there is no counterexample of size $k$, i.e. the Theorem holds for $k=3,4,5,6,7,8$. $\blacksquare$

Step 3. Non-vacuity of the machinery (not required for C3, included as evidence the code is not silently broken)

Running the same, unmodified enumeration with the gcd threshold relaxed from $k-1$ to $k$ (mode non_vacuita), the trivial partition $0,1,\dots,k-1 \pmod k$ — which is an admissible configuration with all gcds equal to $k$ — is found among the cliques: $k=3$: 6688 cliques, $k=4$: 7917, $k=5$: 17856, $k=6$: 17329, $k=7$: 34056 (universe $N=420$), each run printing partizione banale trovata: True. For $k=8$ the modulus 8 does not divide 420, so the universe was enlarged to the divisors of 840 (2879 vertices): 32 097 759 nodes, 58 425 cliques, 14.7 s, trivial partition found. (The certificate of Step 2 uses only $N=420$, which Lemma 1 justifies for gcds $\le7$.)

Step 4. Independent second implementation (cross-check, not part of the certificate)

ricerca_moduli_residui.py uses a different algorithm: it first enumerates non-decreasing $k$-tuples of moduli (divisors of 420, $\ge2$) with all pairwise gcds in $[2,\text{threshold}]$, then solves the residue CSP $a_i\not\equiv a_j \pmod{\gcd(m_i,m_j)}$ by backtracking with the translation normalisation $a_1=0$. For thresholds $k-1$ it examined 51, 77, 221, 293, 1249, 1668 modulus tuples for $k=3,\dots,8$ and found 0 families in every case (2.9 s total). With threshold $k$ it finds e.g. $((0,3),(1,3),(2,3))$, $((0,5),\dots,(4,5))$, $((0,7),\dots,(6,7))$. Its counts are not directly comparable with those of the clique search (different normalisation); only the zero/non-zero outcomes are compared, and they agree.

Step 5. Hand proofs for $k=3$ and $k=4$ (so the cell does not depend on cells 1–2 being accepted)

$k=3$. Suppose three pairwise disjoint classes have all $g_{ij}\le 2$. By (P1)-type reasoning ($g_{ij}=1$ would force the classes to meet), $g_{ij}=2$ for all pairs, so $g_{ij}\nmid a_i-a_j$ says $a_i-a_j$ is odd for all $i<j$. Then $a_1,a_2,a_3$ have pairwise different parities, impossible for three integers with only two parities. Hence some $g_{ij}\ge3$.

$k=4$. Suppose four pairwise disjoint classes have all $g_{ij}\in\{2,3\}$ (values $\le3$ and $\ne1$). Let $E=\{i: 2\mid m_i\}$, $T=\{i:3\mid m_i\}$.
(a) If $g_{ij}=2$ then $i,j\in E$; if $g_{ij}=3$ then $i,j\in T$. Hence every pair lies in $E$ or in $T$.
(b) If $i\ne j$ both lie in $E\cap T$ then $6\mid g_{ij}$, contradicting $g_{ij}\le3$; so $|E\cap T|\le1$.
(c) Two indices $i,j\in E$ have $2\mid g_{ij}$, so $g_{ij}=2$ and $a_i\not\equiv a_j\pmod 2$; thus residues mod 2 of $E$ are distinct and $|E|\le2$. Similarly for $i,j\in T$, $3\mid g_{ij}$ gives $g_{ij}=3$ and $a_i\not\equiv a_j \pmod 3$, so $|T|\le3$.
(d) By (a) no $i\in E\setminus T$ and $j\in T\setminus E$ can coexist (the pair would lie in neither $E$ nor $T$). Hence $E\subseteq T$ or $T\subseteq E$; with (a) (every index lies in $E\cup T$, as it forms a pair with some other index) we get $\{1,2,3,4\}=T$ or $\{1,2,3,4\}=E$, contradicting $|T|\le3$, $|E|\le2$. Hence some $g_{ij}\ge4$.

(These two cases are also covered by the search at $k=3,4$.)

Scope and honesty

Claimed: the Theorem for $k=3,4,5,6,7,8$ (cell 3 in full, including the sizes of cells 1–2). Certified by: Lemma 1 (complete proof above) + exhaustive enumeration with the certificate items 1–5 + rerun. Nothing is claimed for $k\ge9$; the reduction to $N=420$ is valid only for gcds $\le7$, and for larger $k$ one would use $N=\mathrm{lcm}(1,\dots,k-1)$ in Lemma 1 (same proof).

3. Verification: instructions, dependencies, timings

Python 3 standard library only. Scripts (also saved in runs/p4_c3/sandbox/ and re-run in runs/p4_c3/verifica/):
- code_1 (python, rigor exact): Implementation 1 (certificate): exhaustive enumeration of all k-cliques in G_k on the 1343 classes (a,m), m|420, m>=2; no pruning beyond the edge definition; prints node counts, survivors, wall clock; mode non_vacuita relaxes the gcd threshold to k and checks that the trivial partition 0..k-1 (mod k) is found. File runs/p4_c3/sandbox/ricerca_clique_420.py; outputs run1.txt, run2.txt, non_vacuita.txt, non_vacuita_k8_N840.txt.
- code_2 (python, rigor exact): Implementation 2 (independent cross-check, different method): enumerate non-decreasing k-tuples of moduli dividing 420 with pairwise gcd in [2, threshold], then solve the residue CSP a_i != a_j (mod gcd) by backtracking with a_1 = 0. Found 0 families at thresholds k-1 for k=3..8 (51, 77, 221, 293, 1249, 1668 modulus tuples examined; 2.9 s total) and finds the trivial partitions at threshold k. File runs/p4_c3/sandbox/ricerca_moduli_residui.py; outputs impl2_run1.txt, impl2_non_vacuita.txt.

Trusted re-runs by the orchestrator (exit code, wall clock, output):
- orchestrator re-ran code_1.py (python3, clean copy of the researcher sandbox): exit 0 in 2.5s; stdout: 'k=3 soglia_gcd<=2 vertici=1343 nodi=7118 sopravvissuti=0 tempo=0.10s\nk=4 soglia_gcd<=3 vertici=1343 nodi=20241 sopravvissuti=0 tempo=0.10s\nk=5 soglia_gcd<=4 vertici=1343 nodi=56208 sopravvissuti
- orchestrator re-ran code_2.py (python3, clean copy of the researcher sandbox): exit 0 in 3.0s; stdout: 'k=3 soglia_gcd<=2 multinsiemi_moduli=51 famiglie(a1=0)=0 tempo=0.00s\nk=4 soglia_gcd<=3 multinsiemi_moduli=77 famiglie(a1=0)=0 tempo=0.00s\nk=5 soglia_gcd<=4 multinsiemi_moduli=221 famiglie(a1=0)=

4. Sources and contribution

- Problem statement of Problema 4 (criterion (*) and definitions), file problema-4/enunciato.md
- arXiv:2607.24655 (Fornal–Sun) — abstract only, used for literature_position, no result relied upon
- arXiv:2608.15873 (Menon) — abstract only, context for the group form, no result relied upon
- Position with respect to the literature: The listed abstracts do not settle this cell in a usable way: [2607.24655] (Fornal–Sun) proves the asymptotic bound max gcd ≫ k·exp(−(2+o(1))√(log k/log log k)), which is relevant to C6(b), not to small k; [2608.15873] (Menon) concerns the group form (C6(c)) and the tuple (6,6,6,10,15); [2603.26043] and [1511.04293] concern disjoint covering systems with one repeated modulus, unrelated to the gcd question. I did not read the full papers and cite nothing from them; my approach (finite reduction + exhaustive certified search) follows the column's own hand-in rules rather than any of these papers. I recall that the k ≤ 8 case is probably classical (Huhn–Megyesi / Z.-W. Sun on disjoint residue classes) but I have not verified any such source, so I do not cite it as read and I rely on it for nothing.
- Contribution: the proof above is written out in full by the team's Researcher and checked by two independent judges and by a human.

5. Limits and unresolved parts

Gaps declared by the author (all accepted by the judges):
- The search is only as exhaustive as the code is correct; I proved the enumeration invariant in prose (Step 2) but a hostile reader must still read the ~80 lines of Python. The independent second implementation and the non-vacuity runs mitigate but do not replace this.
- The k=8 non-vacuity check needed a larger universe (divisors of 840) because 8 does not divide 420; this is expected from Lemma 1 (valid only for gcds ≤ 7) and does not affect the certificate, but it is a deviation from 'run the machinery unmodified' in the strict C5 sense (not required for C3).
- The survivor counts of the two implementations in non-vacuity mode are not directly comparable (unordered cliques vs. a_1=0-normalised ordered families with repeated moduli), so the cross-check compares only zero/non-zero outcomes at thresholds k−1, plus presence of the trivial partition.
- Literature: I did not fetch or read the full papers listed; I recall that the small-k cases are probably classical (Huhn–Megyesi / Z.-W. Sun) but have not verified this and rely on it for nothing.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family exact_computation, subgoal: Prove the statement for every k with 3 ≤ k ≤ 8 (self-contained, not relying on cells 1–2 being verified): reduction lemma to moduli dividing 420 with pairwise gcds preserved, then a fully certified exhaustive clique search (finite set, proof of exhaustiveness, no pruning beyond the definition, node counts, wall clock, rerun, zero survivors), plus hand proofs for k=3,4 and a non-vacuity test.; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: First natural subgoal (no blocker recorded, no verified claims). The hand-in rules of this column explicitly admit a computation with an exhaustiveness certificate; the only genuinely mathematical step is the finite reduction, which I prove in full. I deliberately used NO pruning beyond the definition of a counterexample (so rule 2 of the certificate is trivially satisfied) and no symmetry reduction, because the search is small (3.5 million nodes at k=8). Since highest_verified_cell = 0, I do not assume cells 1–2 and give short hand proofs for k=3,4 as well; the computation covers them independently.
  - Position w.r.t. the literature: The listed abstracts do not settle this cell in a usable way: [2607.24655] (Fornal–Sun) proves the asymptotic bound max gcd ≫ k·exp(−(2+o(1))√(log k/log log k)), which is relevant to C6(b), not to small k; [2608.15873] (Menon) concerns the group form (C6(c)) and the tuple (6,6,6,10,15); [2603.26043] and [1511.04293] concern disjoint covering systems with one repeated modulus, unrelated to the gcd question. I did not read the full papers and cite nothing from them; my approach (finite reduction + exhaustive certified search) follows the column's own hand-in rules rather than any of these papers. I recall that the k ≤ 8 case is probably classical (Huhn–Megyesi / Z.-W. Sun on disjoint residue classes) but I have not verified any such source, so I do not cite it as read and I rely on it for nothing.
  - Referee: UNKNOWN_STATUS / READY_FOR_HUMAN; next: Human reviews the exact target, proof and evidence, then approves explicit claims
- Human approval: Thomas Tumini (human) at 2026-09-26T15:08:50 (READY_FOR_HUMAN → ACCEPT).

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c3.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c3.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
