# Previsioni di `sciame-interfacce` (f12, 05-schermo)

Scritte alle **2026-11-14T17:50:39+01:00** (`date -Is`), prima di ogni script mio. **Non cieche del tutto:** ho già letto
i quattro verdetti, la consegna del visualizzatore, l'attacco alla specializzazione, le teste di `f10-dati` e il sorgente
`f8-continuita/15-statistica/codice_semi/{gen.h,comp.c}` (per capire le geometrie D, T, L); alcuni conti di geometria li
ho già fatti a mente. Sono cieche rispetto alle uscite dei miei script.

**Notato durante la lettura, prima delle prove (non è una previsione):** le geometrie T e L del verdetto f8 (ombra larga)
hanno il soggetto a 4,0 m e la portata a 6 m (`gen.h`, `geo_make`); la demo di f7 mette il pannello largo 2 m a 1,7–1,9 m
e l'attore a 2,3 m con la portata del nucleo a 3 m. Quindi «con un'ombra larga la zona è stretta» (f8 §6.6) **non è mai
stato misurato alla scala della demo**. La prova qui sotto (P-int-4) lo misura.

## Le prove e le soglie

- **P-int-1, controllo che deve tornare.** La mia copia di `codice_semi` (con una geometria in più, `E`, e due variabili
  d'ambiente per la banda di velocità, spente di norma) rilanciata con `prova D 0.9 0 0.20 0 80000 400 0123456 Dr80000`
  dà un file uguale a `15-statistica/ris/semi_D_80000x400.tsv`, salvo la riga «# tempo del lancio». *La smentisce*
  un'altra riga diversa: in quel caso le prove 4 e 5 non valgono.
- **P-int-2, intervalli del tabellone (Wilson al 95 %).** 27 su 30 → [0,74; 0,97] (±0,01); 46 su 50 ha il limite
  inferiore ≥ 0,80 e 45 su 50 no; 30 su 30 → limite inferiore 0,89 (±0,01); 9 su 10 esatto (Clopper–Pearson)
  → [0,555; 0,997]. *La smentisce* uno scarto oltre 0,01.
- **P-int-3, tempi della demo dal solo conto in pianta** (corpo largo 0,45 m, campo 87°, portata 3 m, attore a 2,3 m,
  pannello a 1,8 m). Pannello da 1 m: nascosto per intero 0,59–0,83 s a 1,4–1,0 m/s e 1,5–1,8 s a 0,5 m/s. Pannello da
  2 m: 1,4–2,3 s a 1,4–1,0 m/s; in vista per intero, per lato, 0,45 s a 1,0 m/s **contando solo il campo**; contando
  anche la portata di 3 m prevedo **meno di 0,30 s**. *La smentisce* uno scarto oltre 0,10 s dai numeri di f7 (prime
  tre cifre) o una vista per lato ≥ 0,30 s con la portata.
- **P-int-4, ombra larga alla scala della demo** (geometria `E`: pannello largo 2 m a 1,9 m, soggetto a 2,3 m, portata
  3 m; passo 0,8–1,0 m/s; 400 semi nuovi da 120000; predittore `sd-1`; soggetto puntiforme, maschera esatta, Pd 0,9).
  (a) scartati (meno di 4 misure prima dell'ombra) **oltre il 10 %** dei «prosegue» [poco sicuro]; (b) area della
  zona su ombra, «prosegue»: **≤ 0,50 a 1 s e ≤ 0,80 a 2 s** (cioè la zona stretta si vede ancora a 2 s) [poco sicuro];
  (c) persona dentro la zona, comportamenti sul percorso (0, 1, 2, 3, 6) messi insieme: limite inferiore di Wilson
  **≥ 0,85 a 1 s e a 2 s**. *Smentite:* (a) ≤ 10 %; (b) un valore oltre la soglia; (c) un limite sotto 0,85.
- **P-int-5, pannello da 1 m a passo lento** (geometria D, passo 0,45–0,55 m/s, stessi 400 semi, `sd-1`). (a) area
  della zona su ombra, «prosegue»: **≥ 0,80 a 2 s** (a 2 s è già «previsto ampio»); (b) come (c) sopra: **≥ 0,85 a 1 s
  e a 2 s**. *Smentite:* (a) sotto 0,80; (b) un limite sotto 0,85.
- **P-int-6, il mio testo.** `SCHERMO_E_DEMO.md` ha al più 3100 parole (quattro pagine a 775 parole) e nessuna delle
  frasi «da non dire» fuori dal §7 (controllo con `grep`, elenco in `controlla_frasi.sh`). *La smentisce* una
  occorrenza fuori dal §7 o un conto oltre 3100.

**Indipendenza.** P-int-4 e P-int-5 usano il codice dello statistico di f8 (generatore, filtro, `sd-1`, taratura T o D):
condividono con il verdetto f8 tutto tranne la geometria e la banda di velocità; non contengono le correzioni c1–c8;
il soggetto è un punto e la maschera d'ombra è esatta. Coprono solo la domanda «che cosa cambia con la geometria».
P-int-2 e P-int-3 sono conti miei, indipendenti dai codici dei ruoli.

## Esiti (scritti dopo, alle 18:04; file: `risultati_schermo.txt`, `esito_frasi.txt`, `prova_geometria/ris/`)

| Previsione | Esito | Cifra |
|---|---|---|
| P-int-1 | **regge** | 1 riga diversa su 966 (la riga del tempo): `ris/controllo_D_80000x400.tsv` contro `15-statistica/ris/semi_D_80000x400.tsv` |
| P-int-2 | **regge** | 27 su 30 → [0,744; 0,965]; 46 su 50 → 0,812; 45 su 50 → 0,786; 30 su 30 → 0,886; 9 su 10 esatto → [0,555; 0,997] |
| P-int-3 | **regge** | pannello 1 m a 1,8 m: 0,59–0,83 s e 1,66 s a 0,5 m/s (1,52–1,81 fra 1,9 e 1,7 m); pannello 2 m: 1,41–2,26 s; vista per lato 0,45 s col solo campo, **0,12–0,27 s** con la portata di 3 m (bordo della portata a 1,93 m, del campo a 2,18 m) |
| P-int-4 (a) | **regge** | scartati 84 su 400 (21,0 %) nei «prosegue»; 546 su 2000 sul percorso |
| P-int-4 (b) | **smentita** | zona su ombra 0,55 a 1 s (soglia 0,50) e 0,87 a 2 s (soglia 0,80): alla scala della demo l'ombra larga non dà una zona stretta a 2 s |
| P-int-4 (c) | **regge** a 1 e 2 s | sul percorso 1206 su 1281 = 0,941 [0,927; 0,953] a 1 s; 1128 su 1275 = 0,885 [0,866; 0,901] a 2 s. **Notato dopo:** a 2 s il limite sta sotto 0,90 (il livello dichiarato «almeno 9 su 10 fino a 2 s») e a 3 s vale 0,864 [0,843; 0,883], sotto 0,85 |
| P-int-5 (a) | **regge** | zona su ombra 1,05 a 2 s (la zona comprende la fascia di 0,20 m: per questo supera 1); 0,52 a 1 s |
| P-int-5 (b) | **regge** | 1992 su 2000 = 0,996 [0,992; 0,998] a 1 s; 1968 su 1999 = 0,984 [0,978; 0,989] a 2 s; a 3 s 0,968 [0,960; 0,975]; 0 scartati; 0 passaggi con un vuoto |
| P-int-6 | **smentita nelle parole, regge nelle frasi** | `wc -w` dà 3635 parole (soglia 3100; la prima stesura ne aveva 4244 e l'ho tagliata due volte); 0 frasi «da non dire» fuori dal §7. Il limite della consegna è in pagine: **4 pagine** con pandoc e xelatex, A4, corpo 10, margini 1,8 cm (la misura dell'arbitro di f7) |

**Bracci di confronto senza previsione** (stessi semi): D a 1,0–1,4 m/s: zona su ombra 0,84 a 1 s, 10 scartati su 400; E a
0,45–0,55 m/s: zona su ombra 0,44 / 0,66 / 0,85 a 1 / 2 / 3 s, scartati 59 su 400 (505 su 2000 sul percorso), sul
percorso 0,975 / 0,931 / 0,911 (limiti 0,966 / 0,917 / 0,895). **Notato dopo:** a passo lento il pannello da 2 m tiene
il livello dichiarato, ma perde un passaggio su quattro prima dell'ombra e il soggetto non ricompare nell'area osservata
(1 ricomparso su 341): non l'ho proposto nel documento; lo segnalo qui.

**Limiti delle prove 4 e 5.** Un codice (quello dello statistico di f8), un autore, 400 semi per braccio; soggetto
puntiforme, maschera esatta, rilevamento 0,9; la geometria `E` usa la taratura T (come L: mai tarata per sé); le
correzioni c1–c8 non ci sono. La banda di passo riscala la velocità estratta e lascia intatto il flusso dei numeri
casuali. Il corpo esteso e l'ombra stimata stretta (K-215) non sono coperti.

**Letture.** Per intero: il contratto d'integrazione, i verdetti f4, f7, f8, f9, la consegna del visualizzatore,
l'attacco alla specializzazione. In parte: `SOLUZIONE_V2.md` (righe trovate con `grep`: B4, B7–B9, tabella dei
requisiti), `MODIFICHE_CONTINUITA.md` (§2.3–§2.10), `CONTROPROVE_MODIFICHE.md` e `ANALISI.md` di f8 (righe su c6, c8 e
sul tabellone), `SPECIALIZZAZIONE.md` (§4), `VALIDAZIONE_DATI.md`, `ATTACCO_DATI.md`, `ANALISI_DATI.md`, `DATI_VERI.md`
e `AMBIENTE.md` di f10 (teste e righe cercate), `ADDENDUM_UTENTE.md` (solo i titoli), `regole_challenge.md` (righe 1–5),
`gen.h` e `comp.c` dello statistico. Non letti: `AUDIT.md`, `MOTO_PROPRIO.md`, `STATO_PROGETTO.md`, `RIFERIMENTI.md`,
`CONTRATTO.md` della convocazione, `TORNEO.md` e `BANCO_DI_PROVA.md` oltre le righe cercate, i fotogrammi PNG e SVG.
Nessuna richiesta alla rete. Il PDF di misura delle pagine è andato nella cartella provvisoria della sessione.

