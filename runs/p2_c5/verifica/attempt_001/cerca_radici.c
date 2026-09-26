/* cerca_radici.c — ricottura (esplorazione, NON prova) sulla famiglia "radici pari / dispari rimossi" per Q_9.
   Stato: R sottoinsieme dei vertici pari (radici), B sottoinsieme dei dispari (rimossi da S).
   S = R + (dispari \ B) deve essere una foresta indotta; etichette: S in ordine di foresta, poi B, poi i pari non radici.
   Costo esatto dell'etichettatura (se S e' foresta): |S| + sum_b k_b + sum_e ( #dispari-S vicini + sum_{b vicino} k_b ),
   con k_b = numero di radici adiacenti a b. Penalita' lambda per ciclo residuo in S.
   Uso: ./cerca_radici seme passi t0 t1 [stato_iniziale.txt]  -> salva migliore_radici_<seme>.txt (512 righe: 0=S,1=B,2=R,3=pari non radice) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define D 9
#define N (1<<D)
static int tipo[N];   /* pari: 2=radice, 3=non radice; dispari: 0=in S, 1=in B */
static int parent[N];
static int find(int x){ while(parent[x]!=x){ parent[x]=parent[parent[x]]; x=parent[x]; } return x; }
static int peso(int v){ return __builtin_popcount(v); }

/* Costo esatto della etichettatura indotta + lambda * cicli residui. */
static long valuta(int lambda, int *cicli_out){
    int k[N]; long tot=0; int cicli=0;
    for(int v=0; v<N; v++) parent[v]=v;
    for(int b=0;b<N;b++) if(peso(b)&1){ k[b]=0; for(int i=0;i<D;i++) if(tipo[b^(1<<i)]==2) k[b]++; }
    for(int v=0; v<N; v++){
        if(peso(v)&1){ if(tipo[v]==0) tot+=1; else tot+=(k[v]>1?k[v]:1); }
        else if(tipo[v]==2){ tot+=1;
            for(int i=0;i<D;i++){ int o=v^(1<<i); if(tipo[o]==0){ int a=find(v),c=find(o); if(a==c) cicli++; else parent[a]=c; } } }
        else { for(int i=0;i<D;i++){ int o=v^(1<<i); tot += (tipo[o]==0||k[o]<2)?1:k[o]; } }
    }
    *cicli_out=cicli; return tot + (long)lambda*cicli;
}

int main(int argc, char **argv){
    int seme=atoi(argv[1]); long passi=atol(argv[2]); double t0=atof(argv[3]), t1=atof(argv[4]); srand(seme);
    for(int v=0; v<N; v++) tipo[v]=(peso(v)&1)?0:3;
    if(argc>5){ FILE *f=fopen(argv[5],"r"); for(int v=0; v<N; v++) fscanf(f,"%d",&tipo[v]); fclose(f); }
    int lambda=40, cicli; long cur=valuta(lambda,&cicli), best=1L<<40; int bestT[N];
    if(cicli==0){ best=cur; memcpy(bestT,tipo,sizeof(tipo)); }
    for(long s=0;s<passi;s++){
        double t=t0*pow(t1/t0,(double)s/passi);
        int v=rand()%N; int vecchio=tipo[v];
        tipo[v] = (peso(v)&1) ? 1-vecchio : 5-vecchio;
        int c2; long nuovo=valuta(lambda,&c2);
        if(nuovo<=cur || (double)rand()/RAND_MAX < exp((cur-nuovo)/t)){ cur=nuovo; cicli=c2;
            if(cicli==0 && cur<best){ best=cur; memcpy(bestT,tipo,sizeof(tipo));
                int nr=0,nb=0; for(int u=0;u<N;u++){ nr+=tipo[u]==2; nb+=tipo[u]==1; }
                fprintf(stderr,"seme %d passo %ld: costo %ld |R|=%d |B|=%d\n",seme,s,best,nr,nb); } }
        else tipo[v]=vecchio;
    }
    char nome[64]; sprintf(nome,"migliore_radici_%d.txt",seme); FILE *f=fopen(nome,"w");
    for(int v=0; v<N; v++) fprintf(f,"%d\n",bestT[v]); fclose(f);
    printf("seme %d: costo migliore %ld\n",seme,best); return 0;
}
