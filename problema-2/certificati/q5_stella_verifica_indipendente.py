"""
Verifica indipendente dell'affermazione (★) usata nel lower bound di U(Q_5) (metodo diverso dagli script del Researcher).

(★): esistono un insieme indipendente I di Q_5 con |I| = 12 e un vertice u ∉ I tali che Q_5 − (I ∪ {u}) è una foresta.
La prova mostra che ogni etichettatura con ≤ 87 cammini implica (★); qui si verifica che (★) è FALSA.

Metodo: enumerazione di tutti gli insiemi indipendenti di taglia 12 come bitmask su 32 bit (backtracking con
maschera dei vertici vietati), senza riduzione per simmetria; per ogni u ∉ I il test di aciclicità è per POTATURA
DELLE FOGLIE: si tolgono ripetutamente i vertici di grado ≤ 1 nel sottografo indotto; è una foresta se e solo se
non resta nulla. Interi esatti, nessuna dipendenza.  Uso: python3 problema-2/certificati/q5_stella_verifica_indipendente.py
"""
import time

D, N = 5, 32
ADJ = [sum(1 << (v ^ (1 << i)) for i in range(D)) for v in range(N)]   # vicini di v come bitmask
TUTTI = (1 << N) - 1


def insiemi_indipendenti(taglia):
    """Genera le bitmask di tutti gli insiemi indipendenti di `taglia` vertici (ordine crescente, senza ripetizioni)."""
    def ricorsione(insieme, vietati, prossimo, mancanti):
        if mancanti == 0:
            yield insieme
            return
        for v in range(prossimo, N - mancanti + 1):
            if not (vietati >> v) & 1:
                yield from ricorsione(insieme | (1 << v), vietati | ADJ[v] | (1 << v), v + 1, mancanti - 1)
    yield from ricorsione(0, 0, 0, taglia)


def e_foresta(vertici):
    """Potatura delle foglie sul sottografo indotto dalla bitmask `vertici`: resta vuoto ⇔ aciclico."""
    while vertici:
        foglie = 0
        for v in range(N):
            if (vertici >> v) & 1 and bin(ADJ[v] & vertici).count("1") <= 1:
                foglie |= 1 << v
        if not foglie:
            return False          # tutti i vertici rimasti hanno grado ≥ 2: contengono un ciclo
        vertici &= ~foglie
    return True


if __name__ == "__main__":
    inizio = time.time()
    n_insiemi = coppie = aciclici = 0
    for I in insiemi_indipendenti(12):
        n_insiemi += 1
        for u in range(N):
            if not (I >> u) & 1:
                coppie += 1
                if e_foresta(TUTTI & ~I & ~(1 << u)):
                    aciclici += 1
    print(f"insiemi indipendenti di taglia 12: {n_insiemi}; coppie (I,u): {coppie}; complementi aciclici: {aciclici}; "
          f"tempo {time.time() - inizio:.2f} s")
    print("(★) è", "VERA" if aciclici else "FALSA")
