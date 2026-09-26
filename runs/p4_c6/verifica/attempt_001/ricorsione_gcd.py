"""
Calcolo ESATTO (interi e frazioni) della ricorsione del Lemma R (problema 4, cella 6).

S(g, P) = massima taglia di una famiglia di classi a due a due disgiunte con tutti i
gcd a coppie <= g e tutti i moduli coprimi con ogni primo < P.
Lemma R:   S(g, P) <= sum_{P <= p <= g, p primo} p * S(floor(g/p), p),   S(g, P) = 1 se P > g.
Qui calcoliamo la funzione R(g, P) definita dalla ricorsione con l'uguaglianza
(quindi F(g) := S(g, 2) <= R(g, 2)) e la confrontiamo con i limiti chiusi
   g^2 * prod_{p <= g} (1 + 2/p)     e     g^3.
Tutto in aritmetica esatta: nessun float.
"""
from fractions import Fraction
from functools import lru_cache
import sys
import time


def primi_fino_a(n):
    """Crivello di Eratostene: lista dei primi <= n."""
    segna = bytearray([1]) * (n + 1)
    segna[0:2] = b"\x00\x00"
    for p in range(2, int(n ** 0.5) + 1):
        if segna[p]:
            segna[p * p::p] = bytearray(len(segna[p * p::p]))
    return [p for p in range(2, n + 1) if segna[p]]


LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
PRIMI = primi_fino_a(LIMITE)


@lru_cache(maxsize=None)
def ricorsione(g, indice_primo):
    """R(g, P) con P = PRIMI[indice_primo]; vale 1 se nessun primo >= P e' <= g."""
    totale = 0
    for i in range(indice_primo, len(PRIMI)):
        p = PRIMI[i]
        if p > g:
            break
        totale += p * ricorsione(g // p, i)
    return totale if totale > 0 else 1


def limite_chiuso(g):
    """g^2 * prod_{p <= g} (1 + 2/p), come frazione esatta."""
    prodotto = Fraction(1)
    for p in PRIMI:
        if p > g:
            break
        prodotto *= Fraction(p + 2, p)
    return g * g * prodotto


inizio = time.time()
sys.setrecursionlimit(10000)
peggior_rapporto = Fraction(0)
for g in range(1, LIMITE + 1):
    r = ricorsione(g, 0)
    chiuso = limite_chiuso(g)
    assert r <= chiuso, f"limite chiuso violato a g={g}"
    assert r <= g ** 3, f"limite cubico violato a g={g}"
    peggior_rapporto = max(peggior_rapporto, Fraction(r, g * g))
    if g <= 12 or g in (16, 20, 24, 30, 50, 100, 300, 1000, LIMITE):
        print(f"g={g:5d}  R(g)={r:12d}  R/g^2={float(r)/g/g:8.3f}  "
              f"g^2*prod(1+2/p)={float(chiuso):14.1f}")
print(f"max R(g)/g^2 per g<={LIMITE}: {float(peggior_rapporto):.4f}")
print(f"tempo: {time.time()-inizio:.2f} s")
