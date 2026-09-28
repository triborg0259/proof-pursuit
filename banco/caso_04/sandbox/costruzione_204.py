"""Costruisce un'etichettatura di Q_6 con 204 cammini in salita e la conta esattamente.

Idea: R = codice pari a distanza minima 4 di taglia 4 (A(6,4)=4): {000000, 111100, 001111, 110011}.
Picchi P = pari \\ R (28 vertici, indipendenti). Il complemento R ∪ O e' una foresta: due vertici di R
a distanza ≥ 4 non hanno vicini dispari comuni, quindi e' l'unione di 4 stelle (centri R, foglie 24
dispari) e di 8 dispari isolati. Etichette: 1-4 centri, 5-12 dispari isolati (valli), 13-36 foglie,
37-64 picchi. Conteggio: p = 1 sui 36 vertici leggeri, p = 6 sui 28 picchi: 36 + 168 = 204.
"""
from conta_cammini import conta_cammini, stringa
from cubo6 import DISPARI, MASCHERA_VICINI, PARI

D = 6
R = [0b000000, 0b001111, 0b110011, 0b111100]  # bit i = coordinata i+1


def costruisci():
    """Ordine dei 64 vertici per etichetta crescente."""
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
