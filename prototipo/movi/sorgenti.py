"""Sorgenti di dati intercambiabili. Il nucleo non sa da dove arriva un fotogramma.

Contratto comune (`Sorgente`): `meta` (dizionario: sensori, frequenza, origine, licenza, simulato sì/no),
`verita(indice)` (None se non nota) e l'iterazione, che rende `Fotogramma(indice, t, dati)`.
  modo corto: dati = {"profondita": matrice uint16 in mm}  (formato comune, riuso/03-infrastruttura/formato_sequenza.md)
  modo lungo: dati = {id_sensore: misure del simulatore a lunga portata}  (forma fissata da movi_lp)
In più, facoltativi (solo simulazione, per il registro e le misure): `ostacoli` (pianta degli ostacoli veri) e
`ombra_vera` (la maschera polare dell'ombra vera degli ostacoli fissi, come in verita.json)."""
import dataclasses
import json
import os
import re

from . import riuso


@dataclasses.dataclass
class Fotogramma:
    indice: int
    t: float
    dati: dict


class Sorgente:
    meta: dict
    ostacoli = ()
    ombra_vera = None

    def __iter__(self):
        raise NotImplementedError

    def verita(self, indice):
        """La verità del fotogramma nella forma del registro ({oggetti: […]}) o None se non è nota."""
        return None


def _verita_registro(fot):
    """Un fotogramma di verita.json (soggetti con x, z) -> forma del registro (pos = [x, y], y in avanti)."""
    v = {"oggetti": [{"id": s["id"], "classe": "persona_a_piedi", "pos": [s["x"], s["z"]],
                      "visibile": bool(s["visibile"]), "frazione_visibile": s.get("frazione_visibile")}
                     for s in fot.get("soggetti", [])]}
    if "evento" in fot:
        v["evento"] = fot["evento"]
    return v


def _ostacoli_registro(lista):
    return [{"id": o["id"], "punti": o["vertici"], "genere": o.get("genere")} for o in lista if o.get("tipo") == "poligono"]


class SorgenteSequenza(Sorgente):
    """Una cartella nel formato comune (meta.json, tempi.csv, profondita/*.npy, verita.json facoltativo).
    Avvolge riuso/catena/sorgente.SorgenteCartella senza cambiarla. Serve sia le sequenze del simulatore
    della camera, sia una REGISTRAZIONE PUBBLICA già convertita nel formato comune (meta["origine"], meta["licenza"])."""

    def __init__(self, cartella, ogni=1, primo=0, ultimo=None):
        self._s = riuso.modulo("catena", "sorgente").SorgenteCartella(cartella, ogni, primo, ultimo)
        self.meta = self._s.meta
        self._verita = {}
        percorso = os.path.join(cartella, "verita.json")
        if os.path.exists(percorso):
            with open(percorso, encoding="utf-8") as f:
                v = json.load(f)
            self._verita = {fot["indice"]: _verita_registro(fot) for fot in v.get("fotogrammi", [])}
            self.ostacoli = _ostacoli_registro(v.get("ostacoli", []))
            self.ombra_vera = (v.get("ombra_suolo") or {}).get("polare")

    def __iter__(self):
        for indice, t, prof in self._s:
            yield Fotogramma(indice, t, {"profondita": prof})

    def verita(self, indice):
        return self._verita.get(indice)


def specifica(nome):
    """La specifica del simulatore per `nome`: una voce del catalogo, oppure un passaggio NUOVO con lo stesso schema
    di nome (`<profilo>_<nom|lim>__pannello_<caso>__s<k>`, k qualsiasi: seme del percorso e del rumore dal nome),
    oppure `…__due_persone__s<k>` (una persona ferma a destra dietro la linea, l'altra le passa davanti)."""
    C = riuso.modulo("simulatore", "catalogo")
    for s in C.catalogo():
        if s["nome"] == nome:
            return s
    m = re.fullmatch(r"(d435i|d455|g335)_(nom|lim)__(pannello_(a12|a05|b|c|d)|due_persone)__s(\d+)", nome)
    if not m:
        raise ValueError(f"scena simulata sconosciuta: {nome}")
    livello = {"nom": "nominale", "lim": "limite"}[m.group(2)]
    k = int(m.group(5))
    if m.group(3) == "due_persone":
        ferma = dict(C._ferma(0.95, 2.85), id="s2")
        return C._spec("due", m.group(1), livello, "pannello", f"due_persone__s{k:02d}",
                       persone=[C._pers("a12", k), ferma])
    return C._spec("nuovi", m.group(1), livello, "pannello", f"pannello_{m.group(4)}__s{k:02d}",
                   persone=[C._pers(m.group(4), k)])


class SorgenteSimulata(Sorgente):
    """Genera al volo una scena del simulatore della camera (riuso/11-simulatore: catalogo.py, genera.simula) senza
    scrivere su disco. `nome`: vedi `specifica`."""

    def __init__(self, nome, larghezza=424, seme=None):
        self._G = riuso.modulo("simulatore", "genera")
        self._spec, self._larghezza = specifica(nome), larghezza
        prof, cam, sc, _, tracce, self.n = self._G.prepara(self._spec, larghezza)
        self.meta, v = self._G.meta_e_verita(self._spec, prof, cam, sc, tracce, [])
        self.ostacoli = _ostacoli_registro(v["ostacoli"])
        self.ombra_vera = v["ombra_suolo"]["polare"]
        self._verita = {}

    def __iter__(self):
        for i, t, prof, ver, _ in self._G.simula(self._spec, self._larghezza):
            self._verita[i] = _verita_registro(ver)
            yield Fotogramma(i, t, {"profondita": prof})

    def verita(self, indice):
        return self._verita.get(indice)


def SorgenteLungaPortata(cfg):
    """Una scena a lunga portata (A1–A4, S1, S2 di scenari.json; E1–E5 di scenari_eventi.json; o una registrazione
    pubblica di moto con occlusione virtuale): vedi movi.lungo.SorgenteLungaPortata."""
    from .lungo import SorgenteLungaPortata as S
    return S(cfg)


def apri(cfg, base=None):
    """Fabbrica: dalla voce `sorgente` della configurazione ({"tipo": "sequenza" | "simulata" | "pubblica" |
    "scena_lp", …}) alla sorgente giusta. «pubblica» è una SorgenteSequenza con origine_dati = "pubblici".
    I percorsi relativi partono da `base` (la cartella del prototipo se manca)."""
    s = cfg.sorgente
    tipo = s.get("tipo")
    base = base or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if tipo in ("sequenza", "pubblica"):
        cartella = s["cartella"] if os.path.isabs(s["cartella"]) else os.path.normpath(os.path.join(base, s["cartella"]))
        return SorgenteSequenza(cartella, s.get("ogni", 1), s.get("primo", 0), s.get("ultimo"))
    if tipo == "simulata":
        return SorgenteSimulata(s["nome"], s.get("larghezza", 424))
    if tipo == "scena_lp":
        return SorgenteLungaPortata(cfg)
    raise ValueError(f"tipo di sorgente sconosciuto: {tipo}")
