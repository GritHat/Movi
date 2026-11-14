# PREVISIONI — piano finale (sciame-pianificatore, f12, passo 21)

Scritte alle 2026-11-14T18:23:59+01:00 (date -Is), dopo aver letto il contratto, la prima stesura del piano, il piano rifatto e VD;
PRIMA di aprire i programmi piano_mc.py e rifai_mc.py, prima di scrivere il mio programma e prima di ogni lancio.
Non ancora letti a quest'ora: COMPLETEZZA, ATTACCO_V3, CONTROLLO_PROVE, LIBERO, PROVA_INSIEME, IDENTITA, DISCORDANZE.

Misura: frazione di 20 000 estrazioni (seme fisso, piu' due semi di controllo); intervallo di Wilson al 95 %.
«Pioli di continuita' e sicurezza» = «libero» nel fotogramma, avviso che finisce solo guardando, regione disegnata
per tutta l'occlusione, identita' corretta (F-401/402/408/409 nella forma sui gruppi), tutti nel tronco.

| Id | Previsione | Soglia di smentita |
|---|---|---|
| pf-P1 | Calendario finale, lettura leggera (modello della prima stesura): P(tutti i pioli di continuita' e sicurezza nel tronco all'ora 14) fra 0,55 e 0,85 | fuori da [0,55; 0,85] |
| pf-P2 | Stesso calendario, lettura media del secondo ruolo: la stessa probabilita' fra 0,25 e 0,60 | fuori da [0,25; 0,60] |
| pf-P3 | P(minimo dimostrabile intero, con tabella firmata e prova generale, entro l'ora 14): leggera fra 0,15 e 0,40; dura sotto 0,05 | leggera fuori da [0,15; 0,40] oppure dura >= 0,05 |
| pf-P4 | I due programmi esistenti, rilanciati senza modifiche, ridanno 0,46 (piano con i tagli) e 0,262 (alternativo, leggero) entro +-0,01 | scarto oltre 0,01 su una delle due |
| pf-P5 | K0 preparato prima dell'ora 0 vale almeno +0,05 su pf-P2 | guadagno sotto 0,05 |
| pf-P6 | Il compito piu' spesso sul percorso critico e' la prima corsa di tutto insieme o la fila della previsione (P2): almeno 0,50 | altro compito in testa, o quota sotto 0,50 |
| pf-P7 | L'intervallo fra le due letture per «pioli nel tronco all'ora 14» e' largo almeno 0,25 (le letture non concordano) | larghezza sotto 0,25 |

Esiti: in fondo, scritti dopo i lanci, senza toccare la tabella sopra.

## Esiti (scritti alle 2026-11-14T18:29:21+01:00, dopo i lanci; la tabella sopra non e' stata toccata)

Tre lanci: (1) primo calendario (risultati_primo_lancio.txt); (2) dopo aver spostato A5 a P5 e THL a P1
(risultati_piano_finale_mc.txt); (3) dopo aver diviso C2 in C2a e C2b (risultati_variante_c2.txt). I ridisegni 2 e 3
sono nati DOPO aver visto i numeri: il calendario finale va letto come scelto dopo. Le previsioni si giudicano sul
lancio 3 (il calendario consegnato); accanto la cifra del lancio 1.

| Id | Esito | Numeri (lancio 3; fra parentesi il lancio 1) |
|---|---|---|
| pf-P1 | SMENTITA (troppo prudente) | stime mie, modello leggero: 0,992 (0,934); previsto 0,55-0,85 |
| pf-P2 | SMENTITA (troppo prudente) | stime del secondo ruolo, modello medio: 0,818 (0,677); previsto 0,25-0,60 |
| pf-P3 | SMENTITA di poco per le stime mie, regge con quelle del secondo ruolo; il duro regge | leggero: 0,428 mie (0,319 al lancio 1, dentro), 0,214 secondo ruolo; duro 0,016 e 0,005 |
| pf-P4 | REGGE | piano_mc.py: 0,460 [0,453; 0,467]; rifai_mc.py: 0,262 [0,256; 0,268]: identici ai file |
| pf-P5 | REGGE | secondo ruolo, medio: 0,818 -> 0,909, cioe' +0,09 (lancio 1: +0,125) |
| pf-P6 | SMENTITA alla lettera | in testa c'e' TAB (0,97-0,98); PI 0,58-0,65; la fila di P2 0,11-0,26 |
| pf-P7 | NON RISOLTA: dipende da quale modello del secondo ruolo si prende | 0,992 contro 0,818 (medio): 0,17, sotto soglia; contro 0,473 (duro): 0,52 |

Notato dopo, non previsto: (a) il piolo che manca piu' spesso al gelo non e' l'avviso ne' l'identita' ma la regione
disegnata (0,48 all'ora 12 con le stime del secondo ruolo, modello medio, prima di dividere C2; 0,71 dopo) e le righe
della regione nel tabellone (0,13); (b) con le stime del secondo ruolo e il suo modello medio il mio programma ridà
la sua scala all'ora 14 entro 0,01 (avviso 0,94 / 0,94; identita' 0,96 / 0,97; stati 0,56 / 0,57; regione 0,71 / 0,72
prima di dividere C2): i due programmi concordano quando hanno le stesse ipotesi.
