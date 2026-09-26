"""
Esplorazione (solo conteggio, nessuna prova): quanti multinsiemi di moduli
sopravvivono ai vincoli provabili per k = 9..12?
COSA: enumera multinsiemi non decrescenti di k divisori di N = lcm(1..k-1), >= 2,
con gcd a coppie in [2, k-1], somma 1/m <= 1, e "massimo esponente raggiunto
almeno due volte" per ogni primo (famiglia ridotta).
PERCHE': stimare la dimensione dello spazio prima di scrivere la ricerca certificata.
"""
import sys, time
from math import gcd, lcm
from fractions import Fraction

def divisori(n):
    return [d for d in range(2, n + 1) if n % d == 0]

def val(p, n):
    """Esponente di p in n."""
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e

def ridotta(moduli, primi):
    """Vero se per ogni primo l'esponente massimo compare almeno due volte."""
    for p in primi:
        es = sorted(val(p, m) for m in moduli)
        if es[-1] > 0 and es[-2] < es[-1]:
            return False
    return True

def conta(k):
    N = lcm(*range(1, k))
    primi = [p for p in range(2, k) if all(p % q for q in range(2, p))]
    D = divisori(N)
    soglia = k - 1
    tot = [0, 0]  # nodi visitati, multinsiemi completi
    def estendi(parz, da, dens):
        tot[0] += 1
        if len(parz) == k:
            if ridotta(parz, primi):
                tot[1] += 1
            return
        for m in D:
            if m < da: continue
            if dens + Fraction(1, m) > 1: continue
            if all(2 <= gcd(m, q) <= soglia for q in parz):
                estendi(parz + [m], m, dens + Fraction(1, m))
    t0 = time.time()
    estendi([], 2, Fraction(0))
    print(f"k={k} N={N} |D|={len(D)} nodi={tot[0]} multinsiemi_ridotti={tot[1]} t={time.time()-t0:.1f}s", flush=True)

for k in map(int, sys.argv[1:]):
    conta(k)
