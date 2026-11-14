# Previsioni scritte prima delle prove (sciame-avversario, f13, sovraffermazioni e riferimenti interni)

Ora di registrazione: 2026-11-14T19:26:33+01:00. Scritte prima di leggere i capitoli dell'allegato (letto finora: solo il contratto e l'elenco dei file).

- **avversario-P1 (riferimenti interni, A-4).** Misura: numero di occorrenze trovate dal mio programma (sorgente + testo del PDF) delle classi vietate dal contratto, dopo lo scarto a mano dei falsi positivi. Previsione: almeno 3 occorrenze vere (parafrasi comprese). Smentita: 0 occorrenze vere.
- **avversario-P2 (verbi di garanzia).** Misura: frasi con «garantisce/assicura/valida/dimostra/sempre/mai/100 %» riferite a un risultato di simulazione o senza dominio. Previsione: almeno 5 frasi da correggere. Smentita: meno di 2.
- **avversario-P3 (negativi omessi).** Misura: dei 7 risultati negativi elencati nella consegna (secondo soggetto nella stessa ombra; identità al ritorno su profondità realistica; falsi «in movimento»; vetro; errore di posa; precisione fuori dal dominio; latenza non misurata), quanti mancano o sono senza cifra. Previsione: almeno 1 manca o è senza cifra. Smentita: tutti e 7 presenti con cifra coerente con la fonte.
- **avversario-P4 (classificatore).** Misura: presenza delle quattro frasi obbligatorie (richiesto; non realizzato né valutato; simulato con etichette a mano; nessuna classe diversa da «persona» nella catena completa; sicurezza non dipende dall'etichetta). Previsione: almeno una manca o è attenuata in un capitolo che ne parla. Smentita: tutte presenti dovunque serva.
- **avversario-P5 (sensore fisico).** Misura: frasi che lasciano intendere una misura su sensore fisico o con persone. Previsione: almeno 1. Smentita: 0.

Indipendenza: il mio programma non condivide codice con controlla_interni.py di chi ha unito (non lo leggo prima di aver scritto il mio); condivide il contratto (l'elenco A-4) e il modello che scrive.

## Esiti (scritti dopo le prove, 19:36)

- P1: smentita in senso stretto (0 parole o sigle dell'elenco A-4 nel sorgente e nel PDF); regge solo per le parafrasi (correzioni 15-17 di VERIFICA.md).
- P2: non raggiunta (4 frasi, previste almeno 5), sopra la soglia di smentita (2): non risolta.
- P3: regge (falsi «in movimento» fuori dominio: 7 su 10 omesso).
- P4: regge (sommario: «simulato e non valutato», senza «non realizzato» e senza «a mano»).
- P5: regge («400 percorsi registrati», tre luoghi), con la riserva che non ho aperto il generatore.
- Notato dopo, non previsto: le conclusioni enunciano la proposizione sul «libero» in forma più forte della proposizione stessa (correzione 1).
