"""Certificato per il bound inferiore U(Q_5) >= 88 (implementazione 1: backtracking).

Enunciato verificato (Lemma computazionale):
  per ogni insieme indipendente I di Q_5 con |I| = 12 e per ogni vertice u di Q_5,
  il sottografo indotto da V meno (I u {u}) contiene un ciclo.
Riduzione: le traslazioni x -> x XOR t sono automorfismi di Q_5, quindi basta considerare
gli I che contengono il vertice 0 (ogni I non vuoto si trasla a contenerne uno).
Aciclicita' decisa con conteggio esatto: componenti + spigoli (un grafo e' una foresta sse
spigoli = vertici - componenti). Tutto intero: rigore = exact.
"""
import time
from conta_cammini import vicini

D = 5
N = 1 << D
ADJ = [set(vicini(v, D)) for v in range(N)]


def e_foresta(S):
    """True sse il sottografo indotto da S e' aciclico (spigoli = |S| - componenti)."""
    S = set(S)
    spigoli = sum(len(ADJ[v] & S) for v in S) // 2
    visti, comp = set(), 0
    for s in S:
        if s in visti:
            continue
        comp += 1
        pila, visti = [s], visti | {s}
        while pila:
            v = pila.pop()
            for w in ADJ[v] & S:
                if w not in visti:
                    visti.add(w)
                    pila.append(w)
    return spigoli == len(S) - comp


def indipendenti_con_zero(k):
    """Genera tutti gli insiemi indipendenti di taglia k contenenti 0 (vertici in ordine crescente)."""
    def ric(I, prossimo, vietati):
        if len(I) == k:
            yield list(I)
            return
        for v in range(prossimo, N):
            if v not in vietati and N - v >= k - len(I):
                yield from ric(I + [v], v + 1, vietati | ADJ[v] | {v})
    yield from ric([0], 1, ADJ[0] | {0})


if __name__ == "__main__":
    inizio = time.time()
    n_insiemi, n_test, violazioni = 0, 0, []
    for I in indipendenti_con_zero(12):
        n_insiemi += 1
        for u in range(N):
            if u in I:
                continue
            n_test += 1
            if e_foresta(set(range(N)) - set(I) - {u}):
                violazioni.append((I, u))
    print(f"insiemi indipendenti di taglia 12 contenenti 0: {n_insiemi}")
    print(f"coppie (I,u) esaminate: {n_test}; complementi aciclici trovati: {len(violazioni)}")
    print(f"tempo {time.time()-inizio:.2f}s")
