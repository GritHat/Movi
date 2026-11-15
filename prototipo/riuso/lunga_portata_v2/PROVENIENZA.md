# Provenienza di riuso/lunga_portata_v2 (fase 2b)

Copiati TALI E QUALI con `cp -n` il 2026-11-15T02:24:02+01:00 da `sciame-sviluppatore`; nessuna modifica. Impronte sha256:

    73d6299ab0dec946ca5948b1f42d068b34b12dc1f6a1e6c6c14622a1f91ec4c6  movi_lp_v2.py
    ef84d5750f30e2bd727767b508e0ae172bf962ef4125d42316943c78955b77ff  regole_lunga_portata_v2.json
    ee8bc0cda5978c62f0fc5453ebff379105eada26d4d95355da1d7cbae26078d4  eventi_v2.py

| File | Origine | Autore |
|---|---|---|
| movi_lp_v2.py | .sciame/20261114-1301-percezione-challenge/f15-lunga-portata/50-fase2b/01-nucleo/movi_lp_v2.py | sciame-tracciamento (NUCLEO_V2.md) |
| regole_lunga_portata_v2.json | stessa cartella | sciame-tracciamento |
| eventi_v2.py | .sciame/…/50-fase2b/02-eventi/eventi_v2.py | sciame-scene-dinamiche (EVENTI_V2.md) |

Uso nel prototipo: `movi/lungo.py` (nucleo «v2», predefinito; «v1» con `--nucleo v1` o `MOVI_NUCLEO_LP=v1`).
- `movi_lp_v2` entra al posto di `movi_lp_import.nucleo` (sys.modules) per prove_lp, sim_lp, eventi_lp di
  `riuso/lunga_portata/10-simulatore`, che restano intatti; `MAPPA_CERTIFICATA_PREDEFINITA = True` (dichiarato).
- `eventi_v2.py` cerca il nucleo in `../../50-fase2b/01-nucleo`, che qui non esiste: prende allora `eventi_lp.m`,
  cioè lo stesso movi_lp_v2. Le regole di eventi_lp sono sostituite dalle v2 prima dell'importazione.
- Il registro per fotogramma di eventi_v2 viene da una copia ricompilata di `eventi_v2.passaggio` con UNA riga in più
  alla fine del ciclo (`_REG_CICLO(locals())`, sola lettura): `lungo.passaggio_eventi_v2`.
Tutto è simulazione dalle schede; niente è «validato».
