# Problema 1 — Parte 1 — bozza di consegna

**Stato dichiarato: RISOLTA (approvata).** Prova completa scritta dal team; Referee automatico READY_FOR_HUMAN
(giudice A matematica PASS, giudice B evidenze PASS); approvazione umana registrata in `runs/p1_c1/approval.json`.

## 1. Risultato e ambito
Somma degli angoli fra rette nel piano: l'enunciato della parte è dimostrato integralmente, nella generalità richiesta (vedi la prova per le
ipotesi esatte). Nessun calcolo al computer è necessario.

## 2. Dimostrazione
# Cell 1: the sum of the angles between $N$ lines in the plane

**Target.** For lines $\ell_1,\dots,\ell_N$ through the origin of $\mathbb R^2$ (repetitions allowed),
$S=\sum_{i<j}\theta(\ell_i,\ell_j)\le \frac{\pi}{2}\left\lfloor \frac{N^2}{4}\right\rfloor$, where $\theta(\ell,\ell')=\arccos|\langle x,x'\rangle|$ for unit vectors $x,x'$ spanning $\ell,\ell'$.

## 1. Directions and angles
Every line $\ell$ through the origin of $\mathbb R^2$ is spanned by exactly one unit vector of the form $(\cos t,\sin t)$ with $t\in[0,\pi)$ (the two unit vectors of $\ell$ are $\pm(\cos t,\sin t)$, and exactly one of the two angles $t,t+\pi$ lies in $[0,\pi)$). Call $t=\tau(\ell)$ the *direction* of $\ell$.
For two lines with directions $t,t'\in[0,\pi)$ we have $\langle(\cos t,\sin t),(\cos t',\sin t')\rangle=\cos(t-t')$, hence $\theta(\ell,\ell')=\arccos|\cos(t-t')|$.
Put $u=|t-t'|\in[0,\pi)$. If $u\le\pi/2$ then $\cos u\ge 0$, so $|\cos u|=\cos u$ and $\arccos(\cos u)=u$ because $u\in[0,\pi]$. If $u>\pi/2$ then $\cos u<0$, so $|\cos u|=-\cos u=\cos(\pi-u)$ with $\pi-u\in(0,\pi/2)$, and $\arccos(\cos(\pi-u))=\pi-u$. In both cases
$$\theta(\ell,\ell')=\min(u,\pi-u),\qquad u=|\tau(\ell)-\tau(\ell')|.\tag{1}$$
Coincident lines have $u=0$ and angle $0$, as they should. Note also that $\min(u,\pi-u)$ is unchanged if $u$ is replaced by $\pi-u$, so (1) also holds with $u=(\tau(\ell')-\tau(\ell))\bmod\pi$ (the representative in $[0,\pi)$): indeed this quantity equals $|t-t'|$ or $\pi-|t-t'|$.

## 2. A random half-turn of directions
For $x\in\mathbb R$ write $x\bmod\pi$ for the unique representative of $x+\pi\mathbb Z$ in $[0,\pi)$. For $\psi\in[0,\pi)$ define
$$A_\psi=\{t\in[0,\pi):\ (t-\psi)\bmod\pi\in[0,\pi/2)\}.$$
Let $\psi$ be a random variable with the uniform distribution on $[0,\pi)$, i.e. $\Pr[\psi\in B]=|B|/\pi$ for every Borel set $B\subseteq[0,\pi)$, where $|B|$ is Lebesgue measure.

**Lemma 1.** For fixed $t,t'\in[0,\pi)$ let $u=(t'-t)\bmod\pi$ and $\varphi=\min(u,\pi-u)$. Then
$$\Pr\big[\text{exactly one of } t,t' \text{ lies in } A_\psi\big]=\frac{2\varphi}{\pi}.$$

*Proof.* Step 1 (reduction to $t=0$). Put $\psi'=(\psi-t)\bmod\pi$. The map $x\mapsto(x-t)\bmod\pi$ is a bijection of $[0,\pi)$ onto itself which is a translation on each of the two pieces $[0,t)$ and $[t,\pi)$, hence it preserves Lebesgue measure; therefore $\psi'$ is again uniform on $[0,\pi)$. Moreover $(t-\psi)\bmod\pi=(-(\psi-t))\bmod\pi=(-\psi')\bmod\pi=(0-\psi')\bmod\pi$ and $(t'-\psi)\bmod\pi=((t'-t)-(\psi-t))\bmod\pi=(u-\psi')\bmod\pi$. Hence $t\in A_\psi\iff 0\in A_{\psi'}$ and $t'\in A_\psi\iff u\in A_{\psi'}$. So it suffices to prove the claim for the pair $(0,u)$ with $u\in[0,\pi)$ and a uniform $\psi$ (we rename $\psi'$ as $\psi$).

Step 2 (the two sets). For $s\in[0,\pi)$ let $J_s=\{\psi\in[0,\pi): s\in A_\psi\}=\{\psi: (s-\psi)\bmod\pi<\pi/2\}$. Since $s-\psi\in(-\pi,\pi)$: if $\psi\le s$ then $(s-\psi)\bmod\pi=s-\psi$ and the condition reads $\psi>s-\pi/2$; if $\psi>s$ then $(s-\psi)\bmod\pi=s-\psi+\pi$ and the condition reads $\psi>s+\pi/2$. Therefore
$$J_s=\big(\max(0,s-\tfrac{\pi}{2}),\,s\big]\ \cup\ \big(s+\tfrac{\pi}{2},\,\pi\big)\cap[0,\pi),$$
where the second interval is empty when $s+\pi/2\ge\pi$. In particular $|J_s|=\pi/2$ for every $s$: if $s<\pi/2$ the two pieces have lengths $s$ and $\pi/2-s$; if $s\ge\pi/2$ the first piece has length $\pi/2$ and the second is empty. For $s=0$ the first piece is $\{0\}$ (measure $0$) and $J_0=\{0\}\cup(\pi/2,\pi)$.

Step 3 (the symmetric difference). The event "exactly one of $0,u$ lies in $A_\psi$" is $\{\psi\in J_0\triangle J_u\}$, and $|J_0\triangle J_u|=|J_0|+|J_u|-2|J_0\cap J_u|=\pi-2|J_0\cap J_u|$.
*Case $u\le\pi/2$.* Then $J_u=(0,u]\cup(u+\pi/2,\pi)$ (the second piece is empty if $u=\pi/2$). Up to the null set $\{0\}$, $J_0=(\pi/2,\pi)$; since $u\le\pi/2$, $(0,u]\cap(\pi/2,\pi)=\emptyset$, so $J_0\cap J_u=(u+\pi/2,\pi)$ up to a null set, of measure $\pi/2-u$. Hence $|J_0\triangle J_u|=\pi-2(\pi/2-u)=2u=2\varphi$.
*Case $u>\pi/2$.* Then $u+\pi/2>\pi$, so $J_u=(u-\pi/2,u]$ with $0<u-\pi/2<\pi/2$. Thus $J_0\cap J_u=(\pi/2,\pi)\cap(u-\pi/2,u]=(\pi/2,u]$ up to a null set, of measure $u-\pi/2$. Hence $|J_0\triangle J_u|=\pi-2(u-\pi/2)=2(\pi-u)=2\varphi$.
In both cases the probability is $|J_0\triangle J_u|/\pi=2\varphi/\pi$. $\square$

## 3. Counting the pairs separated by $A_\psi$
Let $t_i=\tau(\ell_i)$ and, for $\psi\in[0,\pi)$, $k_\psi=\#\{i: t_i\in A_\psi\}\in\{0,1,\dots,N\}$. A pair $\{i,j\}$ has exactly one member with direction in $A_\psi$ if and only if one index is among the $k_\psi$ "inside" indices and the other among the $N-k_\psi$ "outside" indices; hence the number of such pairs is exactly $k_\psi(N-k_\psi)$. Writing $X_{ij}(\psi)$ for the indicator of the event of Lemma 1 for the pair $(t_i,t_j)$, we have $k_\psi(N-k_\psi)=\sum_{i<j}X_{ij}(\psi)$ for every $\psi$ (each $X_{ij}$ is the indicator of a finite union of intervals, so everything is measurable), and by linearity of expectation, Lemma 1 and (1),
$$\mathbb E\big[k_\psi(N-k_\psi)\big]=\sum_{i<j}\Pr[X_{ij}=1]=\sum_{i<j}\frac{2}{\pi}\theta(\ell_i,\ell_j)=\frac{2}{\pi}S.\tag{2}$$

## 4. Conclusion
For every integer $k$ we have $N^2-4k(N-k)=(N-2k)^2\ge0$, so $k(N-k)\le N^2/4$; as $k(N-k)$ is an integer, $k(N-k)\le\lfloor N^2/4\rfloor$. Applying this to $k=k_\psi$ for every $\psi$ and taking expectations, (2) gives
$$S=\frac{\pi}{2}\,\mathbb E\big[k_\psi(N-k_\psi)\big]\le\frac{\pi}{2}\left\lfloor\frac{N^2}{4}\right\rfloor.\qquad\blacksquare$$

*Remark (not needed for the cell).* The bound is attained: put $\lceil N/2\rceil$ lines along the $x$-axis and $\lfloor N/2\rfloor$ along the $y$-axis; the only nonzero angles are the $\lceil N/2\rceil\lfloor N/2\rfloor=\lfloor N^2/4\rfloor$ cross pairs, each equal to $\pi/2$.


## 3. Verifica: istruzioni, dipendenze, tempi
Prova a mano, nessuna dipendenza. Verifica meccanica non necessaria; il Referee automatico (due giudici indipendenti,
`runs/p1_c1/attempts/packet_001.json`) non ha trovato passaggi non giustificati.

## 4. Fonti e contributo
- arXiv:1801.07837 Bilyk, Matzke, On the Fejes Toth problem about the sum of angles between lines (context only: the planar case is the only settled case; the proof below is self-contained and does not use the paper)
- Posizione rispetto allo stato dell'arte: Bilyk-Matzke [1801.07837] state that d=1 (the plane) is the only settled case and give several proofs, one of which is a Stolarsky-type identity; our argument is of the same nature but written independently and in full, so nothing is cited as a black box. Lim-McCann [2007.08698] concern a one-parameter deformation and are not used.
- Contributo: la prova qui scritta è del team, per esteso.

## 5. Limiti e parti irrisolte
Nessuna: la parte è dimostrata. Gap dichiarati: nessuno.
