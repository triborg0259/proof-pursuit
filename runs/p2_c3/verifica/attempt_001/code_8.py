import random, sys, time
from conta_cammini import conta_cammini, stringa
D = 6
N = 1 << D

def ricottura(seed, passi, t0=3.0, t1=0.05):
    rng = random.Random(seed)
    ordine = list(range(N)); rng.shuffle(ordine)
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
    seed = int(sys.argv[1]); passi = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
    v, o = ricottura(seed, passi)
    tot, p, valli = conta_cammini(o, D)
    print(f"seed {seed}: migliore {v}, valli {len(valli)}")
    print("ordine:", ",".join(stringa(x, D) for x in o))
