#define main main_rovescia
#include "rovescia.c"
#undef main
static void p8(const char*nome){
  memset(gsuolo,0,sizeof gsuolo);memset(gocc,0,sizeof gocc);
  for(int j=0;j<H;j++)for(int i=0;i<W;i++){ float t=depth[j][i]; if(t==0)continue; double x=O[0]+t*dirs[j][i][0],y=O[1]+t*dirs[j][i][1],z=O[2]+t*dirs[j][i][2];
    int ia=(int)floor(atan2(x,y)*180/PI+50),ir=(int)floor(hypot(x,y)/0.1); if(ia<0||ia>=NA||ir>=30)continue;
    if(z<0.07)gsuolo[ia][ir]++; else if(z<=2.0)gocc[ia][ir]++; }
  long nlib=0,piene15=0,piene10=0,pienetetto=0; double sh=0;
  for(int ia=0;ia<NA;ia++){ int primo=99; for(int ir=0;ir<30;ir++) if(gocc[ia][ir]){primo=ir;break;}
    for(int ir=13;ir<30;ir++){ if(ir>primo||!(gsuolo[ia][ir]&&!gocc[ia][ir])) continue;
      double az=(ia+0.5-50)*PI/180,r=(ir+0.5)*0.1,x=r*sin(az),y=r*cos(az); int q=0;
      while(q<193&&classe(x,y,0.07+0.01*q+0.005)==0)q++;   // quota fino a cui la colonna e' osservata-libera senza interruzioni
      double hq=0.07+0.01*q; sh+=hq; nlib++; if(hq>=1.5)piene15++; if(hq>=1.0)piene10++; if(hq>=1.2+0.2489*y-0.03)pienetetto++; } }
  printf("P8 [%s] celle 'libero' del nucleo %ld: colonna osservata-libera senza interruzioni fino a 1,5 m: %ld (%.1f %%); fino a 1,0 m: %ld (%.1f %%); fino al tetto del campo: %ld (%.1f %%); quota media raggiunta %.2f m\n",
    nome,nlib,piene15,100.0*piene15/nlib,piene10,100.0*piene10/nlib,pienetetto,100.0*pienetetto/nlib,sh/nlib);
}
static void p9(const char*nome){
  griglia(0.05); integra_denso(1,1); long occ=0,centro=0,tutti=0; double h=0.05;
  for(int z=0;z<N3[2];z++)for(int y=0;y<N3[1];y++)for(int x=0;x<N3[0];x++){ if(!(vdense(x,y,z)->nu&2))continue; occ++;
    if(classe(G0[0]+(x+.5)*h,G0[1]+(y+.5)*h,G0[2]+(z+.5)*h)==0)centro++;
    int nf=0; for(int c=0;c<4;c++)for(int b=0;b<4;b++)for(int a=0;a<4;a++) if(classe(G0[0]+(x+(a+.5)/4)*h,G0[1]+(y+(b+.5)/4)*h,G0[2]+(z+(c+.5)/4)*h)==0)nf++;
    if(nf==64)tutti++; }
  printf("P9 [%s] voxel occupati %ld: 'visti attraverso' col solo centro %ld; con tutti i 64 sottopunti %ld\n",nome,occ,centro,tutti);
}
int main(void){ camera();
  scena(3); render(0); p8("parete a 4 m");
  scena(0); render(0); p8("parete a 5,5 m"); p9("demo");
  scena(1); render(0); p8("senza parete");
  scena(2); render(0); p9("peggiore"); return 0; }
