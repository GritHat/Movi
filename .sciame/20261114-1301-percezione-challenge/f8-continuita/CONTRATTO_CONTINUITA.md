# Contratto dell'estensione f8 — la continuità visiva come obiettivo imperativo

Estensione della convocazione «percezione-challenge» (classica, profilo percezione), aperta il 14 novembre 2026 dopo il quarto addendum dell'utente (`../ADDENDUM_UTENTE.md`). Restano validi il contratto originale (`../CONTRATTO.md`: requisiti R1–R8, principi, regole sulle prove) e i principi conservati dell'estensione f7 (`../f7-estensione/CONTRATTO_ESTENSIONE.md`).

## L'imperativo (parole dell'utente)

«La continuità visiva» è l'obiettivo imperativo e principale. «A prescindere da su quale sistema si decida di implementarlo, è necessario fornire predizioni efficaci con una valutazione realistica della precisione della predizione, che consenta di effettuare una visualizzazione continua del movimento sotto una certa incertezza controllata.»

## Le due domande

**Q3 — è rispettato?** L'imperativo è rispettato in tutte le parti di ciò che lo sciame ha prodotto finora: il nucleo (soluzione versione 2), i suoi criteri di accettazione, la specializzazione a più profili, l'analisi del sensore in moto, la demo, i documenti dati all'utente? Parte per parte: rispettato, rispettato in parte, non rispettato, con la prova.

**Q4 — come si modifica?** Dove non è rispettato, quali modifiche minime lo fanno rispettare, senza violare i principi di sicurezza? La risposta è una proposta di modifica provata: quale predittore, quale rappresentazione dell'incertezza, quale regola di visualizzazione, quali misure di accettazione; con il prima e il dopo sui numeri.

## Criterio (controlli, non meccanismi)

1. **Continuità.** Per ogni oggetto seguito e confermato, in ogni ciclo fra l'ultima osservazione e la ricomparsa (o una chiusura motivata e dichiarata), il sistema emette una stima visualizzabile del movimento: una posizione più probabile e una regione d'incertezza a un livello dichiarato. Misure: quota dei cicli senza osservazione in cui la stima è emessa; lunghezza dei vuoti; salto fra la previsione e la prima misura alla ricomparsa, confrontato con la regione dichiarata; regolarità del movimento mostrato (nessun salto indietro o tremolio non motivato).
2. **Efficacia.** L'errore della previsione in funzione del tempo senza osservazione (da 0,5 a 5 s almeno) batte le linee di base ovvie (fermo all'ultima posizione; velocità costante senza vincoli) e sta sotto una soglia utile, dichiarata prima.
3. **Precisione valutata in modo realistico (taratura).** La regione dichiarata a livello p (per esempio 50 % e 90 %) contiene davvero il soggetto in una quota di casi vicina a p, **per tempo senza osservazione e per comportamento** (prosegue, rallenta, si ferma, torna indietro, svolta, esce dal lato lontano), su traiettorie generate da un modello che NON è quello dell'autore del predittore, e con i parametri tarati su dati diversi da quelli della prova. Si riportano la copertura con il suo intervallo, la larghezza della regione (una regione enorme è tarata ma inutile) e una misura complessiva della qualità della previsione probabilistica. Una media che nasconde un comportamento coperto male non basta.
4. **Incertezza controllata.** La regione mostrata è limitata: non cresce senza limite, usa ciò che il sensore vede (dove vede vuoto, l'oggetto non c'è) e la geometria dell'ostacolo; quando supera una soglia dichiarata il sistema lo dice e continua a visualizzare con un segno diverso, invece di sparire. Nessuna parte della regione sta su spazio visto libero in quel momento.
5. **Sicurezza conservata.** Una previsione non esce mai come osservazione; ciò che non è osservato non diventa mai «libero»; la possibile presenza non la toglie un timer né la previsione; le prove di sicurezza già superate dal nucleo (nessun falso «libero») non peggiorano.
6. **Costo e portabilità.** Il calcolo sta in un ciclo a 15 al secondo su CPU (misurato), e la soluzione dice che cosa le serve per valere su una stazione fissa, su una piattaforma in moto e su un ausilio indossato (che cosa è parametro, che cosa va riprovato).

