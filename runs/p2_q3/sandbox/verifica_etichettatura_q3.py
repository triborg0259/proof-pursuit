"""
Verifica indipendente della singola etichettatura consegnata per Q_3:
stampa valli, p(v) per ogni vertice e il totale dei cammini in salita (interi esatti).
"""
D = 3
CONSEGNA = ['000', '100', '010', '110', '101', '011', '001', '111']   # ordine crescente di etichetta


def vicini(s):
    """Stringhe 0/1 che differiscono da s in esattamente una coordinata."""
    return [s[:i] + ('1' if s[i] == '0' else '0') + s[i + 1:] for i in range(D)]


def verifica(consegna):
    """Calcola p(v) in ordine di etichetta e restituisce (valli, p, totale)."""
    assert sorted(consegna) == sorted(format(k, f'0{D}b') for k in range(2 ** D)), "non e' una biiezione"
    etichetta = {s: k + 1 for k, s in enumerate(consegna)}
    p, valli = {}, []
    for s in consegna:
        minori = [w for w in vicini(s) if etichetta[w] < etichetta[s]]
        if not minori:
            valli.append(s)
        p[s] = (1 if not minori else 0) + sum(p[w] for w in minori)
    return valli, p, sum(p.values())


if __name__ == "__main__":
    valli, p, totale = verifica(CONSEGNA)
    print("valli:", valli)
    for s in CONSEGNA:
        print(f"  {s}  etichetta {CONSEGNA.index(s)+1}  p = {p[s]}")
    print("cammini in salita totali:", totale)
