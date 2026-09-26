# Problem 1 — Part 6 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proved beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 6 — $N$ lines in $\mathbb{R}^d$

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Fejes Tóth's conjecture from the Setting, for every $N$ and every $d$. For $N$ lines in $\mathbb{R}^d$, write
$N = qd + s$ with $0 \le s < d$, and let
$$
M(N,d) = s \binom{q+1}{2} + (d-s) \binom{q}{2}.
$$
Prove or disprove: every $N$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{N}{2} - M(N,d) \right) \frac{\pi}{2}.
$$
This is the value attained by splitting the lines as evenly as possible among $d$ mutually orthogonal
directions. Settling any infinite family not already covered above counts as partial progress.

*(End of problem 1. Scores: 1+2+3+5+8+13 = 32.)*

**What we submit.** Open problem. No new infinite family. Contribution: numerical verification of the bound for $N\le10$ in the plane (harness) and setup of the counterexample search.

## 2. Proof
Full Fejes Tóth conjecture. With the numerical harness (`tools/autoloop.py`, hill climbing with restarts) the maximum found coincides with the conjectured value within $2\cdot10^{-5}$ for all cases tested; no exceedance. This is not a proof (floating point).

## 3. Verification: instructions, dependencies, timings
Code available (Python 3, standard library; each script runs in under one minute):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); abstract only read.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); abstract only read.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); abstract only read.
Bilyk–Matzke [1801.07837]: general bound via energy and reduction from high to low dimension; Lim–McCann [2007.08698]: equivalence with the uniqueness of the optimizer for every $\alpha>1$, proved for $\alpha=\infty$.

## 5. Limits and unresolved parts
Everything.
