# Problema 4 — Disjoint congruence classes and large gcd

*(Enunciato formattato in LaTeX, contenuto fedele all'originale; ricevuto il 2026-09-26. Titolo della colonna
non riportato nel testo incollato; la domanda di apertura è: "If congruence classes are pairwise disjoint, must
two of their moduli share a large common factor?")*

## Preambolo

For integers $a$ and $m \ge 1$ write
$$
a \pmod m = \{\, a + mt : t \in \mathbb{Z} \,\}
$$
for the congruence class of $a$ modulo $m$. A finite family of classes $a_1 \pmod{m_1}, \ldots, a_k \pmod{m_k}$
is *pairwise disjoint* if $a_i \pmod{m_i} \cap a_j \pmod{m_j} = \emptyset$ whenever $i < j$. Nothing is assumed
about the moduli beyond $m_i \ge 1$: they may repeat, and the residues $a_i$ may repeat as well.

By the Chinese remainder theorem, two classes meet if and only if the congruences $x \equiv a_i \pmod{m_i}$ and
$x \equiv a_j \pmod{m_j}$ are compatible, that is
$$
a_i \pmod{m_i} \cap a_j \pmod{m_j} \ne \emptyset \iff \gcd(m_i, m_j) \mid a_i - a_j. \qquad (*)
$$
The question of this column is how large the moduli of a disjoint family must be forced to overlap in the gcd sense.

**Question.** Let $k \ge 2$ and let $a_1 \pmod{m_1}, \ldots, a_k \pmod{m_k}$ be pairwise disjoint. Must there be
a pair $i < j$ with
$$
\gcd(m_i, m_j) \ge k \,?
$$
This is believed to be true for every $k$. It is sharp: the $k$ classes $1, 2, \ldots, k \pmod k$ are pairwise
disjoint — their differences have absolute value less than $k$, so $k$ divides none of them — and every pairwise
gcd equals exactly $k$. So $k$ could not be replaced by $k+1$ in the statement.

**Examples.** The three classes $0 \pmod 2$, $1 \pmod 4$, $3 \pmod 8$ are pairwise disjoint by $(*)$, and their
pairwise gcds are $2, 2, 4$; the largest is $4 \ge 3$, as the question predicts for $k = 3$. By contrast
$0 \pmod 2$ and $0 \pmod 3$ have coprime moduli and do meet, at $0$.

**Trivial bounds.** Two observations are immediate and you should assume they are already on the table;
presenting either as progress counts for nothing.

1. If $\gcd(m_i, m_j) = 1$ then by $(*)$ the two classes meet. Hence in any pairwise disjoint family every
   pairwise gcd is at least $2$. This answers the question for $k = 2$, and for a family of size $k$ that fails
   the question it confines every pairwise gcd to the range $2 \le \gcd(m_i, m_j) \le k - 1$.
2. The class $a \pmod m$ has density $1/m$, so a pairwise disjoint family satisfies $\sum_{i=1}^k 1/m_i \le 1$.
   In particular some modulus satisfies $m_i \ge k$.

Observation 2 bounds a single modulus from below; it says nothing about any gcd, and the two together settle no
size $k \ge 3$. Every cell below needs a genuinely new argument.

**What to hand in.** For each cell you attempt, hand in a written proof. You may use a computer to explore.
A proof may rely on a computation only if you include the code, it runs in under ten minutes on a laptop, and
the computation is exhaustive over a finite set that your own argument has reduced the problem to.

A computational cell is accepted only with an *exhaustiveness certificate*, meaning all four of:

1. an exact description of the finite set your search enumerates, together with the proof that nothing outside
   it can be a counterexample;
2. every pruning rule you use, stated precisely, each with the proof that it discards only objects that cannot
   be completed to a counterexample;
3. the node count of the search at each size you claim, and the wall clock;
4. a rerun that reproduces those counts;
5. and, if anything at all survives your pruning at a size you claim, a separate decision for every survivor —
   not a sample — together with, for each one, the smallest part of it that already forces the decision, and
   your proof that no smaller part does. A survivor you cannot decide means the size is not certified.

A run that reports "I searched and found nothing" without 1–5 is not a certificate and scores nothing. If a
search does not finish at some size, report it as unfinished and do not claim that size; a partial search is a
legitimate partial result and should be handed in as one, with the counts it reached.

Where a cell asks you to determine a boundary, state the exact value you claim. Claim only what you have
certified: an unfinished size, or one certified under an assumption you have not verified, must be reported as
such. Say clearly which cells you consider solved and which are partial.

Citing a published result for the statement you are asked to prove does not count as a solution; a proof written
out in full does, whatever its source. If you rely on a published argument, you are responsible for it: check it
yourself, and report it if it does not hold up.

## Parte 1 (C1) — Three classes

**Punteggio:** 1 point · **Valutazione:** Judged

The first size that the two trivial observations above do not settle. Prove the statement for $k = 3$: any three
pairwise disjoint classes have $\gcd(m_i, m_j) \ge 3$ for some $i < j$.

## Parte 2 (C2) — Four classes

**Punteggio:** 2 points · **Valutazione:** Judged

The same question for four classes. Prove the statement for $k = 4$.

## Parte 3 (C3) — Every $k$ up to 8

**Punteggio:** 3 points · **Valutazione:** Judged

A first range of sizes: after C1 and C2, the sizes $k = 5, 6, 7$ and $8$ remain. Prove the statement for every
$k \le 8$.

## Parte 4 (C4) — Every $k$ up to 12

**Punteggio:** 5 points · **Valutazione:** Judged

A longer range, and a precise account of your method at the sizes just beyond it. Prove the statement for every
$k \le 12$. Then, for each $k$ from $9$ to $16$ in turn, report exactly what your method leaves undecided at that
$k$: if nothing, say so and prove it; if something, exhibit it in full. If that disagrees with any source you
consulted, say which of the two is right and why. An answer that reports agreement with a source it did not test
will be marked wrong.

## Parte 5 (C5) — The certified boundary

**Punteggio:** 8 points · **Valutazione:** Judged

The main certification cell: an initial range of sizes as long as you can make it, plus two isolated sizes
further out. Determine the largest $k$ for which you can certify the statement for all sizes up to and including
$k$, and certify it. The range you claim must be contiguous, and if your argument at a given size assumes that
all smaller sizes have already been settled you must say so. Then decide the two isolated sizes $k = 24$ and
$k = 30$: show that neither is the least size at which the statement can fail.

For this cell the exhaustiveness certificate of the hand-in rules is not enough on its own. Add:

(i) a demonstration that your method is not vacuous. Construct a case in which an admissible configuration
genuinely exists, run your machinery on it unmodified, and show it returns that configuration. A method that
reports "nothing survives" at every size it is pointed at is indistinguishable from a method with a bug, and will
be graded as one;

(ii) for every object your pruning leaves undecided, at every $k$ you claim — not a sample — an individual
decision, plus the smallest part of that object which already forces the decision, plus a proof that no smaller
part does;

(iii) the exact list, not merely the count, of what survives at each $k$;

(iv) every pruning rule you use beyond those you have proved, proved. If your search needs a rule you invented
to finish a size, that rule is part of your claim: state it, prove it, and show the survivor list is unchanged
when you switch it off. A size that only closes with an unproved rule is not certified;

(v) a second implementation, written independently of your first, that differs in method — not the same
algorithm twice — and the two survivor lists compared elementwise at every $k$ you claim. Report any difference
rather than reconciling it silently: a disagreement means one of them is wrong, and finding which is part of the
cell.

## Parte 6 (C6) — Beyond the boundary

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Three directions beyond the certified range; any one of them counts. Any of the following.

(a) Decide a size $k \ge 25$.

(b) The asymptotic form. It is known that a pairwise disjoint family of size $k$ always has a pair with
$$
\gcd(m_i, m_j) \;\ge\; k \cdot \exp\!\left( -(2 + o(1)) \frac{\log k}{\log\log k} \right),
$$
which is $k^{1 - o(1)}$ but not linear in $k$. Prove the statement in full, or prove the weaker bound
$\gcd(m_i, m_j) \ge ck$ for some absolute constant $c > 0$, or improve the exponential factor above.

(c) The group form. Let $G$ be a group, let $G_1, \ldots, G_k$ be subgroups of finite index $n_i = [G : G_i]$,
and let $x_1 G_1, \ldots, x_k G_k$ be pairwise disjoint cosets. Is there a pair $i < j$ with
$\gcd(n_i, n_j) \ge k$? This is known for $k \le 5$ and open for every $k \ge 6$; settling $k = 6$ counts as
progress.

*(Fine del problema 4. Punteggi: 1+2+3+5+8+13 = 32.)*
