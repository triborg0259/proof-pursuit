import sys

def vicini_stringa(s):
    return [s[:i] + ("1" if s[i] == "0" else "0") + s[i + 1:] for i in range(len(s))]

def conta(ordine):
    etichetta = {s: i + 1 for i, s in enumerate(ordine)}
    assert len(etichetta) == 64 and all(len(s) == 6 for s in ordine)
    valli = [s for s in ordine if all(etichetta[t] > etichetta[s] for t in vicini_stringa(s))]
    def cammini_da(s):
        return 1 + sum(cammini_da(t) for t in vicini_stringa(s) if etichetta[t] > etichetta[s])
    return sum(cammini_da(v) for v in valli), len(valli)

if __name__ == "__main__":
    ordine = sys.stdin.read().replace("\n", "").replace(" ", "").split(",")
    totale, n_valli = conta(ordine)
    print("cammini in salita (DFS):", totale, "valli:", n_valli)
