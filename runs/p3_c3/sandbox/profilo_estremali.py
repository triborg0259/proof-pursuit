"""Profilo di fusione delle partizioni estremali di n = T_k - 1.

Cosa fa: per ogni k calcola l'insieme S_j = {B^j(lam) : lam estremale} e stampa |S_j|;
trova il primo j con |S_j| = 1 (la partizione "collo di bottiglia" mu_k) e verifica che
l'insieme estremale coincida con la preimmagine B^{-j}(mu_k). Stampa anche l'indice da cui
le successioni c_u (numero di parti) delle estremali coincidono.
Perche': la cella chiede QUALI partizioni raggiungono il massimo; una descrizione
"lam estremale <=> B^j(lam) = mu_k" sarebbe una caratterizzazione esplicita.
Aritmetica esatta.
"""
import sys
from db_table import distanze_dal_ciclo, shift


def profilo(k):
    n = k * (k + 1) // 2 - 1
    d = distanze_dal_ciclo(n)
    D = max(d.values())
    estr = {lam for lam, v in d.items() if v == D}
    immagini, j = set(estr), 0
    taglie = []
    while len(immagini) > 1:
        immagini = {shift(l) for l in immagini}
        j += 1
        taglie.append(len(immagini))
    mu = next(iter(immagini))
    preimg = {lam for lam, v in d.items() if v == D - j}
    print(f"k={k} n={n} D={D} #estr={len(estr)} |S_j|={taglie} j={j} mu={mu} d_B(mu)={d[mu]} "
          f"#{{d_B = D-j}}={len(preimg)} unico={preimg == {mu}}")
    # successioni c_u: indice da cui coincidono
    seqs = []
    for lam in estr:
        s, cur = [], lam
        for _ in range(D + 2 * k):
            s.append(len(cur)); cur = shift(cur)
        seqs.append(s)
    primo = next(i for i in range(D + 2 * k) if len({tuple(s[i:]) for s in seqs}) == 1)
    print(f"   c_u coincidono da u={primo+1}: {seqs[0][primo:primo+ 3*k]}")
    return mu, j


if __name__ == "__main__":
    for k in range(4, int(sys.argv[1]) + 1):
        profilo(k)
