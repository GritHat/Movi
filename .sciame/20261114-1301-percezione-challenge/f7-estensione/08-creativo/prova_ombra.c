/* prova_ombra.c — sciame-creativo, f7, corsia B.
 * Confronta, su una scena sintetica e un solo fotogramma di profondita':
 *   A = griglia voxel densa con lancio dei raggi (riferimento di promptMare.txt)
 *   B = interrogazione del buffer di profondita' (creativo-1, "mappa d'ombra del sensore")
 *   verita' = visibilita' analitica del centro del voxel
 * e prova la "sagoma limite" (creativo-2) contro la regola piana del nucleo.
 * Uso: prova_ombra <rumore 0|1> <montaggio 0=orizzontale 1=verticale> <pannello 0|1>
 * Compilazione: gcc -O2 -o prova_ombra prova_ombra.c -lm        Seme fisso: 1.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define PI 3.14159265358979323846
typedef struct { double lo[3], hi[3]; int vivo; } Box;
enum { SCATOLA = 0, PANNELLO = 1, BARRA = 2, PERSONA = 3, FONDO = 4, PSX = 5, PDX = 6, SOFFITTO = 7, NBOX = 8 };
static Box box[NBOX] = {
    {{-1.00, 1.40, 0.00}, {-0.50, 1.70, 0.30}, 1}, /* scatola bassa */
    {{ 0.20, 2.00, 0.00}, { 1.20, 2.05, 2.00}, 1}, /* pannello 1 x 2 m */
    {{-0.40, 1.50, 1.70}, { 0.40, 1.60, 1.85}, 1}, /* barra alla quota della testa */
    {{ 0.50, 2.40, 0.00}, { 0.95, 2.70, 1.75}, 1}, /* persona nascosta */
    {{-3.05, 4.00, 0.00}, { 3.05, 4.05, 3.05}, 0}, /* parete di fondo (variante stanza) */
    {{-3.05, 0.00, 0.00}, {-3.00, 4.05, 3.05}, 0}, /* parete sinistra */
    {{ 3.00, 0.00, 0.00}, { 3.05, 4.05, 3.05}, 0}, /* parete destra */
    {{-3.05, 0.00, 3.00}, { 3.05, 4.05, 3.05}, 0}, /* soffitto */
};
/* camera */
static int W = 320, H = 240;
static double HS = 1.2, PITCH = 15.0, HFOV = 87.0, VFOV = 58.0, TMAX = 6.0;
static double S[3], F[3], R[3], U[3], TX, TY;
static float *D, *Dmin, *Dmax;       /* profondita' lungo l'asse; 0 = non valido */
static signed char *ID;               /* oggetto colpito: -1 suolo, -2 niente */
static int RUMORE = 0, NFUS = 1, INGENUO = 0;
static float *Dlo, *Dhi; /* fusione di NFUS fotogrammi: minimo e massimo dei validi */
static double E0 = 0.02;
static double sigma(double z) { return RUMORE ? 0.00375 * z * z : 0.0; }
static double eps(double z) { return E0 + 3.0 * sigma(z); }

