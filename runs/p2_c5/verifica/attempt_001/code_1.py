"""Verifica esaustiva (esatta) del Lemma B su Q_4 e Q_5: ogni insieme indipendente H tale che Q_d - H e' una foresta
sta in una sola classe di parita' e ha taglia >= 2^{d-1} - A(d,4) (A(4,4)=2, A(5,4)=2).
Enumera tutti gli insiemi indipendenti per ricorsione; controlla l'aciclicita' del complemento con union-find."""
import sys, time
peso = lambda v: bin(v).count("1")

def foresta(d, H):
    """True se il sottografo indotto da V \\ H e' aciclico (union-find sugli spigoli interni)."""
    parent = list(range(1 << d))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for v in range(1 << d):
        if v in H: continue
        for i in range(d):
            u = v ^ (1 << i)
            if u > v and u not in H:
                a, b = find(u), find(v)
                if a == b: return False
                parent[a] = b
    return True

def indipendenti(d):
    """Genera tutti gli insiemi indipendenti di Q_d (ricorsione sul vertice da includere o no)."""
    n = 1 << d
    def ric(v, H, vietati):
        if v == n:
            yield H; return
        yield from ric(v + 1, H, vietati)
        if v not in vietati:
            yield from ric(v + 1, H | {v}, vietati | {v ^ (1 << i) for i in range(d)})
    yield from ric(0, frozenset(), frozenset())

for d, A4 in [(4, 2), (5, 2)]:
    inizio = time.time(); tot = decyc = 0; misti = 0; minimo = 1 << d
    for H in indipendenti(d):
        tot += 1
        if not H or not foresta(d, H): continue
        decyc += 1
        parita = {peso(v) % 2 for v in H}
        misti += len(parita) == 2
        minimo = min(minimo, len(H))
    print(f"d={d}: indipendenti={tot} decycling indipendenti={decyc} con parita' mista={misti} "
          f"taglia minima={minimo} (lemma: >= {(1 << (d-1)) - A4})  tempo {time.time()-inizio:.1f}s")
