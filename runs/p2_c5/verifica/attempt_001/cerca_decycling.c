/* cerca_decycling.c — ricottura simulata su sottoinsiemi H di V(Q_9) (esplorazione, NON prova).
   Cerca H tale che Q_9 - H sia una foresta e il costo 8|H| + 6|E(H)| sia piccolo:
   per la riduzione (ogni etichettatura ha #cammini >= 2^d + (d-1)|H| + ...), un tale H con costo <= 1887
   produce una etichettatura con <= 2399 cammini. Penalita' lambda per ogni ciclo residuo in S = V \ H.
   Uso: ./cerca_decycling seme passi [file_iniziale]   -> stampa il costo migliore e salva H in migliore_<seme>.txt */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define D 9
#define N (1<<D)
static int inH[N], parent[N];
static int find(int x){ while(parent[x]!=x){ parent[x]=parent[parent[x]]; x=parent[x]; } return x; }

/* Calcola cicli residui di S (numero di spigoli di S non in una foresta di supporto) e numero di spigoli dentro H. */
static void valuta(int *cicli, int *spigoliH){
    int c=0, eh=0;
    for(int v=0; v<N; v++) parent[v]=v;
    for(int v=0; v<N; v++) for(int i=0;i<D;i++){ int u=v^(1<<i); if(u<v) continue;
        if(inH[v]&&inH[u]) eh++;
        else if(!inH[v]&&!inH[u]){ int a=find(v), b=find(u); if(a==b) c++; else parent[a]=b; }
    }
    *cicli=c; *spigoliH=eh;
}
static long costo(int h, int eh, int cicli, int lambda){ return 8L*h + 6L*eh + (long)lambda*cicli; }

int main(int argc, char **argv){
    int seme = atoi(argv[1]); long passi = atol(argv[2]); srand(seme);
    int h=0;
    if(argc>3){ FILE *f=fopen(argv[3],"r"); for(int v=0; v<N; v++){ fscanf(f,"%d",&inH[v]); h+=inH[v]; } fclose(f); }
    else for(int v=0; v<N; v++){ inH[v]=rand()%2; h+=inH[v]; }
    int lambda=24, cicli, eh; valuta(&cicli,&eh);
    long cur=costo(h,eh,cicli,lambda), best=1L<<40; double t0=8.0, t1=0.3;
    int bestH[N];
    for(long k=0;k<passi;k++){
        double t = t0*pow(t1/t0,(double)k/passi);
        int v=rand()%N; inH[v]^=1; h += inH[v]?1:-1;
        int c2,e2; valuta(&c2,&e2); long nuovo=costo(h,e2,c2,lambda);
        if(nuovo<=cur || (double)rand()/RAND_MAX < exp((cur-nuovo)/t)){ cur=nuovo; cicli=c2; eh=e2;
            if(cicli==0 && cur<best){ best=cur; memcpy(bestH,inH,sizeof(inH));
                fprintf(stderr,"seme %d passo %ld: costo %ld |H|=%d E(H)=%d\n",seme,k,best,h,eh); } }
        else { inH[v]^=1; h += inH[v]?1:-1; }
    }
    fprintf(stderr,"fine: |H|=%d E(H)=%d cicli=%d cur=%ld\n",h,eh,cicli,cur);
    char nome[64]; sprintf(nome,"migliore_%d.txt",seme); FILE *f=fopen(nome,"w");
    for(int v=0; v<N; v++) fprintf(f,"%d\n",bestH[v]); fclose(f);
    printf("seme %d: costo migliore %ld\n",seme,best); return 0;
}
