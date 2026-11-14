# Previsioni del curatore delle fonti (f12, passo 51-riferimenti)

Scritte alle 2026-11-14T19:20:33+01:00, prima di ogni estrazione dai file nuovi e prima di ogni richiesta alla rete. A quest'ora ho letto solo il contratto f12 e il §0 dell'elenco delle 17:36; ho copiato i due file nella cartella di consegna.

- **P1 (fonti nuove).** Misura: numero di fonti esterne senza voce nell'elenco delle 17:36, trovate nei file scritti dopo le 17:36 o non coperti (f7/16-verdetto, f8/16-verdetto, f10-dati, f12-integrazione, f13-allegato, f14-classificazione). Attesa: fra 5 e 40. Smentita: meno di 5 o più di 40.
- **P2 (esistenza).** Misura: quota delle fonti nuove con indirizzo o identificativo che risponde in rete (codice 200 o registro che restituisce la scheda). Attesa: almeno l'80 %. Smentita: sotto l'80 %. Nessuna fonte inesistente fra quelle con identificativo arXiv o DOI (smentita: almeno una).
- **P3 (BibTeX).** Misura: controllo con un programma mio dopo le aggiunte. Attesa: 0 chiavi doppie, graffe bilanciate, 0 campi obbligatori mancanti. Smentita: almeno un errore al primo passaggio del programma sul file finale.
- **P4 (numerazione).** Misura: le 291 voci tengono chiave e numero; le nuove partono da [292]. Attesa: 0 chiavi o numeri cambiati (confronto per programma con l'originale). Smentita: almeno uno.
- **P5 (cambi di stato imposti dai verdetti).** Misura: numero di voci esistenti il cui campo «Verifica» o le cui note cambiano per effetto di VD (f10) o delle discordanze dei fascicoli (f13). Attesa: fra 2 e 15. Smentita: 0 oppure più di 15.
- **P6 (completezza sugli indirizzi).** Misura: dopo l'aggiornamento, indirizzi di rete distinti scritti nei file .md della convocazione fuori da f11 (escluse scaricati/, pagine/, ambiente/, scaricato/) e assenti dall'elenco, che siano fonti. Attesa: 0. Smentita: almeno uno non spiegato.

Esiti: in fondo a questo file, scritti dopo.

## Esiti (scritti alle 2026-11-14T19:38:36+01:00, dopo le prove)

- **P1: smentita, di una.** 41 fonti nuove (soglia: fra 5 e 40): 6 dal fascicolo di bibliografia di f13, 35 da f14. Nessuna nei verdetti f7 e f8, in f10-dati e in f12-integrazione. Comando: `python3 estrai.py <convocazione> <elenco>` (programma mio nella cartella temporanea della sessione), 2912 file letti alle 19:22: 42 indirizzi, 7 identificativi arXiv e 11 DOI assenti dall'elenco delle 17:36.
- **P2: regge.** 45 richieste fra le 19:24 e le 19:28. Delle 41 fonti nuove, 40 hanno un registro o una pagina che risponde con il contenuto (due 429 di Crossref riprovati con successo); una (pagina di un costruttore di droni) rinvia altrove senza contenuto; due indirizzi secondari (un aggregatore e la pagina di un editore) danno 403, ma i loro DOI rispondono su Crossref. Nessuna fonte inesistente fra quelle con arXiv o DOI. Un DOI scritto in un file punta a un altro articolo (voce `green2000`).
- **P3: smentita al primo passaggio.** Il mio controllo ha trovato 184 voci invece di 189 e una voce con il numero sbagliato: errore mio nella sostituzione dello stato (un'espressione regolare che usciva dalla voce). Corretto e rilanciato: 189 voci, graffe 1945 aperte e 1945 chiuse, 0 chiavi doppie, 0 campi obbligatori mancanti; `bibtex` (stile plain): 0 errori, 1 avviso atteso (`vovk2005` senza autore).
- **P4: regge.** 0 chiavi e 0 numeri cambiati fra le 291 voci (confronto per programma con `documentazione/RIFERIMENTI.md`); le nuove vanno da [292] a [332].
- **P5: smentita.** 24 voci esistenti toccate (10 cambi di stato dal fascicolo f13, 14 note da VD e dalle discordanze), contro un'attesa fra 2 e 15.
- **P6: regge.** Alle 19:36, su 2969 file: 464 indirizzi distinti, 8 assenti, nessuno è una fonte (un indirizzo d'esempio, uno spazio dei nomi, un'espressione regolare, due modelli d'indirizzo di programmi, una copia diretta di una pagina che ha la voce, due indirizzi troncati di una voce che c'è); 75 identificativi arXiv, 0 assenti; 122 DOI, 1 assente che è un DOI presente scritto con la barra di LaTeX.

Notato dopo, senza previsione: (a) il DOI sbagliato di `green2000`; (b) due cifre attribuite a una pagina che non le contiene (`tronair-traino-aerei`); (c) l'edizione del regolamento dell'aeroporto di Monaco (nome del file «2016», testo «Revision 03, 20.02.2026»); (d) nel riassunto di `ohm2016` la fase di stabilizzazione dopo l'arresto dura 0,96–1,41 s.

Ricalcolo fatto da me (non una misura del sistema): `python3 -c "n=400; z=1.959964; print(n/(n+z*z), 0.05**(1/n))"` dà 0,99049 (Wilson bilaterale al 95 %, 400 su 400) e 0,99254 (limite esatto unilaterale al 95 %); con n = 2000: 0,99808 e 0,99850. Conferma le discordanze D1 (dimostrazioni) e D2 (stima) dei fascicoli.

Conteggi finali per stato: 204 verificate, 58 in parte, 23 con un dato diverso, 21 aperte dal ruolo, 6 solo riassunto, 8 non verificate, 12 non raggiungibili = 332 (alle 17:36: 165 / 58 / 21 / 22 / 5 / 8 / 12 = 291). Ricontati due volte, con due programmi miei.

Indipendenza: i programmi sono miei e non riusano quelli dei curatori precedenti; condivido con loro e con i ruoli il modello linguistico. I dieci cambi di stato delle voci esistenti vengono dalle riaperture del curatore di f13, non rifatte da me.
