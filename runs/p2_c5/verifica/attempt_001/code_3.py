"""Cerca un codice di 20 parole di peso pari e lunghezza 9 a distanza mutua >= 4 (A(8,3)=20) con ricerca locale
casuale (esplorazione; il risultato e' verificato esattamente alla fine). Salva stelle20.txt per cerca_radici."""
import random
peso = lambda v: bin(v).count("1")
pari = [v for v in range(512) if peso(v) % 2 == 0]
compat = {v: {u for u in pari if peso(u ^ v) >= 4} for v in pari}

def greedy(rng):
    """Greedy casuale: aggiunge parole compatibili finche' possibile."""
    cod, cand = [], set(pari)
    while cand:
        v = rng.choice(sorted(cand)); cod.append(v); cand &= compat[v]
    return cod

rng = random.Random(0)
migliore = []
for tent in range(20000):
    c = greedy(rng)
    if len(c) > len(migliore):
        migliore = c; print(tent, len(c), flush=True)
    if len(migliore) >= 20: break
assert all(peso(a ^ b) >= 4 for a in migliore for b in migliore if a != b)
open("stelle20.txt", "w").write("\n".join(str(0 if peso(v) % 2 else (2 if v in migliore else 3)) for v in range(512)) + "\n")
print("codice:", [format(v, "09b") for v in migliore])
