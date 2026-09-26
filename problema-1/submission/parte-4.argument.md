Problem 1 — Part 4 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proved beyond what is written.

1. Result and scope

Official request.

Parte 4 — Five lines in $\mathbb{R}^3$, six in $\mathbb{R}^4$

Punteggio: 5 points · Valutazione: Judged

Two concrete instances of the next case, $N = d+2$: five lines in three dimensions and six lines in four.
In each, the conjectured optimum repeats two of the coordinate axes. Prove that any $5$ lines in $\mathbb{R}^3$
satisfy $S \le 4\pi$, and that any $6$ lines in $\mathbb{R}^4$ satisfy $S \le 13\pi/2$.

What we deliver. No proof. Reformulation: both instances are the case $N=d+2$, equivalent to total deficit $\ge\pi$. Numerical verification (not a proof) of the bound on both instances.

2. Proof

The two required inequalities are the cases $(d,N)=(3,5)$ and $(4,6)$ of part 5. With $\delta_{ij}=\pi/2-\theta_{ij}=\arcsin|\langle x_i,x_j\rangle|$ the claims become $\sum_{i<j}\delta_{ij}\ge\pi$. Computational route allowed by the cell: rigorous maximization of $S$ over $(S^2)^5$ and $(S^3)^6$ with interval arithmetic and branch-and-bound; 7 and 12 free parameters after symmetries, with non-smooth maxima (orthogonal or coincident pairs), so a local argument around the optima is needed. Set up, not executed: the case in $\mathbb R^4$ is at the limit of the 10 minutes.

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; each script runs in under one minute):
- problema-1/esperimenti/lines_Rd.py
- problema-1/esperimenti/p1_somma_angoli.py

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); abstract only read.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); abstract only read.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); abstract only read.
Fejes Tóth (1959) covers $\mathbb R^3$ with $N\le6$ according to Bilyk–Matzke [1801.07837]: the first instance is known in the literature, but the citation does not count as a proof.

5. Limits and unresolved parts

Both instances: proof missing. Realistic route: deduce them from part 5 or complete the interval branch-and-bound for $\mathbb R^3$.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018), found by query angles between lines; abstract read, full text not relied upon.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020), found by query angles between lines; abstract read, full text not relied upon.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012), found by query angles between lines; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p1_c4.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp1_c4.tex&snip_name=p1_c4.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p1_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
