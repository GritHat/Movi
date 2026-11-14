/* fasce.c — nuvole-punti-f9, strategia S10.
 * Confronto fra: mappa polare a una fascia (nucleo, due letture), mappa a tre fasce di quota
 * (lettera della preproposta e versione corretta), griglia voxel a 10 cm (cartesiana e cilindrica).
 * Camera di profondita' simulata (pinhole 87x58 gradi, 640x480), ferma. Nessun dato esterno.
 * Compilare: gcc -O2 -o fasce fasce.c -lm      Lanciare: timeout 120 ./fasce
 * Semi: 20261114 (solo nel braccio con rumore).
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define W 640
#define H 480
#define NPIX (W*H)
#define NAZ 87
#define NR 30
#define DR 0.1
#define ZTOP 2.0
#define NF 80            /* strati fini della verita', 2,5 cm */
#define DZF 0.025
#define MAXS 20
#define R0 3             /* prima corona del dominio dei conti: 0,3 m */
#define HFOV 87.0
#define VFOV 58.0
#define RAD (M_PI/180.0)

enum { FREE=0, OCC=1, SHADOW=2, UNK=3 };
enum { BMA=0, BM=1, PM=2 };
static const char *PNAME[3]={"BMA","BM","M"};
static const double PZ0[3]={0.0,0.0,0.6}, PZ1[3]={2.0,1.6,1.6};

typedef struct { double x0,x1,y0,y1,z0,z1; } Box;

/* ---- scena e sensore ---- */
static double hs, tilt; static int walls; static Box box[8]; static int nbox;
static double XW=4.5, YW=4.5;
static int KOCC=1, KG=1; static double FTOL=0.0; static int MARG=0;

/* ---- tabella dei raggi ---- */
static float rdx[NPIX], rdy[NPIX], rdz[NPIX], rch[NPIX], rsl[NPIX], rcz[NPIX];
static int16_t raz[NPIX];
static float dep[NPIX];      /* distanza lungo il raggio; 0 = non valido */
static float dep0[NPIX];     /* senza rumore */
static int8_t hid[NPIX];     /* -1 suolo, -2 parete, -3 niente, k scatola */

static void make_rays(void){
  double fx=(W/2.0)/tan(HFOV/2*RAD), fy=(H/2.0)/tan(VFOV/2*RAD);
  double ct=cos(tilt*RAD), st=sin(tilt*RAD);
  for(int v=0;v<H;v++) for(int u=0;u<W;u++){
    double a=(u+0.5-W/2.0)/fx, b=(v+0.5-H/2.0)/fy;
    /* avanti=(ct,0,-st); destra=(0,-1,0); giu'=(-st,0,-ct) */
    double x=ct - b*st, y=-a, z=-st - b*ct;
    double n=sqrt(x*x+y*y+z*z); x/=n; y/=n; z/=n;
    int i=v*W+u; rdx[i]=x; rdy[i]=y; rdz[i]=z;
    double ch=sqrt(x*x+y*y); rch[i]=ch; rsl[i]=z/ch; rcz[i]=1.0/n;
    double az=atan2(y,x)/RAD; int ab=(int)floor(az+NAZ/2.0);
    raz[i]=(ab>=0&&ab<NAZ)?ab:-1;
  }
}
static void cast(void){
  for(int i=0;i<NPIX;i++){
    double dx=rdx[i],dy=rdy[i],dz=rdz[i]; double tb=1e30; int id=-3;
    if(dz<0){ double t=hs/(-dz); if(t<tb){tb=t;id=-1;} }
    if(walls){ double t=XW/dx; if(t<tb){tb=t;id=-2;} if(fabs(dy)>1e-9){ t=YW/fabs(dy); if(t<tb){tb=t;id=-2;} } }
    for(int k=0;k<nbox;k++){ Box*B=&box[k]; double t0=0,t1=1e30,a,b2;
      a=(B->x0)/dx; b2=(B->x1)/dx; if(a>b2){double q=a;a=b2;b2=q;} if(a>t0)t0=a; if(b2<t1)t1=b2;
      if(fabs(dy)<1e-12){ if(0<B->y0||0>B->y1) continue; } else { a=(B->y0)/dy; b2=(B->y1)/dy; if(a>b2){double q=a;a=b2;b2=q;} if(a>t0)t0=a; if(b2<t1)t1=b2; }
      if(fabs(dz)<1e-12){ if(hs<B->z0||hs>B->z1) continue; } else { a=(B->z0-hs)/dz; b2=(B->z1-hs)/dz; if(a>b2){double q=a;a=b2;b2=q;} if(a>t0)t0=a; if(b2<t1)t1=b2; }
      if(t0<=t1 && t0>1e-6 && t0<tb){ tb=t0; id=k; }
    }
    if(id==-3){ dep0[i]=0; } else dep0[i]=(float)tb;
    hid[i]=id;
  }
  memcpy(dep,dep0,sizeof dep);
}
/* rumore: sigma(Z)=0.00375 Z^2 (1,5 cm a 2 m), 2 % di pixel non validi */
static uint64_t rs=20261114ULL;
static double urand(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*(1.0/9007199254740992.0); }
static double grand(void){ double u=urand()+1e-12, v=urand(); return sqrt(-2*log(u))*cos(2*M_PI*v); }
static void add_noise(void){
  for(int i=0;i<NPIX;i++){ if(dep0[i]<=0){dep[i]=0;continue;}
    if(urand()<0.02){dep[i]=0;continue;}
    double Z=dep0[i]*rcz[i]; double Z2=Z+0.00375*Z*Z*grand(); if(Z2<0.05)Z2=0.05; dep[i]=(float)(dep0[i]*Z2/Z); }
}