static unsigned long long rs = 1;
static double urand(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static double nrand(void) { double u = urand() + 1e-300, v = urand(); return sqrt(-2 * log(u)) * cos(2 * PI * v); }
static double adesso(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec * 1e-6; }

/* raggio o + t d contro una scatola: ritorna t d'ingresso (>0) o -1 */
static double ray_box(const double o[3], const double d[3], const Box *b) {
    double t0 = 0, t1 = 1e30;
    for (int k = 0; k < 3; k++) {
        if (fabs(d[k]) < 1e-12) { if (o[k] < b->lo[k] || o[k] > b->hi[k]) return -1; continue; }
        double a = (b->lo[k] - o[k]) / d[k], c = (b->hi[k] - o[k]) / d[k];
        if (a > c) { double x = a; a = c; c = x; }
        if (a > t0) t0 = a;
        if (c < t1) t1 = c;
        if (t0 > t1) return -1;
    }
    return t0;
}
static void pixel_dir(int i, int j, double d[3]) {
    double a = ((i + 0.5) / W * 2 - 1) * TX, b = (1 - (j + 0.5) / H * 2) * TY;
    for (int k = 0; k < 3; k++) d[k] = F[k] + a * R[k] + b * U[k];
}
/* proiezione: ritorna 1 se dentro l'immagine */
static int proietta(const double p[3], double *t, double *fi, double *fj) {
    double q[3] = {p[0] - S[0], p[1] - S[1], p[2] - S[2]};
    *t = q[0] * F[0] + q[1] * F[1] + q[2] * F[2];
    if (*t <= 1e-9) return 0;
    double a = (q[0] * R[0] + q[1] * R[1] + q[2] * R[2]) / *t, b = (q[0] * U[0] + q[1] * U[1] + q[2] * U[2]) / *t;
    *fi = (a / TX + 1) * 0.5 * W; *fj = (1 - b / TY) * 0.5 * H;
    return (*fi >= 0 && *fi < W && *fj >= 0 && *fj < H);
}
static void rendi(void) {
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        double d[3]; pixel_dir(i, j, d);
        double best = 1e30; int id = -2;
        if (d[2] < -1e-12) { best = -S[2] / d[2]; id = -1; }
        for (int b = 0; b < NBOX; b++) if (box[b].vivo) { double t = ray_box(S, d, &box[b]); if (t > 0 && t < best) { best = t; id = b; } }
        if (best > TMAX) { best = 0; id = -2; }
        if (best > 0 && RUMORE) { best += sigma(best) * nrand(); if (urand() < 0.05) best = 0; }
        D[j * W + i] = (float)best; ID[j * W + i] = (signed char)id;
    }
}
static void minmax(void) { /* 3x3; bordo o vicino non valido -> non valido */
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        float mn = 1e30f, mx = 0; int ok = (i > 0 && j > 0 && i < W - 1 && j < H - 1);
        if (ok) for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) {
            float v = Dlo[(j + dj) * W + i + di], w = Dhi[(j + dj) * W + i + di]; if (v <= 0) ok = 0; if (v < mn) mn = v; if (w > mx) mx = w; }
        Dmin[j * W + i] = ok ? mn : 0; Dmax[j * W + i] = ok ? mx : 0;
    }
}
enum { V_OCC, V_VIS, V_NASC, V_FUORI };            /* verita' */
enum { B_LIBERO, B_BORDO, B_OMBRA, B_BUCO, B_FUORI }; /* risposta di B */
static int verita(const double p[3]) {
    for (int b = 0; b < NBOX; b++) if (box[b].vivo &&
        p[0] >= box[b].lo[0] && p[0] <= box[b].hi[0] && p[1] >= box[b].lo[1] && p[1] <= box[b].hi[1] && p[2] >= box[b].lo[2] && p[2] <= box[b].hi[2]) return V_OCC;
    double t, fi, fj; if (!proietta(p, &t, &fi, &fj) || t > TMAX) return V_FUORI;
    double d[3] = {p[0] - S[0], p[1] - S[1], p[2] - S[2]};
    for (int b = 0; b < NBOX; b++) if (box[b].vivo) { double tb = ray_box(S, d, &box[b]); if (tb > 0 && tb < 1.0) return V_NASC; }
    return V_VIS;
}
static inline int interroga(const double p[3]) {
    double t, fi, fj; if (!proietta(p, &t, &fi, &fj)) return B_FUORI;
    int k = (int)fj * W + (int)fi; float mn = Dmin[k], mx = Dmax[k];
    if (INGENUO) { float v = D[k]; if (v <= 0) return t < TMAX ? B_LIBERO : B_FUORI; return t < v ? B_LIBERO : B_OMBRA; }
    if (mn <= 0) return B_BUCO;
    if (t < mn - eps(mn)) return B_LIBERO;
    if (t > mx + eps(mx)) return B_OMBRA;
    return B_BORDO;
}
/* ---- A: griglia voxel densa, lancio dei raggi (Amanatides-Woo) ---- */
static const double G0[3] = {-3, 0, 0}, GL[3] = {6, 4, 3};
static int NX, NY, NZ; static unsigned char *G; /* 0 sconosciuto, 1 libero, 2 occupato */
static long passi;
static void lancia(double vox) {
    memset(G, 0, (size_t)NX * NY * NZ); passi = 0;
    int n[3] = {NX, NY, NZ};
    for (int pass = 0; pass < 2; pass++)
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        double dep = D[j * W + i]; if (dep <= 0) continue;
        double d[3]; pixel_dir(i, j, d);
        if (pass == 1) { /* fine del raggio: occupato vince */
            int c[3], ok = 1; for (int k = 0; k < 3; k++) { c[k] = (int)floor((S[k] + dep * d[k] - G0[k]) / vox); if (c[k] < 0 || c[k] >= n[k]) ok = 0; }
            if (ok) G[((size_t)c[2] * NY + c[1]) * NX + c[0]] = 2; continue; }
        double tend = dep - eps(dep); if (tend <= 0) continue;
        double o[3]; int c[3], st[3]; double tm[3], td[3];
        for (int k = 0; k < 3; k++) { o[k] = S[k] + 1e-6 * d[k]; c[k] = (int)floor((o[k] - G0[k]) / vox);
            st[k] = d[k] > 0 ? 1 : -1;
            if (fabs(d[k]) < 1e-12) { tm[k] = 1e30; td[k] = 1e30; }
            else { double nb = G0[k] + (c[k] + (d[k] > 0)) * vox; tm[k] = (nb - S[k]) / d[k]; td[k] = vox / fabs(d[k]); } }
        for (;;) {
            if (c[0] < 0 || c[1] < 0 || c[2] < 0 || c[0] >= NX || c[1] >= NY || c[2] >= NZ) break;
            int a = tm[0] < tm[1] ? (tm[0] < tm[2] ? 0 : 2) : (tm[1] < tm[2] ? 1 : 2);
            if (tm[a] > tend) break; /* il voxel non e' attraversato per intero prima di D - eps */
            G[((size_t)c[2] * NY + c[1]) * NX + c[0]] = 1; passi++;
            c[a] += st[a]; tm[a] += td[a];
        }
    }
}
static double mediana(double *v, int n) { for (int i = 1; i < n; i++) { double x = v[i]; int j = i - 1; while (j >= 0 && v[j] > x) { v[j + 1] = v[j]; j--; } v[j + 1] = x; } return v[n / 2]; }

