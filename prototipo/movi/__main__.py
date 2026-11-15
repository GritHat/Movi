"""Riga di comando di MoVi (prototipo simulato).

  python -I -m movi esegui <scena o sequenza> --config scene/<nome>.json [--uscita uscite/<nome>] [--celle]
  python -I -m movi tabellone <registro.jsonl> … [--banco "prova geo=T n=400"]
  python -I -m movi mostra <registro.jsonl> [--uscita uscite/<nome>/viste] [--filmato]
  python -I -m movi convalida <registro.jsonl>          controlla forma e principi di un registro
  python -I -m movi scene                               elenca le scene d'esempio

Codici d'uscita: 0 fatto; 2 uso sbagliato; 3 registro non valido o invariante violato; 4 parte non ancora costruita."""
import argparse
import sys


def main(argv=None):
    p = argparse.ArgumentParser(prog="movi", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="comando", required=True)
    e = s.add_parser("esegui"); e.add_argument("scena"); e.add_argument("--config", required=True)
    e.add_argument("--uscita", default=None); e.add_argument("--celle", action="store_true")
    e.add_argument("--ultimo", type=int, default=None)
    e.add_argument("--nucleo", choices=("v1", "v2"), default=None,
                   help="modo lungo: nucleo di f15 (v1) o della fase 2b (v2, predefinito; anche MOVI_NUCLEO_LP)")
    t = s.add_parser("tabellone"); t.add_argument("registri", nargs="+"); t.add_argument("--banco", default=None)
    m = s.add_parser("mostra"); m.add_argument("registro"); m.add_argument("--uscita", default=None)
    m.add_argument("--filmato", action="store_true"); m.add_argument("--ogni", type=int, default=1)
    c = s.add_parser("convalida"); c.add_argument("registro")
    s.add_parser("scene")
    a = p.parse_args(argv)
    try:
        if a.comando == "esegui":
            import os
            from . import esegui
            if not os.path.exists(a.config):
                raise NotImplementedError(f"configurazione non ancora scritta: {a.config}")
            if a.nucleo:
                from . import lungo
                lungo.scegli_nucleo(a.nucleo)
                lungo.NUCLEO_DA_RIGA_DI_COMANDO = True
            print(esegui.principale(a.scena, a.config, a.uscita or "uscite/" + a.scena.replace("/", "_"), a.celle,
                                    a.ultimo))
        elif a.comando == "tabellone":
            from . import tabellone
            tabellone.principale(a.registri, a.banco)
        elif a.comando == "mostra":
            from . import mostra
            mostra.principale(a.registro, a.uscita or a.registro + ".viste", a.filmato, a.ogni)
        elif a.comando == "convalida":
            from . import registro
            righe = list(registro.leggi(a.registro))
            errori = registro.valida_sequenza(righe)
            # collaudo (sciame-tester, 15-11-2026): un registro interrotto (esecuzione caduta) non ha il riassunto
            if not righe or righe[-1].get("tipo") != "riassunto":
                errori.append((max(len(righe) - 1, 0), "registro interrotto: manca la riga di riassunto in fondo"))
            for n, x in errori[:50]:
                print(f"riga {n}: {x}")
            print(f"errori: {len(errori)}")
            return 3 if errori else 0
        elif a.comando == "scene":
            from . import scene
            for riga in scene.elenco():
                print(riga)
    except NotImplementedError as x:
        print(f"NON ANCORA COSTRUITO: {x}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
