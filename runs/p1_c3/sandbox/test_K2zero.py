"""Esplorazione FLOAT (non una prova). Unico passo non dimostrato (K2_0):
arcsin(tan a tan b) <= ab/(D-a) + ab/(D-b),  D = pi/2, a,b >= 0, a+b <= D.
Griglia fine + condizione al bordo tan b <= b/(D-b) + b/D (derivata in a = 0)."""
import numpy as np
D = np.pi / 2
n = 2000
a = np.linspace(0, D, n + 1)[1:-1]
A, B = np.meshgrid(a, a)
maschera = A + B < D
lhs = np.arcsin(np.minimum(np.tan(A) * np.tan(B), 1.0))
rhs = A * B / (D - A) + A * B / (D - B)
print("(K2_0) min(RHS-LHS) sulla griglia:", (rhs - lhs)[maschera].min())
print("(K2_0) min rapporto LHS/RHS:", (lhs / rhs)[maschera].min(), " max:", (lhs / rhs)[maschera].max())
b = np.linspace(1e-4, D - 1e-4, 100000)
print("bordo: min di b/(D-b)+b/D - tan b:", (b / (D - b) + b / D - np.tan(b)).min())
