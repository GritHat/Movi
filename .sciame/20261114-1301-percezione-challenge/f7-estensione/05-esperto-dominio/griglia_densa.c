/* P6 e P8 - costo di una griglia 3D DENSA sulla regione 6 x 4 x 3 m.
 * Scena sintetica, un solo processo, nessun dato casuale salvo le scatole
 * (seme fisso). Non e' il prototipo ne' il sensore.
 * Compilare: gcc -O2 -o griglia_densa griglia_densa.c -lm
 * Lanciare:  timeout 100 ./griglia_densa
 * (primo lancio fallito: 200 fotogrammi anche a piena risoluzione superavano i 120 s e
 *  l'uscita, in coda nel buffer, e' andata persa; ora 200 fotogrammi per le righe
 *  decimate, 30 per quelle a piena risoluzione, e una riga scritta subito a ogni prova)
 * Regione: x in [0,6] (avanti), y in [-2,2], z in [0,3] (quota).
 * Sensore in (0,0,1.2), inclinato di 15 gradi verso il basso, 87 x 58 gradi.
 * Per voxel: log-odds int8 (saturato), eta' uint16 (ultimo fotogramma visto),
 * stato uint8 -> 4 byte. Il voxel mai toccato resta 'sconosciuto' (eta' = 0). */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define LX 6.0
#define LY 4.0
#define LZ 3.0
#define SH 1.2
#define PITCH (15.0 * M_PI / 180.0)
#define HF (87.0 * M_PI / 180.0)
#define VF (58.0 * M_PI / 180.0)
#define RMAX 6.0
static int NFRAME = 200;

typedef struct { int8_t lo; uint8_t st; uint16_t age; } Vox;
typedef struct { double x0, x1, y0, y1, z0, z1; } Box;

static double now_ms(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec * 1e-6;
}
static int cmpd(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y);
}
/* distanza lungo il raggio fino a una scatola (slab), o -1 */
static double hit_box(const Box *b, const double o[3], const double d[3]) {
    double tn = 0, tf = 1e9; const double lo[3] = {b->x0, b->y0, b->z0}, hi[3] = {b->x1, b->y1, b->z1};
    for (int i = 0; i < 3; i++) {
        if (fabs(d[i]) < 1e-12) { if (o[i] < lo[i] || o[i] > hi[i]) return -1; continue; }
        double t1 = (lo[i] - o[i]) / d[i], t2 = (hi[i] - o[i]) / d[i];
        if (t1 > t2) { double s = t1; t1 = t2; t2 = s; }
        if (t1 > tn) tn = t1; if (t2 < tf) tf = t2; if (tn > tf) return -1;
    }
    return tn;
}

