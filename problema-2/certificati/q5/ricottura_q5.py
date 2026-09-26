"""Ricerca locale (simulated annealing) sul numero di cammini in salita di Q_5.

Esplorazione: trova etichettature con pochi cammini. NON e' una prova (minimo locale possibile).
Stato = permutazione dei 32 vertici; mossa = scambio di due etichette; punteggio esatto (interi).
"""
import random
import sys
import time
from conta_cammini import conta_cammini, stringa

D = 5
N = 1 << D


def ricottura(seed, passi=200000, t0=2.0, t1=0.05):
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
    semi = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    inizio = time.time()
    globale = None
    for seed in range(semi):
        v, o = ricottura(seed)
        print(f"seed {seed}: {v}", flush=True)
        if globale is None or v < globale[0]:
            globale = (v, o)
    v, o = globale
    tot, p, valli = conta_cammini(o, D)
    print("migliore:", v, "valli:", [stringa(x, D) for x in valli])
    print("ordine:", ",".join(stringa(x, D) for x in o))
    print(f"tempo {time.time()-inizio:.1f}s")
