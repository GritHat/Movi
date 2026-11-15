"""Eventi del registro aggiunti dal prototipo a quelli della catena (che `registro.da_catena` già marca «osservato» o
«dedotto»). Regola dell'originale (riuso/eventi/eventi.py, «un evento osservato nasce solo in un fotogramma con una
misura»): qui
  * «avviso_acceso»          dedotto   (la traccia è entrata in ombra: nessuno l'ha vista entrare in quel punto)
  * «avviso_tolto_guardando» osservato (le celle dello strato sono state viste «libero»: evento strato_finito)
  * «non_ricomparso»         dedotto   (a ogni secondo intero senza misura: mai «uscito» o «in sosta»)
  * «affidabilita_persa» / «affidabilita_tornata» osservato (dal sensore stesso: pixel validi, fotogrammi)
NOTA: la classe Eventi di riuso/eventi/eventi.py (zone, soste, ingressi) non è collegata in questo passo: non
verificato che il suo modello a zone serva al modo corto. Lo si dice nel rapporto."""


class EventiDelRegistro:
    def __init__(self):
        self._avvisi, self._aff, self._secondi = set(), "ok", {}

    def passo(self, riga):
        t, nuovi = riga["t"], []
        if riga["affidabilita"] != self._aff:
            nuovi.append({"t": t, "tipo": "affidabilita_" + ("persa" if riga["affidabilita"] == "persa" else "tornata"),
                          "come_lo_so": "osservato", "traccia": None, "settore": None,
                          "causa": riga["sensori"][0].get("causa")})
            self._aff = riga["affidabilita"]
        ora = {a["id_traccia"] for a in riga["avvisi"]}
        for i in sorted(ora - self._avvisi):
            nuovi.append({"t": t, "tipo": "avviso_acceso", "come_lo_so": "dedotto", "traccia": i, "settore": None})
        finiti = {ev.get("traccia") for ev in riga["eventi"] if ev.get("tipo") == "strato_finito"}
        for i in sorted(self._avvisi - ora):
            if i in finiti:
                nuovi.append({"t": t, "tipo": "avviso_tolto_guardando", "come_lo_so": "osservato", "traccia": i,
                              "settore": None, "tolto_guardando": True})
        self._avvisi = ora
        for tr in riga["tracce"]:
            if tr["stato"] in ("non_vista", "previsto_ampio"):
                s = int(tr["non_vista_da_s"])
                if s >= 1 and self._secondi.get(tr["id"]) != s:
                    self._secondi[tr["id"]] = s
                    nuovi.append({"t": t, "tipo": "non_ricomparso", "come_lo_so": "dedotto", "traccia": tr["id"],
                                  "settore": None, "da_s": s})
        return nuovi
