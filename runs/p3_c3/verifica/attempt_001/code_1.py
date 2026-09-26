"""Certificato per il caso k = 4 della cella 3 e controlli di sanita'.

Cosa fa: (1) calcola esaustivamente D_B(n) per n = 7, 8, 9 (tutte le partizioni, aritmetica
esatta su tuple) e verifica D_B(n) <= 7 = 4^2 - 2*4 - 1; (2) verifica d_B(lambda*) = k^2-2k-1
per lambda* = (k-1, k-2, k-2, k-3, ..., 1, 1), k = 4..12 (solo controllo, non usato nella prova);
(3) confronta D_B(T_k - 1) con k^2-2k-1 per k = 4..9 (solo controllo).
Perche': la prova generale del bound usa k >= 5 nel caso A; per k = 4 serve l'esaustione.
"""
import time
from db_table import distanze_dal_ciclo, shift, partizioni


def d_B_diretto(lam):
    """d_B(lam) seguendo l'orbita finche' non si ripete (memoria esplicita)."""
    visti, orbita, cur = {}, [], lam
    while cur not in visti:
        visti[cur] = len(orbita)
        orbita.append(cur)
        cur = shift(cur)
    return visti[cur]  # indice della prima partizione ciclica dell'orbita


if __name__ == "__main__":
    t0 = time.time()
    for n in (7, 8, 9):
        d = distanze_dal_ciclo(n)
        num = sum(1 for _ in partizioni(n))
        assert len(d) == num
        print(f"n={n}: {num} partizioni, D_B(n)={max(d.values())} <= 7: {max(d.values()) <= 7}")
    print(f"(1) tempo caso k=4: {time.time()-t0:.2f}s")
    for k in range(4, 13):
        lam = tuple([k - 1, k - 2] + list(range(k - 2, 0, -1)) + [1])
        assert sum(lam) == k * (k + 1) // 2 - 1
        print(f"k={k}: d_B(lambda*)={d_B_diretto(lam)}  k^2-2k-1={k*k-2*k-1}")
    for k in range(4, 10):
        n = k * (k + 1) // 2 - 1
        D = max(distanze_dal_ciclo(n).values())
        print(f"k={k} n={n}: D_B={D}  k^2-2k-1={k*k-2*k-1}  uguali: {D == k*k-2*k-1}")
    print(f"tempo totale: {time.time()-t0:.2f}s")
