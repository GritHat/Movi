// rovescia.c — prove del rovesciatore (f7). Scena sintetica deterministica, nessun numero casuale.
// Compilare: gcc -O2 -o rovescia rovescia.c -lm      Lanciare: ./rovescia analisi | ./rovescia tempi
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

#define W 640
#define H 480
#define PI 3.14159265358979323846
typedef struct { double lo[3], hi[3]; const char *nome; } Box;
static Box boxes[16]; static int nbox;
static const double O[3] = {0, 0, 1.2};
static double F[3], R[3] = {1, 0, 0}, U[3], fx, fy;
static const double RMIN = 0.4, RMAX = 6.0, EPS = 0.03;
static const double G0[3] = {-2.013, -0.017, -0.021}; // origine della griglia voxel: nessuna superficie cade su un bordo
static float depth[H][W];           // distanza lungo il raggio; 0 = non valido
static float dirs[H][W][3];
static long colpi[16];              // pixel che colpiscono ciascun oggetto

static double now_ms(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec*1e3+t.tv_nsec/1e6; }

static void add(const char*n,double x0,double x1,double y0,double y1,double z0,double z1){
  Box b={{x0,y0,z0},{x1,y1,z1},n}; boxes[nbox++]=b; }
static void scena(int tipo){ // 0 demo con parete, 1 demo senza parete, 2 peggiore (vuota con parete)
  nbox=0;
  if(tipo==3) add("parete",-10,10,4.0,4.2,0,10); else if(tipo!=1) add("parete",-10,10,5.5,5.7,0,10);
  if(tipo==2) return;
  add("pannello",-0.23,0.79,1.83,1.87,0,2.0);
  add("scatola bassa",0.95,1.35,1.43,1.73,0,0.20);
  add("barra in quota",-1.10,-0.50,1.50,1.55,1.75,1.90);
  add("oggetto in volo",-1.50,-1.30,2.30,2.50,1.00,1.20);
}
static void camera(void){
  double p=15*PI/180; F[0]=0;F[1]=cos(p);F[2]=-sin(p); U[0]=0;U[1]=sin(p);U[2]=cos(p);
  fx=(W/2.0)/tan(43.5*PI/180); fy=(H/2.0)/tan(29*PI/180);
  for(int j=0;j<H;j++)for(int i=0;i<W;i++){
    double a=(i+0.5-W/2.0)/fx,b=(H/2.0-(j+0.5))/fy,d[3],n=0;
    for(int k=0;k<3;k++){d[k]=F[k]+a*R[k]+b*U[k];n+=d[k]*d[k];} n=sqrt(n);
    for(int k=0;k<3;k++)dirs[j][i][k]=(float)(d[k]/n);
  }
}
static double ray(const double*d,int*id){
  double best=1e30; *id=-1;
  if(d[2]<0){ best=-O[2]/d[2]; *id=15; }
  for(int b=0;b<nbox;b++){
    double t0=0,t1=1e30; int ok=1;
    for(int k=0;k<3&&ok;k++){
      if(fabs(d[k])<1e-12){ if(O[k]<boxes[b].lo[k]||O[k]>boxes[b].hi[k]) ok=0; }
      else { double a=(boxes[b].lo[k]-O[k])/d[k],c=(boxes[b].hi[k]-O[k])/d[k]; if(a>c){double s=a;a=c;c=s;}
             if(a>t0)t0=a; if(c<t1)t1=c; if(t0>t1)ok=0; }
    }
    if(ok&&t0>1e-9&&t0<best){best=t0;*id=b;}
  }
  return best;
}
static void render(double delta_deg){ // delta = imbardata vera non nota a chi integra
  double c=cos(delta_deg*PI/180),s=sin(delta_deg*PI/180); memset(colpi,0,sizeof colpi);
  for(int j=0;j<H;j++)for(int i=0;i<W;i++){
    double d[3]={c*dirs[j][i][0]-s*dirs[j][i][1], s*dirs[j][i][0]+c*dirs[j][i][1], dirs[j][i][2]}; int id;
    double t=ray(d,&id);
    if(t>=RMIN&&t<=RMAX){depth[j][i]=(float)t; colpi[id]++;} else depth[j][i]=0;
  }
}
// classe di un punto per lettura dell'immagine di profondita': 0 libero osservato, 1 superficie, 2 ombra,
// 3 raggio senza ritorno valido, 4 fuori campo
static inline int classe(double x,double y,double z){
  double v[3]={x-O[0],y-O[1],z-O[2]};
  double zc=v[0]*F[0]+v[1]*F[1]+v[2]*F[2]; if(zc<=0.01) return 4;
  double a=(v[0]*R[0]+v[1]*R[1]+v[2]*R[2])/zc,b=(v[0]*U[0]+v[1]*U[1]+v[2]*U[2])/zc;
  int i=(int)floor(a*fx+W/2.0),j=(int)floor(H/2.0-b*fy);
  if(i<0||i>=W||j<0||j>=H) return 4;
  float t=depth[j][i]; if(t==0) return 3;
  double r=sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
  if(r<t-EPS) return 0; if(r<=t+EPS) return 1; return 2;
}

