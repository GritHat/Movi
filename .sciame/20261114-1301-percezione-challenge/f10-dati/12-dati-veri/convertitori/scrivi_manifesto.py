"""Scrive 12-dati-veri/manifesto.json: l'elenco delle sequenze e delle tracce, con ciò che ciascuna permette di
misurare (ipotesi 1–6 del contratto f10) e ciò che NON permette. I numeri vengono da statistiche.json e dai meta.json.
Uso: …/ambiente/venv/bin/python -I -B scrivi_manifesto.py   (dopo statistiche_tutte.py)"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402

SQUADRA = "camera stereo attiva a 1,2 m da terra, inclinata di 15° in basso, al chiuso, fino a 3 m"
IPOTESI = {"1": "«libero» calcolato da una profondità vera (quattro stati)", "2": "errore vero della maschera d'ombra",
           "3": "rumore del centro di una persona in funzione della distanza", "4": "previsione durante l'occlusione su persone vere",
           "5": "elementi mobili e ostacoli su scene vere", "6": "costo per ciclo su CPU"}
VOCI = {
 "tum_fr3_walking_static": {
  "scena": "ufficio con scrivania; due persone sedute che si alzano e camminano; camera tenuta in mano quasi ferma",
  "permette": {"1": "sì: unica sequenza con posa nota (altezza e inclinazione per fotogramma) e pavimento in vista; il suolo torna a quota 0 entro 1 cm",
               "2": "solo descrittivo (bordi e ombre di parallasse veri, nessuna geometria vera degli ostacoli)",
               "5": "solo descrittivo (nessuna annotazione): falsi «in movimento» su mobili fermi, a camera quasi ferma",
               "6": "sì (640×480, 723 fotogrammi)"},
  "non_permette": ["sensore diverso: Kinect v1 a luce strutturata, non stereo attivo (niente banda senza dato della visione stereo, rumore diverso)",
                   "montaggio diverso: 1,42 m e 8,2° (mediana), non 1,2 m e 15°: il suolo si vede solo da circa 2,2 m",
                   "nessuna verità sulle persone: niente ipotesi 3 e 4", "la camera si sposta di 0,28 m: usare posa_per_fotogramma.csv"]},
 "realsense_stands_still": {
  "scena": "camera ferma davanti a una superficie piana a circa 0,35 m (99,6 % dei pixel validi sotto 0,5 m)",
  "permette": {"1": "solo i buchi: quota e stabilità dei pixel senza dato su stereo attivo (37 % mai validi, 6,6 % intermittenti)",
               "2": "no", "6": "sì (640×360)",
               "modello_del_sensore": "rumore nel tempo a scena ferma: scarto tipo mediano 0,36 mm a 0,35 m; scarto dal piano 1,08 mm"},
  "non_permette": ["distanza fuori dal campo d'interesse (0,35 m, non 1–3 m): il rumore a 2–3 m NON si ricava da qui",
                   "nessuna persona, nessun pavimento, posa ignota, nessuna verità", "sensore: D435i a 640×360 (modulo stereo della classe giusta, risoluzione diversa)"]},
 "realsense_stairs": {
  "scena": "una scala ripresa da vicino (mediana 0,79 m), camera probabilmente in moto (77 % dei pixel intermittenti)",
  "permette": {"1": "descrittivo: che cosa fa un suolo NON piano (gradini) e il 39 % di pixel senza dato alla regola del «libero»; la posa va stimata dai dati",
               "2": "descrittivo: bordi dei gradini su stereo attivo", "6": "sì, a 1280×720 (quattro volte i pixel di 640×360)"},
  "non_permette": ["posa ignota, nessuna verità, persone non presenti (non verificato fotogramma per fotogramma)",
                   "tempi irregolari: 18 salti, passo mediano 45,6 ms contro 33,3 nominali: non usarla per misure di velocità"]},
 "realsense_structured": {
  "scena": "scena ravvicinata (mediana 0,54 m) ripresa con un SR300",
  "permette": {"lettore": "prova che il lettore gestisce un'unità diversa (0,125 mm) e una distorsione non nulla"},
  "non_permette": ["NON è stereo attivo: SR300 a luce codificata, portata corta. Non dice niente sul sensore della squadra",
                   "posa ignota, nessuna verità, nessuna persona nota; distorsione non corretta"]},
 "princeton_child_no1": {
  "scena": "atrio con pavimento a piastrelle; un bambino cammina fra tre adulti; camera bassa e ferma (posa non documentata)",
  "permette": {"3": "solo limite superiore e solo descrittivo: dispersione del centro derivato dal riquadro, a 2–4 m",
               "5": "sì in forma descrittiva: rilevare una persona vera che cammina su un pavimento vero, contro il riquadro annotato",
               "1": "descrittivo, stimando il piano del suolo dai dati (posa ignota)", "6": "sì"},
  "non_permette": ["nessun tratto nascosto: niente ipotesi 4", "sensore diverso: Kinect v1 a luce strutturata",
                   "verità = riquadro nell'immagine: nessuna posizione metrica indipendente"]},
 "princeton_new_ex_occ4": {
  "scena": "atrio; una persona cammina ed è coperta da un'altra persona che le passa davanti; 51 fotogrammi a 15 Hz",
  "permette": {"4": "un solo caso (n = 1): 3 fotogrammi nascosti, ricomparsa dopo 0,17 s; identità alla ricomparsa fra due persone",
               "5": "descrittivo", "6": "sì"},
  "non_permette": ["un solo tratto nascosto e brevissimo: nessuna statistica", "Kinect v1; posa ignota; verità = riquadro",
                   "profondità mediana 4,3 m: solo il 16 % dei pixel validi sta entro 3 m"]},
 "princeton_face_occ5": {
  "scena": "sala studio; il bersaglio è il VISO di una persona seduta, coperto da un foglio per 14 fotogrammi (0,70 s)",
  "permette": {"4": "un solo caso (n = 1) di bersaglio fermo che sparisce e ricompare: utile per «possibile presenza», non per la previsione del moto"},
  "non_permette": ["il bersaglio non è una persona che cammina", "Kinect v1; posa ignota; verità = riquadro; 15 Hz con un salto di 200 ms"]},
 "depthtrack_human02_indoor": {
  "scena": "mensa con tavoli e sedie; più persone camminano; il bersaglio è una di loro, spesso coperta in parte dalle altre",
  "permette": {"1": "descrittivo, su STEREO ATTIVO con persone: buchi (23 % senza dato), valori lontani rumorosi (19 % dei validi oltre 10 m); posa da stimare dai dati",
               "2": "descrittivo: bordi delle persone su stereo attivo",
               "4": "identità alla ricomparsa fra persone simili: 3 tratti del tutto nascosti (0,03–0,13 s) e 332 fotogrammi di occlusione parziale; troppo brevi per l'errore di previsione",
               "5": "descrittivo: persone in moto fra sedie ferme, contro il riquadro", "6": "sì (640×360, 1740 fotogrammi)"},
  "non_permette": ["parametri della camera NON documentati: fx, fy, cx, cy sono nominali (errore laterale fino a circa il 9 %)",
                   "unità non documentata (millimetri: sostenuta dall'altezza metrica dei riquadri, mediana 1,43 m)",
                   "posa ignota; camera forse tenuta in mano (solo il 16 % dei pixel resta valido per 120 fotogrammi)",
                   "sensore: D415 (stereo attivo della stessa famiglia, base 55 mm): non è il sensore della squadra",
                   "verità = riquadro: nessuna posizione metrica indipendente; i tratti nascosti durano al più 0,13 s"]},
}
TRACCE = {
 "thor_exp1_run1": {"uso": "TARATURA (per esempio del rumore di processo q)"},
 "thor_exp3_run1": {"uso": "PROVA (dati diversi da quelli della taratura)"},
}


def main():
    base = os.path.join(comune.F10, "12-dati-veri")
    with open(os.path.join(base, "statistiche.json"), encoding="utf-8") as f:
        st = json.load(f)
    seqs = []
    for nome, v in VOCI.items():
        c = os.path.join(comune.SEQUENZE, nome)
        m = comune.leggi_meta(c)
        s = st["sequenze"][nome]
        seqs.append({
            "nome": nome, "cartella": f"sequenze/{nome}", "tipo": "sequenza del formato comune", "scena": v["scena"],
            "origine": m["origine"], "licenza": m["licenza"], "sensore": m["sensore"], "posa": m["posa"],
            "immagine": [m["larghezza"], m["altezza"]], "fps": m["fps"], "fotogrammi": s["fotogrammi"], "durata_s": s["durata_s"],
            "frequenza_mediana_hz": s["frequenza_mediana_hz"], "pixel_validi_mediana": s["pixel_validi_per_fotogramma"]["mediana"],
            "profondita_mediana_mm": s["profondita_mm"]["mediana_delle_mediane"], "quota_validi_entro_3_m": s["quota_validi_entro_3_m"],
            "verita": ("nessuna" if s["verita"] is None else {
                "tipo": "riquadro del bersaglio e visibilità (x, z derivati dalla profondità: NON indipendenti)",
                "identita": s["verita"]["identita"], "tratti_nascosti": s["verita"]["tratti_nascosti"],
                "tratti_nascosti_con_ricomparsa": s["verita"]["tratti_nascosti_con_ricomparsa"],
                "durata_tratti_s": s["verita"]["durata_tratti_con_ricomparsa_s"]}),
            "verita_sul_suolo": "posa della camera per fotogramma (cattura del moto)" if m["posa"] else "nessuna",
            "permette": v["permette"], "non_permette": v["non_permette"],
            "controllo": {"errori": len(s["controllo_infrastruttura"]["errori"]), "avvisi": s["controllo_infrastruttura"]["avvisi"]},
            "byte": s["byte_su_disco"]})
    tracce = []
    for nome, v in TRACCE.items():
        with open(os.path.join(comune.TRACCE, nome, "meta.json"), encoding="utf-8") as f:
            m = json.load(f)
        s = st["tracce"][nome]
        tracce.append({
            "nome": nome, "cartella": f"tracce/{nome}", "tipo": "tracce (NON è una sequenza: nessuna profondità)", "uso_proposto": v["uso"],
            "origine": m["origine"], "licenza": m["licenza"], "sensore": m["sensore"], "frequenza_hz": 100.0,
            "istanti": s["istanti"], "durata_s": s["durata_s"], "persone": len(s["persone"]),
            "quota_tracciata_per_persona": s["quota_tracciata_per_persona"], "tratti_continui": s["tratti_continui"],
            "velocita_m_s": s["velocita_m_s"], "verita": "posizione vera del casco a 100 Hz, identità; nessuna occlusione annotata",
            "permette": {"4": "errore della previsione in funzione del tempo d'occlusione, copertura della regione dichiarata, taratura di q su pedoni "
                              "veri, nascondendo a posteriori tratti di traiettorie vere (unità statistica: il tratto continuo, non l'istante)"},
            "non_permette": ["nessuna camera di profondità: niente rilevamento, niente rumore del sensore, niente ipotesi 1, 2, 3, 5, 6",
                             "posizioni quasi perfette della testa (casco), non del centro dell'impronta sul suolo",
                             "le occlusioni sono inventate da chi prova, non vere: la geometria dell'ostacolo va dichiarata",
                             "le persone sono tracciate solo per una parte del tempo (dal 13 % al 76 %): fuori, la posizione è ignota",
                             "a quale variante dell'esperimento corrisponde il file: non verificato"]})
    man = {
        "scritto_da": "sciame-dati (f10), 12-dati-veri/convertitori/scrivi_manifesto.py",
        "sensore_della_squadra": SQUADRA, "ipotesi_del_contratto": IPOTESI,
        "sequenze": seqs, "tracce": tracce,
        "non_convertiti": [
            {"fonte": "RGB-D People di Friburgo (terza scelta del ricercatore)", "motivo": "raggiungibile solo in http://; scarica.sh ammette solo https://: non scaricato, ripiego su Princeton e DepthTrack",
             "che_cosa_manca": "l'unica fonte con la visibilità annotata su molte tracce e camere ferme: i tratti nascosti lunghi con profondità vera"},
            {"fonte": "Princeton bear_front", "motivo": "25 tempi di profondità ripetuti su 295 e bersaglio che non è una persona"},
            {"fonte": "Princeton zcup_move_1", "motivo": "bersaglio = tazza, nessuna occlusione"}],
        "sintesi_per_ipotesi": {
            "1": ["tum_fr3_walking_static (posa nota)", "depthtrack_human02_indoor, realsense_stairs, realsense_stands_still, princeton_child_no1 (descrittivo, posa da stimare)"],
            "2": ["solo descrittivo: tum_fr3_walking_static, depthtrack_human02_indoor, realsense_stairs; nessuna fonte ha la geometria vera degli ostacoli"],
            "3": ["nessuna fonte con posizione metrica indipendente della persona: non decidibile con questi dati (solo limite superiore da princeton_child_no1)"],
            "4": ["thor_exp1_run1 (taratura), thor_exp3_run1 (prova): moto vero, occlusione inventata", "con profondità vera: 5 tratti nascosti in tutto (3 DepthTrack, 1 + 1 Princeton), da 0,03 a 0,70 s"],
            "5": ["descrittivo: tum_fr3_walking_static, princeton_child_no1, princeton_new_ex_occ4, depthtrack_human02_indoor"],
            "6": ["tutte le sequenze (640×360, 640×480, 1280×720)"]}}
    comune.salva_json(os.path.join(base, "manifesto.json"), man)
    print(f"manifesto.json: {len(seqs)} sequenze, {len(tracce)} tracce; byte delle sequenze {sum(s['byte'] for s in seqs)}")


if __name__ == "__main__":
    main()
