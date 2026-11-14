/* vq3c.c — sciame-validazione, estensione f7, verifica della decisione.
 * Rifacimento INDIPENDENTE del predicato «stato(p)» (Q3c) della DECISIONE §1.3,
 * scritto dallo pseudocodice, senza leggere 11-torneo/torneo.c.
 * Compilare: gcc -O2 -o vq3c vq3c.c -lm     Lanciare: timeout 120 ./vq3c > risultati_vq3c.txt
 * Semi fissati (SEME). Camera ideale a foro: 1,2 m, 15 gradi in giu', 87 x 58 gradi, 320 x 240,
 * rumore gaussiano 0,004 z^2, 15 fotogrammi al secondo. Stanza 6 x 4 x 3 m.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define W 320
#define H 240
#define NPIX (W*H)
#define FPS 15.0
#define NF 92
#define PI 3.14159265358979323846
#define SEME 20261114ULL

static const double CAMH = 1.2, TILT = 15.0, HFOV = 87.0, VFOV = 58.0;
static double ax, az_, fx, fy;            /* asse ottico (ax,0,az_) ; giu' = (az_... ) */
static uint64_t rs;
static double rnd(void){ rs ^= rs>>12; rs ^= rs<<25; rs ^= rs>>27; return ((rs*2685821657736338717ULL)>>11)*(1.0/9007199254740992.0); }
static double gauss(void){ double u=rnd(), v=rnd(); if(u<1e-300)u=1e-300; return sqrt(-2*log(u))*cos(2*PI*v); }

/* corpi: 0 = scatola, 1 = cilindro verticale */
typedef struct { int tipo; double x0,x1,y0,y1,z1; double cx,cy,R; int muto; } Corpo;
#define MAXC 8
static Corpo corpi[MAXC]; static int nc;

/* raggio O + t D, t>0: restituisce il t minimo sui corpi (1e30 se nessuno), e quale */
static double colpisci_corpi(const double O[3], const double D[3], int *quale){
  double best=1e30; *quale=-1;
  for(int k=0;k<nc;k++){ Corpo *c=&corpi[k]; double t=1e30;
    if(c->tipo==0){
      double lo[3]={c->x0,c->y0,0}, hi[3]={c->x1,c->y1,c->z1}, t0=1e-9, t1=1e30; int ok=1;
      for(int i=0;i<3&&ok;i++){
        if(fabs(D[i])<1e-12){ if(O[i]<lo[i]||O[i]>hi[i]) ok=0; }
        else { double a=(lo[i]-O[i])/D[i], b=(hi[i]-O[i])/D[i]; if(a>b){double s=a;a=b;b=s;} if(a>t0)t0=a; if(b<t1)t1=b; if(t0>t1) ok=0; }
      }
      if(ok) t=t0;
    } else {
      double dx=O[0]-c->cx, dy=O[1]-c->cy; double A=D[0]*D[0]+D[1]*D[1], B=2*(dx*D[0]+dy*D[1]), Cc=dx*dx+dy*dy-c->R*c->R;
      if(A>1e-14){ double disc=B*B-4*A*Cc; if(disc>=0){ double s=sqrt(disc); double ta=(-B-s)/(2*A), tb=(-B+s)/(2*A);
          if(ta>1e-9){ double z=O[2]+ta*D[2]; if(z>=0&&z<=c->z1) t=ta; }
          if(t>1e29 && fabs(D[2])>1e-12){ /* coperchio */ double tc=(c->z1-O[2])/D[2]; if(tc>1e-9 && tc>=ta && tc<=tb) t=tc; }
      } }
    }
    if(t<best){best=t;*quale=k;}
  }
  return best;
}
/* stanza: pavimento z=0, soffitto z=3, fondo x=6, lati y=+-2 */
static double colpisci_stanza(const double O[3], const double D[3]){
  double best=1e30,t;
  if(D[2]<-1e-12){ t=-O[2]/D[2]; if(t<best)best=t; }
  if(D[2]> 1e-12){ t=(3.0-O[2])/D[2]; if(t<best)best=t; }
  if(D[0]> 1e-12){ t=(6.0-O[0])/D[0]; if(t<best)best=t; }
  if(D[1]> 1e-12){ t=(2.0-O[1])/D[1]; if(t<best)best=t; }
  if(D[1]<-1e-12){ t=(-2.0-O[1])/D[1]; if(t<best)best=t; }
  return best;
}
/* profondita' di penetrazione in un corpo (laterale e dall'alto); <=0 se fuori */
static double dentro(double x,double y,double z){
  double m=-1e30;
  for(int k=0;k<nc;k++){ Corpo *c=&corpi[k]; double d;
    if(z<0||z>c->z1) continue;
    if(c->tipo==0){ d=x-c->x0; if(c->x1-x<d)d=c->x1-x; if(y-c->y0<d)d=y-c->y0; if(c->y1-y<d)d=c->y1-y; }
    else d=c->R-hypot(x-c->cx,y-c->cy);
    if(c->z1-z<d) d=c->z1-z;
    if(d>m) m=d;
  }
  return m;
}

