"""Esplorazione FLOAT (non una prova). Lemma di contrazione candidato:
se t_ij = sin(phi_ij), phi_ij >= 0, sum phi_ij < pi/2, e si elimina il vertice m
(complemento di Schur di I - T normalizzato), i nuovi valori
s_ij = (sin phi_ij + sin phi_im sin phi_jm) / (cos phi_im cos phi_jm)
soddisfano s_ij < 1 e sum arcsin(s_ij) <= sum phi_ij ?  Testato per OGNI scelta del vertice."""
import numpy as np
rng = np.random.default_rng(1)

def elimina(phi, m, k):
    """Restituisce (max s_ij, somma arcsin s_ij) dopo aver eliminato il vertice k."""
    idx = [i for i in range(m) if i != k]
    peggior_s, somma = 0.0, 0.0
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            i, j = idx[a], idx[b]
            s = (np.sin(phi[i, j]) + np.sin(phi[i, k]) * np.sin(phi[j, k])) / (np.cos(phi[i, k]) * np.cos(phi[j, k]))
            peggior_s = max(peggior_s, s)
            somma += np.arcsin(min(s, 1.0))
    return peggior_s, somma

peggior_rapporto = {m: 0.0 for m in range(3, 8)}
peggior_s_glob = 0.0
for _ in range(60000):
    m = rng.integers(3, 8)
    phi = rng.random((m, m)) ** rng.choice([1, 4, 10])
    phi = np.triu(phi, 1); phi = phi + phi.T
    totale = np.triu(phi, 1).sum()
    phi *= (np.pi / 2) * rng.uniform(0.5, 1.0) / totale   # sum phi < pi/2
    totale = np.triu(phi, 1).sum()
    for k in range(m):
        s_max, somma = elimina(phi, m, k)
        peggior_s_glob = max(peggior_s_glob, s_max)
        peggior_rapporto[m] = max(peggior_rapporto[m], somma / totale)
print("max s_ij osservato (deve essere < 1):", peggior_s_glob)
print("max (sum arcsin s) / (sum phi) per m (deve essere <= 1):", peggior_rapporto)
