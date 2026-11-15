"""collauda_registro.py (sciame-tester) — validatore di forma e controllo degli invarianti del registro MoVi.

Scritto da zero dal formato dichiarato in ARCHITETTURA.md §3 e nella docstring di movi/registro.py. NON importa
movi.registro (indipendenza: condivide con il prototipo solo la specifica, non il codice). Legge solo JSON.

Uso: python -I collauda_registro.py <registro.jsonl>… [--json uscita.json]
Per ogni registro stampa: righe, errori di forma, violazioni per invariante (con esempi).
"""
import json, math, sys
from collections import Counter, defaultdict

STATI_CELLA = ("non_osservato", "libero", "occupato", "in_ombra")
SALUTE = ("in_salute", "degradato", "affidabilita_persa")
LIVELLI = ("visto_libero_fino_a", "attenzione", "zona_non_verificata", "affidabilita_persa")
STATI_TRACCIA = ("in_conferma", "vista", "vista_in_parte", "non_vista", "previsto_ampio", "ricomparsa")
VISTI = ("vista", "vista_in_parte", "ricomparsa")
IDENTITA = (None, "certa", "presunta", "ambigua")
ORIGINI = ("a_mano", "assente")
FORME = ("cerchio", "poligono", "settore_anulare", "celle")
OBBL = ("tipo", "modo", "indice", "t", "dichiarazioni", "sensori", "affidabilita", "celle", "settori", "tracce",
        "avvisi", "eventi")
NUM = (int, float)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------ forma
def forma_valida(f, dove, err):
    if not isinstance(f, dict) or f.get("tipo") not in FORME:
        err.append(f"{dove}: forma sconosciuta"); return
    t = f["tipo"]
    if t == "cerchio" and not (isinstance(f.get("centro"), list) and len(f["centro"]) >= 2
                               and isinstance(f.get("raggio_m"), NUM) and f["raggio_m"] >= 0):
        err.append(f"{dove}: cerchio senza centro o raggio_m")
    if t == "settore_anulare":
        a, d = f.get("azimut_gradi"), f.get("distanza_m")
        if not (isinstance(a, list) and len(a) == 2 and isinstance(d, list) and len(d) == 2 and d[0] <= d[1]):
            err.append(f"{dove}: settore anulare malformato")
    if t == "poligono" and not (isinstance(f.get("punti"), list) and len(f["punti"]) >= 3):
        err.append(f"{dove}: poligono con meno di 3 punti")
    if t == "celle" and not isinstance(f.get("indici"), list):
        err.append(f"{dove}: celle senza indici")


