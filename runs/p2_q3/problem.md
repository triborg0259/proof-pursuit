# Uphill paths on the hypercube (competition problem 2, cell 1 — the Q_3 half)

A labelling of a graph G on n vertices is a bijection f: V(G) -> {1..n}. A vertex v is a valley if every neighbour w has f(w) > f(v).
An uphill path is a sequence (v_1,...,v_k), k >= 1, with v_1 a valley, consecutive vertices adjacent, and f(v_1) < ... < f(v_k).
A valley alone (k=1) is an uphill path. U(G) = min over labellings of the number of uphill paths.
Q_d is the d-dimensional hypercube on {0,1}^d (adjacent = differ in one coordinate).

Cell 1: Determine U(Q_3) exactly, and give an explicit labelling attaining it as the list of the 8 vertices
in increasing label order, written as 0/1 strings. The value must be certain (exhaustive exact computation is acceptable
if the code is included and the finite set it covers is stated).
