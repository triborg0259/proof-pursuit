"""Utilita' esatte (interi/bitmask) per Q_6: classi di parita', vicini, foreste."""
D = 6
N = 1 << D
PARI = [v for v in range(N) if bin(v).count("1") % 2 == 0]
DISPARI = [v for v in range(N) if bin(v).count("1") % 2 == 1]

def vicini(v):
    return [v ^ (1 << i) for i in range(D)]

def maschera_vicini(v):
    m = 0
    for u in vicini(v):
        m |= 1 << u
    return m

MASCHERA_VICINI = [maschera_vicini(v) for v in range(N)]

def bit_a_lista(m):
    return [v for v in range(N) if (m >> v) & 1]

def e_foresta(maschera_vertici):
    """True se il sottografo indotto e' aciclico (union-find esatto)."""
    genitore = {}
    def trova(x):
        while genitore[x] != x:
            genitore[x] = genitore[genitore[x]]
            x = genitore[x]
        return x
    vertici = bit_a_lista(maschera_vertici)
    for v in vertici:
        genitore[v] = v
    for v in vertici:
        for u in vicini(v):
            if u > v and (maschera_vertici >> u) & 1:
                ru, rv = trova(u), trova(v)
                if ru == rv:
                    return False
                genitore[ru] = rv
    return True

def stringa(v):
    return "".join(str((v >> i) & 1) for i in range(D))
