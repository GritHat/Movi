/* Costo per ciclo del disegno corretto: campitura a righe su una regione (maschera) piu' contorno
   tratteggiato, quadro 1920x1080 RGB. Rifare:
   gcc -O2 -o /tmp/claude-1000/-home-fede-Scrivania-ed-GitHub-Movi-Hackthon/5e23f93d-4455-4e40-867d-5818514a7c35/scratchpad/costo_disegno costo_disegno.c && timeout 120 <eseguibile> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#define W 1920
#define H 1080
static double ora(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(void){
  unsigned char *img=malloc(W*H*3), *reg=malloc(W*H);
  int n=300; double tmax=0, tsum=0, tsumA=0, tsumB=0, tmaxB=0; unsigned long chk=0;
  for(int f=0;f<n;f++){
    /* la regione cambia a ogni ciclo: cuneo fra due raggi e due distanze (ricalcolata per intero) */
    double a0=-0.27+0.001*f, a1=0.27+0.001*f, r0=1.8*360, r1=3.0*360;
    double t0=ora();
    memset(img,255,W*H*3);
    for(int y=0;y<H;y++) for(int x=0;x<W;x++){
      double dx=x-W/2, dy=H-y; double r=sqrt(dx*dx+dy*dy), a=atan2(dx,dy);
      reg[y*W+x]=(r>=r0&&r<=r1&&a>=a0&&a<=a1);
    }
    double tA=ora();
    for(int y=1;y<H-1;y++) for(int x=1;x<W-1;x++){
      int i=y*W+x; if(!reg[i]) continue;
      int bordo=!(reg[i-1]&&reg[i+1]&&reg[i-W]&&reg[i+W]);
      if(((x+y)&15)<6 || (bordo && ((x+y)%20)<12)){ img[3*i]=22; img[3*i+1]=32; img[3*i+2]=43; }
      else { img[3*i]=255; img[3*i+1]=224; img[3*i+2]=160; }
    }
    double dt=ora()-t0; tsum+=dt; if(dt>tmax)tmax=dt; tsumA+=tA-t0; double dB=ora()-tA; tsumB+=dB; if(dB>tmaxB)tmaxB=dB; chk+=img[3*(600*W+960)];
  }
  printf("quadri %d, 1920x1080: totale media %.2f ms, massimo %.2f ms; di cui sfondo + maschera ricalcolata punto per punto (modo ingenuo) media %.2f ms; sola campitura a righe + contorno tratteggiato sulla maschera media %.2f ms, massimo %.2f ms; controllo %lu\n",n,1e3*tsum/n,1e3*tmax,1e3*tsumA/n,1e3*tsumB/n,1e3*tmaxB,chk);
  return 0;
}
