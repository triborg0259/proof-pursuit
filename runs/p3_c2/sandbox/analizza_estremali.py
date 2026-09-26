"""Esplorazione: struttura delle partizioni estremali di T_k e della loro traiettoria.

Stampa, per ogni k, candidate famiglie semplici e la loro distanza d_B,
piu' la traiettoria (numero di parti s e parte massima) di una estremale.
"""
import sys
from calcola_DB_triangolari import shift, distanze_al_punto_fisso


def coniugata(parti):
    """Partizione coniugata: mu_j = numero di parti >= j."""
    return tuple(sum(1 for p in parti if p >= j) for j in range(1, parti[0] + 1))


def main(k_max):
    for k in range(2, k_max + 1):
        n = k * (k + 1) // 2
        delta = tuple(range(k, 0, -1))
        dist = distanze_al_punto_fisso(n, delta)
        D = max(dist.values())
        estremali = [p for p, d in dist.items() if d == D]
        # candidate: delta_{k-1} + colonna di k carte in piu' su pile diverse
        cand = {
            "delta_{k-1} con parte extra k": tuple(sorted(list(range(k - 1, 0, -1)) + [k], reverse=True)),
            "delta_{k-1} + 1 a tutte le parti + una parte 1": tuple(sorted([p + 1 for p in range(k - 1, 0, -1)] + [1], reverse=True)),
            "coniugata di (k-1,...,1,1)": None,
            "(1^n)": tuple([1] * n),
            "(n)": (n,),
        }
        for nome, p in cand.items():
            if p is None:
                continue
            print(f"k={k} {nome}: {p} d={dist[p]} (D={D})")
        # estremali con meno parti e con piu' parti, e loro coniugate
        emin = min(estremali, key=len); emax = max(estremali, key=len)
        print(f"  estremale con meno parti {emin} coniugata {coniugata(emin)}")
        print(f"  estremale con piu' parti {emax} coniugata {coniugata(emax)}")
        # traiettoria di emin: (s, lambda_1) per passo
        cur = emin; tr = []
        while cur != delta:
            tr.append((len(cur), cur[0])); cur = shift(cur)
        print("  traiettoria (s, max):", tr)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
