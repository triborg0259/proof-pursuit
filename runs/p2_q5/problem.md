# Uphill paths on the hypercube (competition problem 2, cell 2: U(Q_5))

A labelling of a graph G on n vertices is a bijection f: V(G) -> {1..n}. A vertex v is a valley if every neighbour w has f(w) > f(v).
An uphill path is a sequence (v_1,...,v_k), k >= 1, with v_1 a valley, consecutive vertices adjacent, and f(v_1) < ... < f(v_k).
A valley alone (k=1) is an uphill path. U(G) = min over labellings of the number of uphill paths.
Q_d is the d-dimensional hypercube on {0,1}^d. Q_5 has 32 vertices and 80 edges.

Cell 2: Determine U(Q_5), and give an explicit labelling attaining it as the list of the 32 vertices in increasing
label order, written as 0/1 strings. The cell is checked on the value alone, so the value must be the TRUE minimum:
a labelling gives an upper bound; a lower bound needs a proof (hand argument, or exhaustive search over a reduced
finite set with the reduction and every pruning rule proved, node counts and wall-clock under 10 minutes).
Known and usable (verified in this repo, problema-2/submission/parte-1.md): for any labelling, #paths >= |E| + #valleys;
U(Q_3) = 14 = |E|+2 and U(Q_4) = 34 = |E|+2; the optimal Q_4 labelling has two valleys (0000 and 1111) and is built
by weight classes in the order 0, 4, 3, 1, 2; the parity argument (in-degrees in {0,1,d} when the total is |E|+1)
rules out |E|+1 for Q_5 as well (4s = 49 has no solution), so U(Q_5) >= 82.
