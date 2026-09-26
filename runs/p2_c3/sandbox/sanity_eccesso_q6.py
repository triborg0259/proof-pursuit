"""Sanity check (solo evidenza): identita' T = 192 + #valli + X e X ∈ {0} ∪ [4, ∞) su etichettature casuali di Q_6.

X = somma su tutti gli archi orientati (u -> w) di (p(u) - 1). Aritmetica intera.
"""
import random
from conta_cammini import conta_cammini, vicini

D, N = 6, 64
rng = random.Random(0)
minimo_X_positivo = None
for _ in range(20000):
    ordine = list(range(N))
    rng.shuffle(ordine)
    etichetta = {v: i for i, v in enumerate(ordine)}
    totale, p, valli = conta_cammini(ordine, D)
    X = sum(p[u] - 1 for u in range(N) for w in vicini(u, D) if etichetta[u] < etichetta[w])
    assert totale == 192 + len(valli) + X
    assert X == 0 or X >= 4
    if X > 0 and (minimo_X_positivo is None or X < minimo_X_positivo):
        minimo_X_positivo = X
print("20000 etichettature casuali: identita' verificata; minimo X positivo osservato:", minimo_X_positivo)
