"""Certificato per il bound inferiore U(Q_5) >= 88 (implementazione 2, metodo diverso).

Stesso enunciato di verifica_q5_indipendenti.py, ma senza usare la simmetria:
ogni insieme indipendente e' A u B con A sottoinsieme dei vertici di peso pari e
B sottoinsieme dei vertici di peso dispari NON adiacenti ad A. Si scorrono tutti i 2^16
sottoinsiemi A (bitmask), poi tutti i B di taglia 12-|A| tra i dispari disponibili.
Aciclicita' con union-find (metodo diverso dal conteggio componenti). Rigore = exact.
"""
import itertools
import time

D = 5
N = 1 << D
PARI = [v for v in range(N) if bin(v).count("1") % 2 == 0]
DISPARI = [v for v in range(N) if bin(v).count("1") % 2 == 1]
SPIGOLI = [(v, v ^ (1 << i)) for v in range(N) for i in range(D) if v < v ^ (1 << i)]


def maschera_vicini(v):
    """Bitmask dei vicini di v."""
    return sum(1 << (v ^ (1 << i)) for i in range(D))


VIC = [maschera_vicini(v) for v in range(N)]


def ha_ciclo(maschera_vertici):
    """True sse il sottografo indotto dai vertici nella bitmask contiene un ciclo (union-find)."""
    padre = list(range(N))

    def trova(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for a, b in SPIGOLI:
        if (maschera_vertici >> a) & 1 and (maschera_vertici >> b) & 1:
            ra, rb = trova(a), trova(b)
            if ra == rb:
                return True
            padre[ra] = rb
    return False


def insiemi_indipendenti_12():
    """Genera le bitmask di tutti gli insiemi indipendenti di taglia 12."""
    for bits in range(1 << 16):
        A = [PARI[i] for i in range(16) if (bits >> i) & 1]
        if len(A) > 12:
            continue
        vietati = 0
        for a in A:
            vietati |= VIC[a]
        disponibili = [w for w in DISPARI if not (vietati >> w) & 1]
        for B in itertools.combinations(disponibili, 12 - len(A)):
            m = 0
            for x in A + list(B):
                m |= 1 << x
            yield m


if __name__ == "__main__":
    inizio = time.time()
    tutti = (1 << N) - 1
    n_insiemi, n_test, aciclici = 0, 0, 0
    for I in insiemi_indipendenti_12():
        n_insiemi += 1
        for u in range(N):
            if (I >> u) & 1:
                continue
            n_test += 1
            if not ha_ciclo(tutti & ~I & ~(1 << u)):
                aciclici += 1
    print(f"insiemi indipendenti di taglia 12 (tutti, senza simmetria): {n_insiemi}")
    print(f"coppie (I,u) esaminate: {n_test}; complementi aciclici: {aciclici}")
    print(f"tempo {time.time()-inizio:.2f}s")
