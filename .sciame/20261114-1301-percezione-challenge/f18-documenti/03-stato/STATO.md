# Stato del progetto, versione 4: che cosa è cambiato (`sciame-redattore`, f18-documenti/03-stato)

15 novembre 2026, dalle 03:03:44 (`date -Is`). Copia scritta: `STATO_PROGETTO.md`, in questa cartella. È la versione 3 di `documentazione/STATO_PROGETTO.md`, che **non è stata toccata**, con i riquadri «Versione 4» e il capitolo 11 nuovo: 2647 righe contro 2387. Il testo della versione 3 resta tutto. Ogni parte superata porta la dicitura «superata da …», come chiedono le regole scritte in testa al documento.

## 1. In testa: cambi di stato e regole

- **Regole violate:** nessuna, che io sappia. Ho scritto solo in `f18-documenti/` e nella cartella temporanea della sessione. Niente git, sudo o rete; nessun file cancellato; un processo alla volta, sempre con `timeout`. Le previsioni stanno in `../PREVISIONI.md` (03:03:58), scritte prima del lavoro.
- **Fase 2c:** la cartella `60-fase2c/` è comparsa durante il lavoro, ma contiene solo `01-correzioni/`. **`VERDETTO_2C.md` non esiste** all'ultimo controllo (03:17 circa). Per questo le cifre vengono da VERDETTO_2B. Le frasi che la 2c può cambiare (il «libero» di A1 col pannello, E1, le scene del video, K-613) portano il commento `<!-- % 2C -->`: sono 17 occorrenze. Il documento è in Markdown, quindi il commento «% 2C» è chiuso in un commento HTML: così non compare a schermo e si ritrova con `grep`.
- **Non ho ricontato** nessuna cifra. Le ho prese dai verdetti, che dicono che cosa hanno ricontato.

## 2. Che cosa è cambiato, e perché

1. **Testa e avvertenza**: data, file integrati, e la frase «niente della seconda fase è provato su un sensore fisico». Il 46 % dei campi delle schede è un'ipotesi (VF2; `02-sensori`).
2. **Sintesi e «stato in dieci righe»** riscritte per la seconda fase, nel riquadro «Versione 4». La sintesi della versione 3 resta sotto, con la dicitura «superata» per le righe 1, 4 e 10 e per l'ambito.
3. **§1.4**: righe 11, 12 e 13 dell'addendum e la decisione K-603. Il riquadro «Versione 4» registra quattro cambi: allegato da «in corso» a «consegnato»; classificatore da «richiesto» a «supposto esistente, lavori futuri»; inventario vuoto; divieto di cancellare.
4. **Capitolo 11, nuovo.** Contiene: addendum e K-603; componenti; sensori; traiettorie pubbliche; prove per classe (v1 e v2); i tre principi; eventi E1–E5 (v1 e v2); prototipo, collaudo e scene; video con i tre specialisti (`sciame-marketing`, `sciame-videomaker`, `sciame-comunicazione`); da dire e da non dire; regole violate; aperti; K-601…K-613.
5. **Cap. 7**: tre decisioni nuove per l'utente: il nome «MoVi», che collide con «MōVI» di Freefly; la musica con attribuzione; K-613. Le decisioni I, IV (in parte), V e II(a) sono segnate come superate dall'undicesimo addendum.
6. **§5.7**: che cosa cambia alla prossima valutazione. L'innesto della regione nella catena è dato per fatto (§11.5).
7. **Registro**: righe 4 (a)–(g), più una nota che conserva la riga «4 (da scrivere)» della versione 3 e dice quali attese si sono avverate.
8. **Appendice B**: riquadro con le 61 chiavi nuove dell'elenco aggiornato ([333]–[393]) e con lo stato dichiarato di ciascuna.
9. **Indice**: voce del capitolo 11.

## 3. Critiche e dubbi per l'autore (contenuto, non stile)

1. **E1, 49/60 o 50/60.** V2B scrive 49/60 nel §1 e nell'affermazione 9; nel K-609 scrive che «51/60» vale **50/60**. Ho riportato 49/60 e segnato la discordanza come non risolta (§11.7). La decide una riga di `riconto_2b_esito.txt`, che non ho letto.
2. **«Mai fuori dall'avviso» in A1.** VF2 diceva «rimasto acceso per tutta l'ombra» (200/200), V2B lo smentisce in min (12/200). Nel registro l'ho scritto come cambio di stato. VF2 però misurava col v1 e con un'altra definizione (K-608): il confronto non è alla pari.
3. **I K di VF2 e la decisione K-603.** La sigla K-603 indica sia una contraddizione di VF2 sia la decisione del coordinatore. L'ho segnalato fra gli omonimi (§11.0).
4. **Allegato tecnico.** Non so se contenga già la seconda fase (VF2, §8, chiede il capitolo `10_lunga_portata.tex`): non verificato.

## 4. Stati proposti

- «Le cifre della seconda fase nello stato coincidono con le fonti»: **verificato** su un insieme dichiarato. Sono le 173 cifre con unità, rapporto k/n o intervallo che stanno nei blocchi nuovi. Un programma (`cifre.py`, nella cartella temporanea) le ha cercate nei 15 file citati: tutte ritrovate. Quattro risultavano mancanti per un errore del programma, che le spezzava male (per esempio «v1 149/200»); a mano sono state ritrovate tutte e quattro. Il controllo dice che le cifre stanno nelle fonti, non che siano scritte nel contesto giusto.

## 5. Che cosa propongo dopo

Al verdetto della 2c: cercare `% 2C`, correggere quelle frasi e togliere il commento; scrivere la riga 5 del registro. Poi far rileggere il capitolo 11 a un lettore critico che non sia l'autore.
