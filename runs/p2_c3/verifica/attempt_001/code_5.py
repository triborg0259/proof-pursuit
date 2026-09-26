from conta_cammini import conta_cammini, stringa
from cubo6 import DISPARI, MASCHERA_VICINI, PARI
D = 6
R = [0b000000, 0b001111, 0b110011, 0b111100]  # bit i = coordinata i+1

def costruisci():
    m_foglie = 0
    for r in R:
        m_foglie |= MASCHERA_VICINI[r]
    foglie = [o for o in DISPARI if (m_foglie >> o) & 1]
    isolati = [o for o in DISPARI if not (m_foglie >> o) & 1]
    picchi = [v for v in PARI if v not in R]
    assert len(foglie) == 24 and len(isolati) == 8 and len(picchi) == 28
    return R + isolati + foglie + picchi

if __name__ == "__main__":
    ordine = costruisci()
    totale, p, valli = conta_cammini(ordine, D)
    print("cammini in salita:", totale, "valli:", len(valli))
    print("ordine:", ",".join(stringa(v, D) for v in ordine))