## Ingressi

- Il nucleo: `../f4/H-012/05-correzioni/SOLUZIONE_V2.md`; il suo verdetto `../f4/H-012/09-arbitro/VERDETTO.md` (§3: R3; §5, punto 5: «la previsione vale circa mezzo secondo»); le sue prove `../f4/H-012/03-validazione/MISURE.md`, `MISURE_V2.md`, `MISURE_V2_bis.md` (con i simulatori `sim_h012.py`, `sim_v2.py`), `../f4/H-012/01-avversario/CONTROPROVE.md`; l'audit `../f5/02-audit/AUDIT.md`.
- Ciò che lo sciame sa già sulla previsione durante l'occlusione: il torneo `../f2/04-torneo/TORNEO.md` (parte 2: copertura del filtro a velocità quasi costante con q = 0,2 su tre generatori indipendenti, 0,89–0,93; chi torna indietro coperto nel 56–66 %; parte 3: confronto fra cerchio del filtro, disco raggiungibile e particelle con evidenza negativa, con e senza il modo «sosta»: a 3 s le particelle con sosta contengono il soggetto nel 98–100 % occupando il 60–68 % dell'ombra, ma perdono chi esce dal lato lontano: 22–41 %), con gli script accanto (`scena_parte3.py`, `torneo_parte2.py`); le consegne di f1 di tracciamento (`../f1/992c41c8860e/`), Kalman (`../f1/21d3813ca7e1/`), creativo (`../f1/e30f9e2dd4d7/`: ricerca bayesiana, scommessa sulla riemersione), ricercatore (`../f1/3fff79e9c3ea/`: velocità costante contro predittori appresi sui pedoni; taratura).
- La specializzazione e il moto: `../f6-specializzazione/01-esperto-dominio/SPECIALIZZAZIONE.md`, `../f6-specializzazione/02-slam/MOTO_PROPRIO.md`, `../f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`.
- La traccia `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/regole_challenge.md` (che nomina la «continuità percettiva»), gli addendum `../ADDENDUM_UTENTE.md`, i documenti dati all'utente in `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/proposta/`.
- L'estensione f7 è in corso in parallelo (`../f7-estensione/`): NON leggerla, salvo il suo contratto.

## Vincoli

- Configurazione primaria: una camera di profondità frontale con IMU; prima dimostrazione a sensore fermo. Niente GPU nel percorso critico.
- Un modello appreso può entrare solo se una prova mostra che migliora la previsione o la sua taratura rispetto ai modelli semplici, e mai per decidere un'indicazione di sicurezza.
- Prove ammesse: a mano, calcolo, simulazione o misura su CPU. Disponibili gcc, clang, g++, rustc, Python 3.14 (numpy NON è installato e non si installa niente). Ogni lancio al più due minuti con `timeout`, uno alla volta per agente, semi fissati, comando per rifare. Altri processi girano sulla stessa macchina: i tempi misurati sono indicativi.
- Le previsioni si scrivono prima delle prove, con l'ora di `date -Is`. Gli stati non si mescolano. Niente numeri inventati.
- Ogni agente scrive solo nella propria cartella dentro `f8-continuita/`. Niente modifiche al progetto, niente git.
- Lingua: italiano.

## Esclusioni

- Niente prove su hardware né su persone vere (non disponibili): ciò che ne dipende si dichiara «non verificato» con la prova che lo deciderebbe.
- Niente funzioni d'ingaggio o di puntamento.

## Quota

Al più 18 agenti, in un workflow: corsie cieche, triage, misure indipendenti e torneo, soluzione, attacco e verifica statistica, verdetto.
