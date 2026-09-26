"""
Ricerca esaustiva per il problema 4, parte 3 (k <= 8).

COSA: enumera tutte le famiglie di k classi a_i (mod m_i), a due a due disgiunte,
con m_i | 420, 2 <= m_i, 0 <= a_i < m_i, e con gcd(m_i, m_j) <= soglia per ogni coppia.
PERCHE': il Lemma di riduzione (nella prova) mostra che ogni controesempio di taglia k
(famiglia disgiunta con tutti i gcd <= k-1 <= 7) si riduce a una tale famiglia con
m_i | 420 = 2^2 * 3 * 5 * 7. Se non ne esiste nessuna, la tesi vale per quel k.

Metodo: grafo G sui vertici (a, m); arco fra due vertici se e solo se le due classi
sono disgiunte E il gcd dei moduli e' <= soglia. Enumerazione di TUTTE le clique di
taglia k come tuple crescenti di indici (nessuna potatura oltre la definizione di arco).
Aritmetica: esatta (interi Python).
"""
import sys
import time
from math import gcd

N_RIDUZIONE = 420


def divisori(n):
    """Tutti i divisori di n, in ordine crescente."""
    return [d for d in range(1, n + 1) if n % d == 0]


def costruisci_vertici(n):
    """Lista delle classi (a, m) con m | n, m >= 2, 0 <= a < m."""
    return [(a, m) for m in divisori(n) if m >= 2 for a in range(m)]


def compatibili(v, w, soglia):
    """Vero se le classi v, w sono disgiunte e gcd dei moduli <= soglia (criterio (*))."""
    (a, m), (b, n) = v, w
    g = gcd(m, n)
    return g <= soglia and (a - b) % g != 0


def costruisci_adiacenza(vertici, soglia):
    """Bitset di adiacenza: bit j di adj[i] acceso se i e j compatibili (solo j > i)."""
    adj = []
    for i, v in enumerate(vertici):
        bits = 0
        for j in range(i + 1, len(vertici)):
            if compatibili(v, vertici[j], soglia):
                bits |= 1 << j
        adj.append(bits)
    return adj


def enumera_clique(adj, k, raccogli):
    """
    Enumera tutte le k-clique come tuple crescenti di indici.
    Ritorna (numero_nodi_visitati, lista_clique). Un nodo = una chiamata ricorsiva
    con clique parziale non vuota (ogni prefisso visitato una sola volta).
    """
    nodi = 0
    trovate = []

    def ricorsione(parziale, candidati):
        nonlocal nodi
        nodi += 1
        if len(parziale) == k:
            trovate.append(tuple(parziale))
            return
        c = candidati
        while c:
            j = (c & -c).bit_length() - 1
            c &= c - 1
            ricorsione(parziale + [j], candidati & adj[j])

    tutti = (1 << len(adj)) - 1
    ricorsione([], tutti)
    return nodi - 1, trovate  # il nodo radice (clique vuota) non si conta


def esegui(k, soglia, vertici, stampa_sopravvissuti):
    """Una taglia k con una soglia gcd; stampa conteggi, tempo e sopravvissuti."""
    t0 = time.time()
    adj = costruisci_adiacenza(vertici, soglia)
    nodi, clique = enumera_clique(adj, k, True)
    dt = time.time() - t0
    print(f"k={k} soglia_gcd<={soglia} vertici={len(vertici)} nodi={nodi} "
          f"sopravvissuti={len(clique)} tempo={dt:.2f}s")
    if stampa_sopravvissuti:
        for cl in clique:
            print("   ", [vertici[i] for i in cl])
    return nodi, clique


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "certificato"
    # Universo: divisori di N (default 420). Per il test di non vacuita' a k=8
    # serve N=840, perche' 8 non divide 420 (il certificato usa sempre 420).
    universo = int(sys.argv[3]) if len(sys.argv) > 3 else N_RIDUZIONE
    vertici = costruisci_vertici(universo)
    if modo == "certificato":
        # Controesempio di taglia k: tutti i gcd <= k-1.
        for k in range(3, 9):
            esegui(k, k - 1, vertici, stampa_sopravvissuti=True)
    elif modo == "non_vacuita":
        # Soglia gcd <= k: la partizione 0..k-1 (mod k) DEVE comparire.
        k = int(sys.argv[2])
        nodi, clique = esegui(k, k, vertici, stampa_sopravvissuti=False)
        atteso = tuple(vertici.index((a, k)) for a in range(k))
        print("   partizione banale trovata:", atteso in set(clique))
    else:
        raise SystemExit("modo: certificato | non_vacuita K [N]")


if __name__ == "__main__":
    main()
