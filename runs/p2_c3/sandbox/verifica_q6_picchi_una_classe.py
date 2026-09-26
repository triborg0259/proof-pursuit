"""Certificato (parte 1) per U(Q_6) >= 204: caso 'picchi tutti nella classe pari'.

Enunciato finito da confutare (S0): esistono R ⊆ E (pari) con |R| = r in {5,6,7}, 0 ∈ R,
e H ⊆ R ∪ O con |H| ≤ r - 5, tali che il sottografo indotto da (R ∪ O) \\ H e' una foresta.
(P = E \\ R sono i picchi, q = 32 - r; |H| ≤ 27 - q.) La riduzione WLOG 0 ∈ R usa le traslazioni
per vettori pari, automorfismi di Q_6 che preservano E e sono transitive su E.

Pre-filtro esatto (condizione necessaria): ogni coppia di vertici di R \\ H a distanza 2 ha due vicini
dispari comuni; se nessuno dei due e' in H, i quattro vertici formano un 4-ciclo. Quindi ogni coppia a
distanza 2 di R' = R \\ H_E deve stare dentro N(o) per qualche o ∈ H_O. I sopravvissuti al pre-filtro
sono controllati con union-find sull'intero sottografo indotto.
"""
import itertools
import sys
import time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta

MASCHERA_O = sum(1 << o for o in DISPARI)
DIST2 = {(a, b) for a in PARI for b in PARI if a < b and bin(a ^ b).count("1") == 2}


def coppie_dist2(insieme):
    """Coppie a distanza 2 dentro un insieme di vertici pari."""
    return [(a, b) for a, b in itertools.combinations(sorted(insieme), 2) if (a, b) in DIST2]


def coperte_da(o, coppie):
    """Coppie (a,b) con a,b entrambi vicini di o."""
    m = MASCHERA_VICINI[o]
    return {c for c in coppie if (m >> c[0]) & 1 and (m >> c[1]) & 1}


def prefiltro_ok(R_residuo, H_dispari):
    """True se ogni coppia a distanza 2 di R_residuo e' coperta da un dispari di H."""
    coppie = coppie_dist2(R_residuo)
    coperte = set()
    for o in H_dispari:
        coperte |= coperte_da(o, coppie)
    return len(coperte) == len(coppie)


def candidati_dispari(R):
    """Dispari con almeno 2 vicini in R (rimuovere una foglia/isolato non spezza cicli)."""
    mR = sum(1 << r for r in R)
    return [o for o in DISPARI if bin(MASCHERA_VICINI[o] & mR).count("1") >= 2]


def esiste_H(R, h_max):
    """Esiste H con |H| ≤ h_max tale che (R ∪ O) \\ H sia foresta? Ritorna H o None."""
    mR = sum(1 << r for r in R)
    cand = list(R) + candidati_dispari(R)
    for h in range(h_max + 1):
        for H in itertools.combinations(cand, h):
            R_res = [r for r in R if r not in H]
            if not prefiltro_ok(R_res, [o for o in H if o in DISPARI]):
                continue
            mH = sum(1 << x for x in H)
            if e_foresta((mR | MASCHERA_O) & ~mH):
                return H
    return None


def main():
    inizio = time.time()
    altri_pari = [v for v in PARI if v != 0]
    for r in (5, 6, 7):
        esaminati, soluzioni = 0, 0
        for resto in itertools.combinations(altri_pari, r - 1):
            R = (0,) + resto
            esaminati += 1
            if esiste_H(R, r - 5) is not None:
                soluzioni += 1
                print("SOLUZIONE TROVATA", R)
        print(f"|R|={r}: insiemi esaminati {esaminati}, soluzioni {soluzioni}, "
              f"tempo cumulato {time.time()-inizio:.1f}s", flush=True)


if __name__ == "__main__":
    main()
