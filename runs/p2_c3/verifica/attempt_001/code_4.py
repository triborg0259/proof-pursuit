import itertools, time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta
MASCHERA_O = sum(1 << o for o in DISPARI)
E1 = 1

def conta(m):
    return bin(m).count("1")

def parte_A():
    trovati, contatore = [], [0]
    altri = [o for o in DISPARI if o != E1]
    def dfs(B, mN, idx):
        contatore[0] += 1
        b = len(B)
        if 2 <= b <= 13 and conta(mN) <= 7 + b:
            trovati.append(list(B))
        if b == 13:
            return
        for k in range(idx, len(altri)):
            mN2 = mN | MASCHERA_VICINI[altri[k]]
            if conta(mN2) <= 20:
                B.append(altri[k])
                dfs(B, mN2, k + 1)
                B.pop()
    dfs([E1], MASCHERA_VICINI[E1], 0)
    print(f"parte A: nodi DFS visitati {contatore[0]}, insiemi B con |N(B)| <= 7+|B| trovati: {len(trovati)}")
    return trovati

def parte_B():
    mNB = MASCHERA_VICINI[E1]
    base = [v for v in PARI if (mNB >> v) & 1]
    extra_pari = [v for v in PARI if not (mNB >> v) & 1]
    esaminati, foreste = 0, 0
    for k in range(0, 3):
        for extra in itertools.combinations(extra_pari, k):
            R = base + list(extra)
            mR = sum(1 << r for r in R)
            base_m = (mR | MASCHERA_O) & ~(1 << E1)
            cand = [v for v in range(64) if (base_m >> v) & 1]
            for h in range(0, k + 1):
                for H in itertools.combinations(cand, h):
                    esaminati += 1
                    if e_foresta(base_m & ~sum(1 << x for x in H)):
                        foreste += 1
                        print("FORESTA TROVATA", R, H)
    print(f"parte B: coppie (R,H) esaminate {esaminati}, foreste trovate {foreste}")

if __name__ == "__main__":
    t = time.time()
    parte_A()
    parte_B()
    print(f"tempo {time.time()-t:.1f}s")
