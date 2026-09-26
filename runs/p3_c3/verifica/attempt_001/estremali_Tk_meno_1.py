"""Studia le partizioni estremali di n = T_k - 1 (quelle con d_B = D_B).

Perche': la cella 3 chiede "quali partizioni raggiungono il massimo"; cerchiamo una
descrizione strutturale (es. le prime k-1 righe / il numero di parti / lunghezza massima).
Aritmetica esatta.
"""
import sys
from collections import Counter
from db_table import distanze_dal_ciclo, shift


def analizza(k):
    n = k * (k + 1) // 2 - 1
    d = distanze_dal_ciclo(n)
    D = max(d.values())
    estr = [lam for lam, v in d.items() if v == D]
    print(f"k={k} n={n} D_B={D} #estremali={len(estr)}")
    print("  distribuzione lunghezza (num parti):", sorted(Counter(len(l) for l in estr).items()))
    print("  distribuzione parte massima:", sorted(Counter(l[0] for l in estr).items()))
    # dopo quanti passi le orbite estremali si fondono? conta immagini distinte di B^j
    immagini = set(estr)
    for j in range(1, D + 1):
        immagini = {shift(l) for l in immagini}
        if len(immagini) <= 3:
            print(f"  dopo {j} passi le estremali confluiscono in {len(immagini)} partizioni: {sorted(immagini, reverse=True)}")
            break
    # sequenza dei numeri di parti lungo l'orbita di una estremale canonica
    canon = tuple([k - 1, k - 2] + list(range(k - 2, 0, -1)) + [1])
    print("  candidata Griggs-Ho:", canon, "d_B =", d.get(canon))
    seq, cur = [], canon
    for _ in range(D + k):
        seq.append(len(cur)); cur = shift(cur)
    print("  seq numero di parti:", seq)


if __name__ == "__main__":
    for k in range(4, int(sys.argv[1]) + 1):
        analizza(k)
