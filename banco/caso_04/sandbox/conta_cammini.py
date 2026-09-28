"""Conteggio esatto dei cammini in salita di una etichettatura di Q_d.

Vertici = interi 0..2^d-1 (bit i = coordinata i); vicini = XOR con un bit.
p(v) = [v valle] + somma p(u) sui vicini u con etichetta minore; totale = somma p(v).
Aritmetica intera: risultato esatto.
"""


def vicini(v, d):
    """Restituisce i d vicini di v in Q_d."""
    return [v ^ (1 << i) for i in range(d)]


def conta_cammini(ordine, d):
    """ordine = lista dei vertici in ordine crescente di etichetta. Ritorna (totale, p, valli)."""
    etichetta = {v: i for i, v in enumerate(ordine)}
    assert sorted(ordine) == list(range(1 << d)), "non e' una biiezione"
    p = {}
    valli = []
    for v in ordine:
        minori = [u for u in vicini(v, d) if etichetta[u] < etichetta[v]]
        if not minori:
            valli.append(v)
            p[v] = 1
        else:
            p[v] = sum(p[u] for u in minori)
    return sum(p.values()), p, valli


def stringa(v, d):
    """Vertice intero -> stringa 0/1, coordinata 1 a sinistra."""
    return "".join(str((v >> i) & 1) for i in range(d))


def da_stringa(s):
    """Stringa 0/1 -> vertice intero (coordinata 1 a sinistra)."""
    return sum(int(c) << i for i, c in enumerate(s))
