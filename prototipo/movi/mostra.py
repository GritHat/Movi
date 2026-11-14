"""Dal registro alle immagini (o a un filmato semplice, opencv). Tre viste affiancate, 1920×1080:

  1. SCENA VERA    — la verità in pianta (solo in simulazione; senza verità: «verità non nota»)
  2. CONSOLE       — ciò che il sistema dichiara: tracce con lo stato a parole, regione di previsione, avviso
                     di possibile presenza (tratteggiato, resta finché non si guarda), eventi (osservato | dedotto)
  3. SETTORI       — il livello per settore: «suolo visto libero fino a d», «attenzione», «zona non verificata»

RIGA FISSA, su ogni immagine, sempre: «DATI SIMULATI — nessun sensore fisico · etichette a mano (classificatore
non realizzato) · regole accese: … · spente: … · config xxxxxxxx». Legge SOLO il registro: mai il nucleo."""


def riga_fissa(intestazione):
    """Il testo della riga fissa dalle dichiarazioni dell'intestazione."""
    d = intestazione["dichiarazioni"]
    dati = "DATI SIMULATI" if d["dati"] == "simulati" else "DATI PUBBLICI, sensore simulato"
    return (f"{dati} — {d['hardware']} · etichette {d['etichette']} ({'classificatore ' + d['classificatore']}) · "
            f"accese: {', '.join(d['regole_accese']) or 'nessuna'} · spente: {', '.join(d['regole_spente']) or 'nessuna'}"
            f" · config {d['config']}")


def disegna(intestazione, riga, larghezza=1920, altezza=1080):
    """Un fotogramma del registro -> immagine BGR (numpy uint8) con le tre viste e la riga fissa."""
    raise NotImplementedError("passo 1 (vista corta), passo 2 (scala in km e quote per la lunga portata)")


def principale(registro, uscita, filmato=False, ogni=1, fps=15):
    """Scrive in `uscita` le immagini PNG (una ogni `ogni` fotogrammi) o un filmato .mp4/.avi."""
    raise NotImplementedError("passo 1")
