"""Stampa l'orbita di lambda* = (k-1, k-2, k-2, k-3, ..., 2, 1, 1) (n = T_k - 1) descrivendo
ogni partizione come: diagonali 1..k-1 piene? + celle sulla diagonale k (righe) + celle oltre.

Perche': serve la forma chiusa di B^j(lambda*) per dimostrare il lower bound d_B = k^2-2k-1.
"""
import sys
from db_table import shift


def celle(lam):
    return {(i + 1, j + 1) for i, parte in enumerate(lam) for j in range(parte)}


def descrivi(lam, k):
    c = celle(lam)
    piene = all((i, w + 1 - i) in c for w in range(1, k) for i in range(1, w + 1))
    diag_k = tuple(int((i, k + 1 - i) in c) for i in range(1, k + 1))
    oltre = sorted((i, j) for (i, j) in c if i + j - 1 > k)
    return piene, diag_k, oltre


if __name__ == "__main__":
    k = int(sys.argv[1])
    lam = tuple([k - 1, k - 2] + list(range(k - 2, 0, -1)) + [1])
    for j in range(k * k - 2 * k + 2):
        piene, dk, oltre = descrivi(lam, k)
        print(f"j={j:3d} s={len(lam):2d} l1={lam[0]:2d} diag<k piene={piene} diag_k={''.join(map(str,dk))} oltre={oltre}  {lam}")
        lam = shift(lam)
