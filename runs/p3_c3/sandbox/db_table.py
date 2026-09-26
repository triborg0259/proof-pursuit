"""Calcola D_B(n) esattamente (interi) per n fino a NMAX, con le partizioni estremali.

Perche': serve la tabella dei valori veri di D_B(T_k-1) e delle estremali per congetturare la formula
richiesta dalla cella 3 e per controllare la prova. Aritmetica esatta su tuple: nessun errore numerico.
"""
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
    """Applica lo shift B: togli 1 da ogni parte, aggiungi una parte pari al numero di parti."""
    parti = [p - 1 for p in lam if p > 1] + [len(lam)]
    return tuple(sorted(parti, reverse=True))


def distanze_dal_ciclo(n):
    """Restituisce dict partizione -> d_B, esplorando il grafo funzionale con colorazione."""
    d = {}
    for start in partizioni(n):
        if start in d:
            continue
        cammino, visti = [], {}
        cur = start
        while cur not in d and cur not in visti:
            visti[cur] = len(cammino)
            cammino.append(cur)
            cur = shift(cur)
        if cur in d:
            base = d[cur]
        else:
            # cur e' sul cammino: tutto da visti[cur] in poi e' ciclico
            for lam in cammino[visti[cur]:]:
                d[lam] = 0
            cammino = cammino[:visti[cur]]
            base = -1
        for i, lam in enumerate(reversed(cammino)):
            d[lam] = base + 1 + i
    return d


def rango(n):
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    return k


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    for n in range(1, nmax + 1):
        t0 = time.time()
        d = distanze_dal_ciclo(n)
        D = max(d.values())
        estremali = sorted([lam for lam, v in d.items() if v == D], reverse=True)
        k = rango(n)
        r = n - (k - 1) * k // 2
        print(f"n={n} k={k} r={r} D_B={D} (k^2-2k-1={k*k-2*k-1}) #estr={len(estremali)} "
              f"estremali={estremali if len(estremali) <= 6 else estremali[:6]} t={time.time()-t0:.1f}s", flush=True)
