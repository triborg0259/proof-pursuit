"""Esplorazione FLOAT (non una prova). Disuguaglianza per coppia (K2):
arcsin((sin c + sin a sin b)/(cos a cos b)) <= c + a(b+c)/(D-a) + b(a+c)/(D-b),  D = pi/2,
per a,b,c >= 0, a+b+c <= D.  Poi il caso c = 0 (K2_0) e la concavita' in P = ab (u fisso)."""
import numpy as np
D = np.pi / 2

def lhs(a, b, c):
    s = (np.sin(c) + np.sin(a) * np.sin(b)) / (np.cos(a) * np.cos(b))
    return np.arcsin(np.minimum(s, 1.0))

def rhs(a, b, c):
    return c + a * (b + c) / (D - a) + b * (a + c) / (D - b)

# (K2) su griglia + casuale
n = 200
g = np.linspace(0, D, n + 1)[1:-1]
peggio = 1.0
for a in g:
    for b in g:
        if a + b >= D: continue
        c = np.linspace(0, D - a - b, 60)
        peggio = min(peggio, (rhs(a, b, c) - lhs(a, b, c)).min())
print("(K2) min(RHS-LHS) su griglia:", peggio)
rng = np.random.default_rng(3)
x = rng.dirichlet([1, 1, 1, 1], 400000) * D   # (a,b,c,slack)
a, b, c = x[:, 0], x[:, 1], x[:, 2]
print("(K2) min(RHS-LHS) casuale:", (rhs(a, b, c) - lhs(a, b, c)).min())

# (K2_0) forma equivalente:  L(P) = 2 arctan sqrt(sin u / cos delta) >= R(P) = u (D^2 - P)/(P + u D)
# con P = ab, delta = a-b, a+b = D-u.  Controllo concavita' di L in P e di F = L - R.
def L_di_P(u, P):
    delta = np.sqrt(np.maximum((D - u) ** 2 - 4 * P, 0))
    return 2 * np.arctan(np.sqrt(np.sin(u) / np.cos(delta)))

def R_di_P(u, P):
    return u * (D ** 2 - P) / (P + u * D)

min_secdiff_L, min_secdiff_F = 1e9, 1e9
for u in np.linspace(0.01, D - 0.01, 300):
    Pmax = (D - u) ** 2 / 4
    P = np.linspace(0, Pmax, 400)
    L = L_di_P(u, P); R = R_di_P(u, P); F = L - R
    dL = np.diff(L, 2); dF = np.diff(F, 2)
    min_secdiff_L = min(min_secdiff_L, dL.min()); min_secdiff_F = min(min_secdiff_F, dF.min())
print("L concava in P?  max seconda differenza L:", -min_secdiff_L if False else None, " min seconda diff L (deve essere <=0 per concavita'... segno):", )
# stampo i massimi (concavita' <=> seconde differenze <= 0)
max_sd_L = max_sd_F = -1e9
for u in np.linspace(0.01, D - 0.01, 300):
    Pmax = (D - u) ** 2 / 4
    P = np.linspace(0, Pmax, 400)
    L = L_di_P(u, P); F = L - R_di_P(u, P)
    max_sd_L = max(max_sd_L, np.diff(L, 2).max()); max_sd_F = max(max_sd_F, np.diff(F, 2).max())
print("max seconda differenza di L in P (<=0 se concava):", max_sd_L)
print("max seconda differenza di F in P (<=0 se concava):", max_sd_F)
