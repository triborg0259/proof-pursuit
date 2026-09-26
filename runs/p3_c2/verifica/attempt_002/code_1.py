"""Controllo esaustivo (aritmetica intera esatta) dei lemmi sulla successione
c_i = numero di parti di B^{i-1}(lambda), nella forma in cui li enunciamo noi.

Copre tutte le partizioni di n per n <= N_MAX (lemmi generali) e n = T_k (Lemma 3.3).
Serve a scovare errori di trascrizione: NON e' una prova.
"""
import sys
from calcola_DB_triangolari import shift, partizioni

LUNGHEZZA = 400  # termini della successione calcolati (molto oltre ogni preperiodo per n<=30)


def successione_parti(lam):
    """c_1, ..., c_LUNGHEZZA della partizione lam."""
    c = []
    cur = lam
    for _ in range(LUNGHEZZA):
        c.append(len(cur))
        cur = shift(cur)
    return c


def trova_pattern(c, p, q):
    """Restituisce x se (c_p,...,c_q) (1-based) = (x-1, x,...,x, x+1), q>=p+2; altrimenti None."""
    if q < p + 2:
        return None
    x = c[p]  # c_{p+1}
    if c[p - 1] != x - 1 or c[q - 1] != x + 1:
        return None
    if any(c[j - 1] != x for j in range(p + 1, q)):
        return None
    return x


def controlla_lemmi_generali(n):
    """Lemma 8 (=3.6), Lemma 9 (=3.5 versione nostra), Lemma 7 (=3.4), Lemma 10 e c_{i+1}<=c_i+1."""
    for lam in partizioni(n):
        c = successione_parti(lam)
        assert all(c[i + 1] <= c[i] + 1 for i in range(len(c) - 1)), ("3.2(1)", lam)
        for p in range(1, 60):
            for q in range(p + 2, p + 40):
                x = trova_pattern(c, p, q)
                if x is None:
                    continue
                if q == p + 2:
                    assert p <= x, ("3.6", lam, p, q, x)
                else:
                    if p > x:
                        # deve esistere pattern (x',p',q') con x'<=x, p'>=p-x, 2<=q'-p'<=q-p-1
                        ok = any(
                            (xp := trova_pattern(c, pp, qq)) is not None and xp <= x
                            for pp in range(max(1, p - x), p + 1)
                            for qq in range(pp + 2, pp + q - p))
                        assert ok, ("3.5", lam, p, q, x)
                # conseguenza: p <= x(q-p-1)
                assert p <= x * (q - p - 1), ("catena", lam, p, q, x)
                # Lemma 3.4: pattern (k-2, (k-1)^(k-1), k) di lunghezza k+1 => p+k <= n+1
                k = x + 1
                if q - p == k:
                    assert p + k <= n + 1, ("3.4", lam, p, q, x)


def controlla_lemma_33(k):
    """Lemma 6 per n = T_k: c_t = k-1, c_{t+1..} = k, e (i) oppure (ii) se t >= k+1; e t <= k^2-k."""
    n = k * (k + 1) // 2
    delta = tuple(range(k, 0, -1))
    for lam in partizioni(n):
        c = successione_parti(lam)
        cur, t = lam, 0
        while cur != delta:
            cur = shift(cur); t += 1
        assert all(c[i - 1] == k for i in range(t + 1, LUNGHEZZA + 1)), ("3.3(1)a", lam)
        if t >= 1:
            assert c[t - 1] == k - 1, ("3.3(1)b", lam)
        if t >= k + 1:
            i_ok = any(trova_pattern(c, p, q) == k for p in range(t - k, t) for q in range(p + 2, t))
            ii_ok = any(trova_pattern(c, p, q) == k - 1 for p in range(t - k + 1, t + 1) for q in range(p + 2, t + 2))
            assert i_ok or ii_ok, ("3.3(2)", lam, t)
            assert t <= k * k - k, ("teorema", lam, t)


if __name__ == "__main__":
    import time
    t0 = time.time()
    N_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    for n in range(1, N_MAX + 1):
        controlla_lemmi_generali(n)
    print(f"lemmi generali ok per tutte le partizioni di n <= {N_MAX}")
    for k in range(3, 8):
        controlla_lemma_33(k)
    print("Lemma 3.3 e teorema ok per k = 3..7")
    print(f"tempo {time.time() - t0:.1f} s")