def valida_forma(righe):
    err = []
    if not righe or righe[0].get("tipo") != "intestazione":
        err.append((0, "prima riga non è l'intestazione")); return err
    h = righe[0]
    for c in ("formato", "modo", "dichiarazioni", "griglie", "riferimento"):
        if c not in h:
            err.append((0, f"intestazione senza «{c}»"))
    if righe[-1].get("tipo") != "riassunto":
        err.append((len(righe) - 1, "ultima riga non è il riassunto"))
    prec_i, prec_t = None, None
    for n, r in enumerate(righe[1:], 1):
        if r.get("tipo") == "riassunto":
            if n != len(righe) - 1:
                err.append((n, "riassunto non in fondo"))
            continue
        if r.get("tipo") != "fotogramma":
            err.append((n, f"tipo sconosciuto {r.get('tipo')}")); continue
        e = []
        for c in OBBL:
            if c not in r:
                e.append(f"manca {c}")
        if e:
            err.extend((n, x) for x in e); continue
        if r["modo"] not in ("corto", "lungo") or r["modo"] != h.get("modo"):
            e.append("modo fuori elenco o diverso dall'intestazione")
        if not isinstance(r["indice"], int) or not isinstance(r["t"], NUM):
            e.append("indice/t non numerici")
        else:
            if prec_i is not None and (r["indice"] <= prec_i or r["t"] < prec_t):
                e.append(f"indice/t non crescenti ({prec_i},{prec_t})->({r['indice']},{r['t']})")
            prec_i, prec_t = r["indice"], r["t"]
        d = r["dichiarazioni"]
        for c in ("dati", "etichette", "regole_accese", "config"):
            if c not in d:
                e.append(f"dichiarazioni senza {c}")
        if r.get("verita") is not None:
            for o in r["verita"].get("oggetti", []):
                if not ({"id", "pos", "visibile"} <= set(o)):
                    e.append("oggetto vero senza id/pos/visibile")
        for s in r["sensori"]:
            if s.get("salute") not in SALUTE or "id" not in s:
                e.append(f"sensore {s.get('id')}: salute fuori elenco")
        if r["affidabilita"] not in ("ok", "persa"):
            e.append("affidabilità fuori elenco")
        c = r["celle"]
        if "griglia" not in c or not isinstance(c.get("conteggi"), dict) or set(c["conteggi"]) - set(STATI_CELLA):
            e.append("celle malformate")
        elif c.get("griglia") not in h.get("griglie", {}):
            e.append("celle: griglia non dichiarata nell'intestazione")
        if "rle" in c:
            if any(s not in STATI_CELLA or not isinstance(k, int) or k <= 0 for s, k in c["rle"]):
                e.append("rle malformato")
            tot = sum(k for _, k in c["rle"])
            g = h["griglie"].get(c.get("griglia"), {})
            atteso = g.get("n_azimut", 0) * g.get("n_distanza", 0) if g.get("tipo") == "polare" else \
                (g["n"][0] * g["n"][1] if "n" in g else None)
            if atteso and tot != atteso:
                e.append(f"rle di {tot} celle, griglia di {atteso}")
        for s in r["settori"]:
            if s.get("livello") not in LIVELLI:
                e.append(f"settore {s.get('id')}: livello fuori elenco")
            if s.get("livello") == "visto_libero_fino_a" and not (isinstance(s.get("d_m"), NUM) and s["d_m"] > 0):
                e.append(f"settore {s.get('id')}: visto libero senza d_m")
        for t in r["tracce"]:
            for k in ("id", "classe", "origine_etichetta", "stato", "non_vista_da_s", "identita", "pos", "regione",
                      "sensori"):
                if k not in t:
                    e.append(f"traccia {t.get('id')}: manca {k}")
            if t.get("stato") not in STATI_TRACCIA:
                e.append(f"traccia {t.get('id')}: stato {t.get('stato')}")
            if t.get("origine_etichetta") not in ORIGINI:
                e.append(f"traccia {t.get('id')}: origine {t.get('origine_etichetta')}")
            if t.get("identita") not in IDENTITA:
                e.append(f"traccia {t.get('id')}: identità {t.get('identita')}")
            if t.get("stato") == "previsto_ampio" and t.get("pos") is not None:
                e.append(f"traccia {t.get('id')}: previsto ampio con un punto")
            if t.get("regione") is not None:
                forma_valida(t["regione"], f"regione traccia {t.get('id')}", e)
        ids = {t.get("id") for t in r["tracce"]}
        for a in r["avvisi"]:
            if a.get("tipo") != "possibile_presenza":
                e.append("avviso di tipo sconosciuto")
            forma_valida(a.get("forma"), f"avviso {a.get('id_traccia')}", e)
            if a.get("id_traccia") not in ids:
                e.append(f"avviso della traccia {a.get('id_traccia')} che non è fra le tracce")
        for ev in r["eventi"]:
            if "tipo" not in ev or "t" not in ev:
                e.append("evento senza tipo o t")
        err.extend((n, x) for x in e)
    return err


# ------------------------------------------------------------------ geometria
def dentro_forma(f, p, h):
    x, y = p[0], p[1]
    t = f.get("tipo")
    if t == "cerchio":
        return math.hypot(x - f["centro"][0], y - f["centro"][1]) <= f["raggio_m"]
    if t == "settore_anulare":
        az = math.degrees(math.atan2(x, y)); d = math.hypot(x, y)
        a0, a1 = f["azimut_gradi"]; d0, d1 = f["distanza_m"]
        return a0 <= az <= a1 and d0 <= d <= d1
    if t == "poligono":
        return dentro_poligono(f["punti"], x, y)
    if t == "celle":
        i = indice_cella(h, f.get("griglia"), p)
        return i is not None and i in set(f["indici"])
    return False


