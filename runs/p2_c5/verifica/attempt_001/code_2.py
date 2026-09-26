import numpy as np
peso=lambda v: bin(v).count("1")
pari=[v for v in range(512) if peso(v)%2==0]; idx={v:i for i,v in enumerate(pari)}
M=np.zeros((256,256))
for v in pari:
    for u in pari:
        if peso(u^v)==2: M[idx[v],idx[u]]=1
ev=np.sort(np.linalg.eigvalsh(M))[::-1]
print("grado:",M.sum(1)[0]," autovalori distinti:",sorted(set(np.round(ev,6)),reverse=True))