// ---------------- mappa voxel: stato di promptMare §4 ----------------
typedef struct { float L; uint32_t tau; uint8_t q, nu; } Vox;   // nu: bit0 attraversato, bit1 colpito
static double hh; static int N3[3]; static Vox *dense;
#define TAB 4096
#define MAXB 2048
static uint32_t tkey[TAB]; static uint16_t tidx[TAB]; static Vox (*pool)[512]; static int nblk;
static uint32_t ck; static Vox *cp;
static inline Vox* vdense(int x,int y,int z){ return &dense[((size_t)z*N3[1]+y)*N3[0]+x]; }
static inline Vox* vhash(int x,int y,int z){
  uint32_t key=((uint32_t)(x>>3)|((uint32_t)(y>>3)<<8)|((uint32_t)(z>>3)<<16))+1;
  if(key!=ck){
    uint32_t hsh=(key*2654435761u)>>20;
    for(;;){ if(tkey[hsh]==key) break;
      if(tkey[hsh]==0){ if(nblk>=MAXB) return NULL; tkey[hsh]=key; tidx[hsh]=(uint16_t)nblk; memset(pool[nblk],0,sizeof pool[0]); nblk++; break; }
      hsh=(hsh+1)&(TAB-1); }
    ck=key; cp=pool[tidx[hsh]];
  }
  return &cp[(x&7)|((y&7)<<3)|((z&7)<<6)];
}
static long visite;
static inline __attribute__((always_inline)) void cast(int modo,const float*d,double tend,uint32_t fr){
  double p[3]={(O[0]-G0[0])/hh,(O[1]-G0[1])/hh,(O[2]-G0[2])/hh}; int ix[3],st[3]; double tm[3],td[3];
  for(int a=0;a<3;a++){ ix[a]=(int)floor(p[a]); if(ix[a]>=N3[a])ix[a]=N3[a]-1;
    if(d[a]>0){st[a]=1;tm[a]=((ix[a]+1)-p[a])*hh/d[a];td[a]=hh/d[a];}
    else if(d[a]<0){st[a]=-1;tm[a]=(p[a]-ix[a])*hh/(-d[a]);td[a]=hh/(-d[a]);}
    else {st[a]=0;tm[a]=1e30;td[a]=1e30;} }
  for(;;){
    int a=(tm[0]<tm[1])?((tm[0]<tm[2])?0:2):((tm[1]<tm[2])?1:2);
    Vox*v=modo?vhash(ix[0],ix[1],ix[2]):vdense(ix[0],ix[1],ix[2]); visite++;
    if(tm[a]>=tend){ if(v){ v->L+=0.85f; if(v->L>3.5f)v->L=3.5f; v->tau=fr; v->nu|=2; } return; }
    if(v){ v->L-=0.4f; if(v->L<-2.0f)v->L=-2.0f; v->tau=fr; v->nu|=1; }
    ix[a]+=st[a]; if(ix[a]<0||ix[a]>=N3[a]) return; tm[a]+=td[a];
  }
}
static void integra_denso(int passo,uint32_t fr){ for(int j=0;j<H;j+=passo)for(int i=0;i<W;i+=passo){ float t=depth[j][i]; if(t!=0) cast(0,dirs[j][i],t,fr);} }
static void integra_hash(int passo,uint32_t fr){ for(int j=0;j<H;j+=passo)for(int i=0;i<W;i+=passo){ float t=depth[j][i]; if(t!=0) cast(1,dirs[j][i],t,fr);} }
static void griglia(double h){ hh=h; N3[0]=(int)lround(4/h);N3[1]=(int)lround(6/h);N3[2]=(int)lround(3/h);
  free(dense); dense=calloc((size_t)N3[0]*N3[1]*N3[2],sizeof(Vox)); }
