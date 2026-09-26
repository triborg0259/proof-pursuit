"""Controlla sulle estremali di T_k-1 le successioni c_u (numero di parti di B^{u-1}(lam)).

Cosa fa: stampa le successioni distinte c_1..c_{k^2-2k+k} delle estremali e conta quante
sono; verifica la presenza dei pattern (k-1,k,...,k,k+1) agli indici p_j=(k-3-j)k di
lunghezza k-2-j (j=0..k-4) previsti dall'analisi di tenuta del bound.
Aritmetica esatta.
"""
import sys
from db_table import distanze_dal_ciclo, shift


def successione(lam, lunghezza):
    s, cur = [], lam
    for _ in range(lunghezza):
        s.append(len(cur)); cur = shift(cur)
    return tuple(s)


def controlla(k):
    n = k * (k + 1) // 2 - 1
    d = distanze_dal_ciclo(n)
    D = max(d.values())
    estr = [lam for lam, v in d.items() if v == D]
    seqs = {successione(lam, D + k + 1) for lam in estr}
    print(f"k={k} #estremali={len(estr)} #successioni distinte={len(seqs)}")
    for s in sorted(seqs)[:12]:
        print("  ", s)
    ok = True
    for s in seqs:
        for j in range(0, k - 3):
            p, L = (k - 3 - j) * k, k - 2 - j
            atteso = (k - 1,) + (k,) * (L - 1) + (k + 1,)
            if tuple(s[p - 1:p + L]) != atteso:
                ok = False
                print(f"   pattern j={j} p={p} atteso {atteso} trovato {s[p-1:p+L]}")
                break
    print("   tutti i pattern p_j presenti:", ok)


if __name__ == "__main__":
    for k in range(5, int(sys.argv[1]) + 1):
        controlla(k)
