"""Verifica esatta (interi) della descrizione delle partizioni cicliche e del numero di cicli
del solitario bulgaro per n = 1..N_MAX. Confronta l'enumerazione a forza bruta con:
  - insieme S(n) = { delta_{k-1} + epsilon : epsilon in {0,1}^k, |epsilon| = r }, n = T_{k-1}+r;
  - numero di cicli = (1/k) * sum_{d | gcd(k,r)} phi(d) * C(k/d, r/d)  (collane binarie).
Serve solo come controllo di sanita' della prova: non e' una dimostrazione (copre un insieme finito)."""
from math import comb, gcd
from itertools import combinations
import sys, time


def partizioni(n, massimo=None):
    """Genera tutte le partizioni di n come tuple debolmente decrescenti."""
    if massimo is None:
        massimo = n
    if n == 0:
        yield ()
        return
    for prima in range(min(n, massimo), 0, -1):
        for resto in partizioni(n - prima, prima):
            yield (prima,) + resto


def shift(lam):
    """La mossa B: toglie una carta da ogni pila e crea una nuova pila di lunghezza s."""
    nuove = [p - 1 for p in lam if p > 1] + [len(lam)]
    return tuple(sorted(nuove, reverse=True))


def rango(n):
    """Restituisce (k, r) con n = T_{k-1} + r, 1 <= r <= k."""
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    return k, n - (k - 1) * k // 2


def insieme_S(k, r):
    """Le partizioni delta_{k-1} + epsilon previste dalla prova."""
    risultato = set()
    for posizioni in combinations(range(k), r):
        parti = [k - 1 - i + (1 if i in posizioni else 0) for i in range(k)]
        risultato.add(tuple(p for p in parti if p > 0))
    return risultato


def phi(d):
    """Funzione di Eulero, per interi piccoli."""
    return sum(1 for j in range(1, d + 1) if gcd(j, d) == 1)


def numero_collane(k, r):
    """Numero di collane binarie di lunghezza k con r perle nere (Burnside)."""
    return sum(phi(d) * comb(k // d, r // d) for d in range(1, k + 1)
               if k % d == 0 and r % d == 0) // k


def cicli_forza_bruta(n):
    """Trova le partizioni cicliche e il numero di cicli iterando B da ogni partizione."""
    cicliche, visitate = set(), set()
    for lam in partizioni(n):
        orbita, corrente = [], lam
        while corrente not in visitate and corrente not in orbita:
            orbita.append(corrente)
            corrente = shift(corrente)
        if corrente in orbita:
            cicliche.update(orbita[orbita.index(corrente):])
        visitate.update(orbita)
    # conta i cicli: componenti dell'insieme ciclico sotto B
    resto, numero_cicli = set(cicliche), 0
    while resto:
        mu = resto.pop()
        numero_cicli += 1
        corrente = shift(mu)
        while corrente != mu:
            resto.discard(corrente)
            corrente = shift(corrente)
    return cicliche, numero_cicli


def main(n_max):
    inizio = time.time()
    for n in range(1, n_max + 1):
        k, r = rango(n)
        cicliche, numero_cicli = cicli_forza_bruta(n)
        assert cicliche == insieme_S(k, r), f"insieme ciclico errato per n={n}"
        assert numero_cicli == numero_collane(k, r), f"numero di cicli errato per n={n}"
        if n == k * (k + 1) // 2:
            assert cicliche == {tuple(range(k, 0, -1))}, f"n={n} triangolare: attesa solo delta_k"
    print(f"OK: n = 1..{n_max}, tempo {time.time() - inizio:.1f}s")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 45)