static void run(double res, int step, const Box *boxes, int nb, const char *name) {
    int nx = (int)lround(LX / res), ny = (int)lround(LY / res), nz = (int)lround(LZ / res);
    size_t nv = (size_t)nx * ny * nz;
    Vox *g = calloc(nv, sizeof(Vox));
    int W = 848 / step, H = 480 / step; size_t nr = (size_t)W * H;
    float *dir = malloc(nr * 3 * sizeof(float)), *dep = malloc(nr * sizeof(float));
    const double o[3] = {0.0, 0.0, SH};
    double fx = (W / 2.0) / tan(HF / 2), fy = (H / 2.0) / tan(VF / 2);
    /* immagine di profondita' precalcolata (fuori dal tempo misurato) */
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        double cx = (u + 0.5 - W / 2.0) / fx, cy = (v + 0.5 - H / 2.0) / fy; /* cy>0 = basso */
        double dx = 1.0, dy = -cx, dz = -cy;
        double rx = dx * cos(PITCH) + dz * sin(PITCH), rz = -dx * sin(PITCH) + dz * cos(PITCH);
        double n = sqrt(rx * rx + dy * dy + rz * rz), d[3] = {rx / n, dy / n, rz / n};
        double t = -1;
        if (d[2] < -1e-9) t = -SH / d[2];                       /* suolo */
        for (int b = 0; b < nb; b++) { double tb = hit_box(&boxes[b], o, d); if (tb > 0 && (t < 0 || tb < t)) t = tb; }
        if (t < 0 || t > RMAX) t = -1;                           /* nessun ritorno valido */
        size_t i = (size_t)v * W + u; dir[3*i] = d[0]; dir[3*i+1] = d[1]; dir[3*i+2] = d[2]; dep[i] = (float)t;
    }
    double *ms = malloc(NFRAME * sizeof(double)); unsigned long long visits = 0;
    for (int f = 1; f <= NFRAME; f++) {
        double t0 = now_ms(); unsigned long long vis = 0;
        for (size_t i = 0; i < nr; i++) {
            double t_end = dep[i]; if (t_end < 0) continue;      /* misura mancante: nessun aggiornamento */
            double d[3] = {dir[3*i], dir[3*i+1], dir[3*i+2]};
            /* Amanatides-Woo dal sensore al punto misurato, tagliato alla regione */
            int c[3], stp[3]; double tmax[3], tdel[3]; const int dim[3] = {nx, ny, nz};
            const double org[3] = {0.0, -LY / 2, 0.0};
            for (int k = 0; k < 3; k++) {
                double p = (o[k] - org[k]) / res; c[k] = (int)floor(p);
                if (c[k] >= dim[k]) c[k] = dim[k] - 1; if (c[k] < 0) c[k] = 0;
                if (d[k] > 1e-12) { stp[k] = 1; tmax[k] = ((c[k] + 1) - p) * res / d[k]; tdel[k] = res / d[k]; }
                else if (d[k] < -1e-12) { stp[k] = -1; tmax[k] = (p - c[k]) * res / -d[k]; tdel[k] = res / -d[k]; }
                else { stp[k] = 0; tmax[k] = 1e30; tdel[k] = 1e30; }
            }
            for (;;) {
                int k = (tmax[0] < tmax[1]) ? (tmax[0] < tmax[2] ? 0 : 2) : (tmax[1] < tmax[2] ? 1 : 2);
                Vox *q = &g[((size_t)c[0] * ny + c[1]) * nz + c[2]];
                if (tmax[k] >= t_end) {                           /* voxel del ritorno: occupato */
                    int l = q->lo + 12; q->lo = (int8_t)(l > 100 ? 100 : l); q->st = 2; q->age = (uint16_t)f; vis++; break;
                }
                int l = q->lo - 6; q->lo = (int8_t)(l < -100 ? -100 : l); if (q->st != 2 || q->age != f) q->st = 1;
                q->age = (uint16_t)f; vis++;
                c[k] += stp[k]; tmax[k] += tdel[k];
                if (c[k] < 0 || c[k] >= dim[k]) break;            /* fuori regione */
            }
        }
        ms[f - 1] = now_ms() - t0; visits = vis;
    }
    size_t touched = 0, valid = 0; for (size_t i = 0; i < nv; i++) touched += (g[i].age != 0);
    for (size_t i = 0; i < nr; i++) valid += (dep[i] >= 0);
    qsort(ms, NFRAME, sizeof(double), cmpd);
    printf("%-14s res=%4.0f cm raggi=%6zu (validi %5.1f%%) voxel=%7zu mem=%5.2f MB toccati=%5.1f%% visite/fot=%8llu"
           "  ms: mediana=%7.2f p95=%7.2f max=%7.2f\n",
           name, res * 100, nr, 100.0 * valid / nr, nv, nv * sizeof(Vox) / 1048576.0, 100.0 * touched / nv, visits,
           ms[NFRAME / 2], ms[(int)(NFRAME * 0.95)], ms[NFRAME - 1]);
    fflush(stdout);
    free(g); free(dir); free(dep); free(ms);
}

int main(void) {
    /* stanza vuota: solo il suolo e la parete di fondo a 6 m (caso peggiore di percorrenza) */
    Box fondo[1] = {{5.95, 6.0, -2, 2, 0, 3}};
    /* parete a 2 m */
    Box vicino[1] = {{2.0, 2.05, -2, 2, 0, 3}};
    /* hangar ingombro: 12 scatole, seme fisso */
    Box ing[13]; srand(20261114); ing[0] = fondo[0];
    for (int i = 1; i < 13; i++) {
        double x = 1.5 + 4.0 * rand() / RAND_MAX, y = -1.8 + 3.2 * rand() / RAND_MAX;
        double sx = 0.2 + 0.6 * rand() / RAND_MAX, sy = 0.2 + 0.6 * rand() / RAND_MAX, sz = 0.3 + 1.6 * rand() / RAND_MAX;
        ing[i] = (Box){x, x + sx, y, y + sy, 0, sz};
    }
    printf("sizeof(Vox) = %zu byte; fotogrammi per riga: %d (decimato) o 30 (pieno); tempi del solo aggiornamento della mappa\n", sizeof(Vox), NFRAME);
    const double rs[2] = {0.10, 0.05}; const int st[2] = {4, 1};
    for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) {
        NFRAME = (st[b] == 1) ? 30 : 200; printf("-- %d fotogrammi\n", NFRAME);
        run(rs[a], st[b], fondo, 1, "vuota");
        run(rs[a], st[b], vicino, 1, "parete a 2 m");
        run(rs[a], st[b], ing, 13, "ingombra");
    }
    return 0;
}