/* ---- verita' fine ---- */
static uint8_t tsolid[NAZ][NR][NF], tvis[NAZ][NR][NF];
static int inbox(double x,double y,double z){ for(int k=0;k<nbox;k++){Box*B=&box[k]; if(x>=B->x0&&x<=B->x1&&y>=B->y0&&y<=B->y1&&z>=B->z0&&z<=B->z1) return k+1;} return 0; }
static void truth(void){
  memset(tsolid,0,sizeof tsolid); memset(tvis,0,sizeof tvis);
  for(int a=0;a<NAZ;a++) for(int r=0;r<NR;r++) for(int f=0;f<NF;f++){
    double z=(f+0.5)*DZF; int s=0;
    for(int i=0;i<3&&!s;i++) for(int j=0;j<3&&!s;j++){
      double az=(a-NAZ/2.0+(2*i+1)/6.0)*RAD, rho=(r+(2*j+1)/6.0)*DR;
      s=inbox(rho*cos(az),rho*sin(az),z);
    }
    tsolid[a][r][f]=s;
  }
  for(int i=0;i<NPIX;i++){ int a=raz[i]; if(a<0||dep0[i]<=0) continue;
    double rh=dep0[i]*rch[i]-0.005; if(rh>NR*DR) rh=NR*DR;
    for(double rho=0.005;rho<rh;rho+=0.01){ double z=hs+rho*rsl[i]; if(z<0||z>=ZTOP) continue; tvis[a][(int)(rho/DR)][(int)(z/DZF)]=1; }
  }
}

/* ---- mappa a una fascia (nucleo) ---- */
typedef struct { uint16_t g[NAZ][NR], o[NAZ][NR]; uint8_t st[NAZ][NR]; } NMap;
static void nmap_build(NMap*m,int wedge){
  memset(m->g,0,sizeof m->g); memset(m->o,0,sizeof m->o);
  for(int i=0;i<NPIX;i++){ int a=raz[i]; float t=dep[i]; if(a<0||t<=0) continue;
    float rho=t*rch[i], z=(float)hs+t*rdz[i]; int r=(int)(rho*(1.0f/DR)); if(r>=NR) continue;
    if(z<=0.07f){ if(z>=-0.07f) m->g[a][r]++; } else if(z<=2.0f) m->o[a][r]++;
  }
  for(int a=0;a<NAZ;a++){ int sh=0;
    for(int r=0;r<NR;r++){ int s;
      if(wedge){ if(sh) s=SHADOW; else if(m->o[a][r]>=KOCC){ s=OCC; sh=1; } else if(m->g[a][r]>=KG) s=FREE; else s=UNK; }
      else { if(m->o[a][r]>=KOCC){ s=OCC; sh=1; } else if(m->g[a][r]>=KG) s=FREE; else s=sh?SHADOW:UNK; }
      m->st[a][r]=s; } }
}

