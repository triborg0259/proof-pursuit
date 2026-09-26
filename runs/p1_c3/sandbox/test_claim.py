"""Esplorazione FLOAT (non una prova): verifica numerica della riformulazione
'T simmetrica >= 0 con diagonale nulla, lambda_max(T) >= 1  =>  sum arcsin(t_ij) >= pi/2'
e della disuguaglianza sferica  'perimetro <= pi + gamma' per triangoli con lati <= pi/2."""
import numpy as np
rng = np.random.default_rng(0)

def minimo_somma_arcsin(m, prove):
    """Cerca il minimo di sum arcsin(t_ij) su matrici casuali riscalate a lambda_max = 1."""
    migliore = 10.0
    for _ in range(prove):
        T = rng.random((m, m)) ** rng.choice([1, 3, 8])
        T = np.triu(T, 1); T = T + T.T
        maschera = rng.random((m, m)) < rng.random()
        T = T * np.triu(maschera, 1); T = T + T.T
        lam = np.linalg.eigvalsh(T)[-1]
        if lam <= 0 or T.max() / lam > 1:
            continue
        T = T / lam
        somma = np.arcsin(np.triu(T, 1)).sum()
        migliore = min(migliore, somma)
    return migliore

for m in range(2, 8):
    print("m =", m, " min sum arcsin ~", minimo_somma_arcsin(m, 20000), " pi/2 =", np.pi / 2)

def test_perimetro(prove):
    """Triangoli sferici casuali con lati <= pi/2: controlla a+b+c <= pi + gamma (gamma opposto a c)."""
    peggiore = -10.0
    for _ in range(prove):
        a, b = rng.random(2) * np.pi / 2
        gamma = rng.random() * np.pi
        cosc = np.cos(a) * np.cos(b) + np.sin(a) * np.sin(b) * np.cos(gamma)
        c = np.arccos(np.clip(cosc, -1, 1))
        if c > np.pi / 2:
            continue
        peggiore = max(peggiore, a + b + c - np.pi - gamma)
    return peggiore

print("max (perimetro - pi - gamma) ~", test_perimetro(200000))
