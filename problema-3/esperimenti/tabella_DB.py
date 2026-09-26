"""Tabella esatta di D_B(n) (massimo numero di mosse prima del ciclo) e partizioni estremali, per n <= N.
Grafo funzionale sulle partizioni; d_B via memoizzazione sui cicli. Interi esatti. NON e' una prova per n generico.
Uso: python3 tabella_DB.py 45"""
import sys, time
from functools import lru_cache

def partizioni(n, massimo=None):
    massimo = n if massimo is None else massimo
    if n == 0:
        yield (); return
    for prima in range(min(n, massimo), 0, -1):
        for resto in partizioni(n - prima, prima):
            yield (prima,) + resto

def B(l):
    return tuple(sorted([x - 1 for x in l if x > 1] + [len(l)], reverse=True))

def d_B_tutti(n):
    """d_B per ogni partizione di n: segue le orbite, marca i cicli."""
    dist = {}
    for p in partizioni(n):
        cammino = []
        q = p
        while q not in dist and q not in cammino:
            cammino.append(q); q = B(q)
        if q in cammino:                      # nuovo ciclo trovato
            for c in cammino[cammino.index(q):]:
                dist[c] = 0
            cammino = cammino[:cammino.index(q)]
        base = dist[q]
        for i, c in enumerate(reversed(cammino), start=1):
            dist[c] = base + i
    return dist

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
T = lambda k: k * (k + 1) // 2
inizio = time.time()
for n in range(1, N + 1):
    k = next(k for k in range(1, 100) if T(k - 1) < n <= T(k))
    dist = d_B_tutti(n)
    D = max(dist.values())
    estr = [p for p, d in dist.items() if d == D]
    tipo = "T_k" if n == T(k) else ("T_k-1" if n == T(k) - 1 else ("T_{k-1}+1" if n == T(k - 1) + 1 else ("T_{k-1}+2" if n == T(k - 1) + 2 else "")))
    print(f"n={n:2d} k={k} {tipo:9s} D_B={D:3d}  k^2-k={k*k-k:3d} k^2-2k-1={k*k-2*k-1:3d}  estremali={len(estr)} es. {estr[0]}", flush=True)
print(f"tempo {time.time()-inizio:.1f}s")
