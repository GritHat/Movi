#!/usr/bin/env python3
"""Prove automatiche della catena su scene minime costruite a mano (matrici di profondità senza rumore).

Uso:   <ambiente>/venv/bin/python -I -B prove.py [-v] [ProvaMappa.test_p01_pavimento_vuoto ...]

Gli esiti attesi sono scritti PRIMA in PREVISIONI.md (svil-P1 … svil-P16): il nome di ogni prova porta la sigla.
Geometria: 848×480, fx = fy = 424, camera a 1,2 m inclinata di 15°, 15 fotogrammi al secondo."""
import json
import os
import sys
import tempfile
import time
import unittest

for _nome in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_nome, "1")
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)

import numpy as np                                                   # noqa: E402

import esegui as riga_di_comando                                     # noqa: E402
from catena import Catena, esegui                                    # noqa: E402
from geometria import stima_suolo                                    # noqa: E402
from inseguimento import Inseguitore                                 # noqa: E402
from kalman import Kalman, rumore_processo, ungherese                # noqa: E402
from mappa import InvarianteViolato                                  # noqa: E402
from parametri import IN_OMBRA, LIBERO, NON_OSSERVATO, OCCUPATO, Parametri   # noqa: E402
from presenza import PredittoreVelocitaCostante, StatoIngresso       # noqa: E402
from scene_a_mano import META, Scena, tempi                          # noqa: E402
from sorgente import SorgenteMemoria                                 # noqa: E402

FPS = 15.0
SCENA = Scena()
ESEMPIO = os.path.join(QUI, "..", "03-infrastruttura", "esempio_sequenza")


def az(gradi):
    """Indice della cella di azimut che comincia a `gradi` (griglia da -90° a +90°, passo 1°)."""
    return int(gradi + 90)


def passa(fotogrammi, par=None, meta=META, posa=None):
    """Passa i fotogrammi nella catena; per ognuno tiene l'uscita, gli stati delle celle e la possibile presenza."""
    catena = Catena(meta, par or Parametri(), posa)
    esiti = []
    for i, f in enumerate(fotogrammi):
        t0 = time.perf_counter()
        uscita = catena.ciclo(i, i / FPS, f)
        uscita["ms"] = (time.perf_counter() - t0) * 1000.0
        esiti.append((uscita, catena.mappa_ciclo.stati.copy(), catena.possibile_presenza.copy()))
    return catena, esiti


def traccia(uscita, ident):
    return next((tr for tr in uscita["tracce"] if tr["id"] == ident), None)


def traccia_vicina(uscita, x, z, raggio=0.3):
    """L'id della traccia con posizione più vicina a (x, z), entro `raggio`."""
    vicine = [(np.hypot(tr["x"] - x, tr["z"] - z), tr["id"]) for tr in uscita["tracce"] if "x" in tr]
    vicine = [v for v in vicine if v[0] <= raggio]
    return min(vicine)[1] if vicine else None


def eventi(esiti, tipo):
    return [(u["indice"], e) for u, _, _ in esiti for e in u["eventi"] if e["tipo"] == tipo]


def sagoma(x, z=2.3, larga=0.4, alta=1.7):
    return (x - larga / 2, x + larga / 2, z, alta)


# Alto 1,8 m e non 1,6 come scritto nella previsione: da 1,2 m la camera vede sopra un pannello di 1,6 m a 1,9 m
# tutto ciò che a 2,3 m supera 1,684 m, cioè la testa di una sagoma di 1,7 m (prima prova: 0 fotogrammi nascosti).
PANNELLO_DEMO = (-0.5, 0.5, 1.9, 1.8)


