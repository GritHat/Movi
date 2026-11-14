/* gen.h — GENERATORE del banco indipendente (sciame-validazione, f8, f4).
 * Scena, traiettorie e misure. Scritto da capo; congelato (sha256 in CONGELATO.txt) prima dei predittori.
 * Nessuna riga viene dai generatori altrui (truth(), g1, traiettoria()); niente tassi di manovra al secondo:
 * ogni passaggio ha UNA manovra a un istante uniforme nel tratto nascosto.
 */
#ifndef GEN_H
#define GEN_H
#include <math.h>
#include <stdint.h>
#include <string.h>

#define DT (1.0 / 15.0)
#define HALF_FOV (43.5 * M_PI / 180.0)
#define C6_DIST 0.22      /* nessuna misura entro 0,22 m dal bordo dell'ombra (C6 emulata) */
#define MAXK 200
#define T_PRE 2.5         /* il soggetto parte 2,5 s prima dell'ingresso nell'ombra vera */
#define T_POST 9.0
#define NBEH 10
enum { B_PROSEGUE = 0, B_RALLENTA, B_SOSTA, B_TORNA, B_SVOLTA, B_LONTANO, B_SOSTALUNGA, B_ATT1, B_TRIPLA, B_DUE };
static const char *BEH_NAME[NBEH] = {"prosegue", "rallenta", "sosta", "torna", "svolta", "lontano", "sostalunga",
                                     "attacco1", "tripla", "due"};

