"""Cerca in Q_5 le due strutture che realizzano 84 cammini (= |E| + 4).

Struttura A: insieme indipendente I di 13 "picchi" il cui complemento F (19 vertici) induce una foresta
             (allora F ha 15 spigoli e 4 componenti: 4 valli, tutti i p=1 su F).
Struttura B: insieme indipendente I di 12 picchi, complemento F (20 vertici, 20 spigoli) connesso
             con un solo ciclo, e sul ciclo un vertice b di grado 2 in F.
Backtracking esatto sui sottoinsiemi; si sfrutta la simmetria fissando che il vertice 0 sia un picco
(ogni insieme non vuoto di picchi si porta con una traslazione XOR a contenere 0).
"""
import sys
import time
from conta_cammini import vicini, stringa

D = 5
N = 1 << D
ADJ = [set(vicini(v, D)) for v in range(N)]


def componenti_e_spigoli(F):
    """Numero di componenti connesse e spigoli del sottografo indotto da F."""
    F = set(F)
    visti = set()
    comp = 0
    spigoli = sum(len(ADJ[v] & F) for v in F) // 2
    for s in F:
        if s in visti:
            continue
        comp += 1
        pila = [s]
        visti.add(s)
        while pila:
            v = pila.pop()
            for w in ADJ[v] & F:
                if w not in visti:
                    visti.add(w)
                    pila.append(w)
    return comp, spigoli


def cerca_indipendenti(k, callback):
    """Enumera gli insiemi indipendenti I di taglia k con 0 in I (ordine crescente); chiama callback(I)."""
    contatore = [0]

    def ricorsione(I, prossimo, vietati):
        if len(I) == k:
            contatore[0] += 1
            callback(I)
            return
        # potatura: servono ancora k-len(I) vertici tra prossimo..N-1 non vietati
        for v in range(prossimo, N):
            if v in vietati or N - v < k - len(I):
                continue
            ricorsione(I + [v], v + 1, vietati | ADJ[v] | {v})

    ricorsione([0], 1, ADJ[0] | {0})
    return contatore[0]


def struttura_a(I):
    """Struttura A: complemento aciclico (foresta con 19 vertici, 15 spigoli => 4 componenti)."""
    F = [v for v in range(N) if v not in I]
    comp, spigoli = componenti_e_spigoli(F)
    if spigoli == len(F) - comp:  # aciclico
        print("A trovata: picchi", [stringa(v, D) for v in I], "componenti", comp, flush=True)
        trovate_a.append(list(I))


def struttura_b(I):
    """Struttura B: complemento connesso unicicilico con un vertice di grado 2 sul ciclo."""
    F = [v for v in range(N) if v not in I]
    comp, spigoli = componenti_e_spigoli(F)
    if comp != 1 or spigoli != len(F):
        return
    Fs = set(F)
    # vertici sul ciclo: rimuovi iterativamente foglie (grado 1)
    gradi = {v: len(ADJ[v] & Fs) for v in F}
    resto = set(F)
    cambiato = True
    while cambiato:
        cambiato = False
        for v in list(resto):
            if sum(1 for w in ADJ[v] if w in resto) <= 1:
                resto.discard(v)
                cambiato = True
    if any(gradi[v] == 2 for v in resto):
        print("B trovata: picchi", [stringa(v, D) for v in I], flush=True)
        trovate_b.append(list(I))


if __name__ == "__main__":
    quale = sys.argv[1] if len(sys.argv) > 1 else "A"
    trovate_a, trovate_b = [], []
    inizio = time.time()
    if quale == "A":
        n = cerca_indipendenti(13, struttura_a)
        print(f"insiemi indipendenti di taglia 13 con 0: {n}; strutture A trovate: {len(trovate_a)}")
    else:
        n = cerca_indipendenti(12, struttura_b)
        print(f"insiemi indipendenti di taglia 12 con 0: {n}; strutture B trovate: {len(trovate_b)}")
    print(f"tempo {time.time()-inizio:.1f}s")
