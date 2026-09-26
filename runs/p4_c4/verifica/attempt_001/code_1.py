"""
Ricerca certificata per il problema 4, parte 4 (k <= 12; rapporto per k = 9..16).

COSA: per ogni k enumera i multinsiemi non decrescenti di k moduli m_i | L_k = lcm(1..k-1),
m_i >= 2, con gcd(m_i, m_j) in [2, soglia] (soglia = k-1 per la ricerca, k per la
non-vacuita'), e li pota con regole DIMOSTRATE (vedi prova):
  (R1) gcd a coppie in [2, soglia]            -- definizione di controesempio;
  (R2) criterio di Huhn-Megyesi: per ogni M | L_k multiplo di lcm dei gcd della
       famiglia parziale, somma_i M/gcd(m_i, M) <= M   -- prova nel testo;
  (R3, solo alle foglie) famiglia ridotta: ogni potenza di primo che divide un m_i
       divide anche un altro m_j                        -- Lemma A;
  (R4, solo alle foglie) criterio (R2) su OGNI sottoinsieme di dimensione >= 2.
PERCHE': il Lemma A riduce ogni controesempio a una famiglia con questi moduli; se
nessun multinsieme sopravvive, il caso k e' chiuso. I sopravvissuti vanno poi
decisi sui residui (stadio B, file decidi_residui.py).
Aritmetica: solo interi esatti.
"""
import sys
import time
from itertools import combinations
from math import gcd, lcm


def divisori(n):
    """Divisori di n in ordine crescente."""
    return [d for d in range(1, n + 1) if n % d == 0]


def potenze_di_primo(n):
    """Potenze di primo massime che dividono n, es. 12 -> [4, 3]."""
    out, p = [], 2
    while n > 1:
        if n % p == 0:
            q = 1
            while n % p == 0:
                n //= p
                q *= p
            out.append(q)
        p += 1
    return out


def famiglia_ridotta(moduli):
    """(R3): ogni potenza di primo di ciascun m_i divide un altro m_j."""
    for i, m in enumerate(moduli):
        for q in potenze_di_primo(m):
            if not any(mj % q == 0 for j, mj in enumerate(moduli) if j != i):
                return False
    return True


def criterio_hm(sotto, moltiplicatori):
    """(R2) su un sottoinsieme: True se passa per ogni M multiplo dell'lcm dei gcd."""
    g = lcm(*(gcd(a, b) for a, b in combinations(sotto, 2)))
    for M in moltiplicatori:
        if M % g == 0 and sum(M // gcd(m, M) for m in sotto) > M:
            return False
    return True


def tutti_i_sottoinsiemi_passano(moduli, moltiplicatori):
    """(R4): criterio HM su ogni sottoinsieme di dimensione >= 2."""
    for r in range(2, len(moduli) + 1):
        for sotto in combinations(moduli, r):
            if not criterio_hm(sotto, moltiplicatori):
                return False
    return True


class Ricerca:
    """Enumerazione con potatura incrementale (R1)+(R2); (R3)+(R4) alle foglie."""

    def __init__(self, k, soglia):
        self.k, self.soglia = k, soglia
        self.L = lcm(*range(1, soglia + 1))
        self.M_list = divisori(self.L)
        self.candidati = [d for d in self.M_list if d >= 2]
        # peso[m][M] = M / gcd(m, M): contributo di m alla somma per il modulo M
        self.peso = {m: [M // gcd(m, M) for M in self.M_list] for m in self.candidati}
        self.nodi, self.foglie, self.sopravvissuti = 0, 0, []

    def hm_incrementale(self, somme, g):
        """(R2) sulla famiglia parziale: somma_M <= M per ogni M multiplo di g."""
        return all(s <= M for s, M in zip(somme, self.M_list) if M % g == 0)

    def estendi(self, parziale, somme, g):
        """Nodo della ricerca: parziale non decrescente, somme HM correnti, g = lcm dei gcd."""
        self.nodi += 1
        if len(parziale) == self.k:
            self.foglia(parziale)
            return
        for m in self.candidati:
            if parziale and m < parziale[-1]:
                continue
            gs = [gcd(m, q) for q in parziale]
            if any(not (2 <= x <= self.soglia) for x in gs):
                continue
            g2 = lcm(g, *gs) if gs else g
            somme2 = [s + w for s, w in zip(somme, self.peso[m])]
            if self.hm_incrementale(somme2, g2):
                self.estendi(parziale + [m], somme2, g2)

    def foglia(self, moduli):
        """Foglia: applica (R3) e (R4) e registra i sopravvissuti."""
        self.foglie += 1
        if famiglia_ridotta(moduli) and tutti_i_sottoinsiemi_passano(moduli, self.M_list):
            self.sopravvissuti.append(tuple(moduli))

    def esegui(self):
        t0 = time.time()
        self.estendi([], [0] * len(self.M_list), 1)
        dt = time.time() - t0
        print(f"k={self.k} soglia={self.soglia} L={self.L} candidati={len(self.candidati)} "
              f"nodi={self.nodi} foglie={self.foglie} sopravvissuti={len(self.sopravvissuti)} "
              f"tempo={dt:.2f}s", flush=True)
        for s in self.sopravvissuti:
            print("   sopravvissuto:", s, flush=True)
        return self.sopravvissuti


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "ricerca"
    ks = [int(x) for x in sys.argv[2:]] or list(range(3, 17))
    for k in ks:
        Ricerca(k, k - 1 if modo == "ricerca" else k).esegui()
