# Problem 1 — Part 5 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proven beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 5 — $d+2$ lines in $\mathbb{R}^d$

**Punteggio:** 8 points · **Valutazione:** Judged

The case $N = d+2$ in every dimension, with the same conjectured optimum: the $d$ coordinate axes, two of them
repeated. Prove that for every $d \ge 2$, any $d+2$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{d+2}{2} - 2 \right) \frac{\pi}{2}.
$$

**What we deliver.** No proof. Reformulation in terms of deficits ($\sum\delta_{ij}\ge\pi$) and sanity check of the values.

## 2. Proof
The claim is equivalent to: $d+2$ unit vectors in $\mathbb R^d$ have total deficit $\ge\pi$. If part 3 is obtained by reduction to a chain (deficit $\ge\pi/2$), the natural route is to iterate the reduction over two independent circuits of the linear dependence (rank $\le d$ among $d+2$ vectors: the space of relations has dimension $\ge2$). Not developed.

## 3. Verification: instructions, dependencies, timings
Available code (Python 3, standard library; each script runs in under one minute):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); abstract only read.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); abstract only read.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); abstract only read.
Not known to be established (Bilyk–Matzke [1801.07837]; Lim–McCann [2007.08698]).

## 5. Limits and unresolved parts
Depends on part 3.


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

## 6b. Tokens used by the agents
- Token counts not recorded for this run (older harness version; only cost and turns were logged).

## 7. arXiv literature consulted
- arXiv:1801.07837v1 — *On the Fejes Tóth Problem about the Sum of Angles Between Lines* (Dmitriy Bilyk, Ryan W Matzke, 2018), found by query `angles between lines`; abstract read, full text not relied upon.
- arXiv:2007.08698v2 — *On Fejes Tóth's conjectured maximizer for the sum of angles between lines* (Tongseok Lim, Robert J. McCann, 2020), found by query `angles between lines`; abstract read, full text not relied upon.
- arXiv:1204.3850v1 — *Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons* (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012), found by query `angles between lines`; abstract read, full text not relied upon.

## 8. Code
See the certificates listed in section 3.

---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p1_c5.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
