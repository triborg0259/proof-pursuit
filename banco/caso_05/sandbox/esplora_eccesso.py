"""Esplorazione (esatta, intera): distanza residua d_B in funzione del numero e di celle
oltre la diagonale k e della diagonale massima occupata. Serve a trovare una
decomposizione dimostrabile della stima superiore D_B(T_k) <= k^2-k."""
import sys
from collections import defaultdict
from calcola_DB_triangolari import shift, partizioni, distanze_al_punto_fisso


def celle_eccesso(parti, k):
    """Numero di celle (i,h) con diagonale i+h-1 > k e diagonale massima."""
    e = 0; dmax = 0
    for i, p in enumerate(parti, start=1):
        dmax = max(dmax, i + p - 1)
        e += max(0, min(p, i + p - 1 - k))
    return e, dmax


def main(k):
    n = k * (k + 1) // 2
    delta = tuple(range(k, 0, -1))
    dist = distanze_al_punto_fisso(n, delta)
    peggio = defaultdict(int); esempio = {}
    for lam, d in dist.items():
        e, dmax = celle_eccesso(lam, k)
        if (e, dmax) not in esempio or d > peggio[(e, dmax)]:
            peggio[(e, dmax)] = d; esempio[(e, dmax)] = lam
    print(f"k={k}, k^2-k={k*k-k}")
    for chiave in sorted(peggio):
        print(f"  e={chiave[0]:2d} dmax={chiave[1]:2d} max d_B={peggio[chiave]:3d}  es. {esempio[chiave]}")


if __name__ == "__main__":
    for k in range(3, int(sys.argv[1]) + 1):
        main(k)
