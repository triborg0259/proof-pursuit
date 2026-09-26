"""Calcolo esatto di D_B(T_k) per k piccoli (esplorazione, aritmetica intera esatta).

Enumera tutte le partizioni di n = T_k, applica lo shift B fino a raggiungere
delta_k (unico punto fisso per n triangolare: verifichiamo anche questo)
e registra la distanza massima e le partizioni che la raggiungono.
"""
import sys


def shift(parti):
    """Applica lo shift B: togli 1 da ogni parte, aggiungi la parte s."""
    s = len(parti)
    nuove = [p - 1 for p in parti if p > 1] + [s]
    return tuple(sorted(nuove, reverse=True))


def partizioni(n, massimo=None):
    """Genera tutte le partizioni di n con parti <= massimo (ordine decrescente)."""
    if massimo is None:
        massimo = n
    if n == 0:
        yield ()
        return
    for prima in range(min(n, massimo), 0, -1):
        for resto in partizioni(n - prima, prima):
            yield (prima,) + resto


def distanze_al_punto_fisso(n, punto_fisso):
    """Restituisce dict partizione -> numero di shift per arrivare al punto fisso."""
    dist = {punto_fisso: 0}
    for lam in partizioni(n):
        cammino = []
        cur = lam
        while cur not in dist:
            cammino.append(cur)
            cur = shift(cur)
            assert len(cammino) <= 10 * n * n, "orbita troppo lunga: non converge?"
        base = dist[cur]
        for i, p in enumerate(reversed(cammino)):
            dist[p] = base + i + 1
    return dist


def main(k_max):
    for k in range(1, k_max + 1):
        n = k * (k + 1) // 2
        delta = tuple(range(k, 0, -1))
        dist = distanze_al_punto_fisso(n, delta)
        D = max(dist.values())
        estremali = sorted(p for p, d in dist.items() if d == D)
        print(f"k={k} n={n} #partizioni={len(dist)} D_B={D} k^2-k={k*k-k} "
              f"#estremali={len(estremali)}")
        for p in estremali[:12]:
            print("   ", p)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