/* ---- mappa a fasce (generica: 3 fasce, oppure 20 strati = voxel cilindrico) ---- */
typedef struct {
  int nb; double zb[MAXS+1]; double zg; int strict; int need_ground;
  uint16_t hit[NAZ][NR][MAXS], trav[NAZ][NR][MAXS], blk[NAZ][NR][MAXS], g[NAZ][NR];
  float zmin[NAZ][NR][MAXS], zmax[NAZ][NR][MAXS];
  uint8_t st[NAZ][NR][MAXS], gst[NAZ][NR];
  int8_t lutlo[202], luthi[202];
} SMap;
static void smap_init(SMap*m,int nb,const double*zb,double zg,int strict,int need_ground){
  m->nb=nb; for(int i=0;i<=nb;i++) m->zb[i]=zb[i]; m->zg=zg; m->strict=strict; m->need_ground=need_ground;
  for(int c=0;c<=201;c++){ double z=c*0.01; int lo=nb, hi=-1;
    for(int s=0;s<nb;s++){ if(zb[s+1]>z+1e-9){ lo=s; break; } }
    for(int s=nb-1;s>=0;s--){ if(zb[s]<z+0.01-1e-9){ hi=s; break; } }
    m->lutlo[c]=lo; m->luthi[c]=hi; }
}
static inline void mark(SMap*m,int a,int r,float lo,float hi,int isblk){
  if(hi<=m->zb[0]||lo>=m->zb[m->nb]) return;
  int cl=(int)(lo*100.0f); if(cl<0)cl=0; if(cl>200)cl=200; int chh=(int)(hi*100.0f); if(chh<0)chh=0; if(chh>200)chh=200;
  int s1=m->lutlo[cl], s2=m->luthi[chh];
  for(int s=s1;s<=s2;s++){ float b0=(float)m->zb[s], b1=(float)m->zb[s+1];
    if(hi<=b0+1e-3f||lo>=b1-1e-3f) continue;
    if(isblk){ m->blk[a][r][s]++; }
    else { m->trav[a][r][s]++; float l=lo>b0?lo:b0, h=hi<b1?hi:b1; if(l<m->zmin[a][r][s]) m->zmin[a][r][s]=l; if(h>m->zmax[a][r][s]) m->zmax[a][r][s]=h; } }
}
static void smap_build(SMap*m){
  memset(m->hit,0,sizeof m->hit); memset(m->trav,0,sizeof m->trav); memset(m->blk,0,sizeof m->blk); memset(m->g,0,sizeof m->g);
  for(int a=0;a<NAZ;a++) for(int r=0;r<NR;r++) for(int s=0;s<m->nb;s++){ m->zmin[a][r][s]=1e9f; m->zmax[a][r][s]=-1e9f; }
  float fhs=(float)hs;
  for(int i=0;i<NPIX;i++){ int a=raz[i]; float t=dep[i]; if(a<0||t<=0) continue;
    float tn=t+0.002f; float rho=tn*rch[i], z=fhs+tn*rdz[i], sl=rsl[i]; int rh=(int)(rho*(1.0f/DR)); int rend=(rh<NR?rh:NR)-MARG;
    float za=fhs;
    for(int r=0;r<rend;r++){ float zb2=fhs+(r+1)*(float)DR*sl; if(za<zb2) mark(m,a,r,za,zb2,0); else mark(m,a,r,zb2,za,0); za=zb2; }
    if(rh<NR){
      if(z<=(float)m->zg){ m->g[a][rh]++; }
      else if(z<(float)ZTOP){ int c=(int)(z*100.0f); int s=m->lutlo[c>200?200:c]; if(s<m->nb && z>=m->zb[s]) m->hit[a][rh][s]++;
        za=fhs+(rh+1)*(float)DR*sl;
        for(int r=rh+1;r<NR;r++){ float zb2=fhs+(r+1)*(float)DR*sl; float lo=za<zb2?za:zb2, hi=za<zb2?zb2:za; if(hi<0) break; mark(m,a,r,lo,hi,1); za=zb2; } }
    }
  }
  for(int a=0;a<NAZ;a++) for(int r=0;r<NR;r++){
    m->gst[a][r]=(m->g[a][r]>=KG);
    for(int s=0;s<m->nb;s++){ int st; double b0=m->zb[s], b1=m->zb[s+1]; int tr=m->trav[a][r][s], bk=m->blk[a][r][s];
      if(m->hit[a][r][s]>=KOCC) st=OCC;
      else if(b1<=0.1001){ st = m->gst[a][r]?FREE:(bk>0?SHADOW:UNK); }      /* strato del suolo */
      else if(!m->strict){ st = tr>=1?FREE:(bk>0?SHADOW:UNK); }
      else { double tol=0.05; if(tol>0.25*(b1-b0)) tol=0.25*(b1-b0);
        int cover = tr>=1 && m->zmin[a][r][s]<=b0+tol && m->zmax[a][r][s]>=b1-tol && bk<=FTOL*(tr+bk);
        st = cover?FREE:(bk>0?SHADOW:UNK); }
      m->st[a][r][s]=st; } }
}
static int smap_state3d(SMap*m,int a,int r,double z){
  if(z<m->zb[0]) return m->gst[a][r]?FREE:UNK;
  for(int s=0;s<m->nb;s++) if(z<m->zb[s+1]) return m->st[a][r][s];
  return UNK;
}
/* classe della cella per profilo: FREE / OCC / SHADOW(=non libero, non occupato) */
static int smap_cell(SMap*m,int a,int r,int p){
  int occ=0, allfree=1;
  for(int s=0;s<m->nb;s++){ if(m->zb[s+1]<=PZ0[p]+1e-9||m->zb[s]>=PZ1[p]-1e-9) continue;
    if(m->st[a][r][s]==OCC) occ=1; else if(m->st[a][r][s]!=FREE) allfree=0; }
  if(occ) return OCC;
  if(m->need_ground && p!=PM && !m->gst[a][r]) allfree=0;
  return allfree?FREE:SHADOW;
}