class ProvaMappa(unittest.TestCase):
    def test_p01_pavimento_vuoto(self):
        catena, esiti = passa([SCENA.fotogramma()] * 5)
        for u, stati, _ in esiti:
            self.assertEqual(u["celle"]["occupato"], 0)
            self.assertEqual(u["celle"]["in_ombra"], 0)
            self.assertEqual(u["tracce"], [])
            interne = stati[az(-44):az(44), 13:30]
            self.assertEqual(interne.size, 1496)
            self.assertEqual(int((interne == LIBERO).sum()), 1442)      # previsto 1496: vedi PREVISIONI.md, esito P1
            # scritto DOPO la prima prova: il bordo vicino del suolo visto è la retta z = 1,22 m, non un cerchio
            g = catena.griglia
            oltre_la_retta = (g.z[az(-44):az(44), 13:30] - 0.05) >= 1.3
            self.assertEqual(int(oltre_la_retta.sum()), int((interne[oltre_la_retta] == LIBERO).sum()))
            self.assertFalse((stati[(g.z + 0.07) < 1.2] == LIBERO).any(), "libero prima della retta z = 1,2 m")
            self.assertFalse((stati[:, :12] == LIBERO).any(), "libero nell'anello cieco")
            self.assertFalse((stati[:az(-52)] == LIBERO).any() or (stati[az(52):] == LIBERO).any(), "fuori campo")
        print(f"\n  P1: celle per stato sul pavimento vuoto: {esiti[-1][0]['celle']}")

    def test_p01_suolo_come_l_infrastruttura(self):
        """Il suolo della scena coincide con `profondita_del_suolo` dell'infrastruttura (altro autore)."""
        sys.path.insert(0, os.path.join(QUI, "..", "03-infrastruttura"))
        from controlla_sequenza import profondita_del_suolo
        atteso = profondita_del_suolo(META)
        f = SCENA.fotogramma().astype(np.float64) / 1000.0
        visto = (f > 0) & np.isfinite(atteso)
        self.assertLess(float(np.abs(f[visto] - atteso[visto]).max()), 0.00051)

    def test_p02_nessun_dato(self):
        vuoto = np.zeros((META["altezza"], META["larghezza"]), dtype=np.uint16)
        _, esiti = passa([vuoto] * 3)
        for u, _, _ in esiti:
            self.assertEqual(u["celle"], {"non_osservato": 5400, "libero": 0, "occupato": 0, "in_ombra": 0})
        _, esiti = passa([SCENA.fotogramma()] * 3 + [vuoto] * 4)
        liberi = [u["celle"]["libero"] for u, _, _ in esiti]
        self.assertGreater(liberi[2], 1496)
        self.assertEqual(liberi[3:], [liberi[2], liberi[2], 0, 0])
        self.assertEqual([u["libero_per_eta"] for u, _, _ in esiti[2:6]],
                         [[liberi[2], 0, 0], [0, liberi[2], 0], [0, 0, liberi[2]], [0, 0, 0]])
        print(f"\n  P2: «libero» fotogramma per fotogramma (3 di pavimento, 4 senza dato): {liberi}")

    def test_p03_buchi(self):
        buco = (-10.0, 10.0, 1.8, 2.4)
        con_buco, pieno = SCENA.fotogramma(buco=buco), SCENA.fotogramma()
        _, esiti = passa([con_buco] * 5)
        for _, stati, _ in esiti:
            self.assertTrue((stati[az(-9):az(9), 19:23] == NON_OSSERVATO).all(), "libero dentro il buco fisso")
            self.assertTrue((stati[az(-20):az(-12), 15:27] == LIBERO).all())
            self.assertTrue((stati[az(-9):az(9), 13:17] == LIBERO).all())
            self.assertTrue((stati[az(-9):az(9), 26:30] == LIBERO).all())
        _, esiti = passa([pieno] * 3 + [con_buco] * 2 + [pieno] * 2)        # buco di 2 fotogrammi: la memoria lo copre
        for _, stati, _ in esiti[3:]:
            self.assertTrue(np.array_equal(stati, esiti[2][1]))
        _, esiti = passa([pieno] * 3 + [con_buco] * 4)                      # buco di 4: «non osservato» dal terzo
        self.assertTrue(np.array_equal(esiti[3][1], esiti[2][1]) and np.array_equal(esiti[4][1], esiti[2][1]))
        self.assertTrue((esiti[5][1][az(-9):az(9), 19:23] == NON_OSSERVATO).all())
        self.assertTrue((esiti[6][1][az(-9):az(9), 19:23] == NON_OSSERVATO).all())

    def test_p04_un_ostacolo(self):
        catena, esiti = passa([SCENA.fotogramma([(-0.25, 0.25, 2.05, 1.5)])] * 30)
        for k, (u, stati, _) in enumerate(esiti):
            occupate = np.argwhere(stati == OCCUPATO)
            self.assertIn(len(occupate), (14, 15, 16))
            self.assertTrue((occupate[:, 1] == 20).all(), "celle occupate fuori dall'anello 2,0-2,1 m")
            self.assertEqual(len(u["gruppi"]), 1)
            g = u["gruppi"][0]
            self.assertLessEqual(abs(g["x"]), 0.02)
            self.assertLessEqual(abs(g["z"] - 2.05), 0.02)
            self.assertLessEqual(abs(g["larghezza_m"] - 0.50), 0.08)
            self.assertFalse(g["tagliato"])
            colonne = np.unique(occupate[:, 0])
            dietro = stati[colonne, 21:]
            self.assertFalse((dietro == LIBERO).any(), "libero dietro il pannello")
            self.assertTrue(126 <= int((stati == IN_OMBRA).sum()) <= 144)
            self.assertEqual(int((dietro == IN_OMBRA).sum()), int((stati == IN_OMBRA).sum()))
            self.assertTrue((stati[az(-6):az(6), 13:20] == LIBERO).all(), "non libero davanti al pannello")
            self.assertEqual(len(u["tracce"]), 1)
            tr = u["tracce"][0]
            self.assertEqual(tr["stato"], "osservato" if k >= 2 else "in_conferma")
            self.assertIsNot(tr["si_muove"], True)
            self.assertLessEqual(np.hypot(tr["x"], tr["z"] - 2.05), 0.02)
        u = esiti[-1][0]
        print(f"\n  P4: {u['celle']}; gruppo {u['gruppi'][0]}; si_muove all'ultimo fotogramma: {u['tracce'][0]['si_muove']}")

    def test_p05_ostacolo_basso_con_la_sua_ombra(self):
        f = SCENA.fotogramma([(-0.2, 0.2, 1.6, 0.5)])
        _, esiti = passa([f] * 4)
        u, stati, _ = esiti[-1]
        colonne = np.unique(np.argwhere(stati == OCCUPATO)[:, 0])
        self.assertIn(len(colonne), (14, 15, 16))
        self.assertFalse((stati[colonne, 17:] == LIBERO).any(), "lettura prudente: libero dietro l'ostacolo")
        self.assertGreaterEqual(u["suolo_visto_in_ombra"], 20)
        _, esiti = passa([f] * 4, Parametri(libero_dietro_ostacolo=True))
        larga = esiti[-1][1]
        self.assertGreaterEqual(int((larga[az(-6):az(6), 28:30] == LIBERO).sum()), 22)
        self.assertFalse((larga[az(-6):az(6), 17:27] == LIBERO).any(), "libero nell'ombra vera (1,7-2,7 m)")
        self.assertTrue((larga[az(-6):az(6), 17:27] == IN_OMBRA).all())
        print(f"\n  P5: suolo visto dentro l'ombra (lettura prudente): {u['suolo_visto_in_ombra']} celle; "
              f"con l'interruttore: {int((larga[az(-6):az(6), 28:30] == LIBERO).sum())} libere su 24 oltre 2,8 m")

    def test_portata_configurabile(self):
        _, esiti = passa([SCENA.fotogramma([(-0.25, 0.25, 2.55, 1.5)])] * 2, Parametri(portata_m=2.0))
        u, stati, _ = esiti[-1]
        self.assertEqual(stati.shape, (180, 20))
        self.assertEqual(u["celle"]["occupato"], 0, "un ostacolo oltre la portata non entra nella griglia")
        self.assertEqual(u["celle"]["in_ombra"], 0)