/* ---------- numeri casuali: splitmix64, semi fissati ---------- */
typedef struct { uint64_t s; } Rng;
static inline uint64_t rng_u64(Rng *r) {
    uint64_t z = (r->s += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static inline double rng_u(Rng *r) { return (double)(rng_u64(r) >> 11) * (1.0 / 9007199254740992.0); }
static inline double rng_n(Rng *r) { /* polare di Marsaglia, un valore per chiamata */
    double a, b, s;
    do { a = 2 * rng_u(r) - 1; b = 2 * rng_u(r) - 1; s = a * a + b * b; } while (s >= 1.0 || s == 0.0);
    return a * sqrt(-2.0 * log(s) / s);
}
static inline void rng_seed(Rng *r, uint64_t seed, uint64_t geo, uint64_t beh, uint64_t stream) {
    r->s = seed * 0x9E3779B97F4A7C15ULL + geo * 0xD1B54A32D192ED03ULL + beh * 0x8CB92BA72F3D8DD7ULL + stream * 0xABCDEF1234567ULL;
    rng_u64(r); rng_u64(r);
}
static inline double rng_range(Rng *r, double a, double b) { return a + (b - a) * rng_u(r); }

/* ---------- geometria ---------- */
typedef struct {
    char name;
    double yp, w, ys, rmax, e; /* pannello a yp largo w; linea del soggetto ys; portata; errore della maschera (m per lato, a ys) */
    double tA, tAe;            /* tangente del mezzo angolo dell'ombra: vera, stimata */
} Geo;

static Geo geo_make(char name, double e) {
    Geo g; g.name = name; g.e = e;
    if (name == 'D') { g.yp = 1.9; g.w = 1.0; g.ys = 2.3; g.rmax = 3.0; }
    else if (name == 'T') { g.yp = 2.0; g.w = 1.0; g.ys = 4.0; g.rmax = 6.0; }
    else { g.yp = 2.0; g.w = 2.0; g.ys = 4.0; g.rmax = 6.0; } /* L */
    g.tA = (g.w / 2.0) / g.yp;
    g.tAe = (g.tA * g.ys + e) / g.ys;
    return g;
}
static inline int in_wedge(double x, double y, double yp, double t) { return y >= yp && fabs(x) <= y * t; }
/* distanza di un punto dal cuneo {y >= yp, |x| <= y t}; 0 se dentro */
static double dist_wedge(double x, double y, double yp, double t) {
    double ax = fabs(x);
    if (y >= yp && ax <= y * t) return 0.0;
    double he = yp * t, d1, d2;
    if (ax <= he) d1 = yp - y; else d1 = hypot(ax - he, y - yp);
    double n = sqrt(1.0 + t * t), s = t / n, c = 1.0 / n, dx = ax - he, dy = y - yp, al = dx * s + dy * c;
    d2 = (al <= 0) ? hypot(dx, dy) : fabs(dx * c - dy * s);
    return d1 < d2 ? d1 : d2;
}
static inline int in_domain(const Geo *g, double x, double y) {
    return y > 0 && hypot(x, y) <= g->rmax && fabs(atan2(x, y)) <= HALF_FOV;
}
/* il soggetto (puntiforme) e' rilevabile: nel campo, non nell'ombra vera, a piu' di 0,22 m dall'ombra stimata */
static inline int detectable(const Geo *g, double x, double y) {
    if (!in_domain(g, x, y)) return 0;
    if (in_wedge(x, y, g->yp, g->tA)) return 0;
    if (dist_wedge(x, y, g->yp, g->tAe) <= C6_DIST) return 0;
    return 1;
}

/* ---------- traiettoria ---------- */
typedef struct {
    int n, beh, sudden, mirror;
    double x[MAXK], y[MAXK];
    double v0, head, t_man, t_in, t_out;
    double x2[MAXK], y2[MAXK]; int has2; /* secondo soggetto (solo B_DUE) */
} Traj;

/* Una persona a piedi: velocita' nominale v0 e rotta head (rispetto all'asse x), con
 *  - fluttuazione lenta della velocita' (OU, 6 %, 1,5 s) e della rotta (OU, 3 gradi, 2 s);
 *  - ondeggiamento laterale del passo (2 cm, 0,9 Hz);
 *  - una manovra all'istante t_man, raggiunta con un ritardo del primo ordine (costante tc).
 * Passo d'integrazione DT/4. Il soggetto non attraversa il pannello: dietro di esso si ferma a 0,15 m dalla sua linea. */
static void traj_make(Traj *T, const Geo *g, int beh, uint64_t seed) {
    Rng r; rng_seed(&r, seed, (uint64_t)g->name, (uint64_t)beh, 1);
    memset(T, 0, sizeof(*T));
    T->beh = beh;
    double v0 = rng_range(&r, 0.3, 1.8), h = rng_range(&r, -30.0, 30.0) * M_PI / 180.0, oy = rng_range(&r, -0.10, 0.10);
    if (beh == B_ATT1) { v0 = 1.2; h = 0; oy = 0; }
    if (beh == B_TRIPLA) v0 = rng_range(&r, 0.4, 0.8);
    T->mirror = rng_u(&r) < 0.5;
    double yc = g->ys + oy, ch = cos(h), sh = sin(h);
    double s_in = -g->tA * yc / (ch + g->tA * sh), s_out = g->tA * yc / (ch - g->tA * sh);
    double t_in = T_PRE, t_out = T_PRE + (s_out - s_in) / v0;
    double t_man = t_in + rng_u(&r) * (t_out - t_in);
    if (beh == B_ATT1) t_man = t_in + (0.0 - s_in) / v0;          /* si ferma a meta' pannello (x = 0) */
    if (beh == B_TRIPLA) t_man = t_in;
    if (beh == B_PROSEGUE) t_man = 1e9;
    int sudden = rng_u(&r) < 0.5;
    if (beh == B_ATT1) sudden = 1;
    double f_slow = rng_range(&r, 0.30, 0.60);
    double hold = (beh == B_SOSTA) ? rng_range(&r, 2.0, 4.0) : (beh == B_ATT1 ? 6.0 : rng_range(&r, 6.0, 8.0));
    double pause = rng_range(&r, 0.3, 1.0), fback = rng_range(&r, 0.8, 1.2);
    double turn = rng_range(&r, 45.0, 90.0) * M_PI / 180.0 * (rng_u(&r) < 0.5 ? -1 : 1);
    double ph = rng_range(&r, 0, 2 * M_PI);
    T->v0 = v0; T->head = h; T->t_man = t_man; T->t_in = t_in; T->t_out = t_out; T->sudden = sudden;
    /* stato */
    double s0 = s_in - v0 * T_PRE;
    double px = s0 * ch, py = yc + s0 * sh;
    double m = 1.0, mt = 1.0, tcm = 0.4;     /* moltiplicatore della velocita', suo bersaglio, costante di tempo */
    double gh = 0.0, ght = 0.0, tcg = 0.3;   /* scarto di rotta dovuto alla manovra */
    double es = 0.15 * rng_n(&r), eh = (8.0 * M_PI / 180.0) * rng_n(&r);
    const double h_sub = DT / 4.0;
    int nk = (int)((T_PRE + T_POST) / DT) + 1; if (nk > MAXK) nk = MAXK;
    T->n = nk;
    double t = 0.0, dist = 0.0;
    for (int k = 0; k < nk; k++) {
        double hd = h + gh + eh;
        double sway = 0.02 * sin(2 * M_PI * 0.9 * (dist / (v0 > 0.5 ? v0 : 0.5)) + ph) * fmin(1.0, fabs(m));
        T->x[k] = px - sin(hd) * sway; T->y[k] = py + cos(hd) * sway;
        for (int q = 0; q < 4; q++) {
            /* bersagli della manovra */
            if (t >= t_man) {
                double ta = t - t_man;
                switch (beh) {
                case B_RALLENTA: mt = f_slow; tcm = 0.4; break;
                case B_SOSTA: case B_SOSTALUNGA: case B_ATT1: case B_DUE:
                    if (ta < hold) { mt = 0.0; tcm = sudden ? 0.07 : 0.35; } else { mt = 1.0; tcm = 0.4; }
                    break;
                case B_TORNA:
                    if (ta < pause + 0.3) { mt = 0.0; tcm = 0.15; } else { mt = -fback; tcm = 0.4; }
                    break;
                case B_SVOLTA: ght = turn; tcg = 0.3; break;
                case B_LONTANO: { double hr = atan2(py, px); /* direzione radiale, via dal sensore */
                    double d = hr - h; while (d > M_PI) d -= 2 * M_PI; while (d < -M_PI) d += 2 * M_PI;
                    ght = d; tcg = 0.3; } break;
                case B_TRIPLA: mt = 3.0; tcm = 0.2; break;
                default: break;
                }
            }
            /* fluttuazioni lente (OU esatto sul passo) */
            double as = exp(-h_sub / 1.5), ah = exp(-h_sub / 2.0);
            es = as * es + 0.15 * sqrt(1 - as * as) * rng_n(&r);
            eh = ah * eh + (8.0 * M_PI / 180.0) * sqrt(1 - ah * ah) * rng_n(&r);
            m += (mt - m) * (1 - exp(-h_sub / tcm));
            gh += (ght - gh) * (1 - exp(-h_sub / tcg));
            double hh = h + gh + eh, sp = v0 * m * (1.0 + es);
            double vx = sp * cos(hh), vy = sp * sin(hh);
            if (fabs(px) <= g->w / 2 + 0.10 && py >= g->yp && py < g->yp + 0.15 && vy < 0) { vx = 0; vy = 0; } /* non attraversa il pannello */
            px += vx * h_sub; py += vy * h_sub; dist += fabs(sp) * h_sub; t += h_sub;
        }
    }
    /* secondo soggetto, solo per «entra uno, escono due»: era gia' fermo nell'ombra, mai tracciato;
     * esce dal lato lontano lungo la stessa rotta, partendo fra 0,5 e 3 s dopo l'ingresso del primo. */
    if (beh == B_DUE) {
        T->has2 = 1;
        double tgo = t_in + rng_range(&r, 0.5, 3.0), v2 = rng_range(&r, 0.5, 1.5);
        double sst = s_in + rng_range(&r, 0.5, 0.9) * (s_out - s_in);
        for (int k = 0; k < nk; k++) {
            double tt = k * DT, s = sst + (tt > tgo ? v2 * (tt - tgo) : 0.0);
            T->x2[k] = s * ch; T->y2[k] = yc + s * sh;
        }
    }
    if (T->mirror) for (int k = 0; k < nk; k++) { T->x[k] = -T->x[k]; T->x2[k] = -T->x2[k]; }
}

/* ---------- misura ---------- */
/* ritorna 1 e scrive z se il soggetto e' rilevato in questo ciclo. sigma: 0 = 5 cm per asse; 1 = curva 4/9/16 cm a 2/3/4 m */
static inline int measure(const Geo *g, Rng *rm, double x, double y, double pd, int curve, double z[2]) {
    int det = detectable(g, x, y);
    double u = rng_u(rm), n1 = rng_n(rm), n2 = rng_n(rm); /* consumati sempre: stessi numeri fra le condizioni */
    if (!det || u >= pd) return 0;
    double s = 0.05;
    if (curve) { double rr = hypot(x, y) / 2.0; s = 0.04 * rr * rr; }
    z[0] = x + s * n1; z[1] = y + s * n2;
    return 1;
}
#endif
