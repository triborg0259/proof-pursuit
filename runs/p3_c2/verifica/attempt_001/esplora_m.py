"""Esplorazione: statistiche sulla successione m(t) = numero di pile lungo le orbite.

Per ogni partizione di T_k calcola l'orbita fino a delta_k e registra:
  - primo istante dopo il quale m(t) resta in {k-1,k,k+1};
  - primo istante in cui le diagonali 1..k-1 sono piene;
  - la distanza residua da quell'istante.
"""
import sys
from collections import Counter
from calcola_DB_triangolari import shift, partizioni


def conteggio_diagonali(parti):
    """c_d = numero di celle (i,j) del diagramma (righe = pile) con i+j-1 = d."""
    c = Counter()
    for i, p in enumerate(parti, start=1):
        for j in range(1, p + 1):
            c[i + j - 1] += 1
    return c


def diagonali_piene_fino(parti, d_max):
    """True se le diagonali 1..d_max sono tutte piene (c_d = d)."""
    c = conteggio_diagonali(parti)
    return all(c[d] == d for d in range(1, d_max + 1))


def main(k):
    n = k * (k + 1) // 2
    delta = tuple(range(k, 0, -1))
    peggio_stab = 0; peggio_pieno = 0; combinazioni = Counter()
    for lam in partizioni(n):
        orbita = [lam]
        while orbita[-1] != delta:
            orbita.append(shift(orbita[-1]))
        d = len(orbita) - 1
        m = [len(p) for p in orbita]
        t_stab = max([t + 1 for t in range(len(m)) if abs(m[t] - k) > 1] + [0])
        t_pieno = next(t for t, p in enumerate(orbita) if diagonali_piene_fino(p, k - 1))
        peggio_stab = max(peggio_stab, t_stab)
        peggio_pieno = max(peggio_pieno, t_pieno)
        combinazioni[(t_pieno, d - t_pieno)] += 1
    print(f"k={k}: max t_stab={peggio_stab}, max t_pieno={peggio_pieno}, k^2-k={k*k-k}")
    print("  (t_pieno, residuo) con residuo massimo per t_pieno:")
    best = {}
    for (tp, res), cnt in combinazioni.items():
        best[tp] = max(best.get(tp, 0), res)
    for tp in sorted(best):
        print(f"   t_pieno={tp:3d} residuo max={best[tp]:3d} somma={tp+best[tp]}")


if __name__ == "__main__":
    for k in range(3, int(sys.argv[1]) + 1):
        main(k)