static float D3[3][NPIX];                 /* tre fotogrammi; <=0 = non valido */
static const double O[3]={0,0,1.2};

static void fotogramma(float *D, double sparsi, double chiazze){
  static unsigned char buco[(H/20+1)*(W/20+1)];
  int bw=W/20+1;
  for(int i=0;i<(H/20+1)*bw;i++) buco[i]= chiazze>0 && rnd()<chiazze;
  for(int j=0;j<H;j++) for(int i=0;i<W;i++){
    double a=(i+0.5-W/2.0)/fx, b=(j+0.5-H/2.0)/fy;
    /* destra = (0,-1,0) ; giu' = (az_... ) = (-sin t,0,-cos t) = (az_,0,-ax) con az_=-sin t */
    double Dd[3]={ ax + b*az_, -a, az_ - b*ax };
    int q; double tc=colpisci_corpi(O,Dd,&q), ts=colpisci_stanza(O,Dd); double t; int muto=0;
    if(tc<ts){ t=tc; muto=corpi[q].muto; } else t=ts;
    float d=-1;
    if(!muto && t>0.3 && t<10.0){ double z=t+0.004*t*t*gauss(); if(z>0.3) d=(float)z; }
    if(sparsi>0 && rnd()<sparsi) d=-1;
    if(buco[(j/20)*bw+(i/20)]) d=-1;
    D[j*W+i]=d;
  }
}

enum { LIBERO=1, OCCUPATO=2, IN_OMBRA=3, NON_VALIDO=4, FUORI=5 };
typedef struct { int iu,iv; double z; int ok; } Proj;
static Proj proietta(double x,double y,double z){
  Proj p; double vx=x, vy=y, vz=z-CAMH;
  double Z=vx*ax+vz*az_, X=-vy, Y=vx*az_ - vz*ax;
  p.z=Z; p.ok=0; p.iu=p.iv=0;
  if(Z<=0.05) return p;
  double u=W/2.0+fx*X/Z, v=H/2.0+fy*Y/Z;
  p.iu=(int)floor(u); p.iv=(int)floor(v);
  if(p.iu>=1&&p.iu<W-1&&p.iv>=1&&p.iv<H-1) p.ok=1;
  return p;
}
static double marg(double z){ return 0.03+3*0.004*z*z; }
static int leggi(const float *D, const Proj *p){
  if(!p->ok) return FUORI;
  double mn=1e30,mx=-1e30;
  for(int dj=-1;dj<=1;dj++) for(int di=-1;di<=1;di++){ float d=D[(p->iv+dj)*W+p->iu+di]; if(d<=0) return NON_VALIDO; if(d<mn)mn=d; if(d>mx)mx=d; }
  double m=marg(p->z);
  if(p->z<mn-m) return LIBERO;
  if(p->z>mx+m) return IN_OMBRA;
  return OCCUPATO;
}
/* nessun pixel valido del 3x3 piu' vicino di z+m(z) nel fotogramma corrente */
static int non_contraddetto(const float *D, const Proj *p){
  double lim=p->z+marg(p->z);
  for(int dj=-1;dj<=1;dj++) for(int di=-1;di<=1;di++){ float d=D[(p->iv+dj)*W+p->iu+di]; if(d>0 && d<lim) return 0; }
  return 1;
}
static int centro_valido(const float *D, const Proj *p){ return D[p->iv*W+p->iu]>0; }

