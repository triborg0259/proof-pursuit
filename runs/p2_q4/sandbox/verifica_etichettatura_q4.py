"""Verifica ESATTA (interi Python) dell'etichettatura candidata di Q_4 con 34 cammini in salita.
Due metodi indipendenti: (i) DP di Lemma 1 in ordine di etichetta; (ii) enumerazione esplicita
(DFS) di tutti i cammini in salita da ogni valle. Stampa la tabella p(v) per la consegna."""
D = 4
N = 1 << D
# Convenzione: carattere i-esimo della stringa (da sinistra) = coordinata i; bit i dell'intero.
ETICHETTATURA = ['0000', '1111', '0111', '1101', '1110', '1011', '0001', '1000',
                 '0010', '0100', '1001', '0110', '0011', '1010', '0101', '1100']


def da_stringa(s):
    """Converte la stringa 0/1 (carattere i = coordinata i) nell'intero con bit i = coordinata i."""
    return sum(int(c) << i for i, c in enumerate(s))


def vicini(v):
    """I d vicini di v in Q_d: si cambia esattamente una coordinata."""
    return [v ^ (1 << i) for i in range(D)]


def conta_con_dp(ordine, etichetta):
    """Metodo (i): p(v) = [v valle] + somma p(u) sui vicini u con etichetta minore."""
    p = {}
    righe = []
    for v in ordine:
        minori = [u for u in vicini(v) if etichetta[u] < etichetta[v]]
        p[v] = 1 if not minori else sum(p[u] for u in minori)
        righe.append((format(v, f'0{D}b')[::-1], etichetta[v], [format(u, f'0{D}b')[::-1] for u in minori], p[v]))
    return sum(p.values()), righe


def conta_con_dfs(etichetta):
    """Metodo (ii): enumera esplicitamente ogni cammino in salita partendo da ogni valle."""
    def estendi(v):
        totale = 1  # il cammino che termina qui
        for w in vicini(v):
            if etichetta[w] > etichetta[v]:
                totale += estendi(w)
        return totale
    valli = [v for v in range(N) if all(etichetta[w] > etichetta[v] for w in vicini(v))]
    return sum(estendi(v) for v in valli), valli


def main():
    ordine = [da_stringa(s) for s in ETICHETTATURA]
    assert sorted(ordine) == list(range(N)), "non e' una biiezione"
    etichetta = {v: i + 1 for i, v in enumerate(ordine)}
    totale_dp, righe = conta_con_dp(ordine, etichetta)
    totale_dfs, valli = conta_con_dfs(etichetta)
    for stringa, lab, minori, p in righe:
        print(f"{stringa}  etichetta {lab:2d}  vicini minori {minori}  p = {p}")
    print("valli:", [format(v, f'0{D}b')[::-1] for v in valli])
    print("totale (DP di Lemma 1):", totale_dp)
    print("totale (DFS esplicita):", totale_dfs)
    assert totale_dp == totale_dfs == 34


if __name__ == "__main__":
    main()