def dentro_poligono(pts, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def indice_cella(h, nome, p):
    g = h["griglie"].get(nome)
    if not g:
        return None
    x, y = p[0], p[1]
    if g["tipo"] == "polare":
        az = math.degrees(math.atan2(x, y)); d = math.hypot(x, y)
        ia = int(math.floor((az + g["azimut_max_gradi"]) / g["passo_azimut_gradi"]))
        ir = int(math.floor(d / g["passo_distanza_m"]))
        if not (0 <= ia < g["n_azimut"] and 0 <= ir < g["n_distanza"]):
            return None
        return ia * g["n_distanza"] + ir
    # cartesiana: campioni nei punti di linspace (movi/lungo.py _Osservatore.pianta), righe = y
    (x0, x1), (y0, y1), (nx, ny) = g["x"], g["y"], g["n"]
    i = round((x - x0) / (x1 - x0) * (nx - 1)); j = round((y - y0) / (y1 - y0) * (ny - 1))
    if not (0 <= i < nx and 0 <= j < ny):
        return None
    return j * nx + i


def decodifica(rle):
    out = []
    for s, k in rle:
        out.extend([s] * k)
    return out


# ------------------------------------------------------------------ invarianti
def invarianti(righe):
    h = righe[0]
    corto = h.get("modo") == "corto"
    vic = 0.6 if corto else 150.0          # ipotesi: distanza entro cui una traccia «segue» un oggetto vero
    V = Counter(); es = defaultdict(list); M = Counter()
    fr = [r for r in righe if r.get("tipo") == "fotogramma"]
    eti_cfg = (h.get("dichiarazioni") or {}).get("etichette")
    seguiti, accesi_prima, salute_prima, tracce_prima, ultima_rle = set(), {}, {}, {}, None

    def viol(k, r, msg):
        V[k] += 1
        if len(es[k]) < 3:
            es[k].append(f"indice {r['indice']} t={r['t']}: {msg}")

    for r in fr:
        ver = (r.get("verita") or {}).get("oggetti", [])
        rle = r["celle"].get("rle")
        stati = decodifica(rle) if rle else None
        gnome = r["celle"].get("griglia")
        persa = r["affidabilita"] == "persa"
        # I1 libero dove c'è un oggetto vero / dove non osservato
        if stati:
            for o in ver:
                i = indice_cella(h, gnome, o["pos"])
                if i is not None and i < len(stati) and stati[i] == "libero":
                    viol("I1a_cella_libera_su_oggetto_vero", r, f"{o['id']} in cella {i} «libero»"
                         + ("" if o.get("visibile") else " (oggetto NASCOSTO)"))
            if persa and any(s in ("libero", "occupato") for s in stati):
                viol("I1b_rle_libero_con_affidabilita_persa", r, "griglia intera con celle libere/occupate")
        for s in r["settori"]:
            if s["livello"] == "visto_libero_fino_a":
                if persa:
                    viol("I1c_settore_libero_con_affidabilita_persa", r, f"settore {s['id']}")
                a = s.get("azimut_gradi")
                for o in ver:
                    if a:
                        az = math.degrees(math.atan2(o["pos"][0], o["pos"][1])); d = math.hypot(*o["pos"][:2])
                        if a[0] <= az < a[1] and d <= s["d_m"]:
                            viol("I1d_settore_visto_libero_su_oggetto_vero", r, f"{o['id']} a {d:.2f} m, settore {s['id']} libero fino a {s['d_m']}")
        # I2 oggetto seguito e nascosto: avviso che lo contiene; regione o previsto ampio
        tr_vis = [t for t in r["tracce"] if t["stato"] in VISTI and t.get("pos")]
        for o in ver:
            if o.get("visibile"):
                if any(math.hypot(t["pos"][0] - o["pos"][0], t["pos"][1] - o["pos"][1]) <= vic for t in tr_vis):
                    seguiti.add(o["id"])
                continue
            if o["id"] not in seguiti:
                continue
            M["nascosti_seguiti"] += 1
            if not r["avvisi"]:
                viol("I2a_nascosto_seguito_senza_alcun_avviso", r, o["id"])
            elif any(dentro_forma(a["forma"], o["pos"], h) for a in r["avvisi"]):
                M["nascosti_dentro_avviso"] += 1
            if not any(t["stato"] == "previsto_ampio" or (t["stato"] in ("non_vista",) and t.get("regione"))
                       for t in r["tracce"]):
                viol("I2b_nascosto_senza_regione_ne_previsto_ampio", r, o["id"])
        # I3 avviso non si spegne senza osservazione (indipendente dal campo «tolto_guardando»)
        ora = {a["id_traccia"] for a in r["avvisi"]}
        oss = {ev.get("traccia") for ev in r["eventi"] if ev.get("come_lo_so") == "osservato"}
        stato_ora = {t["id"]: t["stato"] for t in r["tracce"]}
        for i in accesi_prima:
            if i not in ora and i not in oss and stato_ora.get(i) not in VISTI:
                viol("I3_avviso_spento_senza_osservazione", r, f"traccia {i} (stato ora {stato_ora.get(i)})")
        accesi_prima = ora
        # I4 «vista» senza misura nel ciclo (sostituto: un sensore in salute fra i suoi; se c'è la verità, un oggetto vero vicino)
        salute = {s["id"]: s["salute"] for s in r["sensori"]}
        for t in r["tracce"]:
            if t["stato"] in VISTI:
                if t.get("pos") is None:
                    viol("I4a_vista_senza_posizione", r, f"traccia {t['id']}")
                ss = [salute.get(s) for s in t.get("sensori") or []]
                if persa or (ss and all(x == "affidabilita_persa" for x in ss)):
                    viol("I4b_vista_con_i_suoi_sensori_persi", r, f"traccia {t['id']}")
                if ver and t.get("pos") and not any(math.hypot(t["pos"][0] - o["pos"][0], t["pos"][1] - o["pos"][1]) <= vic for o in ver):
                    M["viste_lontane_dal_vero"] += 1      # falso ritorno: misura, non violazione di principio
                M["viste"] += 1
                # I4c: l'unico oggetto vero vicino è NASCOSTO a tutti i sensori, eppure la traccia è «vista»
                if ver and t.get("pos"):
                    vicini = [o for o in ver if math.hypot(t["pos"][0] - o["pos"][0], t["pos"][1] - o["pos"][1]) <= vic]
                    if vicini and all(not o.get("visibile") for o in vicini):
                        viol("I4c_vista_mentre_l_oggetto_vero_e_nascosto", r,
                             f"traccia {t['id']} {t['stato']} vicino a {[o['id'] for o in vicini]} nascosto")
        # I5 eventi
        for ev in r["eventi"]:
            if ev.get("come_lo_so") not in ("osservato", "dedotto"):
                viol("I5_evento_senza_come_lo_so", r, ev.get("tipo"))
        # I6 etichette
        for t in r["tracce"]:
            cl = t.get("classe")
            if t["origine_etichetta"] == "a_mano" and eti_cfg in ("nessuna", "assenti"):
                viol("I6a_etichetta_a_mano_con_etichette_spente", r, f"traccia {t['id']}")
            if cl not in (None, "non_classificato") and t["origine_etichetta"] != "a_mano":
                viol("I6b_classe_senza_origine_a_mano", r, f"traccia {t['id']} classe {cl}")
            if t["origine_etichetta"] == "a_mano" and cl in (None, "non_classificato"):
                viol("I6c_a_mano_senza_classe", r, f"traccia {t['id']}")
        # I7 sensore spento: evento «affidabilità persa» alla transizione; settori non «visto libero»
        for sid, sa in salute.items():
            if sa == "affidabilita_persa" and salute_prima.get(sid) != "affidabilita_persa":
                M["transizioni_persa"] += 1
                if not any("affidabilita" in str(ev.get("tipo")) for ev in r["eventi"]):
                    viol("I7a_sensore_perso_senza_evento", r, sid)
            if sa == "affidabilita_persa":
                for s in r["settori"]:
                    if (s["id"] == sid or len(salute) == 1) and s["livello"] not in ("affidabilita_persa", "zona_non_verificata"):
                        viol("I7b_settore_del_sensore_perso_non_dice_non_verificata", r, f"{sid}: {s['livello']}")
            if sa != "affidabilita_persa" and salute_prima.get(sid) == "affidabilita_persa":
                M["ritorni_sensore"] += 1
        if persa:
            M["fotogrammi_persa"] += 1
            if any(s["livello"] not in ("affidabilita_persa", "zona_non_verificata") for s in r["settori"]):
                viol("I7c_sistema_perso_settore_non_dice_non_verificata", r, "")
        salute_prima = salute
        # I8 nessuna etichetta riduce l'avviso: non controllabile su una riga sola (prova a coppie in prova_lunga.py L3)
    return V, es, M, len(fr)


def main(argv):
    out_json = None
    if "--json" in argv:
        k = argv.index("--json"); out_json = argv[k + 1]; argv = argv[:k] + argv[k + 2:]
    tutti = {}
    for p in argv:
        try:
            righe = [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]
        except Exception as ex:
            print(f"{p}: ILLEGGIBILE {ex}"); tutti[p] = {"illeggibile": str(ex)}; continue
        ef = valida_forma(righe)
        V, es, M, nf = invarianti(righe) if righe and righe[0].get("tipo") == "intestazione" else (Counter(), {}, Counter(), 0)
        print(f"== {p}: {len(righe)} righe, {nf} fotogrammi, errori di forma {len(ef)}")
        for n, e in ef[:5]:
            print(f"   forma riga {n}: {e}")
        for k in sorted(V):
            print(f"   {k}: {V[k]}  es. {es[k][0]}")
        if M.get("nascosti_seguiti"):
            k, n = M["nascosti_dentro_avviso"], M["nascosti_seguiti"]; lo, hi = wilson(k, n)
            print(f"   misura: nascosto seguito dentro un avviso {k}/{n} (Wilson 95% {lo:.3f}-{hi:.3f})")
        print(f"   misure: {dict(M)}")
        tutti[p] = {"righe": len(righe), "fotogrammi": nf, "forma": len(ef), "esempi_forma": ef[:5],
                    "violazioni": dict(V), "esempi": {k: v for k, v in es.items()}, "misure": dict(M)}
    if out_json:
        json.dump(tutti, open(out_json, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
