# Previsioni — f18-documenti (sciame-redattore), scritte prima del lavoro

Ora: 2026-11-15T03:03:58+01:00

P1. STATO_PROGETTO v4: tutte le cifre della seconda fase e della 2b citate nello stato
    si ritrovano letteralmente in VERDETTO_FASE2.md o VERDETTO_2B.md (o nel rapporto citato).
    Misura: controllo a campione di tutte le cifre con grep. Smentita: almeno una cifra non ritrovata.
P2. riferimenti.bib v4 passa bibtex senza errori (warning ammessi, contati).
    Misura: numero di errori riportati da bibtex. Smentita: errori > 0.
P3. Nessuna chiave duplicata nel .bib. Misura: conteggio chiavi uniche = conteggio voci. Smentita: differenza > 0.
P4. Le voci nuove sono fra 25 e 70. Soglia di smentita: fuori dall'intervallo (indica stima sbagliata del materiale).
P5. VERDETTO_2C.md non esiste alla fine del lavoro (2c in corso): quindi uso VERDETTO_2B e i commenti «% 2C».
    Smentita: il file esiste al controllo finale.

## Esiti (scritti dopo, 2026-11-15T03:17:43+01:00)

- P1 **regge** sull'insieme controllato: 173 cifre (k/n, intervalli, valori con unità) dei blocchi nuovi dello stato, cercate da `cifre.py` in 15 file citati; 4 «non trovate» erano errori di taglio del programma («v1 149/200»), ritrovate a mano. Non esaustivo sulle cifre senza unità.
- P2 **regge**: bibtex, 0 errori, 1 avviso atteso (vovk2005); al primo passaggio 5 avvisi miei, corretti.
- P3 **regge**: 0 chiavi doppie nel .bib (211), 393 chiavi uniche nell'elenco.
- P4 **regge**: 61 voci nuove (intervallo 25–70).
- P5 **regge**: VERDETTO_2C.md non esiste al controllo finale (la cartella 60-fase2c contiene solo 01-correzioni).
