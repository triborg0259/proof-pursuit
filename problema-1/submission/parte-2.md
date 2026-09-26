# Problema 1 — Parte 2 — bozza di consegna

**Stato dichiarato: RISOLTA (approvata).** Prova completa scritta dal team; Referee automatico READY_FOR_HUMAN
(giudice A matematica PASS, giudice B evidenze PASS); approvazione umana registrata in `runs/p1_c2/approval.json`.

## 1. Risultato e ambito
Lemma di ortogonalità per una catena di versori: l'enunciato della parte è dimostrato integralmente, nella generalità richiesta (vedi la prova per le
ipotesi esatte). Nessun calcolo al computer è necessario.

## 2. Dimostrazione
# Cell 2: the orthogonality lemma for a chain of unit vectors

**Target.** Let $m\ge2$ and let $x_1,\dots,x_m$ be unit vectors in $\mathbb R^{m-1}$ with $\langle x_i,x_j\rangle=0$ whenever $|i-j|\ge2$. Then $\sum_{i=1}^{m-1}\theta(x_i,x_{i+1})\le(m-2)\frac{\pi}{2}$, where $\theta(x,y)=\arccos|\langle x,y\rangle|\in[0,\pi/2]$.

Write $\theta_i=\theta(x_i,x_{i+1})$ for $1\le i\le m-1$. We say that a list of unit vectors $y_1,\dots,y_r$ in a Euclidean space $V$ is a *chain* if $\langle y_i,y_j\rangle=0$ whenever $|i-j|\ge2$. The statement to prove is: (P$_m$) every chain of $m$ unit vectors in a Euclidean space of dimension $m-1$ satisfies $\sum_{i=1}^{m-1}\theta(y_i,y_{i+1})\le(m-2)\pi/2$. (Stating it for an arbitrary Euclidean space of dimension $m-1$ instead of $\mathbb R^{m-1}$ is harmless: choosing an orthonormal basis gives a linear isometry onto $\mathbb R^{m-1}$, which preserves inner products, hence the chain condition and all the angles.)

## Two elementary facts
**Fact A.** For $\beta,\psi\in[0,\pi/2]$: $\arccos(\cos\beta\cos\psi)\le\beta+\psi$.
*Proof.* $\cos(\beta+\psi)=\cos\beta\cos\psi-\sin\beta\sin\psi\le\cos\beta\cos\psi$ because $\sin\beta,\sin\psi\ge0$. Both $\cos(\beta+\psi)$ and $\cos\beta\cos\psi$ lie in $[-1,1]$ and $\arccos$ is decreasing on $[-1,1]$, so $\arccos(\cos\beta\cos\psi)\le\arccos(\cos(\beta+\psi))=\beta+\psi$, the last equality because $\beta+\psi\in[0,\pi]$. $\square$

**Fact B.** If $V$ is a Euclidean space of dimension $n\ge1$ and $v_1,\dots,v_{n-1}\in V$ (possibly fewer vectors, possibly none), there is a unit vector $y\in V$ orthogonal to all of them.
*Proof.* The orthogonal complement of $\mathrm{span}(v_1,\dots,v_{n-1})$ in $V$ has dimension $\ge n-(n-1)=1$, so it contains a nonzero vector; normalise it. $\square$

## Induction on $m$
**Base $m=2$.** $x_1,x_2$ are unit vectors in a $1$-dimensional space, so $x_2=\pm x_1$, $|\langle x_1,x_2\rangle|=1$ and $\theta_1=\arccos 1=0\le0=(m-2)\pi/2$.

**Step.** Let $m\ge3$ and assume (P$_{m-1}$). Let $x_1,\dots,x_m$ be a chain of unit vectors in a Euclidean space $W$ of dimension $m-1$. Put $U=x_m^{\perp}=\{v\in W:\langle v,x_m\rangle=0\}$, a subspace of dimension $m-2$. For $j\le m-2$ we have $|j-m|\ge2$, hence $\langle x_j,x_m\rangle=0$: so $x_1,\dots,x_{m-2}\in U$. Let $c=\langle x_{m-1},x_m\rangle\in[-1,1]$ and $w=x_{m-1}-c\,x_m$. Then $\langle w,x_m\rangle=c-c=0$, so $w\in U$, and $\|w\|^2=1-2c^2+c^2=1-c^2$.

