"""Branch-and-bound ESATTO (interi) su Q_4: cerca un'etichettatura con < SOGLIA cammini in salita.
Si piazzano i vertici in ordine crescente di etichetta; p(v) e' determinato al piazzamento (Lemma 1).
Riduzione per simmetria: a ogni nodo si prova un solo candidato per orbita dello stabilizzatore
puntuale (in Aut(Q_4), ordine 384) dell'insieme gia' piazzato. Bound inferiore dimostrato nel testo.
Conferma indipendente della prova a mano; NON e' la prova principale."""
import sys, time
from itertools import permutations

D = 4
N = 1 << D
VICINI = [[v ^ (1 << i) for i in range(D)] for v in range(N)]


def automorfismi():
    """Tutti i 384 automorfismi di Q_4 come tuple immagine: v -> perm(coordinate) XOR maschera."""
    gruppo = []
    for perm in permutations(range(D)):
        for maschera in range(N):
            immagine = tuple(sum(((v >> i) & 1) << perm[i] for i in range(D)) ^ maschera for v in range(N))
            gruppo.append(immagine)
    return gruppo


GRUPPO = automorfismi()


def bound_inferiore(p, piazzati, non_piazzati):
    """Bound: per v non piazzato p(v) >= max(1, a(v) + d(v)), a(v) = somma p sui vicini piazzati,
    d(v) = archi entranti da vertici non piazzati (somma dei d(v) = archi interni E(U)).
    Minimizzando sui d(v) a somma fissata: somma_{a>=1} a(v) + max(|U0|, E(U)), U0 = {a(v)=0}."""
    totale = sum(p[v] for v in piazzati)
    zeri, archi_interni = 0, 0
    for v in non_piazzati:
        a = sum(p[u] for u in VICINI[v] if u in piazzati)
        if a == 0:
            zeri += 1
        else:
            totale += a
        archi_interni += sum(1 for u in VICINI[v] if u not in piazzati)
    return totale + max(zeri, archi_interni // 2)


def rappresentanti(non_piazzati, stabilizzatore):
    """Un candidato per orbita dello stabilizzatore sui vertici non piazzati."""
    visti, scelti = set(), []
    for v in sorted(non_piazzati):
        if v in visti:
            continue
        scelti.append(v)
        visti.update(g[v] for g in stabilizzatore)
    return scelti


class Ricerca:
    def __init__(self, soglia):
        self.soglia = soglia
        self.nodi = 0
        self.trovate = []

    def esplora(self, ordine, p, piazzati, stabilizzatore):
        """Espande un nodo: prova ogni rappresentante d'orbita come prossimo vertice."""
        self.nodi += 1
        non_piazzati = [v for v in range(N) if v not in piazzati]
        if not non_piazzati:
            self.trovate.append(list(ordine))
            return
        if bound_inferiore(p, piazzati, non_piazzati) >= self.soglia:
            return
        for v in rappresentanti(non_piazzati, stabilizzatore):
            minori = [u for u in VICINI[v] if u in piazzati]
            p[v] = 1 if not minori else sum(p[u] for u in minori)
            piazzati.add(v)
            ordine.append(v)
            self.esplora(ordine, p, piazzati, [g for g in stabilizzatore if g[v] == v])
            ordine.pop()
            piazzati.discard(v)
            del p[v]


def main():
    soglia = int(sys.argv[1]) if len(sys.argv) > 1 else 34
    inizio = time.time()
    ricerca = Ricerca(soglia)
    ricerca.esplora([], {}, set(), GRUPPO)
    print(f"soglia {soglia}: etichettature con < {soglia} cammini trovate: {len(ricerca.trovate)}")
    for ordine in ricerca.trovate[:5]:
        print("  ", [format(v, f'0{D}b')[::-1] for v in ordine])
    print(f"nodi visitati: {ricerca.nodi}; tempo: {time.time() - inizio:.1f} s")


if __name__ == "__main__":
    main()
