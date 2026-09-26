"""Controllo di sanita' (solo evidenza) dell'identita' usata nella prova:
totale = |E| + #valli + X, X = somma sugli spigoli u->w di (p(u)-1), e X in {0} u [3, inf).
Etichettature casuali di Q_5 con aritmetica esatta.
"""
import random
from conta_cammini import conta_cammini, vicini

D, N = 5, 32
rng = random.Random(1)
valori_x = set()
for _ in range(200000):
    ordine = list(range(N))
    rng.shuffle(ordine)
    tot, p, valli = conta_cammini(ordine, D)
    et = {v: i for i, v in enumerate(ordine)}
    x = sum(p[u] - 1 for u in range(N) for w in vicini(u, D) if et[u] < et[w])
    assert tot == 80 + len(valli) + x
    valori_x.add(x)
print("identita' verificata su 200000 etichettature casuali; min X>0 osservato:", min(v for v in valori_x if v > 0))
print("valori di X osservati sotto 10:", sorted(v for v in valori_x if v < 10))
