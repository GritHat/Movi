# Contratto dell'estensione f9 — le strategie avanzate della preproposta esterna

Estensione della convocazione «percezione-challenge» (classica, profilo percezione), aperta il 14 novembre 2026 dopo il quinto addendum dell'utente (`../ADDENDUM_UTENTE.md`: leggilo, elenca le strategie S1–S12). Restano validi il contratto originale (`../CONTRATTO.md`), i principi conservati di `../f7-estensione/CONTRATTO_ESTENSIONE.md` e l'imperativo della continuità visiva di `../f8-continuita/CONTRATTO_CONTINUITA.md`.

## La domanda

**Q5.** Quali delle strategie avanzate di `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prepropostaEsterna.md` lo sciame approva per l'integrazione nella soluzione, quali approva con correzioni o condizioni, quali respinge, e perché? Per ogni strategia un verdetto motivato con la prova: **approvata** (regge alle prove possibili oggi), **approvata con correzioni** (quali), **da provare sull'hardware** (non decidibile oggi: con la prova che la decide), **respinta** (con il controesempio o il motivo).

Questa estensione valuta: **S1** (selettore automatico della configurazione), **S6** (punto di massimo avvicinamento e volume protetto probabilistico), **S7** (indice di rotta convergente), **S8** (logica a livelli nominale / attenzione / attesa prudente / avaria), **S9** (sensori a tempo di volo laterali come preallarme), **S12** (piano a 24 e 38 ore), gli **attacchi 3 e 4** del file, e l'**audit delle ipotesi nascoste** su S3 e S4 (inseguitore a due ipotesi e ritaglio con l'informazione negativa). In più dà un secondo parere indipendente, in sola lettura critica e senza banco di prova, su S2–S5, S10 e S11, che sono provate altrove (f8 e f7): serve a trovare errori di formulazione, non a duplicare le misure.

## Criterio (controlli, non meccanismi)

1. **Ogni strategia ha un verdetto con la prova**, e ogni attacco proposto dal file è eseguito (a ragionamento, con un conto, con una simulazione o con una fonte) oppure dichiarato non eseguibile oggi, con la prova che lo deciderebbe.
2. **Nessuna strategia approvata viola** i principi conservati (mai «libero» sul non osservato; previsione mai mostrata come osservazione; la possibile presenza non la toglie un timer né un cambio di configurazione; nessuna grandezza non osservabile stimata; nessun modello appreso decide un'indicazione di sicurezza) né l'imperativo della continuità visiva.
3. **Fedeltà delle parole.** I termini presi in prestito da altri campi (prevenzione delle collisioni in volo, sorveglianza delle piste, urti con volatili) sono usati nel loro significato vero, verificato su fonti; dove il prestito è improprio o promette più di ciò che il prototipo fa (che dichiara e chiede, ma non comanda), si propone il nome onesto.
4. **Costo.** Per ogni strategia approvata: ore di lavoro stimate all'hackathon, costo di calcolo per ciclo (misurato se si può), e che cosa si taglia per farle posto, tenendo conto che il nucleo ne chiede già circa 54 ore-persona, 38 in fila.
5. **Lettura corretta dei documenti.** Dove la preproposta ha letto male il PDF v0.5 o i limiti del nucleo, lo si dice (per esempio: il limite «sotto 1,1 m» è una distanza dal sensore o un'altezza?).

## Ingressi

- La preproposta: `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prepropostaEsterna.md` (per intero), e il PDF a cui si riferisce: sorgente in `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/proposta/proposta_sciame.tex` (v0.5).
- Il nucleo e le sue prove: `../f4/H-012/05-correzioni/SOLUZIONE_V2.md`; `../f4/H-012/09-arbitro/VERDETTO.md` (nove condizioni; contraddizioni aperte); `../f4/H-012/03-validazione/MISURE_V2.md` e `MISURE_V2_bis.md` (con i simulatori accanto); `../f4/H-012/01-avversario/CONTROPROVE.md`; `../f5/02-audit/AUDIT.md`.
- Ciò che lo sciame sa già su inseguimento e occlusione: `../f2/04-torneo/TORNEO.md` (parte 3: cerchio del filtro, disco raggiungibile, particelle con evidenza negativa, con e senza il modo «sosta»; un falso «vuoto» di 0,3 s porta la massa giusta sotto il 5 %), con gli script accanto.
- Sensori: `../f1/985ccd9bca46/CONSEGNA.md` (hardware a tempo di volo) e `../f3/fonti/FONTI_VERIFICATE.md`. Dominio: `../f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` e `SPECIALIZZAZIONE.md`; `../f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`.
- La traccia `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/regole_challenge.md`; gli addendum `../ADDENDUM_UTENTE.md`.
- Le estensioni f7 e f8 sono in corso in parallelo: NON leggere le loro cartelle (solo i loro contratti).

## Vincoli

- Configurazione primaria: una camera di profondità frontale con IMU; prima dimostrazione a sensore fermo; niente scheda grafica nel percorso critico.
- Ambito: osservazione, monitoraggio, ispezione, navigazione sicura, avviso a una persona non vedente. Nessuna funzione d'ingaggio o di puntamento; il prototipo dichiara e chiede, non comanda.
- Prove ammesse: a mano, calcolo, simulazione o misura su CPU. Disponibili gcc, clang, g++, rustc, Python 3.14 (numpy NON è installato e non si installa niente). Ogni lancio al più due minuti con `timeout`, uno alla volta per agente, semi fissati, comando per rifare. Altri processi girano sulla macchina: i tempi sono indicativi.
- Le previsioni si scrivono prima delle prove, con l'ora di `date -Is`. Gli stati non si mescolano. Niente numeri né fonti inventati: ciò che non si verifica porta «non verificato».
- Ogni agente scrive solo nella propria cartella dentro `f9-preproposta/`. Niente modifiche al progetto, niente git. Lingua: italiano.

## Quota

Al più 13 agenti: una tornata di valutazioni indipendenti e di attacchi, poi il verdetto dell'arbitro strategia per strategia.