class ProvaInseguimento(unittest.TestCase):
    def test_p06_un_oggetto_che_attraversa(self):
        xs = [-1.5 + k / FPS for k in range(46)]
        _, esiti = passa([SCENA.fotogramma([sagoma(x, 2.2)]) for x in xs])
        ids = set()
        errori = []
        for k, (u, _, _) in enumerate(esiti):
            self.assertEqual(len(u["tracce"]), 1)
            tr = u["tracce"][0]
            ids.add(tr["id"])
            self.assertEqual(tr["stato"], "osservato" if k >= 2 else "in_conferma")
            if k >= 7:
                self.assertIs(tr["si_muove"], True, f"fotogramma {k}")
            if k >= 10:
                errori.append(float(np.hypot(tr["x"] - xs[k], tr["z"] - 2.2)))
        self.assertEqual(len(ids), 1)
        self.assertLessEqual(max(errori), 0.03)
        ultima = esiti[-1][0]["tracce"][0]
        self.assertLessEqual(abs(ultima["vx"] - 1.0), 0.1)
        self.assertLessEqual(abs(ultima["vz"]), 0.1)
        primo_moto = next(k for k, (u, _, _) in enumerate(esiti) if u["tracce"][0]["si_muove"])
        print(f"\n  P6: «si muove» dal fotogramma {primo_moto}; errore massimo del centro {max(errori) * 100:.1f} cm; "
              f"velocità finale ({ultima['vx']:.3f}; {ultima['vz']:.3f}) m/s")

    def test_p06b_fermo_tagliato_da_un_ombra(self):
        fermo = (0.3, 0.9, 2.7, 1.7)
        xs = [-1.5 + k / FPS for k in range(46)]
        _, esiti = passa([SCENA.fotogramma([fermo, sagoma(x, 2.2)]) for x in xs])
        id_fermo = traccia_vicina(esiti[5][0], 0.6, 2.7)
        self.assertIsNotNone(id_fermo)
        tagliati = 0
        for u, _, _ in esiti:
            tr = traccia(u, id_fermo)
            self.assertIsNotNone(tr, "il pannello fermo ha perso la sua identità")
            self.assertIsNot(tr["si_muove"], True)
            tagliati += tr["misura_tagliata"]
        self.assertGreater(tagliati, 0, "la prova non ha mai tagliato il pannello: è cieca")
        self.assertEqual(traccia(esiti[-1][0], id_fermo)["stato"], "osservato")
        print(f"\n  P6b: pannello fermo con misura tagliata in {tagliati} fotogrammi su {len(esiti)}, mai «si muove»")

    def test_p11_ungherese(self):
        import itertools
        gen = np.random.default_rng(11)
        for _ in range(200):
            n, m = (int(v) for v in gen.integers(1, 7, size=2))
            c = gen.random((n, m))
            coppie = ungherese(c)
            self.assertEqual(len(coppie), min(n, m))
            costo = sum(c[i, j] for i, j in coppie)
            if n <= m:
                minimo = min(sum(c[i, p[i]] for i in range(n)) for p in itertools.permutations(range(m), n))
            else:
                minimo = min(sum(c[p[j], j] for j in range(m)) for p in itertools.permutations(range(n), m))
            self.assertAlmostEqual(costo, minimo, places=9)
        from scipy.optimize import linear_sum_assignment               # altro autore
        for _ in range(200):
            n, m = (int(v) for v in gen.integers(1, 13, size=2))
            c = gen.random((n, m))
            righe, colonne = linear_sum_assignment(c)
            self.assertAlmostEqual(sum(c[i, j] for i, j in ungherese(c)), float(c[righe, colonne].sum()), places=9)

    def test_p12_kalman_e_predittore(self):
        par = Parametri()
        kf = Kalman(0.5, 2.0, np.diag([1e-4, 4e-4]), 0.3)
        kf.x[2:] = [1.0, -0.2]
        ingresso = StatoIngresso(1, 0.0, kf.x.copy(), kf.p.copy(), (0.5, 2.0, 0.0), 0.4, np.zeros((1, 1), bool))
        pred = PredittoreVelocitaCostante(ingresso, par)
        for k in range(1, 31):
            kf.predici(1 / FPS, par.q)
        prev = pred.passo(30 / FPS, None, None)
        self.assertLess(abs(prev.x - kf.x[0]) + abs(prev.z - kf.x[1]), 1e-9)
        self.assertLess(float(np.abs(prev.p - kf.p[:2, :2]).max()), 1e-9)
        self.assertAlmostEqual(rumore_processo(2.0, 0.2)[0, 0], 0.2 * 8 / 3, places=12)
        fermo = Kalman(0.0, 2.0, np.eye(2) * 1e-4, 0.0)                 # velocità nota: P(t) = P0 + q t^3 / 3
        fermo.predici(2.0, 0.2)
        self.assertAlmostEqual(fermo.p[0, 0], 1e-4 + 0.2 * 8 / 3, places=12)


