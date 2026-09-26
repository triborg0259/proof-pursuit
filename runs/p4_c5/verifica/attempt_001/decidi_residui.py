"""
Stadio B per il problema 4, parte 4: decisione sui residui di un multinsieme di moduli.

COSA: dati moduli (m_1..m_k), cerca residui a_i (a_1 = 0 per traslazione) con
gcd(m_i, m_j) non divisore di a_i - a_j per ogni coppia (criterio (*)):
backtracking esatto sugli indici, dominio Z/m_i, controllo su tutte le coppie precedenti.
PERCHE': i moduli sopravvissuti allo stadio A (ricerca_moduli_hm.py) vanno decisi uno per
uno; un testimone trovato viene riverificato direttamente con (*).
Esito per ciascun multinsieme: FATTIBILE (testimone), INFATTIBILE (esaurito), o
NON_DECISO (limite di nodi raggiunto: risultato onesto, non una prova).
"""
import sys
import time
from math import gcd

from ricerca_moduli_hm import Ricerca


def verifica_diretta(famiglia):
    """Controlla con (*) che le classi (a, m) siano a due a due disgiunte."""
    for i in range(len(famiglia)):
        for j in range(i + 1, len(famiglia)):
            (a, m), (b, n) = famiglia[i], famiglia[j]
            if (a - b) % gcd(m, n) == 0:
                return False
    return True


def cerca_residui(moduli, limite_nodi):
    """Backtracking: restituisce (esito, testimone, nodi)."""
    k = len(moduli)
    g = [[gcd(moduli[i], moduli[j]) for j in range(k)] for i in range(k)]
    residui, stato = [], {"nodi": 0}

    def estendi():
        stato["nodi"] += 1
        if stato["nodi"] > limite_nodi:
            return "NON_DECISO"
        i = len(residui)
        if i == k:
            return "FATTIBILE"
        for a in ([0] if i == 0 else range(moduli[i])):
            if all((a - residui[j]) % g[i][j] != 0 for j in range(i)):
                residui.append(a)
                esito = estendi()
                if esito != "INFATTIBILE":
                    return esito
                residui.pop()
        return "INFATTIBILE"

    esito = estendi()
    testimone = tuple(zip(residui, moduli)) if esito == "FATTIBILE" else None
    return esito, testimone, stato["nodi"]


def decidi_tutti(k, soglia, limite_nodi):
    """Stadio A poi stadio B su ogni sopravvissuto; stampa un verdetto per ciascuno."""
    sopravvissuti = Ricerca(k, soglia).esegui()
    for moduli in sopravvissuti:
        t0 = time.time()
        esito, testimone, nodi = cerca_residui(moduli, limite_nodi)
        if testimone is not None:
            assert verifica_diretta(testimone), "testimone non valido"
        print(f"   {esito} moduli={moduli} nodi_B={nodi} tempo_B={time.time()-t0:.2f}s "
              f"testimone={testimone}", flush=True)


if __name__ == "__main__":
    modo = sys.argv[1]
    limite = int(sys.argv[2])
    for k in map(int, sys.argv[3:]):
        decidi_tutti(k, k - 1 if modo == "ricerca" else k, limite)
