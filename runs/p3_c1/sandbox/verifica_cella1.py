"""Verifica esatta (interi) delle conclusioni della cella 1 per n <= N_MAX.

Per ogni n: enumera tutte le partizioni, calcola le partizioni cicliche
per forza bruta, le confronta con l'insieme S_{k,r} = {lambda^eps},
conta i cicli e confronta con la formula delle collane.
Controlla anche la monotonia del potenziale Phi sulle composizioni.
"""
from math import comb, gcd
from itertools import combinations, product
import time

N_MAX = 40


def partizioni(n, massimo=None):
    """Genera tutte le partizioni di n come tuple decrescenti."""
    if massimo is None:
        massimo = n
    if n == 0:
        yield ()
        return
    for prima in range(min(n, massimo), 0, -1):
        for resto in partizioni(n - prima, prima):
            yield (prima,) + resto


def shift_B(lam):
    """Applica la mossa B: toglie 1 da ogni parte e aggiunge la parte len(lam)."""
    parti = [p - 1 for p in lam if p > 1] + [len(lam)]
    return tuple(sorted(parti, reverse=True))


def rango(n):
    """Restituisce (k, r) con n = T_{k-1} + r, 1 <= r <= k."""
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    return k, n - (k - 1) * k // 2


def famiglia_S(k, r):
    """Insieme S_{k,r}: parti positive tra k-i+eps_i, eps binaria di peso r."""
    insieme = set()
    for posizioni in combinations(range(1, k + 1), r):
        parti = [k - i + (1 if i in posizioni else 0) for i in range(1, k + 1)]
        insieme.add(tuple(p for p in parti if p > 0))
    return insieme


def cicliche_forza_bruta(n):
    """Partizioni cicliche di n: quelle che si trovano su un ciclo di B."""
    cicliche = set()
    for lam in partizioni(n):
        visto, corrente = set(), lam
        while corrente not in visto:
            visto.add(corrente)
            corrente = shift_B(corrente)
        # 'corrente' e' sul ciclo: percorrilo
        inizio = corrente
        while True:
            cicliche.add(corrente)
            corrente = shift_B(corrente)
            if corrente == inizio:
                break
    return cicliche


def numero_cicli(cicliche):
    """Conta i cicli di B sull'insieme delle partizioni cicliche."""
    restanti, cicli = set(cicliche), 0
    while restanti:
        corrente = next(iter(restanti))
        while corrente in restanti:
            restanti.remove(corrente)
            corrente = shift_B(corrente)
        cicli += 1
    return cicli


def phi_eulero(m):
    """Funzione phi di Eulero."""
    return sum(1 for j in range(1, m + 1) if gcd(j, m) == 1)


def formula_collane(k, r):
    """(1/k) * sum_{d | gcd(k,r)} phi(d) * C(k/d, r/d)."""
    g = gcd(k, r)
    totale = sum(phi_eulero(d) * comb(k // d, r // d)
                 for d in range(1, g + 1) if g % d == 0)
    assert totale % k == 0
    return totale // k


def potenziale(comp):
    """Phi(c) = somma su tutte le carte di (colonna + altezza)."""
    return sum(i * c + c * (c + 1) // 2 for i, c in enumerate(comp, start=1))


def shift_ordinato(comp):
    """B tilde: (s, c_1-1, ..., c_s-1) con gli zeri cancellati."""
    return tuple(x for x in (len(comp),) + tuple(c - 1 for c in comp) if x > 0)


def composizioni(n):
    """Tutte le composizioni di n (successioni di interi positivi)."""
    if n == 0:
        yield ()
        return
    for prima in range(1, n + 1):
        for resto in composizioni(n - prima):
            yield (prima,) + resto


def controlla_potenziale(n_max):
    """Verifica Phi(B~c) <= Phi(c), uguaglianza sse gli 1 sono un segmento finale."""
    for n in range(1, n_max + 1):
        for comp in composizioni(n):
            prima, dopo = potenziale(comp), potenziale(shift_ordinato(comp))
            uni = [i for i, c in enumerate(comp) if c == 1]
            terminale = all(c == 1 for c in comp[uni[0]:]) if uni else True
            assert dopo <= prima and (dopo == prima) == terminale, comp


inizio = time.time()
for n in range(1, N_MAX + 1):
    k, r = rango(n)
    cicliche = cicliche_forza_bruta(n)
    assert cicliche == famiglia_S(k, r), n
    assert numero_cicli(cicliche) == formula_collane(k, r), n
    if r == k:
        assert cicliche == {tuple(range(k, 0, -1))}
controlla_potenziale(14)
print(f"OK: n=1..{N_MAX} e potenziale su composizioni di n<=14, "
      f"tempo {time.time()-inizio:.1f}s")