static void azzera_hash(void){ memset(tkey,0,sizeof tkey); nblk=0; ck=0; cp=NULL; }
static int materia(int x,int y,int z){ double lo[3]={G0[0]+x*hh,G0[1]+y*hh,G0[2]+z*hh};
  for(int b=0;b<nbox;b++){ int ok=1; for(int k=0;k<3;k++) if(!(lo[k]<boxes[b].hi[k]-1e-9&&lo[k]+hh>boxes[b].lo[k]+1e-9)) ok=0; if(ok) return 1; } return 0; }
static int dentro(double x,double y,double z){ double p[3]={x,y,z};
  for(int b=0;b<nbox;b++){ int ok=1; for(int k=0;k<3;k++) if(p[k]<boxes[b].lo[k]||p[k]>boxes[b].hi[k]) ok=0; if(ok) return 1; } return 0; }
static int cmpd(const void*a,const void*b){ double x=*(double*)a,y=*(double*)b; return (x>y)-(x<y); }

static void analisi_voxel(double h,const char*nome){
  griglia(h); integra_denso(1,1);
  long nv=(long)N3[0]*N3[1]*N3[2],occ=0,lib=0,toc=0,misti=0,magg=0,libmat=0,libsost=0,libB=0,libBmat=0,libC=0,libCmat=0,lomb=0,lomb2=0,lfc=0,lnv=0;
  int nb[3]={(N3[0]+7)/8,(N3[1]+7)/8,(N3[2]+7)/8}; long NB=(long)nb[0]*nb[1]*nb[2];
  char*bt=calloc(NB,1),*bo=calloc(NB,1);
  for(int z=0;z<N3[2];z++)for(int y=0;y<N3[1];y++)for(int x=0;x<N3[0];x++){
    Vox*v=vdense(x,y,z); long bi=((long)(z>>3)*nb[1]+(y>>3))*nb[0]+(x>>3);
    if(v->nu){toc++;bt[bi]=1;} if(v->nu&2){occ++;bo[bi]=1;}
    int cc=classe(G0[0]+(x+.5)*h,G0[1]+(y+.5)*h,G0[2]+(z+.5)*h); int m=materia(x,y,z);
    int nf=0,nin=0,nom=0,nfc=0,nnv=0; for(int c=0;c<4;c++)for(int b=0;b<4;b++)for(int a=0;a<4;a++){
      double px=G0[0]+(x+(a+.5)/4)*h,py=G0[1]+(y+(b+.5)/4)*h,pz=G0[2]+(z+(c+.5)/4)*h; int k=classe(px,py,pz); if(k==0)nf++; if(k==2)nom++; if(k==4)nfc++; if(k==3)nnv++; if(dentro(px,py,pz))nin++; }
    if(cc==0){libC++; if(m)libCmat++;}
    if(nf==64){libB++; if(m)libBmat++;}
    if((v->nu&1)&&!(v->nu&2)){ lib++; if(nf<64)misti++; if(nf<32)magg++; if(m)libmat++; if(nin>=16)libsost++; if(nom)lomb++; if(nom>=32)lomb2++; if(nfc)lfc++; if(nnv)lnv++; }
  }
  long nbt=0,nbo=0; for(long i=0;i<NB;i++){nbt+=bt[i];nbo+=bo[i];}
  printf("[%s] h=%.2f m: voxel %ld (%d x %d x %d); denso %zu B/voxel = %.0f kB (a 1 B/voxel: %.0f kB)\n",nome,h,nv,N3[0],N3[1],N3[2],sizeof(Vox),nv*sizeof(Vox)/1e3,nv/1e3);
  printf("   toccati %ld (%.1f %%), colpiti %ld (%.2f %%), 'libero' da raggi %ld\n",toc,100.0*toc/nv,occ,100.0*occ/nv,lib);
  printf("   blocchi 8^3: totali %ld; con libero memorizzato %ld (%.1f %%) = %.0f kB (+%.0f kB tabella); solo occupato %ld (%.1f %%) = %.0f kB\n",
    NB,nbt,100.0*nbt/NB,nbt*512.0*sizeof(Vox)/1e3,TAB*6/1e3,nbo,100.0*nbo/NB,nbo*512.0*sizeof(Vox)/1e3);
  printf("   P3 'libero' da raggi: con >=1 sottopunto su 64 non osservato-libero %ld (%.1f %%); con >=33 su 64 %ld (%.1f %%); che intersecano materia %ld (%.3f %%); con >=16/64 dentro materia %ld\n",
    misti,100.0*misti/lib,magg,100.0*magg/lib,libmat,100.0*libmat/lib,libsost);
  printf("   di cui: con >=1 sottopunto IN OMBRA %ld (%.1f %%), con >=32 in ombra %ld; con >=1 fuori campo %ld; con >=1 su raggio senza ritorno valido %ld\n",lomb,100.0*lomb/lib,lomb2,lfc,lnv);
  printf("   lettura immagine: 'libero' se il CENTRO e' osservato-libero %ld (con materia %ld); se TUTTI i 64 sottopunti %ld (con materia %ld)\n",libC,libCmat,libB,libBmat);
  free(bt);free(bo);
}
static void posa(double h){
  griglia(h); render(0); integra_denso(1,1); long nv=(long)N3[0]*N3[1]*N3[2]; uint8_t*A=malloc(nv); for(long i=0;i<nv;i++)A[i]=dense[i].nu;
  double ds[5]={0,0.1,0.5,1,2};
  for(int k=0;k<5;k++){ griglia(h); render(ds[k]); integra_denso(1,1); long lm=0,ls=0,ab=0;
    for(int z=0;z<N3[2];z++)for(int y=0;y<N3[1];y++)for(int x=0;x<N3[0];x++){ long i=((long)z*N3[1]+y)*N3[0]+x; Vox*v=&dense[i];
      if((v->nu&1)&&!(v->nu&2)){ if(materia(x,y,z)){lm++; int nin=0; for(int c=0;c<4;c++)for(int b=0;b<4;b++)for(int a=0;a<4;a++) if(dentro(G0[0]+(x+(a+.5)/4)*h,G0[1]+(y+(b+.5)/4)*h,G0[2]+(z+(c+.5)/4)*h))nin++; if(nin>=16)ls++;}
        if(A[i]&2)ab++; } }
    printf("   P5 h=%.2f delta=%.1f gradi: 'libero' con materia %ld; con >=16/64 dentro materia %ld; colpiti al fotogramma 1 che ora ricevono solo 'libero' %ld\n",h,ds[k],lm,ls,ab); }
  free(A); render(0);
}
#define NA 100
static int gsuolo[NA][30],gocc[NA][30];
static void nucleo(const char*nome){
  memset(gsuolo,0,sizeof gsuolo);memset(gocc,0,sizeof gocc);
  for(int j=0;j<H;j++)for(int i=0;i<W;i++){ float t=depth[j][i]; if(t==0)continue; double x=O[0]+t*dirs[j][i][0],y=O[1]+t*dirs[j][i][1],z=O[2]+t*dirs[j][i][2];
    int ia=(int)floor(atan2(x,y)*180/PI+50),ir=(int)floor(hypot(x,y)/0.1); if(ia<0||ia>=NA||ir>=30)continue;
    if(z<0.07)gsuolo[ia][ir]++; else if(z<=2.0)gocc[ia][ir]++; }
  long nlib=0,cat[5]={0}; double som=0,mn=2,sr[30]={0}; long nr[30]={0}; long ombravista=0,ombra=0;
  for(int ia=0;ia<NA;ia++){ int primo=99; for(int ir=0;ir<30;ir++) if(gocc[ia][ir]){primo=ir;break;}
    for(int ir=13;ir<30;ir++){
      if(ir>primo){ ombra++; if(gsuolo[ia][ir]&&!gocc[ia][ir]) ombravista++; continue; }
      if(!(gsuolo[ia][ir]&&!gocc[ia][ir])) continue;
      double az=(ia+0.5-50)*PI/180,r=(ir+0.5)*0.1,x=r*sin(az),y=r*cos(az); int nf=0,n=0;
      for(int q=0;q<194;q++){ int c=classe(x,y,0.07+0.01*q+0.005); cat[c]++; if(c==0)nf++; n++; }
      double f=(double)nf/n; som+=f; if(f<mn)mn=f; sr[ir]+=f; nr[ir]++; nlib++; } }
  printf("[%s] nucleo: celle 'libero' fra 1,3 e 3 m: %ld; quota della colonna 0,07-2,0 m osservata-libera: media %.1f %%, minimo %.1f %%\n",nome,nlib,100*som/nlib,100*mn);
  printf("   per anello: 1,3 m %.1f %% | 2,0 m %.1f %% | 2,9 m %.1f %%;  campioni: libero %ld, superficie %ld, ombra %ld, senza ritorno valido %ld, fuori campo %ld\n",
    100*sr[13]/nr[13],100*sr[20]/nr[20],100*sr[29]/nr[29],cat[0],cat[1],cat[2],cat[3],cat[4]);
  printf("   celle che il nucleo da' 'in ombra' (oltre il primo ritorno) fra 1,3 e 3 m: %ld; di queste con il suolo visto in questo fotogramma: %ld\n",ombra,ombravista);
}
static void barra_e_scatola(void){
  for(int b=0;b<nbox;b++) printf("   pixel che colpiscono '%s': %ld\n",boxes[b].nome,colpi[b]);
  double x=-0.8,y=1.52; int ia=(int)floor(atan2(x,y)*180/PI+50),ir=(int)floor(hypot(x,y)/0.1); int primo=99; for(int k=0;k<30;k++) if(gocc[ia][k]){primo=k;break;}
  printf("   cella sotto la barra (az %d gradi, anello %d): suolo visto %d pixel, ritorni 0,07-2 m %d, primo ritorno sull'azimut all'anello %d -> nucleo: %s; classe 3D a quota 1,80 m: %d (4 = fuori campo); a quota 1,00 m: %d\n",
    ia-50,ir,gsuolo[ia][ir],gocc[ia][ir],primo,(gsuolo[ia][ir]&&!gocc[ia][ir]&&ir<=primo)?"LIBERO":"non libero",classe(x,y,1.80),classe(x,y,1.00));
  x=1.15;y=1.58; ia=(int)floor(atan2(x,y)*180/PI+50); printf("   azimut della scatola bassa (%d gradi), anelli 12..29: ",ia-50);
  for(int k=12;k<30;k++) printf("%c",gocc[ia][k]?'O':(gsuolo[ia][k]?'s':'.')); printf("   (O ritorno 0,07-2 m; s suolo visto; . niente)\n");
}
static void tempi(void){
  const char*ns[2]={"demo","peggiore"}; int st[2]={0,2}; double hs[2]={0.10,0.05}; int ps[2]={1,2}; static double t[60];
  pool=malloc(sizeof(Vox[512])*MAXB);
  for(int s=0;s<2;s++){ scena(st[s]); render(0);
    for(int a=0;a<2;a++)for(int b=0;b<2;b++)for(int m=0;m<2;m++){
      griglia(hs[a]); azzera_hash(); visite=0;
      for(int r=0;r<40;r++){ double t0=now_ms(); if(m)integra_hash(ps[b],r+1); else integra_denso(ps[b],r+1); t[r]=now_ms()-t0; }
      double primo=t[0],som=0; for(int r=0;r<40;r++)som+=t[r]; qsort(t,40,sizeof(double),cmpd);
      printf("T scena=%-8s h=%.2f raggi=%6d %-5s: media %7.2f ms | mediana %7.2f | p95 %7.2f | max %7.2f | primo fotogramma %7.2f | visite voxel/fotogramma %ld | blocchi %d | memoria %.0f kB\n",
        ns[s],hs[a],(W/ps[b])*(H/ps[b]),m?"hash":"denso",som/40,t[20],t[37],t[39],primo,visite/40,m?nblk:0,
        m?(nblk*512.0*sizeof(Vox)+TAB*6)/1e3:(double)N3[0]*N3[1]*N3[2]*sizeof(Vox)/1e3);
    } }
  // P6: lettura per fasce di quota sulla griglia polare, senza mappa
  scena(0); render(0); long acc[5]={0}; double t0=now_ms(); int rip=500;
  for(int r=0;r<rip;r++) for(int ia=7;ia<94;ia++)for(int ir=12;ir<30;ir++){ double az=(ia+0.5-50)*PI/180,rr=(ir+0.5)*0.1,x=rr*sin(az),y=rr*cos(az);
      for(int q=0;q<39;q++) acc[classe(x,y,0.07+0.05*q+0.025)]++; }
  double dt=(now_ms()-t0)/rip; printf("P6 lettura polare a fasce (87 x 18 x 39 = %d letture): %.3f ms a fotogramma; classi: libero %ld, superficie %ld, ombra %ld, senza ritorno %ld, fuori campo %ld; memoria: immagine %d x %d x 4 B = %.0f kB\n",
    87*18*39,dt,acc[0]/rip,acc[1]/rip,acc[2]/rip,acc[3]/rip,acc[4]/rip,W,H,W*H*4/1e3);
  // costo del solo passaggio sui pixel (retroproiezione, come nel nucleo)
  t0=now_ms(); double chk=0; for(int r=0;r<200;r++){ render(0); chk+=depth[H/2][W/2]; } printf("   (per confronto: generare la scena sintetica costa %.2f ms a fotogramma: non entra nei tempi sopra) %g\n",(now_ms()-t0)/200,chk>0?1.0:0.0);
}
int main(int argc,char**argv){
  camera(); printf("sizeof(Vox)=%zu byte; raggi %d x %d; ritorno valido %.1f-%.1f m; EPS %.2f m\n",sizeof(Vox),W,H,RMIN,RMAX,EPS);
  if(argc>1&&!strcmp(argv[1],"tempi")){ tempi(); return 0; }
  scena(0); render(0); long val=0; for(int j=0;j<H;j++)for(int i=0;i<W;i++) if(depth[j][i]!=0)val++;
  printf("scena demo con parete: pixel validi %ld su %d (%.1f %%)\n",val,W*H,100.0*val/(W*H));
  analisi_voxel(0.10,"demo"); analisi_voxel(0.05,"demo");
  nucleo("demo con parete"); barra_e_scatola();
  posa(0.10); posa(0.05);
  scena(2); render(0); analisi_voxel(0.10,"peggiore"); analisi_voxel(0.05,"peggiore");
  scena(1); render(0); val=0; for(int j=0;j<H;j++)for(int i=0;i<W;i++) if(depth[j][i]!=0)val++;
  printf("scena demo SENZA parete: pixel validi %ld su %d (%.1f %%)\n",val,W*H,100.0*val/(W*H));
  nucleo("demo senza parete"); analisi_voxel(0.05,"demo senza parete");
  scena(3); render(0); nucleo("demo con parete a 4 m [aggiunta dopo]");
  return 0;
}
