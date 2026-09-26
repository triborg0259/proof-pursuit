import itertools, time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta
MASCHERA_O = sum(1 << o for o in DISPARI)
E1 = 1

def coppia_coperta(a, b, H_O):
    return any((MASCHERA_VICINI[o] >> a) & 1 and (MASCHERA_VICINI[o] >> b) & 1 for o in H_O)

def compatibile(v, R, H_O):
    return all(bin(v ^ r).count("1") != 2 or coppia_coperta(v, r, H_O) for r in R)

def dfs(R, idx, taglia, H_O, contatori):
    if len(R) == taglia:
        contatori["candidati"] += 1
        m = sum(1 << r for r in R) | (MASCHERA_O & ~sum(1 << o for o in H_O))
        if e_foresta(m):
            contatori["foreste"] += 1
            print("FORESTA TROVATA", R, H_O)
        return
    for k in range(idx, len(PARI)):
        if compatibile(PARI[k], R, H_O):
            R.append(PARI[k])
            dfs(R, k + 1, taglia, H_O, contatori)
            R.pop()

def main():
    inizio = time.time()
    altri = [o for o in DISPARI if o != E1]
    scelte_H = {0: [()], 1: [(E1,)], 2: [(E1, o) for o in altri]}
    for h in (0, 1, 2):
        contatori = {"candidati": 0, "foreste": 0}
        for H_O in scelte_H[h]:
            dfs([], 0, 5 + h, list(H_O), contatori)
        print(f"h={h}: insiemi H_O {len(scelte_H[h])}, candidati R' sopravvissuti alla potatura "
              f"{contatori['candidati']}, foreste {contatori['foreste']}, tempo {time.time()-inizio:.1f}s")

if __name__ == "__main__":
    main()
