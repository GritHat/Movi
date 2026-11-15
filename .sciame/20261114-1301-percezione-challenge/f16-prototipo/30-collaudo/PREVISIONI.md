# Previsioni del collaudo (sciame-tester) — scritte prima delle prove
Ora: 2026-11-15T01:39:37+01:00

P1. `sh prova_tutto.sh` in una copia pulita (senza uscite/) termina con esito 0 entro 30 min (tetto mio; lo script dichiara «pochi minuti»). Smentita: esito ≠ 0 o > 30 min. Il tempo dichiarato «pochi minuti» lo considero smentito se > 10 min.
P2. Validatore mio (indipendente da registro.valida_riga, ma condivide l'autore della specifica = docstring di registro.py e ARCHITETTURA §3): 0 righe non valide per forma su tutte le scene. Smentita: ≥ 1 riga non valida in una scena.
P3. Invarianti (programma mio): prevedo 0 violazioni di «libero dove la verità ha un oggetto» e di «avviso tolto senza osservazione» nelle scene con chiamante prudente; prevedo ≥ 1 violazione nelle scene *_interfaccia (falla P2 dichiarata dal README). Previsione debole: qualche violazione di «vista senza misura» nel modo lungo (camere orientate dal radar). Smentita della prima parte: ≥ 1 violazione in una scena non «interfaccia».
P4. Le cifre del tabellone ristampate coincidono con CORTO_RAGGIO.md / LUNGA_PORTATA.md a meno dell'arrotondamento; smentita: una cifra k/n diversa.
P5. Casi limite: prevedo che almeno uno fra scena vuota/sequenza troncata/configurazione senza classi faccia fallire il programma con un'eccezione non gestita (50 %).
P6. Le immagini di «mostra» portano «simulat» nel testo (controllo nel codice + controllo a campione delle immagini). Smentita: un'immagine senza la scritta.
Soglia per le frequenze: intervallo di Wilson al 95 %.
