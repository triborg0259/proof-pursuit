Problem 3 — Part 3 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proven beyond what is written.

1. Result and scope

Official request.

Part 3 (C3) — A general upper bound

Score: 3 points · Evaluation: Judged

Now the numbers strictly between two consecutive triangular numbers. Prove that for every $k \ge 4$ and every
non-triangular $n$ with $T_{k-1} < n < T_k$,
$$D_B(n) \le k^2 - 2k - 1,$$
and determine $D_B(T_k - 1)$ exactly. Determine also, for that $n$, which partitions attain the maximum.

What we deliver. No proof. Plan: exact table of $D_B(n)$ for $n\le60$ with extremal partitions, then formula and proof.

2. Proof

Exact computation on the functional graph of partitions (integers, no numerical error), with two implementations (partitions as tuples; cards in position on the diagram). Conjecture to be confirmed: $D_B(T_k-1)$ and the explicit extremals in $k$. Not carried out within the competition time.

3. Verification: instructions, dependencies, timings

Code available (Python 3, standard library; each script runs in under one minute):
- No code yet.

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
Griggs–Ho (1998) probably contain the bound $k^2-2k-1$: to be verified, not read.

5. Limits and unresolved parts

Everything except the plan.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family direct_proof, subgoal: Prove the general upper bound D_B(n) ≤ k^2−2k−1 for every non-triangular n of rank k ≥ 4, and prove D_B(T_k−1) = k^2−2k−1 exactly (lower bound via an explicit partition λ*_k), as a single self-contained argument (Brandt's characterisation of cyclic partitions re-proved inside).; declared LEMMA_CANDIDATE.
  - Why this approach: No blocker and no verified claims: the natural first subgoal is the whole quantitative content of the cell (general bound + exact value at T_k−1). The literature (Griggs–Ho 1998) contains a proof sketch of exactly this bound; the rules allow a proof 'written out in full, whatever its source', so I fetched the preprint, reconstructed every lemma in a cleaner language, filled the gaps (their proof of Brandt's theorem is a sketch; their Lemma 3.5 statement contains an unused/incorrect constraint q' ≤ p+1 which I dropped; their Lemma 3.3 uses Theorem 2.1 in a way I replaced by an explicit recognition lemma), and verified numerically that the value is k^2−2k−1 (an off-by-one bug in my first table, which suggested k^2−2k−2, was found and fixed by comparing with Griggs–Ho's Figure 1). The characterisation of all extremal partitions of T_k−1 is deliberately left for a later iteration.
  - Position w.r.t. the literature: The arXiv abstracts listed (math/0401385, 1503.00885, 2607.17194, 1101.1546, 1703.07102, 2208.14496) do not treat D_B(n) for non-triangular n; 2607.17194 and 1503.00885 are surveys citing Brandt (1982) for the cyclic partitions, 1101.1546 concerns Toom's convergence proof. The relevant source is not on arXiv: J. R. Griggs, C.-C. Ho, 'The cycling of partitions and compositions under repeated shifts', Adv. Appl. Math. 21 (1998) 205–227 (doi:10.1006/aama.1998.0597); I downloaded and read the authors' preprint (people.math.sc.edu/griggs/cycling.pdf, dated Mar. 2, 1998). Its Theorem 4.4 states: '(1) D_B(n) ≤ k^2−2k−1 for k ≥ 4 [n = 1+…+(k−1)+r, 1 ≤ r < k]; (2) equality holds when k ≥ 4 and r = k−1', with the extremal partition λ_1=k−1, λ_2=k−2, λ_i=k−i+1 (3≤i≤k), λ_{k+1}=1 and the remark 'imitating the proof of Theorem 3.1, we can show d_B(λ)=k^2−2k−1' (no details). My attempt FOLLOWS Griggs–Ho's strategy but reproduces every proof in full (as required: citing does not count), in a 'pile lifetime' formalism equivalent to their diagram_B; it ADAPTS their Lemma 3.5 (dropping the constraint q' ≤ p+1, which their own proof does not establish and which is not needed) and their Theorem 2.1 proof (their CRT sketch is written out with the potential Φ), and SUPPLIES the omitted lower-bound orbit computation for λ*_k. Griggs–Ho give, for triangular n, only necessary conditions on extremal partitions (their Thm 3.8, converse false for k=8) and nothing for T_k−1, consistent with my leaving that sub-question open.
  - Referee: UNKNOWN_STATUS / INCOMPLETE; next: Provide the missing review or independently checked evidence

6b. Tokens used by the agents

- Referee judge B: input 43,265 · output (incl. reasoning) 3,993
- Total: input 43,265 · output 3,993 tokens

7. arXiv literature consulted

- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022), found by query Bulgarian solitaire; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p3_c3.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp3_c3.tex&snip_name=p3_c3.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c3.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
