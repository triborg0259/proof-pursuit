# Problema 3 — Bulgarian solitaire

*(Enunciato formattato in LaTeX, contenuto fedele all'originale; ricevuto il 2026-09-26.)*

## Preambolo

**Bulgarian solitaire.** Repeatedly take one card from every pile and form a new pile. How many moves can it
take before the piles start to cycle?

A partition of a positive integer $n$ is a weakly decreasing sequence $\lambda = (\lambda_1, \ldots, \lambda_s)$
of positive integers with $\lambda_1 + \cdots + \lambda_s = n$. Think of it as a division of $n$ cards into
$s$ piles.

The shift $B(\lambda)$ is the partition of $n$ obtained as follows: remove one card from every pile, discard the
piles that become empty, and add one new pile consisting of the $s$ removed cards. Formally, $B(\lambda)$ is the
partition whose parts are the positive numbers among $\lambda_1 - 1, \ldots, \lambda_s - 1$ together with one
extra part equal to $s$.

Iterating $B$ from any starting partition must eventually repeat, since there are finitely many partitions of
$n$. Call $\lambda$ *cyclic* if $B^i(\lambda) = \lambda$ for some $i \ge 1$, and let
$$
d_B(\lambda) = \min\{\, i \ge 0 : B^i(\lambda) \text{ is cyclic} \,\}, \qquad
D_B(n) = \max\{\, d_B(\lambda) : \lambda \text{ is a partition of } n \,\}.
$$
So $D_B(n)$ is the largest number of shifts that can be needed before the process starts to cycle.

Write $T_k = k(k+1)/2$ and $\delta_k = (k, k-1, \ldots, 2, 1)$, the partition of $T_k$ into distinct parts.
Every $n \ge 1$ satisfies $T_{k-1} < n \le T_k$ for exactly one $k$, which we call the *rank* of $n$.

Examples: $B((2,1,1,1,1)) = (5,1)$; $B((5,1)) = (4,2)$; $B((4,2)) = (3,2,1)$; $B((3,2,1)) = (3,2,1)$.
Here $d_B((2,1,1,1,1)) = 3$.

**What to hand in.** For each cell you attempt, hand in a written proof. You may use a computer to explore.
A proof may rely on a computation only if you include the code, it runs in under 10 minutes on a laptop, and
the computation is exhaustive over a finite set that your argument has reduced the problem to. Where a cell asks
you to determine a quantity, give the exact value as a formula in $k$ and prove both bounds; state any partitions
you use explicitly as functions of $k$. Say clearly which cells you consider solved and which are partial.

Citing a published result for the statement you are asked to prove does not count as a solution; a proof
written out in full does, whatever its source.

## Parte 1 (C1) — Cyclic partitions and cycles

**Punteggio:** 1 point · **Valutazione:** Judged

First, the long-run behaviour: which partitions repeat under the shift, and how they fall into cycles.
Let $n = T_k$. Prove that for every partition $\lambda$ of $n$ there is an $i$ with $B^i(\lambda) = \delta_k$,
and that $\delta_k$ is the only cyclic partition of $n$. Then let $n$ be arbitrary of rank $k$, say
$n = T_{k-1} + r$ with $1 \le r \le k$: determine all cyclic partitions of $n$, and determine the number of
distinct cycles of $B$ on the partitions of $n$. Prove both.

## Parte 2 (C2) — $D_B$ at triangular $n$

**Punteggio:** 2 points · **Valutazione:** Judged

Next, how long the process can take to reach a cycle, starting with the triangular numbers.
Determine $D_B(T_k)$ for every $k$, with proof of both bounds.

## Parte 3 (C3) — A general upper bound

**Punteggio:** 3 points · **Valutazione:** Judged

Now the numbers strictly between two consecutive triangular numbers. Prove that for every $k \ge 4$ and every
non-triangular $n$ with $T_{k-1} < n < T_k$,
$$
D_B(n) \le k^2 - 2k - 1,
$$
and determine $D_B(T_k - 1)$ exactly. Determine also, for that $n$, which partitions attain the maximum.

## Parte 4 (C4) — One above a triangular number

**Punteggio:** 5 points · **Valutazione:** Judged

The first family just above a triangular number: $n = T_{k-1} + 1$, that is $n = 11, 16, 22, 29, \ldots$ for
$k = 5, 6, 7, 8, \ldots$. Determine $D_B(T_{k-1} + 1)$ for every $k \ge 5$, with proof of both bounds.

## Parte 5 (C5) — Two above a triangular number

**Punteggio:** 8 points · **Valutazione:** Judged

The next family: $n = T_{k-1} + 2$, that is $n = 3, 5, 8, 12, 17, 23, \ldots$ for $k = 2, 3, 4, 5, 6, 7, \ldots$.
Determine $D_B(T_{k-1} + 2)$ for every $k$, with proof of both bounds. State exactly for which $k$ your formula
holds, and give the remaining values separately. Your upper bound must be a single argument valid for all $k$ in
that range, not a separate treatment of each $k$, and you must give the extremal partitions explicitly as a
function of $k$.

Say also where the straightforward extension of the C3 argument stops: give the bound it does yield, show it is
strictly weaker than the truth, and identify precisely what your proof supplies in its place.

## Parte 6 (C6) — $D_B(n)$ for every $n$

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Finally, the whole function $n \mapsto D_B(n)$. Determine $D_B(n)$ for every $n$.

*(Fine del problema 3. Punteggi: 1+2+3+5+8+13 = 32.)*


# TARGET CELL 5
Determine D_B(T_{k-1} + 2) for every k, with proof of both bounds; state exactly for which k the formula holds and give the remaining values; the upper bound must be one uniform argument; give the extremal partitions explicitly in k; say where the straightforward extension of the C3 argument stops and what replaces it.
