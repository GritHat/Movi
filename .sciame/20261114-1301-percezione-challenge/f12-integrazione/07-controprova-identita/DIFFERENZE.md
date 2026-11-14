# DIFFERENZE — la copia `catena/` di 07-controprova-identita

`catena/` è la copia **identica** di `../06-identita/catena` (la catena di f10 più le correzioni dell'autore, cioè
`../06-identita/DIFFERENZE.diff`: 7 file, 105 righe). **Io non ho cambiato nessuna riga** della catena: controllo
`diff -r -x __pycache__ ../06-identita/catena catena` (vuoto; lo rifà `rifai.sh`). `prova_autore.py` è la copia identica di
`../06-identita/prova.py` (`cmp`). Né `f10-dati` né `06-identita` sono stati toccati.

Ciò che cambio lo cambio **in memoria, dentro `attacco.py`**, senza scrivere nel simulatore di f10:
- `catalogo.PANNELLO` e `catalogo.Z_ATTORE` (posizione del pannello e linea di cammino) per gruppo d'attacco;
- `catalogo.passaggio`: quattro percorsi in più (`v16`, `bordo`, `estA`, `estB`), gli altri invariati;
- `catalogo.scena`: una scena in più (`cubo`) e l'inclinazione vera del sensore spostata di ±0,5° (la catena crede 15°);
- `simsens.carica_profilo`: le tre probabilità di buco moltiplicate per 3,5 (tetto 0,95) quando il gruppo lo chiede;
- `misura_passaggi.sul_pannello`: il rettangolo del pannello segue il pannello spostato (serve solo a «pannello in movimento»).
Le configurazioni sono quelle dell'autore: «prima» (interruttori spenti) e «tutte_p» (la sua finale).
