Problem 4 — Part 6 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proved beyond what is written.

1. Result and scope

Official request.

Parte 6 (C6) — Beyond the boundary

Punteggio: 13 points · Valutazione: Judged · Open question

Three directions beyond the certified range; any one of them counts. Any of the following.

(a) Decide a size $k \ge 25$.

(b) The asymptotic form. It is known that a pairwise disjoint family of size $k$ always has a pair with
$$\gcd(m_i, m_j) \;\ge\; k \cdot \exp\!\left( -(2 + o(1)) \frac{\log k}{\log\log k} \right),$$
which is $k^{1 - o(1)}$ but not linear in $k$. Prove the statement in full, or prove the weaker bound
$\gcd(m_i, m_j) \ge ck$ for some absolute constant $c > 0$, or improve the exponential factor above.

(c) The group form. Let $G$ be a group, let $G_1, \ldots, G_k$ be subgroups of finite index $n_i = [G : G_i]$,
and let $x_1 G_1, \ldots, x_k G_k$ be pairwise disjoint cosets. Is there a pair $i < j$ with
$\gcd(n_i, n_j) \ge k$? This is known for $k \le 5$ and open for every $k \ge 6$; settling $k = 6$ counts as
progress.

(End of problem 4. Scores: 1+2+3+5+8+13 = 32.)

What we submit. No proof. Relevant remark: the asymptotic bound quoted in the statement has already been improved in the literature.

2. Proof

Fornal–Sun [2607.24655] (July 2026) prove $\max\gcd(m_i,m_j)\gg k\exp(-(2+o(1))\sqrt{\log k/\log\log k})$, with a square root in the exponent: an improvement of the exponential factor requested in (b). Reproducing their proof in full (gcd graph, structural lemma, sieving partition, Möbius inversion, discrete Fourier transform) would count under the rules; not done.

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); abstract only read.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); abstract only read.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); abstract only read.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); abstract only read.
[2607.24655].

5. Limits and unresolved parts

Everything; route (b) via reproduction of the proof is the indicated one.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family induction, subgoal: Establish, with a complete self-contained proof, a quantitative lower bound on the maximal gcd valid for every k (direction (b)): a "prime-splitting recursion" for the maximal size F(g) of a pairwise disjoint family with all pairwise gcds at most g, and the closed bounds F(g) <= g^3 (fully elementary) and F(g) <= g^2  prod_{p<=g}(1+2/p) (hence max gcd >= csqrt(k)/log k with Mertens).; declared LEMMA_CANDIDATE.
  - Why this approach: No blocker, no verified claims and no failed attempts are recorded, so this is the first iteration on an OPEN cell. Of the three directions, (a) needs a certified search at k>=25 that presupposes the cell-5 machinery (nothing verified yet), and (c) (group form, k=6) is an open case-analysis problem. Direction (b) admits a genuinely self-contained, checkable first step: a lower bound valid for all k, proved in full rather than cited. The bound obtained is weaker than the literature (k^{1/2-o(1)} vs k^{1-o(1)}), and I say so; its value is that every step is verifiable, it already re-proves cell 1 (R(2)=2), and it isolates exactly where the loss occurs (the union bound over primes), which is the natural target for the next iteration.
  - Position w.r.t. the literature: State of the art for this cell (direction (b)): arXiv:2607.24655 (Fornal–Sun, 27 Jul 2026), Theorem 1.1, which I fetched and read in part (introduction and section structure, not the full proofs): "Let a_1 (mod m_1),...,a_k (mod m_k) be pairwise disjoint residue classes. Then max gcd(m_i,m_j) >> k exp(-(2+o(1)) sqrt(log k / log log k))." — CITED, not reproduced. Note this is stronger than the bound quoted in the problem statement (exponent log k/log log k without the square root): the square-root version already "improves the exponential factor" asked for in (b); but by the hand-in rules a citation scores nothing, and the paper is ~2000 lines (weighted gcd graph, sieve-theoretic partition Prop. 2.1, Möbius inversion and DFT in Prop. 2.2, key Lemma 4.1), which I judged not reproducible and checkable within one iteration. Its introduction also records (CITED, not checked): O'Bryant proved the integer conjecture for k <= 20 [K. O'Bryant, On Z.-W. Sun's disjoint congruence classes conjecture, Combinatorial Number Theory, de Gruyter 2007, 403–412]; Zhu proved the group form for k=3,4 [Int. J. Mod. Math. 3 (2008)]; Sun proved k=2 and finite p-groups [Internat. J. Math. 17 (2006)]. The problem's statement that the group form is known for k<=5 is consistent with arXiv:2608.15873 (Menon) / Margolis–Schnabel on G-harmonic tuples, relevant only to direction (c). arXiv:2603.26043 and arXiv:1511.04293 concern disjoint covering systems with one repeated modulus and are not relevant here. My approach departs from Fornal–Sun: instead of weighting vertices over all n <= d and using Fourier analysis, it uses only the affine rescaling y -> r+py inside a residue class mod a prime, an elementary recursion, and a closed-form induction. The price is the exponent (1/2 instead of 1-o(1)); the gain is a complete proof.
  - Referee: REJECT / NEEDS_WORK; fatal error: The strongest result actually proved is Corollary 6: max gcd(m_i,m_j) >= k^{1/3} unconditionally, and >= csqrt(k)/log k conditional on Mertens/Rosser–Schoenfeld. The cell-6 target requires one of: (a) deciding a size k >= 25; (b) gcd >= ck for an absolute c > 0, or an improvement of the known factor kexp(-(2+o(1)) log k/log log k) (i.e. something better than k^{1-o(1)}); (c) the group form at k = 6. A bound of order k^{1/2-o(1)} is strictly weaker than the already-known k^{1-o(1)} and does not touch (a) or (c). The submission's own remarks concede that the recursion of Lemma 4 cannot give better than F(g) ≲ g^2/2, i.e. gcd ≳ sqrt(2k), so no route to the target is present. The declared claim 'main' is therefore not established, and no other reusable claim was declared.; next: Address the stated blocking obligation without silently changing the target

6b. Tokens used by the agents

- Researcher attempt_001: input 288,456 · output (incl. reasoning) 39,814
- Referee judge A: input 34,416 · output (incl. reasoning) 4,108
- Referee judge B: input 34,924 · output (incl. reasoning) 3,914
- Total: input 357,796 · output 47,836 tokens

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p4_c6.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp4_c6.tex&snip_name=p4_c6.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c6.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
