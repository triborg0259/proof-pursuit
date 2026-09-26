# Uphill paths on the hypercube (competition problem 2, cell 1 — the Q_4 half)

A labelling of a graph G on n vertices is a bijection f: V(G) -> {1..n}. A vertex v is a valley if every neighbour w has f(w) > f(v).
An uphill path is a sequence (v_1,...,v_k), k >= 1, with v_1 a valley, consecutive vertices adjacent, and f(v_1) < ... < f(v_k).
A valley alone (k=1) is an uphill path. U(G) = min over labellings of the number of uphill paths.
Q_d is the d-dimensional hypercube on {0,1}^d (adjacent = differ in one coordinate). Q_4 has 16 vertices and 32 edges.

Cell 1 (Q_4 half): Determine U(Q_4) exactly, and give an explicit labelling attaining it as the list of the 16 vertices
in increasing label order, written as 0/1 strings. The value must be CERTAIN: 16! labellings cannot be enumerated
directly, so either (a) an exhaustive search over a reduced finite set with a PROOF that the reduction loses no
optimal labelling and that every pruning rule is sound (state node counts and wall-clock, under 10 minutes), or
(b) a hand proof of the lower bound plus an explicit labelling for the upper bound. Known facts you may use:
total >= |E| + #valleys for any labelling (proved for Q_3 in the repo, problema-2/submission/parte-1.md, and the
argument is general); U(Q_3) = 14 = |E| + 2.
