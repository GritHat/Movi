"""Le scene d'esempio da consegnare: scene/SCENE.json (nome, modo, configurazione, sorgente, che cosa mostra)."""
import json
import os

FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scene", "SCENE.json"))


def carica():
    with open(FILE, encoding="utf-8") as f:
        return json.load(f)["scene"]


def elenco():
    """Una riga di testo per scena: nome, modo, stato (pronta | da costruire), che cosa mostra."""
    return [f"{s['nome']:28s} {s['modo']:6s} {s['stato']:14s} {s['mostra']}" for s in carica()]
