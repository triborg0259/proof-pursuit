"""
Verifica indipendente di U(Q_3) = 14 (scritta separatamente dal Researcher, metodo diverso).

Metodo: per ogni etichettatura (8! = 40320) si costruisce l'insieme di tutte le sequenze crescenti di vertici
adiacenti per lunghezza crescente (BFS per livelli sull'ordine delle etichette), partendo dalle sole valli.
Nessuna ricorsione e nessuna programmazione dinamica: si contano le sequenze una per una, come oggetti espliciti.
Interi esatti. Uso: python3 problema-2/certificati/q3_verifica_indipendente.py
"""
import itertools
import time

VERTICI = list(range(8))                       # vertice = intero 0..7, bit i = coordinata i
VICINI = {v: [v ^ (1 << i) for i in range(3)] for v in VERTICI}


def valli(etichetta):
    """Vertici con tutti i vicini più alti: sono gli unici punti di partenza ammessi."""
    return [v for v in VERTICI if all(etichetta[w] > etichetta[v] for w in VICINI[v])]


def conta_cammini(etichetta):
    """Costruisce esplicitamente tutti i cammini in salita, livello per livello, e li conta."""
    livello = [(v,) for v in valli(etichetta)]  # cammini di lunghezza 1
    totale = 0
    while livello:
        totale += len(livello)
        livello = [c + (w,) for c in livello for w in VICINI[c[-1]] if etichetta[w] > etichetta[c[-1]]]
    return totale


def stringa(v):
    """Vertice come stringa 0/1 con la posizione i = coordinata i (bit 0 a sinistra)."""
    return "".join(str((v >> i) & 1) for i in range(3))


if __name__ == "__main__":
    inizio = time.time()
    minimo, esempio, quante_ottime = None, None, 0
    for perm in itertools.permutations(VERTICI):          # perm[k] = vertice con etichetta k+1
        etichetta = {v: k + 1 for k, v in enumerate(perm)}
        n = conta_cammini(etichetta)
        if minimo is None or n < minimo:
            minimo, esempio, quante_ottime = n, perm, 1
        elif n == minimo:
            quante_ottime += 1
    print(f"U(Q_3) = {minimo}; etichettature ottime: {quante_ottime}; tempo {time.time() - inizio:.2f} s")
    print("esempio ottimo (ordine crescente di etichetta):", [stringa(v) for v in esempio])
    # controllo della specifica etichettatura consegnata dal Researcher
    consegnata = ["000", "100", "010", "110", "101", "011", "001", "111"]
    et = {int(s[::-1], 2): k + 1 for k, s in enumerate(consegnata)}
    print("cammini dell'etichettatura consegnata:", conta_cammini(et))
