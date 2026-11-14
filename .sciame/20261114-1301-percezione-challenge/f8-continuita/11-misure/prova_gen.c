/* controllo a vista del generatore: semi di sviluppo 5000+, mai quelli di taratura o di prova */
#include <stdio.h>
#include "gen.h"
int main(void){
    const char gs[3]={'D','T','L'};
    for(int gi=0;gi<3;gi++){ Geo g=geo_make(gs[gi],0.0);
        for(int b=0;b<NBEH;b++){ int nvis=0,nhid=0,nre=0,nval=0; double svis=0,shid=0;
            for(int s=5000;s<5100;s++){ Traj T; traj_make(&T,&g,b,s);
                int k=0,first=-1,khide=-1,kre=-1,cnt=0;
                for(k=0;k<T.n;k++){ int d=detectable(&g,T.x[k],T.y[k]);
                    if(khide<0){ if(d){cnt++; if(first<0)first=k;} else if(first>=0) khide=k; }
                    else if(kre<0 && d) kre=k; }
                if(khide>=0 && cnt>=4){ nval++; svis+=cnt*DT; nhid++; if(kre>=0){nre++; shid+=(kre-khide)*DT;} }
                (void)nvis;
            }
            printf("%c %-10s validi %3d/100  in vista medio %.2f s  ricompaiono %3d  buio medio (ricomparsi) %.2f s\n",g.name,BEH_NAME[b],nval,nval?svis/nval:0,nre,nre?shid/nre:0);
        }
        Traj T; traj_make(&T,&g,B_SOSTA,5001);
        printf("  es. sosta seme 5001: v0 %.2f rotta %.1f t_man %.2f t_in %.2f t_out %.2f specchio %d\n   ",T.v0,T.head*180/M_PI,T.t_man,T.t_in,T.t_out,T.mirror);
        for(int k=0;k<T.n;k+=10) printf("(%.2f,%.2f)%c ",T.x[k],T.y[k],detectable(&g,T.x[k],T.y[k])?'v':'n'); printf("\n");
    }
    return 0; }
