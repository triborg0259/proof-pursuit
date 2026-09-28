# Problema 1 — Angles between lines

*(Enunciato formattato in LaTeX, contenuto fedele all'originale; ricevuto a parti il 2026-09-26.)*

## Preambolo

**Angles between lines.** How large can the sum of pairwise angles between $N$ lines through the origin be?
Fejes Tóth conjectured in 1959 that orthogonal lines win.

A line here always means a line through the origin of $\mathbb{R}^d$. The angle between two lines
$\ell, \ell'$ is the acute (non-obtuse) angle $\theta(\ell,\ell') \in [0,\pi/2]$ between them.
If $\ell, \ell'$ are spanned by unit vectors $x, x'$, then
$$
\theta(\ell,\ell') = \arccos\,\lvert \langle x, x' \rangle \rvert .
$$
For lines $\ell_1, \ldots, \ell_N$ in $\mathbb{R}^d$ (repetitions allowed), write
$$
S(\ell_1,\ldots,\ell_N) = \sum_{1 \le i < j \le N} \theta(\ell_i,\ell_j).
$$
The question is how large $S$ can be. In 1959 L. Fejes Tóth conjectured that $S$ is maximised by taking
$d$ mutually orthogonal lines, each used either $\lfloor N/d \rfloor$ or $\lceil N/d \rceil$ times.
When $N = d + k$ with $0 \le k \le d$, that configuration (the $d$ coordinate axes, $k$ of them used twice) has
$$
S = \left( \binom{N}{2} - k \right) \cdot \frac{\pi}{2},
$$
because exactly $k$ pairs of lines coincide and every other pair is orthogonal.

Each cell below asks you to prove this bound, or a special case of it. Unless a cell says otherwise, you need
a complete proof. Citing a published result for the statement you are asked to prove does not count.

**What to hand in.** For each cell you attempt, hand in a written proof. You may use a computer to explore.
A proof may rely on a computation only if you include the code, it runs in under 10 minutes on a laptop, and
it is rigorous: exact or interval arithmetic, or an argument that bounds the numerical error. Say clearly
which cells you consider solved and which are partial.

## Parte 1 — Lines in the plane

**Punteggio:** 1 point · **Valutazione:** Judged

We begin in the plane ($d = 2$), where the conjectured optimum splits the $N$ lines as evenly as
possible between two perpendicular directions. Let $\ell_1, \ldots, \ell_N$ be lines in $\mathbb{R}^2$.
Prove that
$$
S(\ell_1, \ldots, \ell_N) \;\le\; \frac{\pi}{2} \cdot \left\lfloor \frac{N^2}{4} \right\rfloor .
$$

## Parte 2 — An orthogonality lemma

**Punteggio:** 2 points · **Valutazione:** Judged

A statement about a chain of vectors, in which each vector may fail to be orthogonal only to its immediate
neighbours in the list. Let $m \ge 2$ and let $x_1, \ldots, x_m$ be unit vectors in $\mathbb{R}^{m-1}$ with
$\langle x_i, x_j \rangle = 0$ whenever $|i - j| \ge 2$. Prove that
$$
\sum_{i=1}^{m-1} \theta(x_i, x_{i+1}) \;\le\; (m-2) \cdot \frac{\pi}{2},
$$
where $\theta(x,y) = \arccos\,\lvert \langle x, y \rangle \rvert$.

## Parte 3 — $d+1$ lines in $\mathbb{R}^d$

**Punteggio:** 3 points · **Valutazione:** Judged

The first case in every dimension: one line more than the dimension, $N = d+1$, where the conjectured optimum
repeats exactly one of the $d$ coordinate axes. Let $d \ge 1$. Prove that any $d+1$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{d+1}{2} - 1 \right) \cdot \frac{\pi}{2}.
$$

## Parte 4 — Five lines in $\mathbb{R}^3$, six in $\mathbb{R}^4$

**Punteggio:** 5 points · **Valutazione:** Judged

Two concrete instances of the next case, $N = d+2$: five lines in three dimensions and six lines in four.
In each, the conjectured optimum repeats two of the coordinate axes. Prove that any $5$ lines in $\mathbb{R}^3$
satisfy $S \le 4\pi$, and that any $6$ lines in $\mathbb{R}^4$ satisfy $S \le 13\pi/2$.

## Parte 5 — $d+2$ lines in $\mathbb{R}^d$

**Punteggio:** 8 points · **Valutazione:** Judged

The case $N = d+2$ in every dimension, with the same conjectured optimum: the $d$ coordinate axes, two of them
repeated. Prove that for every $d \ge 2$, any $d+2$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{d+2}{2} - 2 \right) \frac{\pi}{2}.
$$

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

*(Fine del problema 1. Punteggi: 1+2+3+5+8+13 = 32.)*


# TARGET CELL 2
Let m >= 2 and x_1..x_m unit vectors in R^{m-1} with <x_i,x_j> = 0 whenever |i-j| >= 2. Prove sum_{i=1}^{m-1} theta(x_i,x_{i+1}) <= (m-2) pi/2, where theta(x,y) = arccos|<x,y>|.
