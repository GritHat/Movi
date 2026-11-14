# Previsioni del lettore della società (sciame-esperto-dominio, f12, 42-lettore-societa)

Scritte alle 2026-11-14T19:22:06+01:00, DOPO aver letto solo CONTRATTO_INTEGRAZIONE.md e 40-documento/TESTO_DUE_PAGINE.md, PRIMA di aprire VERDETTO_INTEGRAZIONE.md, SOLUZIONE_V3.md, CIFRE.md e ogni altro file. La lettura a freddo (punti 1–7) è in PRIMA.md, stessa ora.

Le «prove» di questo passo sono riscontri di lettura (grep e lettura dei file), non misure. Indipendenza: stesso modello e stessa famiglia di documenti dell'autore del testo; diverso il ruolo e l'ordine di lettura (testo prima, verdetti dopo).

- **esperto-42-P1.** Almeno una delle correzioni che proporrò a freddo urta una frase «da non dire» o un'affermazione senza prova dei verdetti, e andrà ritirata o riscritta. Misura: numero di correzioni a freddo ritirate o riscritte dopo il riscontro. Smentita se sono 0.
- **esperto-42-P2.** La dimensione della zona prevista (raggio o area, in metri, a 1, 2 e 3 s) sta in SOLUZIONE_V3.md o nei file di f8 ma NON nel testo delle due pagine. Misura: grep nel testo e nei due file. Smentita se il testo la riporta, o se nessun file la dà.
- **esperto-42-P3.** «Sensore ideale» non è definito nel testo; in SOLUZIONE_V3.md o nel verdetto vuol dire «posizioni esatte o con rumore gaussiano, senza buchi né risoluzione della profondità». Smentita se la definizione nei file è un'altra.
- **esperto-42-P4.** Il testo non dichiara che la regola dell'avviso NON è una funzione di sicurezza nel senso delle norme (nessun livello d'integrità), mentre il verdetto o la soluzione lo dicono. Smentita se il verdetto e la soluzione tacciono anch'essi.
- **esperto-42-P5.** Le 400 traiettorie da cui è «ricavata» la zona e i dati su cui è misurato il «9 su 10» non sono dichiarati indipendenti nel testo; nei file la separazione fra taratura e prova esiste. Smentita se nei file taratura e prova usano gli stessi percorsi.

## Esiti (scritti alle 2026-11-14T19:25:32+01:00, dopo il riscontro)

- P1 **regge**: tre correzioni a freddo ritirate o riscritte («tempo d'allarme»; «in sosta» e «volo stazionario»; la dimensione della zona in metri).
- P2 **smentita**: il testo non la riporta, ma nessuno dei file cercati (V3 §1.6, verdetto e analisi di f8, analisi di f12) dà l'area della zona.
- P3 **regge**: VI §3 «un punto con 5 cm di rumore»; banco di f8 riga 92.
- P4 **smentita a metà**: il testo non lo dichiara; nemmeno VI, V3 e BL (0 occorrenze di «funzione di sicurezza»).
- P5 **smentita a metà**: il testo non dichiara l'indipendenza; V8 riga 31 dice che libreria e passaggi vengono dallo stesso generatore.
