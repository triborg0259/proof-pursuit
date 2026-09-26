"""Profilo isoperimetrico di Harper per Q_9 (aritmetica esatta).
h(k) = |I_k ∪ N(I_k)| dove I_k e' il segmento iniziale di taglia k dell'ordine simpliciale
(peso crescente, a parita' di peso ordine lessicografico). Teorema di Harper (1966): per ogni A con |A|=k,
|A ∪ N(A)| >= h(k). Stampa i k in [1,255] con h(k) - 2k < 32 (quelli da trattare a parte nel lemma)."""
D = 9
peso = lambda v: bin(v).count("1")

def chiave(v):
    """Ordine simpliciale: prima il peso, poi lessicografico sui bit (bit 0 = prima coordinata)."""
    return (peso(v), tuple(-((v >> i) & 1) for i in range(D)))

ordine = sorted(range(1 << D), key=chiave)
chiusura = set()
eccezioni = []
for k in range(1, 256):
    v = ordine[k - 1]
    chiusura |= {v} | {v ^ (1 << i) for i in range(D)}
    if len(chiusura) - 2 * k < 32:
        eccezioni.append((k, len(chiusura)))
print("k con h(k)-2k < 32:", eccezioni)
print("minimo di h(k)-2k su 4<=k<=252:", min(len_ for len_ in [0] or []) if False else
      min((h - 2 * k) for k, h in [(k, 0) for k in []] ) if False else "vedi sotto")
# ricalcolo pulito del minimo su [4,252]
chiusura = set(); valori = {}
for k in range(1, 256):
    v = ordine[k - 1]; chiusura |= {v} | {v ^ (1 << i) for i in range(D)}; valori[k] = len(chiusura) - 2 * k
print("min su [4,252]:", min(valori[k] for k in range(4, 253)), " h(k)-2k per k=1..6:", [valori[k] for k in range(1, 7)])