class ProvaOcclusione(unittest.TestCase):
    """Geometria della demo del nucleo: pannello largo 1 m a 1,9 m, sagoma sulla linea a 2,3 m, a 1 m/s."""

    def passaggio(self, xs, par=None, z=2.3, altri=lambda k: []):
        """xs: la x della sagoma a ogni fotogramma (None = resta solo il pavimento). `nascosta` è la verità sulla
        visibilità: il fotogramma è identico, pixel per pixel, a quello senza la sagoma."""
        fotogrammi, nascosta = [], []
        for k, x in enumerate(xs):
            if x is None:
                fotogrammi.append(SCENA.fotogramma())
                nascosta.append(False)
                continue
            fotogrammi.append(SCENA.fotogramma([PANNELLO_DEMO, sagoma(x, z)] + altri(k)))
            nascosta.append(np.array_equal(fotogrammi[-1], SCENA.fotogramma([PANNELLO_DEMO] + altri(k))))
        catena, esiti = passa(fotogrammi, par)
        return catena, esiti, nascosta

    def test_p07_passaggio_dietro_il_pannello(self):
        xs = [-1.6 + k / FPS for k in range(49)]
        catena, esiti, nascosta = self.passaggio(xs)
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        id_pannello = traccia_vicina(esiti[5][0], 0.0, 1.9)
        self.assertIsNotNone(id_sagoma)
        self.assertGreater(sum(nascosta), 8)
        stati_nascosta = []
        for k, (u, _, presenza) in enumerate(esiti):
            self.assertIsNot(traccia(u, id_pannello)["si_muove"], True)
            if nascosta[k]:
                tr = traccia(u, id_sagoma)
                self.assertIsNotNone(tr)
                self.assertIn(tr["stato"], ("previsto", "perso"), f"fotogramma {k}")
                stati_nascosta.append(tr["stato"])
                self.assertEqual(len(u["possibili_presenze"]), 1)
                self.assertTrue(presenza[catena.griglia.cella(xs[k], 2.3)], "centro vero fuori dallo strato")
        ultimo = traccia(esiti[-1][0], id_sagoma)
        self.assertIsNotNone(ultimo, "identità non conservata")
        self.assertEqual(ultimo["stato"], "osservato")
        self.assertLessEqual(np.hypot(ultimo["x"] - xs[-1], ultimo["z"] - 2.3), 0.05)
        riagganci = eventi(esiti, "riaggancio")
        persi = eventi(esiti, "perso")
        self.assertEqual(len(riagganci), 1)
        self.assertEqual(riagganci[0][1]["id"], id_sagoma)
        self.assertEqual(len(persi), 1, "previsto → perso non avvenuto prima della ricomparsa")
        self.assertLess(persi[0][0], riagganci[0][0])
        self.assertTrue(0.2 <= persi[0][1]["previsto_s"] <= 0.8, persi)
        self.assertEqual(eventi(esiti, "chiusura"), [])
        tagliate = sum(traccia(u, id_sagoma)["misura_tagliata"] for u, _, _ in esiti)
        self.assertGreater(tagliate, 0)
        print(f"\n  P7: nascosta {sum(nascosta)} fotogrammi ({stati_nascosta.count('previsto')} «previsto», "
              f"{stati_nascosta.count('perso')} «perso»); misure tagliate {tagliate}; perso dopo "
              f"{persi[0][1]['previsto_s']} s; riaggancio {riagganci[0][1]}; "
              f"prima misura piena {[e for _, e in eventi(esiti, 'prima_misura_piena')]}")

    def test_p07n_fascia_zero_deve_fallire(self):
        xs = [-1.6 + k / FPS for k in range(49)]
        _, esiti, _ = self.passaggio(xs, Parametri(fascia_m=0.0))
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        self.assertIsNone(traccia(esiti[-1][0], id_sagoma), "con la fascia a 0 l'identità si conserva: P7 è cieca")
        print(f"\n  P7n: fascia 0 → eventi {[(k, e['tipo']) for k, e in eventi(esiti, 'chiusura') + eventi(esiti, 'ingresso_in_ombra')]}")

    def test_p08_sosta_dietro_il_pannello(self):
        xs = [-1.6 + k / FPS for k in range(25)] + [0.0] * 75 + [k / FPS for k in range(1, 25)]
        catena, esiti, nascosta = self.passaggio(xs)
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        celle, eta = [], []
        for k, (u, stati, presenza) in enumerate(esiti):
            if nascosta[k]:
                self.assertEqual(len(u["possibili_presenze"]), 1, f"strato spento al fotogramma {k}")
                celle.append(u["possibili_presenze"][0]["celle"])
                eta.append(u["possibili_presenze"][0]["eta_s"])
                cella = catena.griglia.cella(xs[k], 2.3)
                self.assertNotEqual(stati[cella], LIBERO)
                self.assertTrue(presenza[cella])
        self.assertEqual(len(set(celle)), 1, "lo strato ha cambiato numero di celle")
        self.assertGreater(eta[-1], 5.0)
        self.assertTrue(all(b > a for a, b in zip(eta, eta[1:])))
        fine_sosta = max(k for k in range(len(xs)) if nascosta[k])
        self.assertEqual(traccia(esiti[fine_sosta][0], id_sagoma)["stato"], "perso")
        self.assertNotIn("x", traccia(esiti[fine_sosta][0], id_sagoma), "«perso» non porta posizione")
        dopo = traccia(esiti[-1][0], id_sagoma)
        scarto_tagliata = [float(np.hypot(tr["x"] - xs[k], tr["z"] - 2.3)) for k, (u, _, _) in enumerate(esiti)
                           for tr in [traccia(u, id_sagoma)] if k > fine_sosta and tr and tr["misura_tagliata"]]
        print(f"\n  P8: dopo il riaggancio, {len(scarto_tagliata)} fotogrammi «osservato» con misura tagliata: il filtro "
              f"(non aggiornato, C6) dista dalla verità fino a {max(scarto_tagliata):.2f} m")
        print(f"  P8: strato acceso {len(celle)} fotogrammi, {celle[0]} celle, età finale {eta[-1]} s; dopo la sosta "
              f"l'identità {'si conserva' if dopo else 'NON si conserva'}; riaggancio "
              f"{[e for _, e in eventi(esiti, 'riaggancio')]}")

    def test_p17_niente_riaggancio_lontano_dall_ombra(self):
        xs = [-1.6 + k / FPS for k in range(25)] + [0.0] * 20
        _, esiti, nascosta = self.passaggio(xs, altri=lambda k: [sagoma(1.5, 2.2)] if k >= 30 else [])
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        self.assertTrue(all(nascosta[25:]))
        self.assertEqual(eventi(esiti, "riaggancio"), [])
        self.assertEqual(eventi(esiti, "identita_ambigua"), [])
        u = esiti[-1][0]
        seconda = traccia_vicina(u, 1.5, 2.2)
        self.assertIsNotNone(seconda)
        self.assertNotEqual(seconda, id_sagoma)
        self.assertIn(traccia(u, id_sagoma)["stato"], ("previsto", "perso"))
        self.assertEqual([p["id_traccia"] for p in u["possibili_presenze"]], [id_sagoma])

    def test_p18_niente_riaggancio_al_bordo_della_portata(self):
        xs = [-1.05 + k / FPS for k in range(32)] + [-1.05 + 31 / FPS] * 5
        _, esiti, nascosta = self.passaggio(xs, z=2.7)
        id_sagoma = traccia_vicina(esiti[1][0], xs[1], 2.7)
        self.assertIsNotNone(id_sagoma)
        self.assertGreater(sum(nascosta), 8)
        self.assertEqual(eventi(esiti, "riaggancio"), [])
        ambigue = eventi(esiti, "identita_ambigua")
        self.assertGreater(len(ambigue), 0)
        self.assertTrue(all("portata" in e["motivo"] for _, e in ambigue), ambigue)
        u = esiti[-1][0]
        nuova = traccia_vicina(u, xs[-1], 2.7)
        self.assertIsNotNone(nuova)
        self.assertNotEqual(nuova, id_sagoma)
        self.assertIn(traccia(u, id_sagoma)["stato"], ("previsto", "perso"))
        self.assertEqual([p["id_traccia"] for p in u["possibili_presenze"]], [id_sagoma])
        print(f"\n  P18: linea a 2,7 m: {len(ambigue)} eventi «identità ambigua» (bordo della portata), identità "
              f"{id_sagoma} → {nuova}, la traccia {id_sagoma} resta «{traccia(u, id_sagoma)['stato']}»")

    def test_p19_affidabilita_persa_su_un_buco(self):
        fotogrammi = ([SCENA.fotogramma([sagoma(0.0, 2.2)])] * 6
                      + [SCENA.fotogramma(buco=(-12.0, 12.0, 1.9, 2.6))] * 6 + [SCENA.fotogramma()] * 5)
        _, esiti = passa(fotogrammi)
        ident = esiti[5][0]["tracce"][0]["id"]
        stati = [(traccia(u, ident) or {"stato": None})["stato"] for u, _, _ in esiti]
        self.assertEqual(stati[6:12], ["affidabilita_persa"] * 6)
        self.assertEqual(stati[12:], ["non_confermato"] * 3 + [None, None])
        self.assertEqual([k for k, _ in eventi(esiti, "chiusura")], [15])
        self.assertTrue(all(u["possibili_presenze"] == [] for u, _, _ in esiti))

    def test_p09_sparizione_in_campo_aperto(self):
        fotogrammi = [SCENA.fotogramma([sagoma(-0.5 + k / FPS, 2.2)]) for k in range(15)] + [SCENA.fotogramma()] * 6
        _, esiti = passa(fotogrammi)
        ident = esiti[14][0]["tracce"][0]["id"]
        for u, _, _ in esiti:
            self.assertEqual(u["possibili_presenze"], [])
        self.assertEqual([traccia(u, ident)["stato"] for u, _, _ in esiti[15:18]], ["non_confermato"] * 3)
        self.assertIsNone(traccia(esiti[18][0], ident))
        self.assertEqual(eventi(esiti, "chiusura"), [(18, {"tipo": "chiusura", "id": ident, "motivo": "non_piu_rilevato"})])

    def test_p10_rilascio_cella_per_cella(self):
        xs = [-1.6 + k / FPS for k in range(25)] + [None] * 5
        _, esiti, _ = self.passaggio(xs)
        self.assertEqual(len(esiti[24][0]["possibili_presenze"]), 1)
        self.assertEqual([len(u["possibili_presenze"]) for u, _, _ in esiti[25:]], [1, 1, 0, 0, 0])
        finiti = eventi(esiti, "strato_finito")
        self.assertEqual(len(finiti), 1)
        self.assertEqual((finiti[0][0], finiti[0][1]["motivo"]), (27, "celle_libere"))

    def test_p21_fumo_con_rumore(self):
        """Rumore indipendente per pixel e buchi a caso: NON è un modello di sensore, serve a esercitare i rami."""
        gen = np.random.default_rng(21)
        xs = [-1.6 + k / FPS for k in range(49)]
        solo_pannello = SCENA.fotogramma([PANNELLO_DEMO])
        fotogrammi, nascosta = [], []
        for x in xs:
            pulito = SCENA.fotogramma([PANNELLO_DEMO, sagoma(x)])
            nascosta.append(np.array_equal(pulito, solo_pannello))
            z = pulito.astype(np.float64) / 1000.0
            z = z + gen.normal(size=z.shape) * 0.00377 * z * z
            z[(pulito == 0) | (gen.random(z.shape) < 0.02)] = 0.0
            fotogrammi.append(np.clip(np.round(z * 1000.0), 0, 65535).astype(np.uint16))
        _, esiti = passa(fotogrammi)
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        self.assertIsNotNone(id_sagoma)
        for k, (u, _, _) in enumerate(esiti):
            if nascosta[k]:
                self.assertFalse(any(tr["stato"] == "osservato" and abs(tr["ultima_misura"][1] - 2.3) < 0.2
                                     and tr["ultima_misura"][2] == u["t"] for tr in u["tracce"]), f"fotogramma {k}")
        ultimo = esiti[-1][0]
        nate = len(eventi(esiti, "nascita"))
        confermate = len(eventi(esiti, "conferma"))
        celle = {n: round(sum(u["celle"][n] for u, _, _ in esiti) / len(esiti)) for n in ultimo["celle"]}
        print(f"\n  P21 (fumo): celle medie {celle}; tracce nate {nate}, confermate {confermate}; identità della sagoma "
              f"{'conservata' if traccia(ultimo, id_sagoma) else 'NON conservata'}; eventi "
              f"{sorted(set(e['tipo'] for u, _, _ in esiti for e in u['eventi']))}; "
              f"celle ambigue medie {sum(u['celle_ambigue'] for u, _, _ in esiti) / len(esiti):.1f}")

    def test_parametri_non_predefiniti(self):
        """Fumo: i parametri che le altre prove lasciano al valore predefinito non rompono la catena."""
        par = Parametri(curva_rumore="torneo", sigma_min_m=0.02, fattore_media_moto=0.577, min_celle_gruppo=2,
                        pendenti_ambito="ombra", min_celle_altro_bordo=3, q=1.0, settore_gradi=15.0)
        xs = [-1.6 + k / FPS for k in range(49)]
        _, esiti, _ = self.passaggio(xs, par)
        id_sagoma = traccia_vicina(esiti[5][0], xs[5], 2.3)
        self.assertEqual(traccia(esiti[-1][0], id_sagoma)["stato"], "osservato")
        self.assertEqual(len(esiti[-1][0]["settori"]), 12)

    def test_p16_costo(self):
        xs = [-1.6 + k / FPS for k in range(49)]
        _, esiti, _ = self.passaggio(xs)
        ms = sorted(u["ms"] for u, _, _ in esiti[1:])                 # il primo ciclo paga l'avvio
        media, p95 = sum(ms) / len(ms), ms[int(np.ceil(0.95 * len(ms))) - 1]
        print(f"\n  P16: tempo per ciclo a 848×480, un filo, invarianti accesi: media {media:.2f} ms, "
              f"p95 {p95:.2f} ms, massimo {ms[-1]:.2f} ms (N = {len(ms)})")
        self.assertLess(media, 15.0)
        self.assertLess(p95, 25.0)


