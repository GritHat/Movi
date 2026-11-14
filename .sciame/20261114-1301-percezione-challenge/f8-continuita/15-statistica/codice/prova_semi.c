/* prova_semi.c — sciame-statistico: i flussi di semi consecutivi sono copie spostate? Include gen.h in sola lettura. */
#include <stdio.h>
#include "gen.h"
int main(void) {
    Geo g = geo_make('D', 0.0); static Traj T; double prev_h = 0; int ok = 0, n = 0;
    for (uint64_t s = 9000; s <= 9006; s++) {
        traj_make(&T, &g, B_PROSEGUE, s);
        double uv = (T.v0 - 0.3) / 1.5, uh = (T.head * 180.0 / M_PI + 15.0) / 30.0;
        printf("seme %llu: u(velocita') = %.12f  u(rotta) = %.12f", (unsigned long long)s, uv, uh);
        if (s > 9000) { double d = fabs(uv - prev_h); printf("  | u(velocita') - u(rotta del seme prima) = %.3e", d); n++; ok += d < 1e-9; }
        printf("\n"); prev_h = uh;
    }
    printf("coincidenze: %d su %d\n", ok, n);
    /* stato grezzo: dopo rng_seed, il primo numero del seme s+1 e' il secondo del seme s? */
    Rng a, b; rng_seed(&a, 9000, 'D', 0, 1); rng_seed(&b, 9001, 'D', 0, 1); rng_u64(&a);
    int same = 0; for (int i = 0; i < 1000; i++) same += rng_u64(&a) == rng_u64(&b);
    printf("flusso del seme 9001 = flusso del seme 9000 avanzato di 1: %d numeri uguali su 1000\n", same);
    Rng c, d; rng_seed(&c, 9000, 'D', 0, 2); rng_seed(&d, 9005, 'D', 0, 2); for (int i = 0; i < 5; i++) rng_u64(&c);
    same = 0; for (int i = 0; i < 1000; i++) same += rng_u64(&c) == rng_u64(&d);
    printf("flusso delle misure (stream 2): seme 9005 = seme 9000 avanzato di 5: %d numeri uguali su 1000\n", same);
    return 0;
}