*Case 1: $|c|<1$.* Then $w\neq0$; let $y=w/\|w\|$, a unit vector of $U$. For $j\le m-3$ we have $|j-(m-1)|\ge2$ and $|j-m|\ge2$, so $\langle y,x_j\rangle=(\langle x_{m-1},x_j\rangle-c\langle x_m,x_j\rangle)/\|w\|=0$. Consequently $x_1,\dots,x_{m-2},y$ is a chain of $m-1$ unit vectors in $U$ (pairs among $x_1,\dots,x_{m-2}$ inherit the chain condition from the original chain; the pairs $(x_j,y)$ with $j\le m-3$, i.e. $|j-(m-1)|\ge2$ in the new indexing, were just checked). Since $\dim U=m-2$, (P$_{m-1}$) gives
$$\sum_{i=1}^{m-3}\theta_i+\psi\le(m-3)\frac{\pi}{2},\qquad\text{where }\psi=\theta(x_{m-2},y)\in[0,\pi/2].\tag{3}$$
(For $m=3$ the sum is empty and (3) says $\psi\le0$, i.e. $\psi=0$, which is indeed what (P$_2$) gives for the chain $x_1,y$ in the $1$-dimensional space $U$.)
Now $x_{m-1}=w+c\,x_m=\|w\|\,y+c\,x_m$. Let $\varphi=\theta_{m-1}=\theta(x_{m-1},x_m)=\arccos|c|$, so $|c|=\cos\varphi$, $\|w\|=\sqrt{1-c^2}=\sin\varphi$ and $\varphi\in(0,\pi/2]$. Using $\langle x_{m-2},x_m\rangle=0$,
$$\langle x_{m-2},x_{m-1}\rangle=\|w\|\langle x_{m-2},y\rangle+c\langle x_{m-2},x_m\rangle=\sin\varphi\,\langle x_{m-2},y\rangle,$$
so $|\langle x_{m-2},x_{m-1}\rangle|=\sin\varphi\cos\psi=\cos\beta\cos\psi$ with $\beta=\pi/2-\varphi\in[0,\pi/2)$. By Fact A,
$$\theta_{m-2}=\arccos(\cos\beta\cos\psi)\le\beta+\psi=\frac{\pi}{2}-\varphi+\psi,\qquad\text{i.e.}\qquad \theta_{m-2}+\theta_{m-1}\le\frac{\pi}{2}+\psi.$$
Adding this to (3): $\sum_{i=1}^{m-1}\theta_i\le(m-3)\frac{\pi}{2}-\psi+\frac{\pi}{2}+\psi=(m-2)\frac{\pi}{2}$.

*Case 2: $|c|=1$, i.e. $x_{m-1}=\pm x_m$.* Then $\theta_{m-1}=\arccos1=0$, and $\langle x_{m-2},x_{m-1}\rangle=\pm\langle x_{m-2},x_m\rangle=0$, so $\theta_{m-2}=\arccos0=\pi/2$. By Fact B applied to $V=U$ (dimension $m-2\ge1$) and the $m-3$ vectors $x_1,\dots,x_{m-3}$, there is a unit vector $y\in U$ with $\langle y,x_j\rangle=0$ for all $j\le m-3$. Then $x_1,\dots,x_{m-2},y$ is a chain of $m-1$ unit vectors in $U$ (same verification as in Case 1), and (P$_{m-1}$) gives $\sum_{i=1}^{m-3}\theta_i+\theta(x_{m-2},y)\le(m-3)\frac{\pi}{2}$, hence $\sum_{i=1}^{m-3}\theta_i\le(m-3)\frac{\pi}{2}$ because $\theta(x_{m-2},y)\ge0$. Therefore
$$\sum_{i=1}^{m-1}\theta_i=\sum_{i=1}^{m-3}\theta_i+\frac{\pi}{2}+0\le(m-2)\frac{\pi}{2}.$$

In both cases (P$_m$) holds, which completes the induction. $\blacksquare$

*Remark (not needed).* For $m=3$ the argument shows $\theta_1+\theta_2=\pi/2$ always; for general $m$ equality is attained e.g. by $x_i=e_i$ ($i\le m-1$), $x_m=e_{m-1}$, where all consecutive angles are $\pi/2$ except the last, which is $0$.


## 3. Verifica: istruzioni, dipendenze, tempi
Prova a mano, nessuna dipendenza. Verifica meccanica non necessaria; il Referee automatico (due giudici indipendenti,
`runs/p1_c2/attempts/packet_001.json`) non ha trovato passaggi non giustificati.

## 4. Fonti e contributo
- Nessuna fonte usata: prova autocontenuta.
- Posizione rispetto allo stato dell'arte: No literature found for this lemma specifically (arXiv search: angles between lines / Fejes Toth); it is an elementary statement and is proved here from scratch.
- Contributo: la prova qui scritta è del team, per esteso.

## 5. Limiti e parti irrisolte
Nessuna: la parte è dimostrata. Gap dichiarati: nessuno.
