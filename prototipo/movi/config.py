"""Configurazione all'avvio: deterministica, letta da un file JSON, viaggia nell'intestazione del registro.

Contiene lo scenario, le classi ammesse, il profilo di chi porta il sensore, il file delle etichette a mano e gli
interruttori delle regole che «partono spente». Niente qui dentro è stimato dai dati."""
import dataclasses
import hashlib
import json
import os

from . import riuso

# Interruttori: nome -> (valore iniziale, che cosa accende, perché parte così). Fonte: SOLUZIONE_V3.md §1.1, §1.5,
# §5 e BLOCCO_CLASSIFICAZIONE.md. Tutti spenti = catena di f10 con il predittore a velocità costante.
INTERRUTTORI = {
    "correzioni_f12": (True, "le dieci correzioni di f12/06-identita (parametri.Parametri, blocco «correzioni f12»)",
                       "provate in simulazione sulle sequenze di f10"),
    "predittore_zona": (False, "regione di previsione a 400 membri (sd-1, porto in Python di insieme.c)",
                        "parte spento finché il porto non supera il confronto col banco in C"),
    "c7_identita_al_ritorno": (False, "c7 e identità presunta alla ricomparsa",
                               "SOLUZIONE_V3 §1.1: restano spente se la prova d'ingresso del rumore non passa"),
    "libero_dal_fotogramma": (False, "regola del «libero» della cella dal solo fotogramma corrente (riuso/libero)",
                              "parte spenta: senza, vale la lettura prudente della catena"),
    "fascia_di_scenario": (False, "fascia di guardia w_scen dalla velocità massima delle classi ammesse",
                           "BLOCCO_CLASSIFICAZIONE: dalla configurazione, mai da un'etichetta"),
    "regione_per_classe": (False, "la classe (a mano) sceglie il modello di moto della regione di previsione",
                           "può solo cambiare la forma della regione di previsione, mai ridurre l'avviso"),
}


@dataclasses.dataclass
class Configurazione:
    modo: str = "corto"                        # "corto" | "lungo"
    scenario: str = "sole_persone_a_piedi"     # nome dichiarato dello scenario
    sorgente: dict = dataclasses.field(default_factory=dict)   # {"tipo": "sequenza"|"simulata"|"pubblica"|"scena_lp", …}
    classi_ammesse: list = dataclasses.field(default_factory=lambda: ["persona_a_piedi"])
    profilo_portatore: str = "stazione_fissa"
    etichette: str = ""                        # file JSON delle etichette a mano ("" = nessuna etichetta)
    interruttori: dict = dataclasses.field(default_factory=dict)
    parametri: dict = dataclasses.field(default_factory=dict)  # scavalcano parametri.Parametri (corto) o quelli di movi_lp
    seme: int = 0
    origine_dati: str = "simulati"             # "simulati" | "pubblici" (con licenza e provenienza nella sorgente)

    def regole(self):
        """Tutti gli interruttori col valore effettivo (iniziale, scavalcato da `interruttori`)."""
        sconosciuti = set(self.interruttori) - set(INTERRUTTORI)
        if sconosciuti:
            raise ValueError(f"interruttori sconosciuti: {sorted(sconosciuti)}")
        return {n: bool(self.interruttori.get(n, v[0])) for n, v in INTERRUTTORI.items()}

    def impronta(self):
        """Otto cifre esadecimali della configurazione: viaggiano in ogni riga del registro."""
        testo = json.dumps(dataclasses.asdict(self), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(testo.encode("utf-8")).hexdigest()[:8]

    def dichiarazioni(self):
        """Ciò che il prototipo dichiara SEMPRE (in ogni riga del registro e in ogni immagine)."""
        regole = self.regole()
        return {"dati": self.origine_dati, "hardware": "nessun sensore fisico",
                "etichette": "a mano" if self.etichette else "assenti",
                "classificatore": "non realizzato (lavori futuri)",
                "scenario": self.scenario, "profilo_portatore": self.profilo_portatore,
                "regole_accese": sorted(n for n, v in regole.items() if v),
                "regole_spente": sorted(n for n, v in regole.items() if not v),
                "config": self.impronta()}


def carica(percorso, **scavalca):
    """Legge una configurazione JSON; controlla modo, classi ammesse e profilo contro i file dei profili riusati."""
    with open(percorso, encoding="utf-8") as f:
        dati = json.load(f)
    dati.pop("commento", None)
    dati.update({k: v for k, v in scavalca.items() if v is not None})
    cfg = Configurazione(**dati)
    if cfg.modo not in ("corto", "lungo"):
        raise ValueError(f"modo sconosciuto: {cfg.modo}")
    cfg.regole()
    classi = {c["id"] for c in profili("classi.json")["classi"]}
    mancanti = set(cfg.classi_ammesse) - classi
    if mancanti and cfg.modo == "corto":       # il modo lungo porta le sue classi (movi_lp): controllo lì
        raise ValueError(f"classi non presenti in classi.json: {sorted(mancanti)}")
    portatori = {p["id"] for p in profili("profili_portatore.json")["profili"]}
    if cfg.profilo_portatore not in portatori and cfg.modo == "corto":
        raise ValueError(f"profilo del portatore sconosciuto: {cfg.profilo_portatore}")
    if cfg.etichette and not os.path.isabs(cfg.etichette):
        cfg.etichette = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(percorso)), cfg.etichette))
    return cfg


def profili(nome):
    """Legge riuso/profili/classi.json o profili_portatore.json (valori a priori, mai stime)."""
    with open(riuso.percorso("profili", nome), encoding="utf-8") as f:
        return json.load(f)