int main(int argc, char **argv) {
    RUMORE = argc > 1 ? atoi(argv[1]) : 0;
    int vert = argc > 2 ? atoi(argv[2]) : 0;
    box[PANNELLO].vivo = argc > 3 ? atoi(argv[3]) : 1;
    int stanza = argc > 4 ? atoi(argv[4]) : 0; NFUS = argc > 5 ? atoi(argv[5]) : 1; INGENUO = argc > 6 ? atoi(argv[6]) : 0;
    for (int b = FONDO; b <= SOFFITTO; b++) box[b].vivo = stanza;
    if (argc > 7 && atoi(argv[7])) for (int b = SCATOLA; b <= PERSONA; b++) box[b].vivo = 0; /* stanza vuota */
    if (vert) { HFOV = 58; VFOV = 87; W = 240; H = 320; }
    double p = PITCH * PI / 180;
    S[0] = 0; S[1] = 0; S[2] = HS; F[0] = 0; F[1] = cos(p); F[2] = -sin(p); R[0] = 1; R[1] = 0; R[2] = 0; U[0] = 0; U[1] = sin(p); U[2] = cos(p);
    TX = tan(HFOV * PI / 360); TY = tan(VFOV * PI / 360);
    D = malloc(sizeof(float) * W * H); Dmin = malloc(sizeof(float) * W * H); Dmax = malloc(sizeof(float) * W * H); ID = malloc(W * H); Dlo = malloc(sizeof(float) * W * H); Dhi = malloc(sizeof(float) * W * H);
    printf("== rumore=%d montaggio=%s pannello=%d stanza=%d fotogrammi fusi per B=%d B ingenuo=%d  immagine %dx%d campo %.0fx%.0f gradi ==\n", RUMORE, vert ? "verticale" : "orizzontale", box[PANNELLO].vivo, stanza, NFUS, INGENUO, W, H, HFOV, VFOV);
    rs = 1; for (int k = 0; k < W * H; k++) { Dlo[k] = 0; Dhi[k] = 0; }
    for (int f = 0; f < NFUS; f++) { rendi(); for (int k = 0; k < W * H; k++) if (D[k] > 0) { if (Dlo[k] <= 0 || D[k] < Dlo[k]) Dlo[k] = D[k]; if (D[k] > Dhi[k]) Dhi[k] = D[k]; } }
    minmax(); /* A usa solo l'ultimo fotogramma (D) */
    int validi = 0; for (int k = 0; k < W * H; k++) validi += D[k] > 0;
    printf("pixel validi %d su %d (%.1f %%)\n", validi, W * H, 100.0 * validi / (W * H));

    /* ---------- A contro B contro verita', a 5 e 10 cm ---------- */
    for (int r = 0; r < 2; r++) {
        double vox = r == 0 ? 0.05 : 0.10;
        NX = (int)lround(GL[0] / vox); NY = (int)lround(GL[1] / vox); NZ = (int)lround(GL[2] / vox);
        size_t N = (size_t)NX * NY * NZ; G = malloc(N);
        double ta[21], tb[21];
        for (int rep = 0; rep < 21; rep++) { double t0 = adesso(); lancia(vox); ta[rep] = adesso() - t0; }
        long c[4][5] = {{0}}, a[4][3] = {{0}}; volatile long sink = 0;
        for (int rep = 0; rep < 21; rep++) { double t0 = adesso(); long s = 0;
            for (int z = 0; z < NZ; z++) for (int y = 0; y < NY; y++) for (int x = 0; x < NX; x++) {
                double q[3] = {G0[0] + (x + 0.5) * vox, G0[1] + (y + 0.5) * vox, G0[2] + (z + 0.5) * vox}; s += interroga(q); }
            sink += s; tb[rep] = adesso() - t0; }
        for (int z = 0; z < NZ; z++) for (int y = 0; y < NY; y++) for (int x = 0; x < NX; x++) {
            double q[3] = {G0[0] + (x + 0.5) * vox, G0[1] + (y + 0.5) * vox, G0[2] + (z + 0.5) * vox};
            int v = verita(q); c[v][interroga(q)]++; a[v][G[((size_t)z * NY + y) * NX + x]]++; }
        long nb = 0, nbtot = 0;
        for (int bz = 0; bz < NZ; bz += 8) for (int by = 0; by < NY; by += 8) for (int bx = 0; bx < NX; bx += 8) { nbtot++; int pieno = 0;
            for (int z = bz; z < bz + 8 && z < NZ && !pieno; z++) for (int y = by; y < by + 8 && y < NY && !pieno; y++) for (int x = bx; x < bx + 8 && x < NX; x++) if (G[((size_t)z * NY + y) * NX + x]) { pieno = 1; break; }
            nb += pieno; }
        long vis = c[V_VIS][0] + c[V_VIS][1] + c[V_VIS][2] + c[V_VIS][3] + c[V_VIS][4];
        long blib = c[0][0] + c[1][0] + c[2][0] + c[3][0], alib = a[0][1] + a[1][1] + a[2][1] + a[3][1], atocc = a[0][1] + a[0][2] + a[1][1] + a[1][2] + a[2][1] + a[2][2] + a[3][1] + a[3][2];
        double amax = 0, bmax = 0; for (int k = 0; k < 21; k++) { if (ta[k] > amax) amax = ta[k]; if (tb[k] > bmax) bmax = tb[k]; }
        printf("-- voxel %.2f m: %dx%dx%d = %zu centri; verita': occupato %ld, visibile vuoto %ld, nascosto %ld, fuori campo %ld\n", vox, NX, NY, NZ, N,
               c[0][0] + c[0][1] + c[0][2] + c[0][3] + c[0][4], vis, c[2][0] + c[2][1] + c[2][2] + c[2][3] + c[2][4], c[3][0] + c[3][1] + c[3][2] + c[3][3] + c[3][4]);
        printf("   B: libero %ld; FALSI LIBERI: su occupato %ld, su nascosto %ld, su fuori campo %ld; visibili non detti liberi %ld (%.1f %%) [bordo %ld, ombra %ld, buco %ld]\n",
               blib, c[V_OCC][0], c[V_NASC][0], c[V_FUORI][0], vis - c[V_VIS][0], 100.0 * (vis - c[V_VIS][0]) / vis, c[V_VIS][1], c[V_VIS][2], c[V_VIS][3]);
        printf("   B: nascosti detti ombra %ld, bordo %ld, buco %ld; fuori campo detti fuori %ld, buco %ld, ombra %ld, bordo %ld\n", c[V_NASC][2], c[V_NASC][1], c[V_NASC][3], c[V_FUORI][4], c[V_FUORI][3], c[V_FUORI][2], c[V_FUORI][1]);
        printf("   A: libero %ld; FALSI LIBERI: su occupato %ld, su nascosto %ld, su fuori campo %ld (%.2f %% dei liberi di A); visibili non detti liberi %ld (%.1f %%)\n",
               alib, a[V_OCC][1], a[V_NASC][1], a[V_FUORI][1], 100.0 * (a[V_OCC][1] + a[V_NASC][1] + a[V_FUORI][1]) / (alib ? alib : 1), vis - a[V_VIS][1], 100.0 * (vis - a[V_VIS][1]) / vis);
        printf("   A: voxel toccati %ld (%.1f %%); blocchi 8^3 toccati %ld su %ld (%.1f %%); passi di raggio %ld\n", atocc, 100.0 * atocc / N, nb, nbtot, 100.0 * nb / nbtot, passi);
        printf("   memoria: A densa %zu B a 1 byte, %zu B a 12 byte per voxel; A a blocchi (senza indice) %ld B a 1 byte, %ld B a 12; B: profondita' uint16 %d B, con min/max float %d B\n",
               N, N * 12, nb * 512, nb * 512 * 12, W * H * 2, W * H * 8);
        printf("   tempo (21 lanci): A aggiornamento mediana %.2f ms, massimo %.2f ms; B interrogazione di tutti i centri mediana %.2f ms, massimo %.2f ms\n", mediana(ta, 21), amax, mediana(tb, 21), bmax);
        free(G);
    }

    /* ---------- P5: ombra al suolo dietro la scatola bassa, griglia polare 1 grado x 0,1 m ---------- */
    {
        double r0[360]; int chi[360]; for (int k = 0; k < 360; k++) { r0[k] = 1e30; chi[k] = -2; }
        for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) { double dep = D[j * W + i]; if (dep <= 0) continue; double d[3]; pixel_dir(i, j, d);
            double x = S[0] + dep * d[0], y = S[1] + dep * d[1], z = S[2] + dep * d[2]; if (z < 0.07 || z > 2.0) continue;
            int az = (int)floor(atan2(x, y) * 180 / PI) + 180; double rr = hypot(x, y); if (rr < r0[az]) { r0[az] = rr; chi[az] = ID[j * W + i]; } }
        long cuneo = 0, bomb = 0, vnasc = 0, ver_in_b = 0;
        for (int az = 0; az < 360; az++) if (chi[az] == SCATOLA) for (int k = 0; k < 30; k++) { double rr = (k + 0.5) * 0.1; if (rr <= r0[az]) continue;
            double an = (az - 180 + 0.5) * PI / 180, q[3] = {rr * sin(an), rr * cos(an), 0.02};
            cuneo++; int b = interroga(q), v = verita(q); bomb += (b == B_OMBRA); vnasc += (v == V_NASC || v == V_OCC); ver_in_b += ((v == V_NASC || v == V_OCC) && (b == B_OMBRA || b == B_BORDO || b == B_BUCO)); }
        printf("-- ombra al suolo dietro la scatola bassa (celle polari 1 grado x 0,1 m fino a 3 m): cuneo del nucleo %ld celle; B in ombra %ld (%.1f %% del cuneo); verita' nascosto %ld; nascosti che B non chiama libero %ld\n",
               cuneo, bomb, 100.0 * bomb / (cuneo ? cuneo : 1), vnasc, ver_in_b);
    }
    /* ---------- P6: sagoma limite 0,1-1,9 m contro la regola piana del nucleo ---------- */
    {
        enum { GX = 60, GY = 40 }; static unsigned char suolo[GY][GX], occ[GY][GX];
        memset(suolo, 0, sizeof suolo); memset(occ, 0, sizeof occ);
        for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) { double dep = D[j * W + i]; if (dep <= 0) continue; double d[3]; pixel_dir(i, j, d);
            double x = S[0] + dep * d[0], y = S[1] + dep * d[1], z = S[2] + dep * d[2]; int cx = (int)floor((x + 3) / 0.1), cy = (int)floor(y / 0.1);
            if (cx < 0 || cx >= GX || cy < 0 || cy >= GY) continue; if (z < 0.07) suolo[cy][cx] = 1; else if (z <= 2.0) occ[cy][cx] = 1; }
        long zona = 0, nlib = 0, nfalsi = 0, nfalsi_barra = 0, spiena = 0, sfalsi = 0, colpiene = 0; double tq[21]; double hsum = 0; long hn = 0;
        for (int rep = 0; rep < 21; rep++) { double t0 = adesso(); if (rep) minmax();
            zona = nlib = nfalsi = nfalsi_barra = spiena = sfalsi = colpiene = 0; hsum = 0; hn = 0;
            for (int cy = 0; cy < GY; cy++) for (int cx = 0; cx < GX; cx++) { double x = -3 + (cx + 0.5) * 0.1, y = (cy + 0.5) * 0.1, rr = hypot(x, y);
                if (rr < 1.24 || rr > 3.0 || fabs(atan2(x, y)) > HFOV * PI / 360) continue; zona++;
                int ogg = -1; for (int b = 0; b < NBOX; b++) if (box[b].vivo && box[b].lo[0] < x + 0.05 && box[b].hi[0] > x - 0.05 && box[b].lo[1] < y + 0.05 && box[b].hi[1] > y - 0.05 && box[b].lo[2] < 1.9 && box[b].hi[2] > 0.07) { ogg = b; break; }
                colpiene += ogg >= 0;
                int lib = suolo[cy][cx] && !occ[cy][cx]; nlib += lib; if (lib && ogg >= 0) { nfalsi++; nfalsi_barra += (ogg == BARRA); }
                static const double ox[5] = {0, -0.05, 0.05, -0.05, 0.05}, oy[5] = {0, -0.05, -0.05, 0.05, 0.05};
                int piena = 1; double hver = 1.9;
                for (int s = 0; s < 5; s++) for (int kz = 1; kz <= 19; kz++) { double q[3] = {x + ox[s], y + oy[s], kz * 0.1};
                    if (interroga(q) != B_LIBERO) { piena = 0; if (q[2] - 0.1 < hver) hver = q[2] - 0.1; break; } }
                spiena += piena; if (piena && ogg >= 0) sfalsi++; if (lib) { hsum += hver; hn++; } }
            tq[rep] = adesso() - t0; }
        double tmax = 0; for (int k = 1; k < 21; k++) if (tq[k] > tmax) tmax = tq[k];
        printf("-- sagoma 0,1-1,9 m, celle da 10 cm nella zona 1,24-3 m: zona %ld celle, colonne con un oggetto %ld\n", zona, colpiene);
        printf("   regola piana del nucleo: libero %ld celle, di cui con un oggetto nella colonna %ld (sotto la barra %ld)\n", nlib, nfalsi, nfalsi_barra);
        printf("   sagoma: verificata libera per intero %ld celle (%.1f %% della zona), di cui con un oggetto nella colonna %ld; quota verificata media sulle celle 'libero' del nucleo %.2f m\n", spiena, 100.0 * spiena / (zona ? zona : 1), sfalsi, hn ? hsum / hn : 0);
        printf("   tempo B per fotogramma (min/max 3x3 + sagoma su tutta la zona; 20 lanci): mediana %.3f ms, massimo %.3f ms\n", mediana(tq + 1, 20), tmax);
    }
    /* ---------- P7: la persona nascosta ---------- */
    {
        long n = 0, k[5] = {0}; Box *b = &box[PERSONA];
        for (double x = b->lo[0] + 0.025; x < b->hi[0]; x += 0.05) for (double y = b->lo[1] + 0.025; y < b->hi[1]; y += 0.05) for (double z = 0.125; z < b->hi[2]; z += 0.05) { double q[3] = {x, y, z}; k[interroga(q)]++; n++; }
        printf("-- persona nascosta, %ld punti (quota >= 0,125 m): libero %ld, bordo %ld, ombra %ld (%.1f %%), buco %ld, fuori campo %ld\n", n, k[0], k[1], k[2], 100.0 * k[2] / n, k[3], k[4]);
    }
    return 0;
}
