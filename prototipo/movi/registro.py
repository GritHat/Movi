"""Il REGISTRO: un file JSON per riga, unico per i due modi (corto raggio e lunga portata).

Riga 1: intestazione (configurazione, dichiarazioni, griglie, ostacoli fissi). Poi una riga per fotogramma.
Ultima riga: riassunto (tabellone). Basta il registro per disegnare il video (`movi mostra`) e per il tabellone.

Coordinate: metri, in pianta; x a destra (est), y in avanti (nord), origine nel riferimento dichiarato
dall'intestazione (il sensore nel modo corto; il punto di riferimento della scena nel modo lungo); quota `q` facoltativa.
Angoli in gradi, 0 = in avanti, positivi a destra. Tempi in secondi dall'inizio.

FORMA DI UN FOTOGRAMMA (i campi con * sono obbligatori)
  tipo*          "fotogramma"
  modo*          "corto" | "lungo"
  indice*, t*    contatore del ciclo e tempo
  dichiarazioni* {dati, etichette, regole_accese, config}            (ciò che si dichiara sempre)
  verita         null | {oggetti: [{id, classe, pos: [x, y] | [x, y, q], visibile}]}   (solo in simulazione)
  sensori*       [{id, tipo, salute, causa, validi, eta_dato_s}]     salute: SALUTE
  affidabilita*  "ok" | "persa"                                      (stato del SISTEMA; persa -> griglia non osservata)
  celle*         {griglia, conteggi: {stato: n}, rle?: [[stato, n], …], per_sensore?: {id: {conteggi, rle?}}}
  settori*       [{id, azimut_gradi: [a0, a1], livello, d_m, motivo}]  livello: LIVELLI
  tracce*        [{id, classe, origine_etichetta, stato, non_vista_da_s, identita, pos, vel, regione, sensori}]
  avvisi*        [{tipo: "possibile_presenza", id_traccia, eta_s, forma}]
  eventi*        [{t, tipo, come_lo_so, traccia, settore, …}]         come_lo_so: "osservato" | "dedotto"
  tabellone      null | {dentro_la_zona: {k, n}, …}                  (cumulato fino a questo fotogramma)
  tempo_ciclo_ms

FORME (regione di previsione e avviso):
  {tipo: "cerchio", centro: [x, y], raggio_m, livello}
  {tipo: "poligono", punti: [[x, y], …], livello?}
  {tipo: "settore_anulare", azimut_gradi: [a0, a1], distanza_m: [d0, d1]}
  {tipo: "celle", griglia, indici: [i, …]}
"""
import json

STATI_CELLA = ("non_osservato", "libero", "occupato", "in_ombra")
SALUTE = ("in_salute", "degradato", "affidabilita_persa")
LIVELLI = ("visto_libero_fino_a", "attenzione", "zona_non_verificata", "affidabilita_persa")
STATI_TRACCIA = ("in_conferma", "vista", "vista_in_parte", "non_vista", "previsto_ampio", "ricomparsa")
IDENTITA = (None, "certa", "presunta", "ambigua")
ORIGINI_ETICHETTA = ("a_mano", "assente")
COME_LO_SO = ("osservato", "dedotto")
FORME = ("cerchio", "poligono", "settore_anulare", "celle")
OBBLIGATORI = ("tipo", "modo", "indice", "t", "dichiarazioni", "sensori", "affidabilita", "celle", "settori", "tracce",
               "avvisi", "eventi")

# catena di riferimento -> parole del registro (SOLUZIONE_V3 §1.6: «perso» non è uno stato: è «previsto ampio»)
_STATO_DA_CATENA = {"in_conferma": "in_conferma", "osservato": "vista", "non_confermato": "non_vista",
                    "previsto": "non_vista", "perso": "previsto_ampio",
                    "affidabilita_persa": "previsto_ampio"}     # inseguimento.py riga 218: buco sull'ultima misura
_EVENTI_OSSERVATI = ("nascita", "conferma", "riaggancio", "prima_misura_piena", "identita_ambigua")


def intestazione(cfg, griglie, riferimento, ostacoli=(), sensori=(), nota=""):
    """La prima riga del registro. `griglie`: {nome: descrizione} (polare o cartesiana) per decodificare le celle."""
    import dataclasses
    from . import PRINCIPI, VERSIONE
    return {"tipo": "intestazione", "formato": 1, "movi": VERSIONE, "modo": cfg.modo,
            "configurazione": dataclasses.asdict(cfg), "dichiarazioni": cfg.dichiarazioni(), "principi": list(PRINCIPI),
            "riferimento": riferimento, "griglie": griglie, "ostacoli": list(ostacoli), "sensori": list(sensori),
            "nota": nota}


def _forma_valida(f):
    return isinstance(f, dict) and f.get("tipo") in FORME


