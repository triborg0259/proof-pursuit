"""Verifica indipendente dell'etichettatura a 88 cammini: enumerazione esplicita per DFS.

Metodo diverso dalla ricorsione p(v): da ogni valle si esplorano tutti i cammini con etichette
crescenti e si contano uno a uno. Controlla anche che l'input sia una biiezione.
"""
ORDINE = ("00000,11110,11001,10101,01101,10011,01011,00111,10000,01000,00100,11100,00010,11010,"
          "10110,01110,00001,11111,11000,10100,01100,10010,01010,00110,10001,01001,00101,11101,"
          "00011,11011,10111,01111").split(",")
D = 5


def vicini(s):
    """Vicini della stringa s: cambia un carattere."""
    return [s[:i] + ("1" if s[i] == "0" else "0") + s[i + 1:] for i in range(D)]


def conta_da(s, etichetta):
    """Numero di cammini in salita che iniziano in s (s incluso come cammino di lunghezza 1)."""
    return 1 + sum(conta_da(w, etichetta) for w in vicini(s) if etichetta[w] > etichetta[s])


if __name__ == "__main__":
    assert len(set(ORDINE)) == 32 and all(len(s) == 5 and set(s) <= {"0", "1"} for s in ORDINE)
    etichetta = {s: i + 1 for i, s in enumerate(ORDINE)}
    valli = [s for s in ORDINE if all(etichetta[w] > etichetta[s] for w in vicini(s))]
    totale = sum(conta_da(s, etichetta) for s in valli)
    print("valli:", valli)
    print("cammini in salita (DFS esplicita):", totale)
