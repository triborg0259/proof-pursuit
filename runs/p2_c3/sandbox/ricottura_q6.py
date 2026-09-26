"""Ricerca locale (simulated annealing) sui cammini in salita di Q_6.

Esplorazione, NON prova: trova etichettature con pochi cammini (possibile minimo locale).
Stato = permutazione dei 64 vertici; mossa = scambio di due etichette; punteggio esatto (interi).
Uso: python3 ricottura_q6.py SEED [PASSI]
"""
import random
import sys
import time
from conta_cammini import conta_cammini, stringa

D = 6
N = 1 << D


def ricottura(seed, passi, t0=3.0, t1=0.05):
    """Un run di annealing con seed fissato; ritorna (miglior_valore, miglior_ordine)."""
    rng = random.Random(seed)
    ordine = list(range(N))
    rng.shuffle(ordine)
    val = conta_cammini(ordine, D)[0]
    migliore, miglior_ordine = val, ordine[:]
    for k in range(passi):
        t = t0 * (t1 / t0) ** (k / passi)
        i, j = rng.randrange(N), rng.randrange(N)
        ordine[i], ordine[j] = ordine[j], ordine[i]
        nuovo = conta_cammini(ordine, D)[0]
        if nuovo <= val or rng.random() < 2.718 ** ((val - nuovo) / t):
            val = nuovo
            if val < migliore:
                migliore, miglior_ordine = val, ordine[:]
        else:
            ordine[i], ordine[j] = ordine[j], ordine[i]
    return migliore, miglior_ordine


if __name__ == "__main__":
    seed = int(sys.argv[1])
    passi = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
    inizio = time.time()
    v, o = ricottura(seed, passi)
    tot, p, valli = conta_cammini(o, D)
    print(f"seed {seed}: migliore {v}, valli {len(valli)}, tempo {time.time()-inizio:.0f}s")
    print("ordine:", ",".join(stringa(x, D) for x in o))