/* reticolo dei punti */
#define NX 65
#define NY 80
#define NZ 40
#define NP (NX*NY*NZ)
static Proj PP[NP]; static float PXYZ[NP][3];
static unsigned char L[3][NP];            /* leggi() dei tre fotogrammi */
/* celle polari 1 grado x 0,1 m fino a 3 m : 87 x 30 = 2610 */
#define NA 87
#define NR 30
#define NCEL (NA*NR)
#define NHQ 3
static const double HQ[NHQ]={0.05,0.10,0.15};
static Proj CP[NHQ][NCEL]; static double CXY[NCEL][2];
static unsigned char CL[NHQ][3][NCEL];
static unsigned char suolo_visto[3][NCEL];

static int fp_cella[NPIX]; static float fp_prof[NPIX]; static int fp_tot[NCEL];
static int visibile(double x,double y,double z,const Proj *p){
  if(!p->ok) return 0;
  double Dd[3]={x-O[0],y-O[1],z-O[2]}; int q; double t=colpisci_corpi(O,Dd,&q);
  return t>=1.0;
}

typedef struct { const char *nome; double sparsi, chiazze; int muti; int fermi; } Cond;

static void scena(int f, int muti, int fermi){
  nc=0;
  corpi[nc++]=(Corpo){0, 1.30,1.90,-1.00,-0.40,1.00, 0,0,0, 0};        /* cassa da 1 m */
  corpi[nc++]=(Corpo){0, 1.75,1.85, 0.20, 1.20,2.00, 0,0,0, 0};        /* pannello da 2 m */
  if(fermi) return;
  double t=f/FPS;
  /* A: di traverso a 1,4 m/s, x=2,4, y fra -1,7 e +1,7 (onda triangolare) */
  double per=2*3.4/1.4, ph=fmod(t,per), ya = ph<per/2 ? -1.7+1.4*ph : 1.7-1.4*(ph-per/2);
  corpi[nc++]=(Corpo){1, 0,0,0,0,1.75, 2.40,ya,0.22, muti};
  /* B: in avvicinamento a 1,0 m/s lungo y=-0,05, x fra 3,4 e 0,9 */
  double perb=2*2.5/1.0, pb=fmod(t,perb), xb = pb<perb/2 ? 3.4-1.0*pb : 0.9+1.0*(pb-perb/2);
  corpi[nc++]=(Corpo){1, 0,0,0,0,1.75, xb,-0.05,0.22, muti};
}