/* ---- voxel cartesiano denso a 10 cm ---- */
#define VX 30
#define VY 60
#define VZ 20
typedef struct { uint16_t hit[VX][VY][VZ], trav[VX][VY][VZ], blk[VX][VY][VZ], g[VX][VY]; } VMap;
static void vmap_build(VMap*m){
  memset(m,0,sizeof *m);
  const float inv=10.0f; float oy=3.0f;
  for(int i=0;i<NPIX;i++){ float t=dep[i]; if(t<=0) continue; float tn=t+0.002f;
    float dx=rdx[i],dy=rdy[i],dz=rdz[i];
    /* origine (0,0,hs): x=0 e' il bordo della griglia */
    int ix=0, iy=(int)((0+oy)*inv), iz=(int)((float)hs*inv);
    int sx=1, sy=dy>0?1:-1, sz=dz>0?1:-1;
    float tdx=0.1f/dx, tdy=dy!=0?0.1f/fabsf(dy):1e30f, tdz=dz!=0?0.1f/fabsf(dz):1e30f;
    float tmx=tdx;
    float fy=(0+oy)*inv-iy, fz=(float)hs*inv-iz;
    float tmy=dy>0?(1-fy)*tdy:(fy>0?fy*tdy:tdy); if(dy==0) tmy=1e30f;
    float tmz=dz>0?(1-fz)*tdz:(fz>0?fz*tdz:tdz); if(dz==0) tmz=1e30f;
    if(dy<0&&fy==0){ iy--; } if(dz<0&&fz==0){ iz--; }
    int after=0; (void)sx;
    for(;;){
      if(iz<0){ if(!after && ix<VX && iy>=0 && iy<VY) m->g[ix][iy]++; break; }
      if(ix>=VX||iy<0||iy>=VY) break;
      float tex=tmx<tmy?(tmx<tmz?tmx:tmz):(tmy<tmz?tmy:tmz);   /* uscita dal voxel */
      if(iz<VZ){
        if(after) m->blk[ix][iy][iz]++;
        else if(tex<tn) m->trav[ix][iy][iz]++;
        else { float z=(float)hs+tn*dz; if(z<=0.07f) { m->g[ix][iy]++; break; } m->hit[ix][iy][iz]++; after=1; }
      } else if(!after && tex>=tn) break;   /* ritorno sopra 2 m */
      if(tmx<=tmy&&tmx<=tmz){ ix++; tmx+=tdx; } else if(tmy<=tmz){ iy+=sy; tmy+=tdy; } else { iz+=sz; tmz+=tdz; }
    }
  }
}
static int vmap_state(VMap*m,int ix,int iy,int iz){
  if(ix<0||ix>=VX||iy<0||iy>=VY||iz<0||iz>=VZ) return UNK;
  if(m->hit[ix][iy][iz]>=KOCC) return OCC;
  if(iz==0) return m->g[ix][iy]>=KG?FREE:(m->blk[ix][iy][iz]>0?SHADOW:UNK);
  int tr=m->trav[ix][iy][iz], bk=m->blk[ix][iy][iz];
  if(tr>=1 && bk<=FTOL*(tr+bk)) return FREE;
  return bk>0?SHADOW:UNK;
}
static int vmap_state3d(VMap*m,double x,double y,double z){ return vmap_state(m,(int)floor(x*10),(int)floor((y+3.0)*10),(int)floor(z*10)); }
static int vmap_col(VMap*m,double x,double y,int p){
  int ix=(int)floor(x*10), iy=(int)floor((y+3.0)*10); int z0=(int)floor(PZ0[p]*10+1e-6), z1=(int)floor(PZ1[p]*10-1e-6);
  int occ=0, allfree=1;
  for(int iz=z0;iz<=z1;iz++){ int s=vmap_state(m,ix,iy,iz); if(s==OCC) occ=1; else if(s!=FREE) allfree=0; }
  if(occ) return OCC; return allfree?FREE:SHADOW;
}
static int vmap_cell(VMap*m,int a,int r,int p){
  int occ=0, allfree=1;
  for(int i=0;i<3;i++) for(int j=0;j<3;j++){ double az=(a-NAZ/2.0+(2*i+1)/6.0)*RAD, rho=(r+(2*j+1)/6.0)*DR;
    int s=vmap_col(m,rho*cos(az),rho*sin(az),p); if(s==OCC) occ=1; else if(s!=FREE) allfree=0; }
  if(occ) return OCC; return allfree?FREE:SHADOW;
}

