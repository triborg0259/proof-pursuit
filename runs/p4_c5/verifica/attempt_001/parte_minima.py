"""
Trova le parti minime (sotto-multinsiemi) di un multinsieme di moduli che sono gia'
infattibili sui residui.
COSA: per ogni sottoinsieme di indici, in ordine di dimensione crescente, esegue lo
stadio B (decidi_residui.cerca_residui); riporta i sottoinsiemi infattibili minimali
(nessun sottoinsieme proprio infattibile).
PERCHE': i regolamenti chiedono "la parte piu' piccola che gia' forza la decisione".
"""
import sys
import time
from itertools import combinations

from decidi_residui import cerca_residui


def parti_minime_infattibili(moduli, limite_nodi):
    """Sottoinsiemi infattibili minimali, in ordine di dimensione."""
    k = len(moduli)
    minimi = []
    for r in range(2, k + 1):
        for idx in combinations(range(k), r):
            if any(set(m).issubset(idx) for m in minimi):
                continue
            esito, _, _ = cerca_residui([moduli[i] for i in idx], limite_nodi)
            if esito == "NON_DECISO":
                print("   NON_DECISO su", idx)
            if esito == "INFATTIBILE":
                minimi.append(idx)
    return minimi


if __name__ == "__main__":
    moduli = tuple(int(x) for x in sys.argv[1:])
    t0 = time.time()
    esito, testimone, nodi = cerca_residui(list(moduli), 10**8)
    print(f"moduli={moduli} esito={esito} nodi_B={nodi} tempo={time.time()-t0:.2f}s testimone={testimone}")
    for idx in parti_minime_infattibili(moduli, 10**7):
        print("   parte minima infattibile: indici", idx, "moduli", tuple(moduli[i] for i in idx))
    print(f"tempo totale {time.time()-t0:.2f}s")
