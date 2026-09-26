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
Regole OPZIONALI (attive solo con i flag; ciascuna e' dimostrata nel testo sotto ipotesi esplicite):
  (M4, flag senza_potenze) nessun modulo e' potenza di primo -- vale se l'enunciato e'
       gia' provato per ogni dimensione <= ceil(k/2) (per k <= 24 basta k <= 12);
  (M5, flag tre_multipli) almeno tre moduli sono multipli di k-1 -- vale se l'enunciato
       e' gia' provato per la dimensione k-1.
Limite di tempo: allo scadere la ricerca si ferma e stampa i conteggi raggiunti (NON TERMINATA).
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


def potenza_di_primo(n):
    """True se n = p^e con p primo, e >= 1."""
    return len(potenze_di_primo(n)) == 1


class TempoScaduto(Exception):
    """Segnala che il limite di tempo e' stato superato."""


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

    def __init__(self, k, soglia, senza_potenze=False, tre_multipli=False, limite_secondi=600):
        self.k, self.soglia = k, soglia
        self.senza_potenze, self.tre_multipli = senza_potenze, tre_multipli
        self.limite_secondi, self.t0 = limite_secondi, None
        self.L = lcm(*range(1, soglia + 1))
        self.M_list = divisori(self.L)
        self.candidati = [d for d in self.M_list if d >= 2]
        if senza_potenze:
            self.candidati = [d for d in self.candidati if not potenza_di_primo(d)]
        # peso[m][M] = M / gcd(m, M): contributo di m alla somma per il modulo M
        self.peso = {m: [M // gcd(m, M) for M in self.M_list] for m in self.candidati}
        self.nodi, self.foglie, self.sopravvissuti = 0, 0, []

    def hm_incrementale(self, somme, g):
        """(R2) sulla famiglia parziale: somma_M <= M per ogni M multiplo di g."""
        return all(s <= M for s, M in zip(somme, self.M_list) if M % g == 0)

    def estendi(self, parziale, somme, g):
        """Nodo della ricerca: parziale non decrescente, somme HM correnti, g = lcm dei gcd."""
        self.nodi += 1
        if time.time() - self.t0 > self.limite_secondi:
            raise TempoScaduto
        if self.tre_multipli and self.multipli_insufficienti(parziale):
            return
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

    def multipli_insufficienti(self, parziale):
        """(M5): i multipli di k-1 presenti piu' i posti liberi non arrivano a tre."""
        presenti = sum(1 for m in parziale if m % (self.k - 1) == 0)
        return presenti + (self.k - len(parziale)) < 3

    def foglia(self, moduli):
        """Foglia: applica (R3) e (R4) e registra i sopravvissuti."""
        self.foglie += 1
        if famiglia_ridotta(moduli) and tutti_i_sottoinsiemi_passano(moduli, self.M_list):
            self.sopravvissuti.append(tuple(moduli))

    def esegui(self):
        self.t0 = time.time()
        stato = "TERMINATA"
        try:
            self.estendi([], [0] * len(self.M_list), 1)
        except TempoScaduto:
            stato = "NON_TERMINATA"
        dt = time.time() - self.t0
        flag = f" senza_potenze={self.senza_potenze} tre_multipli={self.tre_multipli}"
        print(f"k={self.k} soglia={self.soglia} L={self.L} candidati={len(self.candidati)} "
              f"stato={stato}{flag} "
              f"nodi={self.nodi} foglie={self.foglie} sopravvissuti={len(self.sopravvissuti)} "
              f"tempo={dt:.2f}s", flush=True)
        for s in self.sopravvissuti:
            print("   sopravvissuto:", s, flush=True)
        return self.sopravvissuti


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "ricerca"
    flags = [a for a in sys.argv[2:] if a.startswith("--")]
    ks = [int(x) for x in sys.argv[2:] if not x.startswith("--")] or list(range(3, 17))
    for k in ks:
        Ricerca(k, k - 1 if modo == "ricerca" else k,
                senza_potenze="--senza-potenze" in flags,
                tre_multipli="--tre-multipli" in flags).esegui()