/* ---- le mappe ---- */
#define NM 7
static const char *MNAME[NM]={"N-cuneo","N-cella","F3-lett","F3-lett+suolo","F3-corr","V10","V10p"};
static NMap nw, nc; static SMap f3l, f3ls, f3c, v10p; static VMap v10;
static void build_all(void){
  static const double zl[4]={0.15,0.60,1.60,2.00}, zc[4]={0.07,0.60,1.60,2.00};
  double zv[21]; for(int i=0;i<=20;i++) zv[i]=i*0.1;
  nmap_build(&nw,1); nmap_build(&nc,0);
  smap_init(&f3l,3,zl,0.15,0,0); smap_build(&f3l);
  smap_init(&f3ls,3,zl,0.15,0,1); smap_build(&f3ls);
  smap_init(&f3c,3,zc,0.07,1,1); smap_build(&f3c);
  smap_init(&v10p,20,zv,0.07,1,1); smap_build(&v10p);
  vmap_build(&v10);
}
static int state3d(int k,int a,int r,double z){
  double az=(a-NAZ/2.0+0.5)*RAD, rho=(r+0.5)*DR;
  switch(k){ case 0: return nw.st[a][r]; case 1: return nc.st[a][r];
    case 2: return smap_state3d(&f3l,a,r,z); case 3: return smap_state3d(&f3ls,a,r,z);
    case 4: return smap_state3d(&f3c,a,r,z); case 5: return vmap_state3d(&v10,rho*cos(az),rho*sin(az),z);
    default: return smap_state3d(&v10p,a,r,z); }
}
static int cellcls(int k,int a,int r,int p){
  int s;
  switch(k){ case 0: s=nw.st[a][r]; return s==UNK?SHADOW:s; case 1: s=nc.st[a][r]; return s==UNK?SHADOW:s;
    case 2: return smap_cell(&f3l,a,r,p); case 3: return smap_cell(&f3ls,a,r,p);
    case 4: return smap_cell(&f3c,a,r,p); case 5: return vmap_cell(&v10,a,r,p);
    default: return smap_cell(&v10p,a,r,p); }
}

