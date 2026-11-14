// p7.c — si include rovescia.c rinominando il suo main; misura l'inserimento dei soli punti d'arrivo.
#define main main_rovescia
#include "rovescia.c"
#undef main
typedef struct { uint8_t stato; uint8_t eta; } Occ;
int main(void){
  camera(); int st[2]={0,2}; const char*ns[2]={"demo","peggiore"}; static double t[200],t2[200];
  for(int s=0;s<2;s++){ scena(st[s]); render(0); double h=0.05; int n[3]={80,120,60}; Occ*g=calloc((size_t)n[0]*n[1]*n[2],sizeof(Occ));
    int *lista=malloc(sizeof(int)*n[0]*n[1]*n[2]); long nocc=0,visti=0;
    for(int r=0;r<200;r++){
      double t0=now_ms();
      for(int j=0;j<H;j++)for(int i=0;i<W;i++){ float d=depth[j][i]; if(d==0)continue;
        int x=(int)floor((O[0]+d*dirs[j][i][0]-G0[0])/h),y=(int)floor((O[1]+d*dirs[j][i][1]-G0[1])/h),z=(int)floor((O[2]+d*dirs[j][i][2]-G0[2])/h);
        if(x<0||x>=n[0]||y<0||y>=n[1]||z<0||z>=n[2])continue; size_t k=((size_t)z*n[1]+y)*n[0]+x;
        if(!g[k].stato){ g[k].stato=1; lista[nocc++]=(int)k; } g[k].eta=0; }
      t[r]=now_ms()-t0; t0=now_ms(); visti=0;
      for(long q=0;q<nocc;q++){ int k=lista[q]; int x=k%n[0],y=(k/n[0])%n[1],z=k/(n[0]*n[1]);
        if(classe(G0[0]+(x+.5)*h,G0[1]+(y+.5)*h,G0[2]+(z+.5)*h)==0) visti++; }
      t2[r]=now_ms()-t0; }
    qsort(t,200,sizeof(double),cmpd); qsort(t2,200,sizeof(double),cmpd);
    printf("P7 scena=%s h=0.05: inserimento dei punti d'arrivo: mediana %.3f ms | p95 %.3f | max %.3f ; voxel occupati %ld (%.0f kB a 2 B/voxel densi) ; controllo 'visto attraverso' su %ld voxel: mediana %.3f ms | max %.3f ; occupati con il centro visto attraverso: %ld\n",
      ns[s],t[100],t[190],t[199],nocc,n[0]*n[1]*n[2]*2/1e3,nocc,t2[100],t2[199],visti); free(g); free(lista); }
  return 0; }