def valida_riga(riga):
    """Restituisce la lista degli errori di forma e di principio di una riga (vuota = valida)."""
    e = []
    if riga.get("tipo") in ("intestazione", "riassunto"):
        if riga["tipo"] == "intestazione" and "dichiarazioni" not in riga:
            e.append("intestazione senza dichiarazioni")
        return e
    for campo in OBBLIGATORI:
        if campo not in riga:
            e.append(f"manca «{campo}»")
    if e:
        return e
    d = riga["dichiarazioni"]
    for campo in ("dati", "etichette", "regole_accese", "config"):
        if campo not in d:
            e.append(f"dichiarazioni senza «{campo}»")
    if riga["affidabilita"] not in ("ok", "persa"):
        e.append("affidabilita fuori elenco")
    for s in riga["sensori"]:
        if s.get("salute") not in SALUTE:
            e.append(f"sensore {s.get('id')}: salute fuori elenco")
    conteggi = riga["celle"].get("conteggi", {})
    if set(conteggi) - set(STATI_CELLA):
        e.append("celle: stato fuori elenco")
    if riga["affidabilita"] == "persa" and (conteggi.get("libero", 0) or conteggi.get("occupato", 0)):
        e.append("PRINCIPIO: affidabilità persa ma la griglia dichiara celle libere o occupate")
    for s in riga["settori"]:
        if s.get("livello") not in LIVELLI:
            e.append(f"settore {s.get('id')}: livello fuori elenco")
        if s.get("livello") == "visto_libero_fino_a" and not (isinstance(s.get("d_m"), (int, float)) and s["d_m"] > 0):
            e.append(f"PRINCIPIO: settore {s.get('id')} «visto libero» senza la distanza fin dove è stato visto")
        if s.get("livello") == "visto_libero_fino_a" and riga["affidabilita"] == "persa":
            e.append(f"PRINCIPIO: settore {s.get('id')} «visto libero» con affidabilità persa")
    for tr in riga["tracce"]:
        if tr.get("stato") not in STATI_TRACCIA:
            e.append(f"traccia {tr.get('id')}: stato fuori elenco ({tr.get('stato')})")
        if tr.get("origine_etichetta") not in ORIGINI_ETICHETTA:
            e.append(f"traccia {tr.get('id')}: origine dell'etichetta fuori elenco")
        if tr.get("identita") not in IDENTITA:
            e.append(f"traccia {tr.get('id')}: identità fuori elenco")
        if tr.get("stato") == "previsto_ampio" and tr.get("pos") is not None:
            e.append(f"traccia {tr.get('id')}: «previsto ampio» non porta un punto")
        if tr.get("regione") is not None and not _forma_valida(tr["regione"]):
            e.append(f"traccia {tr.get('id')}: regione di forma sconosciuta")
    for a in riga["avvisi"]:
        if a.get("tipo") != "possibile_presenza" or not _forma_valida(a.get("forma")):
            e.append("avviso di forma sconosciuta")
    for ev in riga["eventi"]:
        if ev.get("come_lo_so") not in COME_LO_SO:
            e.append(f"evento {ev.get('tipo')}: manca «osservato» o «dedotto»")
    return e


def valida_sequenza(righe):
    """Controlli fra righe: (1) la prima è l'intestazione; (2) un avviso di possibile presenza non sparisce se non
    in un fotogramma con un evento «osservato» che lo giustifica o con celle rilasciate perché viste (campo
    `tolto_guardando` nell'evento). Restituisce [(indice della riga, errore), …]. DA COMPLETARE (passo 1) per (2)."""
    errori, prima = [], True
    for n, riga in enumerate(righe):
        if prima and riga.get("tipo") != "intestazione":
            errori.append((n, "la prima riga non è l'intestazione"))
        prima = False
        errori.extend((n, x) for x in valida_riga(riga))
    return errori


