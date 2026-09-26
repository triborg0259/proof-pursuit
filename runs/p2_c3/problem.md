# Problema 2 — Uphill paths on the hypercube

*(Enunciato formattato in LaTeX, contenuto fedele all'originale; ricevuto il 2026-09-26.)*

## Preambolo

**Uphill paths on the hypercube.** Label the vertices of the hypercube to make as few uphill paths as possible.
IMO 2022 settled the grid; the cube is still open.

Let $G$ be a finite simple graph on $n$ vertices. A labelling of $G$ is a bijection $f$ from $V(G)$ to
$\{1,2,\ldots,n\}$. Fix a labelling.

- A vertex $v$ is a *valley* if every neighbour $w$ of $v$ has $f(w) > f(v)$. An isolated vertex counts as a valley.
- An *uphill path* is a sequence $(v_1, v_2, \ldots, v_k)$ with $k \ge 1$ in which $v_1$ is a valley, $v_i$ and
  $v_{i+1}$ are adjacent for each $i$, and $f(v_1) < f(v_2) < \cdots < f(v_k)$. A valley on its own ($k=1$) counts
  as an uphill path.

Let $U(G)$ be the smallest possible number of uphill paths, taken over all labellings of $G$.

IMO 2022 Problem 6 asks for $U$ of the $n \times n$ grid graph. The answer is $2n^2 - 2n + 1$.

This column asks about the $d$-dimensional hypercube $Q_d$. Its vertex set is $\{0,1\}^d$, and two vertices are
adjacent when they differ in exactly one coordinate. $Q_d$ has $2^d$ vertices and $d \cdot 2^{d-1}$ edges.

**What to hand in.** For C1 to C4, hand in the values, and for each value an explicit labelling that attains it
as a list of the $2^d$ vertices in increasing label order, written as 0/1 strings. These cells are marked correct
on the values alone, but a value with no labelling behind it will not survive the later cells, which build on
the construction.

For C5, hand in either a labelling of $Q_9$ in the same format, whose uphill paths will be counted mechanically,
or a proof of the lower bound.

For C6, hand in all three of: the value; an explicit labelling that attains it, in the same format; a proof that
no labelling gives fewer uphill paths.

A lower-bound proof may be computer-assisted. If it is, include the code; it must run in under 10 minutes on a
laptop, and you must explain why the computation proves the bound. Say clearly which cells you consider solved
and which are partial.

## Parte 1 (C1) — $U(Q_3)$ and $U(Q_4)$

**Punteggio:** 1 point · **Valutazione:** Checked instantly

The two smallest interesting cubes: $Q_3$ has $8$ vertices and $12$ edges, $Q_4$ has $16$ vertices and $32$ edges.
Determine $U(Q_3)$ and $U(Q_4)$.

## Parte 2 (C2) — $U(Q_5)$

**Punteggio:** 2 points · **Valutazione:** Checked instantly

$Q_5$ has $32$ vertices and $80$ edges. Determine $U(Q_5)$.

## Parte 3 (C3) — $U(Q_6)$

**Punteggio:** 3 points · **Valutazione:** Checked instantly

$Q_6$ has $64$ vertices and $192$ edges. Determine $U(Q_6)$.

## Parte 4 (C4) — $U(Q_7)$ and $U(Q_8)$

**Punteggio:** 5 points · **Valutazione:** Checked instantly

Two larger cubes: $Q_7$ has $128$ vertices and $448$ edges, $Q_8$ has $256$ vertices and $1024$ edges.
Determine $U(Q_7)$ and $U(Q_8)$.

## Parte 5 (C5) — Bounds for $U(Q_9)$

**Punteggio:** 8 points · **Valutazione:** Judged

$Q_9$ has $512$ vertices and $2304$ edges. The best bounds known to the organisers are
$$
2368 \le U(Q_9) \le 2400;
$$
the lower bound is unpublished. Improve either one: prove that $U(Q_9) \ge 2369$, or exhibit a labelling of $Q_9$
with at most $2399$ uphill paths.

## Parte 6 (C6) — $U(Q_9)$

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

The same cube, settled completely. Determine $U(Q_9)$ exactly, with proof of both bounds.

*(Fine del problema 2. Punteggi: 1+2+3+5+8+13 = 32.)*


# TARGET CELL 3
Determine U(Q_6) exactly (64 vertices, 192 edges) and exhibit an optimal labelling in the required format. Checked on the value: it must be the true minimum, so a lower-bound proof (hand or certified computation < 10 min) is needed.
