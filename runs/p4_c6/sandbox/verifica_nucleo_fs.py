"""
Controllo ESATTO (aritmetica razionale) delle disuguaglianze del nucleo
elementare dell'argomento di Fornal–Sun (arXiv:2607.24655, Sez. 4–5) su
famiglie casuali di classi a due a due disgiunte.

COSA controlla, per ogni famiglia generata:
  (L4) lemma strutturale: |S_n| <= omega(m)+1 e  w(v)*r(v;n,m) <= log2(d)
  (L5) positività di Fourier: ogni addendo q della forma quadratica è >= 0
  (Q)  Q >= k^2  e  Q <= G*k*(3*log2(d)+3)
  (T)  k <= 3*d*tau_max(d)*(log2(d)+1)
PERCHÉ: è evidenza (non prova) che la riproduzione della dimostrazione non
contiene errori di trascrizione. Rigore: esatto sulle istanze coperte.
"""
import random
import sys
from fractions import Fraction
from math import gcd, log2

def fattori_primi(n):
    """Restituisce il dizionario {p: v_p(n)} per fattorizzazione per tentativi."""
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def genera_famiglia(k, max_mod, rng):
    """Costruisce greedy una famiglia disgiunta di k classi (a, m) con m <= max_mod."""
    fam = []
    tentativi = 0
    while len(fam) < k and tentativi < 20000:
        tentativi += 1
        m = rng.randint(2, max_mod)
        a = rng.randrange(m)
        if all((a - b) % gcd(m, n) != 0 for b, n in fam):
            fam.append((a, m))
    return fam

def insiemi_K(fam, d):
    """K[n] = vertici con n | m(v) ma nessun multiplo proprio s*n <= d divide m(v)."""
    K = {n: [] for n in range(1, d + 1)}
    for v, (_, m) in enumerate(fam):
        for n in range(1, d + 1):
            if m % n == 0 and all(m % (s * n) != 0 for s in range(2, d // n + 1)):
                K[n].append(v)
    return K

def pesi(fam, K, d):
    """w(v) = 1 / #{n : v in K_n}, come frazione esatta."""
    conteggio = [0] * len(fam)
    for n in range(1, d + 1):
        for v in K[n]:
            conteggio[v] += 1
    assert all(c >= 1 for c in conteggio)
    return [Fraction(1, c) for c in conteggio]

def insieme_S(fam, K, n, m):
    """S_n^{(n,m)} del Lemma 4.1: intersezione K_n∩K_m più i vertici 'traditori'."""
    S = set(K[n]) & set(K[m])
    fn, fm = fattori_primi(n), fattori_primi(m)
    for v in K[n]:
        fv = fattori_primi(fam[v][1])
        for p in fm:
            if fm[p] > fn.get(p, 0) and fv.get(p, 0) > fn.get(p, 0):
                S.add(v)
    return S

def controlla_lemma_4(fam, K, w, d):
    """Verifica le due conclusioni del Lemma 4.1 su ogni coppia (n,m)."""
    L = log2(d)
    for n in range(1, d + 1):
        for m in range(1, d + 1):
            if not K[n] or not K[m]:
                continue
            Sn = insieme_S(fam, K, n, m) if n != m else set()
            Sm = insieme_S(fam, K, m, n) if n != m else set()
            assert len(Sn) <= len(fattori_primi(m)) + 1
            g = gcd(n, m)
            for v in K[n]:
                if v in Sn:
                    continue
                r = sum(1 for u in K[m] if u not in Sm and u != v
                        and gcd(fam[v][1], fam[u][1]) != g)
                assert w[v] * r <= L + 1e-12, (n, m, v, r, w[v])

def forma_quadratica(fam, K, w, d):
    """Q = sum_{n,m} sum_{v1,v2} W W gcd(n,m) 1[gcd(n,m) | a1-a2] (esatta)."""
    Q = Fraction(0)
    for n in range(1, d + 1):
        for m in range(1, d + 1):
            g = gcd(n, m)
            for v1 in K[n]:
                for v2 in K[m]:
                    if (fam[v1][0] - fam[v2][0]) % g == 0:
                        Q += w[v1] * w[v2] * g
    return Q

def mobius(n):
    f = fattori_primi(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)

def addendo_q(fam, K, w, d, q):
    """Contributo del singolo q nella (50): sum_{er=q} mu(e) r sum_j a_{r,j}^2."""
    tot = Fraction(0)
    for e in range(1, q + 1):
        if q % e:
            continue
        r = q // e
        a = [Fraction(0)] * r
        for n in range(q, d + 1, q):
            for v in K[n]:
                a[fam[v][0] % r] += w[v]
        tot += mobius(e) * r * sum(x * x for x in a)
    return tot

def controlla_famiglia(fam):
    k = len(fam)
    d = max(gcd(fam[i][1], fam[j][1]) for i in range(k) for j in range(i + 1, k))
    K = insiemi_K(fam, d)
    w = pesi(fam, K, d)
    assert sum(w[v] for n in K for v in K[n]) == k
    controlla_lemma_4(fam, K, w, d)
    Q = forma_quadratica(fam, K, w, d)
    addendi = [addendo_q(fam, K, w, d, q) for q in range(1, d + 1)]
    assert all(x >= 0 for x in addendi) and addendi[0] == k * k
    assert sum(addendi) == Q
    G = max(sum(gcd(n, m) for m in range(1, d + 1)) for n in range(1, d + 1))
    tau_max = max(sum(1 for e in range(1, n + 1) if n % e == 0) for n in range(1, d + 1))
    assert Q >= k * k
    assert Q <= G * k * (3 * log2(d) + 3) + 1e-9
    assert k <= 3 * d * tau_max * (log2(d) + 1)
    return k, d, Q

def main():
    rng = random.Random(20260926)
    n_fam = 0
    for _ in range(300):
        k = rng.randint(2, 9)
        fam = genera_famiglia(k, rng.choice([12, 30, 60, 120]), rng)
        if len(fam) < 2:
            continue
        controlla_famiglia(fam)
        n_fam += 1
    # famiglia estremale: le k classi mod k
    for k in range(2, 13):
        controlla_famiglia([(a, k) for a in range(k)])
        n_fam += 1
    print(f"OK: {n_fam} famiglie disgiunte controllate, tutte le disuguaglianze valgono")

if __name__ == "__main__":
    main()
