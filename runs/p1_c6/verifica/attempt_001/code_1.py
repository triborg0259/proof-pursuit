"""
Verifica ESATTA (interi Python) delle identita' aritmetiche usate nei lemmi di riduzione
per la congettura di Fejes Toth (problema 1, parte 6).
  M(N,d) = s*C(q+1,2) + (d-s)*C(q,2),  N = q*d + s, 0 <= s < d.
Cosa controlla e perche':
  (a) 2*M(N,d) = q*(N+s-d)                      -> usata nei lemmi 2 e 3
  (b) M(N+1,d) = M(N,d) + q                     -> usata nei lemmi 2 e 3
  (c) M(N+q',d) = M(N,d-1) + C(q',2), q'=N//(d-1) -> usata nel lemma 4
  (d) disuguaglianza del lemma 2 vale sse s = d-1 oppure q = 0 (N>=2)
  (e) disuguaglianza del lemma 3 vale sse s = 0    (N>=1)
Copertura: 1 <= d <= 40, 1 <= N <= 400. Aritmetica esatta: nessun float.
"""
from math import comb


def M(N, d):
    """Numero di coppie coincidenti nella configurazione equidistribuita."""
    q, s = divmod(N, d)
    return s * comb(q + 1, 2) + (d - s) * comb(q, 2)


def B2(N, d):
    """Bound congetturato in unita' di pi/2: C(N,2) - M(N,d)."""
    return comb(N, 2) - M(N, d)


def controlla(d_max=40, N_max=400):
    for d in range(1, d_max + 1):
        for N in range(1, N_max + 1):
            q, s = divmod(N, d)
            assert 2 * M(N, d) == q * (N + s - d), (N, d)
            assert M(N + 1, d) == M(N, d) + q, (N, d)
            if d >= 2:
                qq = N // (d - 1)
                assert M(N + qq, d) == M(N, d - 1) + comb(qq, 2), (N, d)
            if N >= 2:
                lemma2 = (N + 1) * B2(N, d) <= (N - 1) * B2(N + 1, d)
                assert lemma2 == (s == d - 1 or q == 0), (N, d)
            lemma3 = N * B2(N + 1, d) <= (N + 2) * B2(N, d)
            assert lemma3 == (s == 0), (N, d)
    print(f"OK: identita' (a)-(e) verificate per d<=%d, N<=%d" % (d_max, N_max))


if __name__ == "__main__":
    controlla()