static void report(const char*name,int target){
  build_all();
  printf("\n=== %s  (sensore %.2f m, inclinazione %.0f gradi, pareti %d, rumore %s) ===\n",name,hs,tilt,walls,MARG?"si":"no");
  long px[8]={0}; long pg=0,pw=0,pn=0; for(int i=0;i<NPIX;i++){ if(hid[i]>=0)px[hid[i]]++; else if(hid[i]==-1)pg++; else if(hid[i]==-2)pw++; else pn++; }
  printf("pixel: suolo %ld, pareti %ld, senza ritorno %ld", pg,pw,pn); for(int k=0;k<nbox;k++) printf(", scatola%d %ld",k,px[k]); printf("\n");
  /* volumi veri */
  double vs=0,vv=0,vh=0, carea=DR*RAD;
  double e[NM][4]; memset(e,0,sizeof e);     /* FREE&SOLID, FREE&HID, (SH|UNK)&VIS, OCC&VIS */
  for(int a=0;a<NAZ;a++) for(int r=R0;r<NR;r++) for(int f=0;f<NF;f++){
    double vol=(r+0.5)*DR*carea*DZF*1000.0; double z=(f+0.5)*DZF; int ts=tsolid[a][r][f], tv=tvis[a][r][f];
    if(ts) vs+=vol; else if(tv) vv+=vol; else vh+=vol;
    for(int k=0;k<NM;k++){ int s=state3d(k,a,r,z);
      if(s==FREE&&ts) e[k][0]+=vol; else if(s==FREE&&!tv) e[k][1]+=vol;
      else if((s==SHADOW||s==UNK)&&!ts&&tv) e[k][2]+=vol; else if(s==OCC&&!ts&&tv) e[k][3]+=vol; }
  }
  printf("volume vero nel dominio (litri): solido %.0f, vuoto visto %.0f, vuoto mai visto %.0f\n",vs,vv,vh);
  printf("%-14s | litri: libero-su-solido  libero-su-mai-visto  nascosto-a-torto  occupato-a-torto\n","mappa");
  for(int k=0;k<NM;k++) printf("%-14s | %17.1f %20.1f %17.1f %17.1f\n",MNAME[k],e[k][0],e[k][1],e[k][2],e[k][3]);
  /* aree per profilo */
  for(int p=0;p<3;p++){
    printf("profilo %-3s (quota %.2f-%.2f m) | m2: libero  di-cui-su-solido  di-cui-su-mai-visto | nascosto-con-colonna-vista-vuota | bersaglio: celle  libero occupato nascosto\n",PNAME[p],PZ0[p],PZ1[p]);
    for(int k=0;k<NM;k++){ double af=0,afs=0,afh=0,ah=0; int tc=0,tf=0,to=0,th=0;
      for(int a=0;a<NAZ;a++) for(int r=R0;r<NR;r++){ double ar=(r+0.5)*DR*carea;
        int f0=(int)(PZ0[p]/DZF+1e-6), f1=(int)(PZ1[p]/DZF-1e-6); int sol=0,hidn=0,tg=0;
        for(int f=f0;f<=f1;f++){ if(tsolid[a][r][f]) sol=1; else if(!tvis[a][r][f]) hidn=1; }
        for(int f=0;f<NF;f++) if(tsolid[a][r][f]==target+1) tg=1;
        int c=cellcls(k,a,r,p);
        if(c==FREE){ af+=ar; if(sol) afs+=ar; else if(hidn) afh+=ar; }
        if(c==SHADOW && !sol && !hidn) ah+=ar;
        if(tg){ tc++; if(c==FREE)tf++; else if(c==OCC)to++; else th++; } }
      printf("  %-14s | %7.3f %10.3f %14.3f | %10.3f | %5d %6d %6d %6d\n",MNAME[k],af,afs,afh,ah,tc,tf,to,th); }
  }
  /* suolo visto dichiarato non libero e non occupato (P7): strato fine 0 visto, colonna 0-2 m senza solido */
  printf("suolo visto e colonna senza solidi, ma cella dichiarata in ombra/non osservata nel profilo BM (m2):");
  for(int k=0;k<NM;k++){ double ah=0; for(int a=0;a<NAZ;a++) for(int r=R0;r<NR;r++){ int sol=0; for(int f=0;f<NF;f++) if(tsolid[a][r][f]) sol=1;
      if(!sol && tvis[a][r][0] && cellcls(k,a,r,BM)==SHADOW) ah+=(r+0.5)*DR*carea; }
    printf(" %s %.3f;",MNAME[k],ah); }
  printf("\n");
}
static void scene(double h,double t,int w){ hs=h; tilt=t; walls=w; nbox=0; }
static void addbox(double x0,double x1,double y0,double y1,double z0,double z1){ Box b={x0,x1,y0,y1,z0,z1}; box[nbox++]=b; }
static void go(const char*name,int target,int noisy){
  make_rays(); cast(); truth();
  if(noisy){ rs=20261114ULL; add_noise(); KOCC=3; KG=3; FTOL=0.10; MARG=1; } else { KOCC=1; KG=1; FTOL=0.0; MARG=0; }
  report(name,target);
}
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec*1e3+ts.tv_nsec*1e-6; }
static int cmpd(const void*a,const void*b){ double x=*(double*)a,y=*(double*)b; return x<y?-1:x>y; }
#define NREP 200
static void timeit(const char*lab,void(*fn)(void)){
  static double tt[NREP]; for(int i=0;i<NREP;i++){ double t0=now(); fn(); tt[i]=now()-t0; }
  qsort(tt,NREP,sizeof(double),cmpd);
  printf("  %-34s min %.3f  mediana %.3f  p95 %.3f  max %.3f ms\n",lab,tt[0],tt[NREP/2],tt[(int)(NREP*0.95)],tt[NREP-1]);
}
static void t_n(void){ nmap_build(&nw,1); }
static void t_f3(void){ smap_build(&f3c); }
static void t_f3l(void){ smap_build(&f3l); }
static void t_v10p(void){ smap_build(&v10p); }
static void t_v10(void){ vmap_build(&v10); }

