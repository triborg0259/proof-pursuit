"""
Seconda implementazione (metodo diverso) per il problema 4, parte 3.

COSA: cerca famiglie disgiunte di k classi con m_i | 420, tutti i gcd(m_i,m_j) <= soglia.
COME: (1) enumera i multinsiemi non decrescenti di moduli (divisori di 420, >= 2) con
gcd a coppie in [2, soglia]; (2) per ciascuno risolve il CSP sui residui
a_i (mod m_i) con vincolo a_i != a_j (mod gcd), normalizzando a_1 = 0 (traslazione).
PERCHE': controllo incrociato del risultato dell'enumerazione di clique, con un
algoritmo strutturalmente diverso. Aritmetica esatta.
"""
import sys
import time
from math import gcd

MODULI = [d for d in range(2, 421) if 420 % d == 0]


def multinsiemi_moduli(k, soglia):
    """Tuple non decrescenti di k moduli con gcd a coppie in [2, soglia]."""
    def estendi(parziale, da):
        if len(parziale) == k:
            yield tuple(parziale)
            return
        for m in MODULI:
            if m < da:
                continue
            if all(2 <= gcd(m, q) <= soglia for q in parziale):
                yield from estendi(parziale + [m], m)
    yield from estendi([], 2)


def residui_compatibili(moduli):
    """Tutte le assegnazioni di residui (a_1 = 0) che rendono le classi disgiunte."""
    soluzioni = []

    def estendi(res):
        i = len(res)
        if i == len(moduli):
            soluzioni.append(tuple(res))
            return
        for a in range(moduli[i]) if i > 0 else [0]:
            if all((a - res[j]) % gcd(moduli[i], moduli[j]) != 0 for j in range(i)):
                estendi(res + [a])
    estendi([])
    return soluzioni


def esegui(k, soglia):
    """Conta multinsiemi di moduli esaminati e famiglie trovate."""
    t0 = time.time()
    n_moduli, famiglie = 0, []
    for moduli in multinsiemi_moduli(k, soglia):
        n_moduli += 1
        for res in residui_compatibili(moduli):
            famiglie.append(tuple(zip(res, moduli)))
    dt = time.time() - t0
    print(f"k={k} soglia_gcd<={soglia} multinsiemi_moduli={n_moduli} "
          f"famiglie(a1=0)={len(famiglie)} tempo={dt:.2f}s")
    return famiglie


if __name__ == "__main__":
    if len(sys.argv) > 1:
        k, soglia = int(sys.argv[1]), int(sys.argv[2])
        fam = esegui(k, soglia)
        print("   esempio:", fam[0] if fam else None)
    else:
        for k in range(3, 9):
            esegui(k, k - 1)
