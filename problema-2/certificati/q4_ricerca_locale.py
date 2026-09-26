"""Ricerca locale (simulated annealing) di etichettature di Q_4 con pochi cammini in salita.
Serve solo a trovare un buon candidato (upper bound): NON dimostra nulla.
Aritmetica: interi esatti (il conteggio), float solo nella regola di accettazione di SA."""
import random, sys, math

D = 4
N = 1 << D
VICINI = [[v ^ (1 << i) for i in range(D)] for v in range(N)]


def conta_cammini(ordine):
    """Numero di cammini in salita dell'etichettatura data come lista di vertici
    in ordine crescente di etichetta (Lemma 1: p(v) = [valle] + somma p(u) sui vicini minori)."""
    etichetta = [0] * N
    for pos, v in enumerate(ordine):
        etichetta[v] = pos
    p = [0] * N
    totale = 0
    for v in ordine:
        minori = [u for u in VICINI[v] if etichetta[u] < etichetta[v]]
        p[v] = 1 if not minori else sum(p[u] for u in minori)
        totale += p[v]
    return totale


def ricottura(seme, passi=200000):
    """Una corsa di simulated annealing con mosse di scambio e di spostamento."""
    rng = random.Random(seme)
    ordine = list(range(N))
    rng.shuffle(ordine)
    valore = conta_cammini(ordine)
    migliore, migliore_ordine = valore, ordine[:]
    for passo in range(passi):
        temperatura = 2.0 * (1 - passo / passi) + 0.05
        nuovo = ordine[:]
        i, j = rng.randrange(N), rng.randrange(N)
        if rng.random() < 0.5:
            nuovo[i], nuovo[j] = nuovo[j], nuovo[i]
        else:
            nuovo.insert(j, nuovo.pop(i))
        nuovo_valore = conta_cammini(nuovo)
        if nuovo_valore <= valore or rng.random() < math.exp((valore - nuovo_valore) / temperatura):
            ordine, valore = nuovo, nuovo_valore
            if valore < migliore:
                migliore, migliore_ordine = valore, ordine[:]
    return migliore, migliore_ordine


def main():
    corse = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    globale, globale_ordine = None, None
    for seme in range(corse):
        valore, ordine = ricottura(seme)
        if globale is None or valore < globale:
            globale, globale_ordine = valore, ordine
        print(f"seme {seme}: {valore} (migliore finora {globale})", flush=True)
    stringhe = [format(v, f"0{D}b") for v in globale_ordine]
    print("MIGLIORE:", globale, stringhe)


if __name__ == "__main__":
    main()
