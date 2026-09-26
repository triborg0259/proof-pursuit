Problem 1 — Part 3 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proved beyond what is written.

1. Result and scope

Official request.

Parte 3 — $d+1$ lines in $\mathbb{R}^d$

Punteggio: 3 points · Valutazione: Judged

The first case in every dimension: one line more than the dimension, $N = d+1$, where the conjectured optimum
repeats exactly one of the $d$ coordinate axes. Let $d \ge 1$. Prove that any $d+1$ lines in $\mathbb{R}^d$ satisfy
$$S \;\le\; \left( \binom{d+1}{2} - 1 \right) \cdot \frac{\pi}{2}.$$

What we deliver. Reduction of the statement to an inequality on the deficits $\delta_{ij}=\pi/2-\theta_{ij}$: the claim is equivalent to $\sum_{i<j}\delta_{ij}\ge\pi/2$ for $d+1$ unit vectors in $\mathbb R^d$. The lemma of part 2 (proved and approved) provides exactly a total deficit $\ge\pi/2$ along a chain. The case $d=1$ is trivial (two coincident lines, $S=0$).

2. Proof

Fact 1 (proved, part 2). A chain of $m$ unit vectors in $\mathbb R^{m-1}$ has $\sum\theta(x_i,x_{i+1})\le(m-2)\pi/2$, i.e. total deficit over consecutive steps $\ge\pi/2$.

Fact 2 (proved). $d+1$ unit vectors in $\mathbb R^d$ are linearly dependent; there exists a minimal circuit $x_{i_1},\dots,x_{i_m}$ ($m\le d+1$) with $\sum a_j x_{i_j}=0$, $a_j\ne0$, and any $m-1$ of them independent.

Strategy (not completed). Build from the circuit a chain of $m$ unit vectors in a space of dimension $m-1$ (successive projections onto the orthogonal complements of $\mathrm{span}(x_{i_1},\dots,x_{i_k})$) and compare the angles of the chain with the original ones via the spherical triangle inequality; the direct comparison loses a term $\sum_i\delta_i$ for each projection and is not enough: a better choice of the circuit ordering or a finer estimate is needed. Numerical check (harness, problema-1/esperimenti): no configuration found exceeds the bound for $d\le6$.

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; each script runs in under one minute):
- problema-1/esperimenti/lines_Rd.py
- problema-1/esperimenti/p1_somma_angoli.py

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); abstract only read.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); abstract only read.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); abstract only read.
Bilyk–Matzke [1801.07837] claim only the planar case as solved; Lim–McCann [2007.08698] treat a one-parameter deformation: the case $N=d+1$ does not appear to be known, consistent with the fact that the competition provides the lemma of part 2 as a building block.

5. Limits and unresolved parts

The step from generic lines to a chain without loss of deficit is missing. The approved parts 1–2 remain usable as hypotheses.

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

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p1_c3.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p1_c3.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