class ProvaCatena(unittest.TestCase):
    def test_p13_suolo_stimato_senza_posa(self):
        f = SCENA.fotogramma([(-0.25, 0.25, 2.05, 1.5)])
        senza = dict(META, posa=None)
        posa, frazione = stima_suolo([f], senza)
        self.assertLessEqual(abs(posa.altezza_m - 1.2), 0.01)
        self.assertLessEqual(abs(posa.inclinazione_gradi - 15.0), 0.3)
        _, nota = passa([f] * 3)
        _, stimata = passa([f] * 3, meta=senza, posa=posa)
        a, b = nota[-1][0]["celle"]["libero"], stimata[-1][0]["celle"]["libero"]
        self.assertLessEqual(abs(a - b) / a, 0.02)
        riassunto = esegui(SorgenteMemoria(senza, tempi(3), [f] * 3))      # P20: la stima dentro `esegui`
        self.assertTrue(riassunto["posa"]["stimata"])
        self.assertLessEqual(abs(riassunto["posa"]["altezza_m"] - 1.2), 0.01)
        self.assertLessEqual(abs(riassunto["posa"]["inclinazione_gradi"] - 15.0), 0.3)
        self.assertEqual(riassunto["fotogrammi"], 3)
        print(f"\n  P13: posa stimata {posa.altezza_m:.4f} m, {posa.inclinazione_gradi:.3f}°, rollio "
              f"{posa.rollio_gradi:.3f}° ({frazione:.0%} dei punti sul piano); libero {a} con la posa nota, {b} stimata")

    def test_p14_sequenza_dell_infrastruttura_da_riga_di_comando(self):
        with tempfile.TemporaryDirectory() as uscita:
            with open(os.devnull, "w") as muto:
                vecchio, sys.stdout = sys.stdout, muto
                try:
                    codice = riga_di_comando.main([ESEMPIO, uscita, "--salva-griglie"])
                finally:
                    sys.stdout = vecchio
            self.assertEqual(codice, 0)
            with open(os.path.join(uscita, "fotogrammi.jsonl"), encoding="utf-8") as f:
                righe = [json.loads(r) for r in f]
            with open(os.path.join(uscita, "riassunto.json"), encoding="utf-8") as f:
                riassunto = json.load(f)
            griglie = np.load(os.path.join(uscita, "griglie.npz"), allow_pickle=False)
            self.assertEqual(griglie["stati"].shape, (31, 180, 30))
            with open(os.devnull, "w") as muto:                           # P20: --ogni e -p
                vecchio, sys.stdout = sys.stdout, muto
                try:
                    riga_di_comando.main([ESEMPIO, uscita, "--ogni", "2", "-p", "portata_m=2.0"])
                finally:
                    sys.stdout = vecchio
            with open(os.path.join(uscita, "fotogrammi.jsonl"), encoding="utf-8") as f:
                self.assertEqual([json.loads(r)["indice"] for r in f], list(range(0, 31, 2)))
            with open(os.path.join(uscita, "riassunto.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["griglia"]["distanza"], 20)
        self.assertEqual(len(righe), 31)
        self.assertEqual([r["indice"] for r in righe], list(range(31)))
        self.assertEqual(riassunto["fotogrammi"], 31)
        self.assertEqual(sum(riassunto["celle_per_stato"].values()), 31 * 5400)
        print(f"\n  P14: esempio 160×120 dell'infrastruttura: {riassunto['celle_per_stato']}; eventi "
              f"{riassunto['eventi']}; tempo {riassunto['tempo_ciclo_ms']}")

    def test_p15_invarianti_forzati(self):
        vuoto = np.zeros((META["altezza"], META["larghezza"]), dtype=np.uint16)
        # (a) un difetto di memoria: lo stato ricorda 5 fotogrammi, il controllo indipendente ne ammette 3
        catena = Catena(META, Parametri())
        catena.par.memoria_fotogrammi = 5
        for k in range(3):
            catena.ciclo(k, k / FPS, SCENA.fotogramma() if k == 0 else vuoto)
        with self.assertRaises(InvarianteViolato):
            catena.ciclo(3, 3 / FPS, vuoto)
        # (b) un difetto degli stati: una traccia senza misura lasciata «osservato»
        originale = Inseguitore._senza_misura
        Inseguitore._senza_misura = lambda self, tr, *a: True
        try:
            catena = Catena(META, Parametri())
            for k in range(4):
                catena.ciclo(k, k / FPS, SCENA.fotogramma([sagoma(0.0, 2.2)]))
            with self.assertRaises(InvarianteViolato):
                catena.ciclo(4, 4 / FPS, SCENA.fotogramma())
        finally:
            Inseguitore._senza_misura = originale


if __name__ == "__main__":
    unittest.main(verbosity=2)
