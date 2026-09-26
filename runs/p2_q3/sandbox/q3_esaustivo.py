"""
Calcolo esatto di U(Q_3) per enumerazione esaustiva di tutte le 8! = 40320 etichettature.

Due conteggi indipendenti per ogni etichettatura:
  1. DFS: enumera esplicitamente ogni cammino in salita (v_1,...,v_k) partendo da ogni valle.
  2. DP:  p(v) = [v valle] + somma_{u vicino, f(u)<f(v)} p(u);  totale = somma_v p(v).
Aritmetica: solo interi Python (esatta). Insieme coperto: TUTTE le biiezioni V(Q_3) -> {1..8}.
"""
from itertools import permutations
from collections import Counter
import time

D = 3
VERTICI = list(range(2 ** D))                      # vertice = intero, bit i = coordinata i
VICINI = [[v ^ (1 << i) for i in range(D)] for v in VERTICI]


def stringa(v):
    """Vertice intero -> stringa 0/1 di lunghezza D (bit 0 a sinistra)."""
    return "".join(str((v >> i) & 1) for i in range(D))


def valli(etichetta):
    """Vertici con tutti i vicini di etichetta maggiore."""
    return [v for v in VERTICI if all(etichetta[w] > etichetta[v] for w in VICINI[v])]


def conta_dfs(etichetta):
    """Conteggio 1: enumera esplicitamente ogni cammino in salita."""
    def cammini_da(v):
        # il cammino che termina in v conta 1, piu' tutte le estensioni ai vicini maggiori
        return 1 + sum(cammini_da(w) for w in VICINI[v] if etichetta[w] > etichetta[v])
    return sum(cammini_da(v) for v in valli(etichetta))


def conta_dp(etichetta):
    """Conteggio 2: programmazione dinamica in ordine crescente di etichetta."""
    ordine = sorted(VERTICI, key=lambda v: etichetta[v])
    p = {}
    for v in ordine:
        minori = [w for w in VICINI[v] if etichetta[w] < etichetta[v]]
        p[v] = (1 if not minori else 0) + sum(p[w] for w in minori)
    return sum(p.values())


def esplora_tutte():
    """Enumera tutte le 8! etichettature; restituisce (minimo, distribuzione, ottime)."""
    distribuzione = Counter()
    ottime = []
    minimo = None
    for perm in permutations(range(1, 2 ** D + 1)):
        etichetta = list(perm)                     # etichetta[v] = f(v)
        n_dfs = conta_dfs(etichetta)
        n_dp = conta_dp(etichetta)
        assert n_dfs == n_dp, (etichetta, n_dfs, n_dp)
        distribuzione[n_dfs] += 1
        if minimo is None or n_dfs < minimo:
            minimo, ottime = n_dfs, [etichetta]
        elif n_dfs == minimo:
            ottime.append(etichetta)
    return minimo, distribuzione, ottime


def lista_ordinata(etichetta):
    """Formato di consegna: vertici in ordine crescente di etichetta, come stringhe 0/1."""
    return [stringa(v) for v in sorted(VERTICI, key=lambda v: etichetta[v])]


if __name__ == "__main__":
    inizio = time.time()
    minimo, distribuzione, ottime = esplora_tutte()
    print(f"etichettature esaminate: {sum(distribuzione.values())}")
    print(f"U(Q_3) = {minimo}; etichettature ottime: {len(ottime)}")
    print("distribuzione (cammini -> numero etichettature):", sorted(distribuzione.items()))
    print("prima etichettatura ottima (ordine crescente di etichetta):", lista_ordinata(ottime[0]))
    print(f"tempo: {time.time() - inizio:.2f} s")
