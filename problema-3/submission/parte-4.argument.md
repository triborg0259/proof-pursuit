Problem 3 — Part 4 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is declared proven beyond what is written.

1. Result and scope

Official request.

Part 4 (C4) — One above a triangular number

Score: 5 points · Evaluation: Judged

The first family just above a triangular number: $n = T_{k-1} + 1$, that is $n = 11, 16, 22, 29, \ldots$ for
$k = 5, 6, 7, 8, \ldots$. Determine $D_B(T_{k-1} + 1)$ for every $k \ge 5$, with proof of both bounds.

What we deliver. No proof.

2. Proof

Same plan as part 3 on the family $n=T_{k-1}+1$.

2b. Exact finite verification (computed 2026-09-26, integer arithmetic, 8 s for all n up to 56)

Script: problema-3/esperimenti/tabella_DB.py (functional graph on all partitions of $n$, cycles marked, $d_B$ by memoised orbit following); output in tabella_DB.txt. This is VERIFIED ON A FINITE RANGE, not a proof for general $k$.
For every rank $5\le k\le 11$ the exact value is $D_B(T_{k-1}+1)=(k-2)^2-1=k^2-4k+3$ (values 8, 15, 24, 35, 48, 63, 80). Conjectured formula for all $k\ge5$: $D_B(T_{k-1}+1)=k^2-4k+3$.

Values for the family $n=T_{k-1}+1$:
- k=3, n=4: D_B(n)=2; extremal partitions: 1, e.g. (1, 1, 1, 1)
- k=4, n=7: D_B(n)=4; extremal partitions: 1, e.g. (1, 1, 1, 1, 1, 1, 1)
- k=5, n=11: D_B(n)=8; extremal partitions: 3, e.g. (3, 3, 2, 2, 1)
- k=6, n=16: D_B(n)=15; extremal partitions: 12, e.g. (4, 4, 3, 2, 2, 1)
- k=7, n=22: D_B(n)=24; extremal partitions: 62, e.g. (5, 5, 4, 3, 2, 2, 1)
- k=8, n=29: D_B(n)=35; extremal partitions: 288, e.g. (6, 6, 5, 4, 3, 2, 2, 1)
- k=9, n=37: D_B(n)=48; extremal partitions: 1310, e.g. (7, 7, 6, 5, 4, 3, 2, 2, 1)
- k=10, n=46: D_B(n)=63; extremal partitions: 5862, e.g. (8, 8, 7, 6, 5, 4, 3, 2, 2, 1)
- k=11, n=56: D_B(n)=80; extremal partitions: 26399, e.g. (9, 9, 8, 7, 6, 5, 4, 3, 2, 2, 1)

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
As in part 3.

5. Limits and unresolved parts

Everything.

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

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p3_c4.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp3_c4.tex&snip_name=p3_c4.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