int main(int argc,char**argv){
  int only_time = argc>1 && !strcmp(argv[1],"tempi");
  if(!only_time){
  /* P8: braccio che deve fallire/riuscire: sensore basso, la scatola della scena C deve vedersi */
  scene(0.3,0,1); addbox(0.80,0.95,-0.075,0.075,0,0.15); go("P8 controllo: scatola 15 cm a 0,8 m, sensore a 0,3 m orizzontale",0,0);
  /* C */
  scene(1.2,15,1); addbox(0.80,0.95,-0.075,0.075,0,0.15); go("C: scatola 15 cm a 0,8 m",0,0);
  scene(1.2,15,1); addbox(1.20,1.35,-0.075,0.075,0,0.15); go("C2: scatola 15 cm a 1,2 m",0,0);
  /* B */
  scene(1.2,15,1); addbox(2.0,2.1,-0.6,0.6,1.8,1.9); go("B: sbarra a quota 1,8-1,9 m, a 2,0 m",0,0);
  scene(1.2,15,1); addbox(2.6,2.7,-0.6,0.6,1.8,1.9); go("B2: sbarra a quota 1,8-1,9 m, a 2,6 m",0,0);
  /* A */
  scene(1.2,15,1); addbox(1.5,2.1,-0.4,0.4,0,1.0); addbox(2.45,2.75,-0.25,0.25,0,0.9); go("A1: cassa 1 m, persona accovacciata (0,9 m) dietro",1,0);
  scene(1.2,15,1); addbox(1.5,2.1,-0.4,0.4,0,1.0); addbox(2.45,2.75,-0.25,0.25,0,1.7); go("A2: cassa 1 m, persona in piedi (1,7 m) dietro",1,0);
  scene(1.2,15,1); addbox(1.5,2.1,-0.4,0.4,0,1.0); go("A0: cassa 1 m, nessuno dietro",0,0);
  /* D */
  scene(1.2,15,1); addbox(1.8,2.4,-0.5,0.5,0,0.10); go("D: gradino di 10 cm fra 1,8 e 2,4 m",0,0);
  /* E */
  scene(1.2,15,1); addbox(1.5,1.8,-0.3,0.3,0,0.30); go("E: scatola di 30 cm fra 1,5 e 1,8 m",0,0);
  /* T: tavolo (solo il piano) */
  scene(1.2,15,1); addbox(1.6,2.4,-0.5,0.5,0.70,0.75); go("T: piano di tavolo a 0,70-0,75 m fra 1,6 e 2,4 m",0,0);
  /* vuoto con e senza pareti (P9) */
  scene(1.2,15,1); go("V: scena vuota con pareti",-5,0);
  scene(1.2,15,0); go("V0: scena vuota senza pareti (nessun ritorno sopra l'orizzonte)",-5,0);
  /* rumore */
  scene(1.2,15,1); addbox(1.5,2.1,-0.4,0.4,0,1.0); addbox(2.45,2.75,-0.25,0.25,0,0.9); go("A1r: come A1, con rumore e 2 % di pixel non validi",1,1);
  scene(1.2,15,1); addbox(1.8,2.4,-0.5,0.5,0,0.10); go("Dr: come D, con rumore e 2 % di pixel non validi",0,1);
  }
  /* costo */
  scene(1.2,15,1); addbox(1.5,2.1,-0.4,0.4,0,1.0); addbox(2.45,2.75,-0.25,0.25,0,1.7); make_rays(); cast(); KOCC=1; KG=1; FTOL=0; MARG=0; build_all();
  printf("\n=== costo per fotogramma, scena A2, %dx%d, un filo, %d ripetizioni (dall'immagine di profondita' agli stati) ===\n",W,H,NREP);
  timeit("N (una fascia, nucleo)",t_n); timeit("F3-lett (tre fasce, regola larga)",t_f3l); timeit("F3-corr (tre fasce, regola stretta)",t_f3);
  timeit("V10p (voxel cilindrico, 20 strati)",t_v10p); timeit("V10 (voxel cartesiano, DDA)",t_v10);
  printf("memoria: N %zu B; F3 (una mappa a 3 fasce, campi usati) %zu B; V10p (20 strati) %zu B; V10 cartesiano %zu B; tabella dei raggi %zu B\n",
    sizeof(NMap), (size_t)NAZ*NR*(3*(2+2+2+4+4+1)+2+1), (size_t)NAZ*NR*(20*(2+2+2+4+4+1)+2+1), sizeof(VMap), (size_t)NPIX*(6*4+2));
  return 0;
}