def da_catena(uscita, cfg, etichette=None, salute=None, griglia="polare_corto"):
    """Converte l'uscita di `Catena.ciclo` (riuso/catena/catena.py) in un fotogramma del registro. Non ricalcola
    niente: rinomina e completa. La catena usa (x, z in avanti): qui z diventa y.

    `etichette`: {id_traccia: classe} già risolte per questo fotogramma (movi.etichette). `salute`: riga del
    sensore da movi.corto.salute_sensore; se manca, il sensore esce «degradato · salute non valutata».
    Il livello dei settori qui è PRUDENTE: «attenzione» se c'è un occupato o una possibile presenza, altrimenti
    «zona non verificata»; «visto libero fino a d» lo può scrivere solo movi.livelli, che vede la griglia."""
    etichette = etichette or {}
    riaggancati = {ev["id"] for ev in uscita["eventi"] if ev.get("tipo") == "riaggancio"}
    ambigui = {ev.get("id") for ev in uscita["eventi"] if ev.get("tipo") == "identita_ambigua"}
    tracce = []
    for tr in uscita["tracce"]:
        stato = _STATO_DA_CATENA[tr["stato"]]
        if stato == "vista" and tr.get("misura_tagliata"):
            stato = "vista_in_parte"
        identita = "certa" if stato in ("vista", "vista_in_parte") else None
        if tr["id"] in riaggancati:
            stato, identita = "ricomparsa", "presunta"
        if tr["id"] in ambigui:
            identita = "ambigua"
        regione = None
        if "regione_prevista" in tr:
            r = tr["regione_prevista"]
            regione = {"tipo": "cerchio", "centro": [r["x"], r["z"]], "raggio_m": r["raggio95_m"], "livello": 0.95}
        ampio = stato == "previsto_ampio"
        classe = etichette.get(tr["id"])
        tracce.append({"id": tr["id"], "classe": classe or "non_classificato",
                       "origine_etichetta": "a_mano" if classe else "assente", "stato": stato,
                       "non_vista_da_s": tr["eta_stato_s"] if stato in ("non_vista", "previsto_ampio") else 0.0,
                       "identita": identita,
                       "pos": None if ampio or "x" not in tr else [tr["x"], tr["z"]],
                       "vel": None if "vx" not in tr else [tr["vx"], tr["vz"]],
                       "regione": regione, "sensori": ["profondita"]})
    avvisi = [{"tipo": "possibile_presenza", "id_traccia": s["id_traccia"], "eta_s": s["eta_s"],
               "forma": {"tipo": "settore_anulare", "azimut_gradi": s["azimut_gradi"], "distanza_m": s["distanza_m"]},
               "celle": s["celle"], "area_m2": s["area_m2"]} for s in uscita["possibili_presenze"]]
    settori = []
    for k, s in enumerate(uscita["settori"]):
        if s["primo_occupato_m"] is not None or s["possibile_presenza"]:
            livello, d = "attenzione", s["primo_occupato_m"]
            motivo = "occupato" if s["primo_occupato_m"] is not None else "possibile presenza"
        else:
            livello, d, motivo = "zona_non_verificata", None, "regola del libero non applicata (movi.livelli)"
        settori.append({"id": k, "azimut_gradi": s["azimut_gradi"], "livello": livello, "d_m": d, "motivo": motivo,
                        "celle": dict(zip(STATI_CELLA, s["celle"]))})
    eventi = [dict(ev, t=uscita["t"], traccia=ev.get("id"), settore=None,
                   come_lo_so="osservato" if ev.get("tipo") in _EVENTI_OSSERVATI else "dedotto")
              for ev in uscita["eventi"]]
    sensore = salute or {"id": "profondita", "tipo": "camera di profondità (simulata)", "salute": "degradato",
                         "causa": "salute non valutata", "validi": None, "eta_dato_s": 0.0}
    sensore = dict(sensore, pixel_validi=uscita["pixel_validi"])
    return {"tipo": "fotogramma", "modo": "corto", "indice": uscita["indice"], "t": uscita["t"],
            "dichiarazioni": {k: v for k, v in cfg.dichiarazioni().items()
                              if k in ("dati", "etichette", "regole_accese", "config")},
            "verita": None, "sensori": [sensore],
            "affidabilita": "persa" if sensore["salute"] == "affidabilita_persa" else "ok",
            "celle": {"griglia": griglia, "conteggi": uscita["celle"]},
            "settori": settori, "tracce": tracce, "avvisi": avvisi, "eventi": eventi, "tabellone": None,
            "tempo_ciclo_ms": uscita.get("tempo_ciclo_ms")}


def codifica_rle(stati):
    """Griglia di stati (matrice di interi 0–3, per righe) -> [[nome dello stato, quante celle di fila], …]."""
    piatti = [int(v) for v in stati.ravel()]
    fuori = []
    for v in piatti:
        if fuori and fuori[-1][0] == STATI_CELLA[v]:
            fuori[-1][1] += 1
        else:
            fuori.append([STATI_CELLA[v], 1])
    return fuori


class Scrittore:
    """Scrive il registro riga per riga; valida ogni riga prima di scriverla (una riga non valida è un difetto)."""

    def __init__(self, percorso, severo=True):
        self.f, self.severo, self.n = open(percorso, "w", encoding="utf-8"), severo, 0

    def scrivi(self, riga):
        errori = valida_riga(riga)
        if errori and self.severo:
            raise ValueError(f"riga {self.n} non valida: {errori}")
        self.f.write(json.dumps(riga, ensure_ascii=False, separators=(",", ":")) + "\n")
        self.n += 1

    def chiudi(self):
        self.f.close()


def leggi(percorso):
    """Itera sulle righe di un registro (dizionari)."""
    with open(percorso, encoding="utf-8") as f:
        for riga in f:
            if riga.strip():
                yield json.loads(riga)
