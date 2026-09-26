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
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

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
