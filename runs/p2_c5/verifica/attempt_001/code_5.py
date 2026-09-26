/* ricottura_etichette.c — ricottura simulata (esplorazione, NON prova) direttamente sulle etichettature di Q_9.
   Stato: permutazione ordine[0..511] (vertice con etichetta i). Mossa: scambio di due etichette. Punteggio esatto:
   conteggio dei cammini in salita con aritmetica intera (p(v) = [valle] + somma p sui vicini minori).
   Uso: ./ricottura_etichette seme passi t0 t1 [etichettatura_iniziale.txt (512 stringhe 0/1 separate da virgola)] */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define D 9
#define N (1<<D)
static int ordine[N], etichetta[N];
static long long p[N];

/* Conteggio esatto dei cammini in salita. */
static long long conta(void){
    long long tot=0;
    for(int i=0;i<N;i++){ int v=ordine[i]; long long s=0; int valle=1;
        for(int j=0;j<D;j++){ int u=v^(1<<j); if(etichetta[u]<i){ s+=p[u]; valle=0; } }
        p[v]= valle?1:s; tot+=p[v]; }
    return tot;
}
static int da_stringa(const char *s){ int v=0; for(int i=0;i<D;i++) if(s[i]=='1') v|=1<<i; return v; }

int main(int argc,char**argv){
    int seme=atoi(argv[1]); long passi=atol(argv[2]); double t0=atof(argv[3]), t1=atof(argv[4]); srand(seme);
    for(int i=0;i<N;i++) ordine[i]=i;
    if(argc>5){ FILE*f=fopen(argv[5],"r"); char s[16]; for(int i=0;i<N;i++){ fscanf(f,"%[01],",s); ordine[i]=da_stringa(s);} fclose(f); }
    else for(int i=N-1;i>0;i--){ int j=rand()%(i+1); int t=ordine[i]; ordine[i]=ordine[j]; ordine[j]=t; }
    for(int i=0;i<N;i++) etichetta[ordine[i]]=i;
    long long cur=conta(), best=cur; int bestO[N]; memcpy(bestO,ordine,sizeof(ordine));
    fprintf(stderr,"seme %d inizio %lld\n",seme,cur);
    for(long k=0;k<passi;k++){
        double t=t0*pow(t1/t0,(double)k/passi);
        int i=rand()%N, j=rand()%N; if(i==j) continue;
        int a=ordine[i], b=ordine[j]; ordine[i]=b; ordine[j]=a; etichetta[b]=i; etichetta[a]=j;
        long long nuovo=conta();
        if(nuovo<=cur || (double)rand()/RAND_MAX<exp((double)(cur-nuovo)/t)){ cur=nuovo;
            if(cur<best){ best=cur; memcpy(bestO,ordine,sizeof(ordine)); fprintf(stderr,"seme %d passo %ld: %lld\n",seme,k,best);} }
        else { ordine[i]=a; ordine[j]=b; etichetta[a]=i; etichetta[b]=j; }
    }
    char nome[64]; sprintf(nome,"migliore_etichette_%d.txt",seme); FILE*f=fopen(nome,"w");
    for(int i=0;i<N;i++){ for(int j=0;j<D;j++) fputc((bestO[i]>>j)&1?'1':'0',f); fputc(i<N-1?',':'\n',f);} fclose(f);
    printf("seme %d: migliore %lld\n",seme,best); return 0;
}
