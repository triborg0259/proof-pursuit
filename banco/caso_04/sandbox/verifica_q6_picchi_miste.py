"""Certificato (parte 2) per U(Q_6) >= 204: caso 'picchi in entrambe le classi'.

Struttura: P = A ∪ B con A ⊆ E, B ⊆ O indipendente, |A| ≥ |B| = b ≥ 1, |A| + b = q ∈ {25,26,27},
R = E \\ A ⊇ N(B), |R| = 32 - q + b, H con |H| ≤ 27 - q, e (R ∪ (O \\ B)) \\ H foresta.
Condizione necessaria: |N(B)| ≤ |R| ≤ 7 + b, con 1 ≤ b ≤ 13.

Parte A (b ≥ 2): enumera per DFS tutti i B ⊆ O con e_1 ∈ B (WLOG: le traslazioni pari sono
transitive su O) e |N(B)| ≤ 20 (potatura valida perche' N(B) cresce con B e 7 + b ≤ 20);
stampa ogni B con 2 ≤ |B| ≤ 13 e |N(B)| ≤ 7 + |B|. Attesa: nessuno.
Parte B (b = 1): B = {e_1}, R ⊇ N(e_1) con al piu' 2 vertici pari extra, |H| ≤ |R| - 6:
verifica diretta con union-find su ogni H possibile. Attesa: nessuna foresta.
"""
import itertools
import time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta

MASCHERA_O = sum(1 << o for o in DISPARI)
E1 = 1  # il vertice dispari 100000


def conta(m):
    return bin(m).count("1")


def dfs_B(B, mN, inizio_idx, trovati, contatore):
    """Estende B con dispari di indice ≥ inizio_idx mantenendo |N(B)| ≤ 20."""
    contatore[0] += 1
    b = len(B)
    if 2 <= b <= 13 and conta(mN) <= 7 + b:
        trovati.append(list(B))
    if b == 13:
        return
    for k in range(inizio_idx, len(DISPARI)):
        o = DISPARI[k]
        mN2 = mN | MASCHERA_VICINI[o]
        if conta(mN2) <= 20:
            B.append(o)
            dfs_B(B, mN2, k + 1, trovati, contatore)
            B.pop()


def parte_A():
    trovati, contatore = [], [0]
    altri = [o for o in DISPARI if o != E1]
    B = [E1]
    for k in range(len(altri)):
        pass
    # DFS sui dispari diversi da e_1, con e_1 fisso in B
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
    dfs(B, MASCHERA_VICINI[E1], 0)
    print(f"parte A: nodi DFS visitati {contatore[0]}, insiemi B con |N(B)| ≤ 7+|B| trovati: {len(trovati)}")
    for B in trovati[:20]:
        print("  B =", B, "|N(B)| =", conta(sum(MASCHERA_VICINI[o] for o in B)))
    return trovati


def parte_B():
    """b = 1: B = {e_1}; R = N(e_1) ∪ (0..2 pari extra); |H| ≤ |R| - 6."""
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
