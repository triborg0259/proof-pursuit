"""
Verifica indipendente dell'etichettatura di Q_4 consegnata dal Researcher (metodo diverso dal suo):
costruzione esplicita, livello per livello, di tutti i cammini in salita a partire dalle valli.
Controlla anche che la lista sia una biiezione su {0,1}^4. Interi esatti.
Uso: python3 problema-2/certificati/q4_verifica_etichettatura_indipendente.py
"""
D = 4
CONSEGNATA = ["0000", "1111", "0111", "1101", "1110", "1011", "0001", "1000",
              "0010", "0100", "1001", "0110", "0011", "1010", "0101", "1100"]


def vicini(s):
    """Le d stringhe che differiscono da s in una sola posizione."""
    return [s[:i] + ("1" if s[i] == "0" else "0") + s[i + 1:] for i in range(D)]


def conta_cammini(etichetta):
    """Tutti i cammini in salita come tuple esplicite, per lunghezza crescente; ritorna il totale."""
    valli = [v for v in etichetta if all(etichetta[w] > etichetta[v] for w in vicini(v))]
    livello = [(v,) for v in valli]
    totale = 0
    while livello:
        totale += len(livello)
        livello = [c + (w,) for c in livello for w in vicini(c[-1]) if etichetta[w] > etichetta[c[-1]]]
    return totale, valli


if __name__ == "__main__":
    assert len(CONSEGNATA) == 16 and len(set(CONSEGNATA)) == 16 and all(len(s) == 4 and set(s) <= {"0", "1"} for s in CONSEGNATA)
    etichetta = {s: k + 1 for k, s in enumerate(CONSEGNATA)}   # etichetta = posizione nella lista
    totale, valli = conta_cammini(etichetta)
    print(f"biiezione ok; valli: {valli}; cammini in salita: {totale}")