int main(void){
  double tr=TILT*PI/180; ax=cos(tr); az_=-sin(tr);
  fx=(W/2.0)/tan(HFOV/2*PI/180); fy=(H/2.0)/tan(VFOV/2*PI/180);
  int n=0;
  for(int i=0;i<NX;i++) for(int j=0;j<NY;j++) for(int k=0;k<NZ;k++){
    double x=0.3125+0.05*i, y=-1.9625+0.05*j, z=0.0625+0.05*k;
    PXYZ[n][0]=x;PXYZ[n][1]=y;PXYZ[n][2]=z; PP[n]=proietta(x,y,z); n++; }
  for(int a=0;a<NA;a++) for(int r=0;r<NR;r++){ double az=(-43.5+a+0.5)*PI/180, rr=0.05+0.1*r; int c=a*NR+r;
    CXY[c][0]=rr*cos(az); CXY[c][1]=rr*sin(az);
    for(int h=0;h<NHQ;h++) CP[h][c]=proietta(CXY[c][0],CXY[c][1],HQ[h]); }

  /* impronta del suolo: per ogni pixel, cella toccata dal raggio e profondita' attesa (sensore fermo) */
  for(int j=0;j<H;j++) for(int i=0;i<W;i++){ double a=(i+0.5-W/2.0)/fx, b=(j+0.5-H/2.0)/fy; double dz=az_-b*ax; fp_cella[j*W+i]=-1;
    if(dz<-1e-9){ double t=-CAMH/dz; double x=t*(ax+b*az_), y=t*(-a); double r=hypot(x,y), azd=atan2(y,x)*180/PI; int ia=(int)floor(azd+43.5), ir=(int)floor(r/0.1);
      if(ia>=0&&ia<NA&&ir>=0&&ir<NR){ fp_cella[j*W+i]=ia*NR+ir; fp_prof[j*W+i]=(float)t; fp_tot[ia*NR+ir]++; } } }
  Cond cond[]={
    {"(a) senza buchi",0,0,0,0},{"(b) sparsi 5 %",0.05,0,0,0},{"(c) sparsi 30 %",0.30,0,0,0},
    {"(d) chiazze 30 %",0,0.30,0,0},{"(e) soggetti muti",0,0,1,0},{"(f) muti + chiazze 30 %",0,0.30,1,0},
    {"(g) muti + sparsi 5 %",0.05,0,1,0},
    {"(s0) scena ferma, 0 %",0,0,0,1},{"(s5) scena ferma, sparsi 5 %",0.05,0,0,1},{"(s10) scena ferma, sparsi 10 %",0.10,0,0,1}};
  int ncond=sizeof cond/sizeof cond[0];
  printf("# vq3c: reticolo 5 cm, %d punti; %d celle; %d fotogrammi per condizione (i primi 2 non contati); seme %llu\n",NP,NCEL,NF,(unsigned long long)SEME);
  printf("# «prof» = dato per libero e dentro un corpo oltre 5 cm; «bordo» = dentro un corpo fino a 5 cm; F = fotogrammi con almeno un «prof»\n");
  for(int ci=0;ci<ncond;ci++){
    Cond *C=&cond[ci]; rs=SEME+ci*7919ULL; for(int i=0;i<20;i++) rnd();
    long Fq[3]={0,0,0}, prof[3]={0,0,0}, bordo[3]={0,0,0}, lib[3]={0,0,0}, veri=0, lib15[3]={0,0,0}, veri15=0;
    long sN[5]={0}, sPort[5]={0}, sScon[5]={0}, sCambi[5]={0}, sCoppie=0; static long sIst[5][32]; memset(sIst,0,sizeof sIst); static int sPrec[5][20]; static unsigned char qc[5][NCEL], vc[NCEL]; long iF[2]={0,0},iprof[2]={0,0},ilib[2]={0,0},icambi[2]={0,0}; static unsigned char precI[2][NCEL]; static int cntI[NCEL]; long oF=0,oprof=0,olib=0,ocambi=0,onasc=0; static unsigned char precO[NCEL];
    long cF[NHQ]={0}, cprof[NHQ]={0}, clib[NHQ]={0}, cveri[NHQ]={0}, ccambi[NHQ]={0}, ccoppie[NHQ]={0};
    long c1lib=0,c1cambi=0;                 /* Q1 sulle celle a 0,10 m */
    long nF=0,nprof=0,nlib=0,nveri=0,ncambi=0,ncoppie=0, nasc=0;
    static unsigned char prec[NHQ][NCEL], prec1[NCEL], precN[NCEL]; static unsigned char vprec[NHQ][NCEL], vprecN[NCEL];
    int cont=0; long pixval=0; for(int m=0;m<5;m++) for(int i=0;i<20;i++) sPrec[m][i]=-1;
    for(int f=0;f<NF;f++){
      scena(f,C->muti,C->fermi);
      int s=f%3, s1=(f+2)%3, s2=(f+1)%3;
      fotogramma(D3[s],C->sparsi,C->chiazze);
      const float *D=D3[s];
      for(int p=0;p<NP;p++) L[s][p]=(unsigned char)leggi(D,&PP[p]);
      for(int h=0;h<NHQ;h++) for(int c=0;c<NCEL;c++) CL[h][s][c]=(unsigned char)leggi(D,&CP[h][c]);
      /* griglia N1 (mia lettura): suolo visto, occupato, ombra oltre il primo occupato */
      static unsigned char occ[NCEL], omb[NCEL];
      memset(suolo_visto[s],0,NCEL); memset(occ,0,NCEL); memset(omb,0,NCEL);
      for(int j=0;j<H;j++) for(int i=0;i<W;i++){ float d=D[j*W+i]; if(d<=0) continue;
        double a=(i+0.5-W/2.0)/fx, b=(j+0.5-H/2.0)/fy;
        double x=d*(ax+b*az_), y=d*(-a), z=CAMH+d*(az_-b*ax);
        double r=hypot(x,y), azd=atan2(y,x)*180/PI; int ia=(int)floor(azd+43.5), ir=(int)floor(r/0.1);
        if(ia<0||ia>=NA||ir<0||ir>=NR) continue;
        if(z<0.07) suolo_visto[s][ia*NR+ir]=1; else if(z<=2.0) occ[ia*NR+ir]=1; }
      for(int a=0;a<NA;a++){ int primo=-1; for(int r=0;r<NR;r++){ if(primo>=0) omb[a*NR+r]=1; else if(occ[a*NR+r]) primo=r; } }
      memset(cntI,0,sizeof cntI);
      for(int i=0;i<NPIX;i++){ int c=fp_cella[i]; float d=D[i]; if(c<0||d<=0) continue; if(fabs(d-fp_prof[i])<=marg(fp_prof[i])) cntI[c]++; }
      if(f<2) continue;
      cont++;
      for(int i=0;i<NPIX;i++) if(D[i]>0) pixval++;
      /* punti */
      long fp[3]={0,0,0};
      for(int p=0;p<NP;p++){
        int l0=L[s][p]; int mem=(L[s1][p]==LIBERO||L[s2][p]==LIBERO);
        int q[3]; q[0]=(l0==LIBERO);
        int nc_=0, cv=0; if(!q[0] && mem && PP[p].ok){ nc_=non_contraddetto(D,&PP[p]); cv=centro_valido(D,&PP[p]); }
        q[1]= q[0] || (mem && nc_);
        q[2]= q[0] || (mem && nc_ && cv);
        double x=PXYZ[p][0],y=PXYZ[p][1],z=PXYZ[p][2];
        double dn=dentro(x,y,z);
        int vero = dn<=0 && visibile(x,y,z,&PP[p]);
        if(vero){ veri++; if(z>=0.15) veri15++; }
        if(dn>0 && dn<=0.05){ /* nascosto dentro il bordo */ }
        for(int k=0;k<3;k++) if(q[k]){ if(vero){ lib[k]++; if(z>=0.15) lib15[k]++; } if(dn>0.05){prof[k]++;fp[k]++;} else if(dn>0) bordo[k]++; }
      }
      for(int k=0;k<3;k++) if(fp[k]) Fq[k]++;
      /* celle */
      for(int h=0;h<NHQ;h++){ long fpc=0;
        for(int c=0;c<NCEL;c++){ const Proj *p=&CP[h][c];
          int l0=CL[h][s][c]; int mem=(CL[h][s1][c]==LIBERO||CL[h][s2][c]==LIBERO);
          int q=(l0==LIBERO) || (mem && p->ok && centro_valido(D,p) && non_contraddetto(D,p));
          double dn=dentro(CXY[c][0],CXY[c][1],HQ[h]); int vero= dn<=0 && visibile(CXY[c][0],CXY[c][1],HQ[h],p);
          if(vero){ cveri[h]++; if(q) clib[h]++; }
          if(q && dn>0.05){ cprof[h]++; fpc++; }
          if(cont>1 && vero && vprec[h][c]){ ccoppie[h]++; if(q!=prec[h][c]) ccambi[h]++; }
          if(h==1){ int q1=(l0==LIBERO); if(vero&&q1) c1lib++; if(cont>1 && vero && vprec[h][c] && q1!=prec1[c]) c1cambi++; prec1[c]=q1; }
          prec[h][c]=q; vprec[h][c]=vero; if(h==1){ qc[0][c]=q; vc[c]=vero; } }
        if(fpc) cF[h]++; }
      /* N1 */
      { long fpn=0, fpo=0, fpi[2]={0,0}; for(int c=0;c<NCEL;c++){
          int q=(suolo_visto[s][c]||suolo_visto[s1][c]||suolo_visto[s2][c]) && !occ[c] && !omb[c];
          int qo=suolo_visto[s][c] && !occ[c] && !omb[c];
          double dn=dentro(CXY[c][0],CXY[c][1],0.02); const Proj pr=proietta(CXY[c][0],CXY[c][1],0.02);
          int vero= dn<=0 && visibile(CXY[c][0],CXY[c][1],0.02,&pr);
          if(vero){ nveri++; if(q) nlib++; }
          if(q && dn>0.05){ nprof++; fpn++; }
          if(q && dn<=0 && pr.ok && !vero) nasc++;
          if(vero&&qo) olib++; if(qo && dn>0.05){ oprof++; fpo++; } if(qo && dn<=0 && pr.ok && !vero) onasc++;
          if(cont>1 && vero && vprecN[c] && qo!=precO[c]) ocambi++; precO[c]=qo; qc[2][c]=qo;
          for(int k=0;k<2;k++){ int soglia = k==0 ? 1 : (fp_tot[c]+1)/2; if(soglia<1) soglia=1;
            int qi = cntI[c]>=soglia && !occ[c] && !omb[c];
            if(vero&&qi) ilib[k]++; if(qi && dn>0.05){ iprof[k]++; fpi[k]++; }
            if(cont>1 && vero && vprecN[c] && qi!=precI[k][c]) icambi[k]++; precI[k][c]=qi; qc[3+k][c]=qi; }
          if(cont>1 && vero && vprecN[c]){ ncoppie++; if(q!=precN[c]) ncambi++; }
          precN[c]=q; vprecN[c]=vero; qc[1][c]=q; }
        if(fpn) nF++; if(fpo) oF++; for(int k=0;k<2;k++) if(fpi[k]) iF[k]++; }

      /* settori di 5 gradi (regola unica della specializzazione, par. 3.1): estensione del libero da 1,3 m, direzione peggiore */
      for(int st=0;st<17;st++){ int aperto=1;
        for(int a=1+5*st;a<6+5*st;a++) for(int r=13;r<NR;r++) if(!vc[a*NR+r]) aperto=0;
        if(!aperto){ for(int m=0;m<5;m++) sPrec[m][st]=-1; continue; }
        for(int m=0;m<5;m++){ int est=NR;
          for(int a=1+5*st;a<6+5*st;a++){ int r=13; while(r<NR && qc[m][a*NR+r]) r++; if(r<est) est=r; }
          sN[m]++; sIst[m][est]++; if(est==NR) sPort[m]++; if(est==13) sScon[m]++;
          if(sPrec[m][st]>=0){ if(m==0) sCoppie++; if(sPrec[m][st]!=est) sCambi[m]++; }
          sPrec[m][st]=est; }
      }
    }
    static const char *nq[3]={"Q1 ","Q3 ","Q3c"};
    printf("\n## %s — fotogrammi contati %d, pixel validi medi %.1f %%\n",C->nome,cont,100.0*pixval/((double)cont*NPIX));
    printf("  PUNTI (liberi veri visibili per fotogramma: %.0f)\n",(double)veri/cont);
    for(int k=0;k<3;k++) printf("    %s  F %3ld su %d ; prof %7ld ; bordo %6ld ; resa %5.1f %% ; resa a quota >= 0,15 m %5.1f %%\n",nq[k],Fq[k],cont,prof[k],bordo[k],100.0*lib[k]/(veri?veri:1),100.0*lib15[k]/(veri15?veri15:1));
    printf("  CELLE (2610), Q3c sul centro a quota h; cambi = cambi di stato libero/non libero per cella al secondo, sulle celle libere e visibili\n");
    for(int h=0;h<NHQ;h++) printf("    h %.2f m  F %3ld su %d ; prof %6ld ; resa %5.1f %% (celle vere per fotogramma %.0f) ; cambi %.2f /s\n",HQ[h],cF[h],cont,cprof[h],100.0*clib[h]/(cveri[h]?cveri[h]:1),(double)cveri[h]/cont,FPS*ccambi[h]/(ccoppie[h]?ccoppie[h]:1));
    printf("    Q1 sul centro a 0,10 m: resa %5.1f %% ; cambi %.2f /s\n",100.0*c1lib/(cveri[1]?cveri[1]:1),FPS*c1cambi/(ccoppie[1]?ccoppie[1]:1));
    printf("    N1 (suolo visto in 1 di 3, occupato e ombra di ora vincono): F %3ld su %d ; prof %6ld ; libere ma nascoste %ld ; resa %5.1f %% (celle vere %.0f) ; cambi %.2f /s\n",nF,cont,nprof,nasc,100.0*nlib/(nveri?nveri:1),(double)nveri/cont,FPS*ncambi/(ncoppie?ncoppie:1));
    printf("    suolo visto ORA (validazione-1, senza memoria): F %3ld su %d ; prof %6ld ; libere ma nascoste %ld ; resa %5.1f %% ; cambi %.2f /s\n",oF,cont,oprof,onasc,100.0*olib/(nveri?nveri:1),FPS*ocambi/(ncoppie?ncoppie:1));

    for(int k=0;k<2;k++) printf("    impronta del suolo, %s (validazione-2): F %3ld su %d ; prof %6ld ; resa %5.1f %% ; cambi %.2f /s\n",k==0?"k = 1 pixel":"k = meta' dell'impronta",iF[k],cont,iprof[k],100.0*ilib[k]/(nveri?nveri:1),FPS*icambi[k]/(ncoppie?ncoppie:1));
    { static const char *nm[5]={"Q3c sulle celle (h 0,10 m)","N1","suolo visto ORA (validazione-1)","impronta, k = 1 (validazione-2)","impronta, k = meta' (validazione-2)"};
      for(int m=0;m<5;m++){ if(!sN[m]) continue; long acc=0; int med=-1; double media=0; for(int e=0;e<=NR;e++){ acc+=sIst[m][e]; media+=0.1*e*sIst[m][e]; if(med<0 && 2*acc>=sN[m]) med=e; }
        printf("    SETTORI 5 gradi aperti, %s: settori-fotogramma %ld ; estensione mediana %.1f m, media %.2f m (vera 3,0) ; «fino alla portata» %.1f %% ; «sconosciuto» %.1f %% ; cambi %.2f /s\n",nm[m],sN[m],0.1*med,media/sN[m],100.0*sPort[m]/sN[m],100.0*sScon[m]/sN[m],FPS*sCambi[m]/(sCoppie?sCoppie:1)); } }
  }
  return 0;
}
