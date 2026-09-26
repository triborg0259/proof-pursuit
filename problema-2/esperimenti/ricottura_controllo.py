"""Ricottura di controllo per Q_d (esplorazione, NON prova): parte dall'etichettatura a stelle e da permutazioni casuali,
mosse = scambio di due etichette, punteggio esatto. Serve a vedere se mosse locali scendono sotto il valore costruito.
Uso: python3 ricottura_controllo.py d passi semi"""
import random, sys, time
from conta_cammini import conta_cammini, da_stringa

d, passi, semi = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
N = 1 << d
stelle = [da_stringa(s) for s in open(f"etichettatura_q{d}.txt").read().strip().split(",")]


def ricottura(ordine, seed, t0=2.0, t1=0.05):
    rng = random.Random(seed)
    val = conta_cammini(ordine, d)[0]
    migliore = val
    for k in range(passi):
        t = t0 * (t1 / t0) ** (k / passi)
        i, j = rng.randrange(N), rng.randrange(N)
        ordine[i], ordine[j] = ordine[j], ordine[i]
        nuovo = conta_cammini(ordine, d)[0]
        if nuovo <= val or rng.random() < 2.718 ** ((val - nuovo) / t):
            val = nuovo
            migliore = min(migliore, val)
        else:
            ordine[i], ordine[j] = ordine[j], ordine[i]
    return migliore


inizio = time.time()
print(f"d={d} partenza dalle stelle: {conta_cammini(stelle, d)[0]}", flush=True)
print(f"  ricottura dalle stelle -> {ricottura(stelle[:], 0)}", flush=True)
for s in range(semi):
    o = list(range(N)); random.Random(100 + s).shuffle(o)
    print(f"  ricottura da caso seed {s} -> {ricottura(o, s)}", flush=True)
print(f"tempo {time.time() - inizio:.0f}s")
