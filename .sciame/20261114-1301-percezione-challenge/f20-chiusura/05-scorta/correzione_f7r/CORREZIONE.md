# Correzione F7r-c1: esito (sciame-tracciamento, 15-11-2026)

Tutto **simulato**: nessun sensore fisico. Solo osservazione e avviso. Lo scenario e il tracciatore hanno lo stesso
autore e lo stesso modello fisico, quindi il controllo non è indipendente dalla fisica ipotizzata.

## In testa: cambi di stato e regole

- Previsioni scritte alle 2026-11-15T06:33:25+01:00 (`PREVISIONI.md`). Una sola valutazione, sul seme NUOVO 20261124,
  avviata alle 06:36:00 e finita alle 06:41:43 (`avvio_valutazione_c1.txt`).
- **P1 avviso prima del frammento (cella totale): REGGE.** Prima era 0/59 in att e 0/59 in sda; ora è 59/59
  [0,939; 1] in entrambe.
- **P2 riacquisizione ≤ 2 s ≥ 51/60 in att: SMENTITA.** davanti/att 49/60 [0,701; 0,894]; vira/att 40/60
  [0,541; 0,773].
- **P3 nessuna identità spuria non dichiarata: REGGE.** 0 in ogni cella; prima c'era 1/60 in totale/att.
- **P4 falsi avvisi F7c ≤ 0,05: REGGE.** 0/200 [0; 0,019] sia in att sia in sda.
- **P5 continuità e «libero»: REGGE.** Continuità 60/60 (200/200 in F7c) in tutte le celle; «libero» 0 sia sul bersaglio
  sia sui frammenti. In totale/att la continuità era 59/60 prima della correzione.
- Ho violato una regola procedurale, che dichiaro: il «prima» è la valutazione F7r esistente sul seme 20261122, non una
  ripetizione sul seme 20261124. La distribuzione è la stessa ma i semi sono diversi, quindi il confronto non è appaiato.
- Nessun file è stato cancellato o sovrascritto. La seconda prova di sviluppo è nella sottocartella `sv2/`. I registri
  sono file nuovi `registro_F7r_c1_*.jsonl`.

## Che cosa cambia (`scorta_f7r_c1.py`; nessuna decisione usa la verità)

- **(a) Avviso immediato.** Se il radar segnala la saturazione e la camera è saturata insieme (scarto massimo 0,5 s), si
  dichiara l'«evento_vicino_non_localizzato». Il volume è una sfera prudente centrata sulla posa stimata del portatore:
  r0 = 115 m, cresce a 140 m/s e ha il limite di resistenza di `in_volume`. L'avviso al portatore parte subito, e dentro
  il volume non si dichiara mai «libero». Il volume resta attivo per al più 8 s, e per al più 3 s dopo che un volume
  localizzato lo sostituisce. Nel registro l'evento non sparisce. Non ho usato la direzione del lampo: è la variante
  «ignota» della consegna.
- **(b) Riacquisizione.** Ho tolto il blocco nel volume dei detriti. Per prendere una traccia candidata servono cinque
  condizioni:
  - porta di Mahalanobis ≤ 16,27 su P_bersaglio + P_traccia;
  - velocità coerente con l'insieme di presenza;
  - velocità orizzontale fra 0,7 e 1,3 volte quella del bersaglio;
  - |Δvz| ≤ 10 m/s;
  - conferma su 3 scansioni (prima ne servivano 5).

  Il Doppler resta nella porta di associazione.
- **(c) Identità dichiarata.** Ogni riacquisizione con un evento aperto, o da una traccia nel volume, è «presunta_dubbia».

## Tabella prima/dopo (celle critiche; passaggi, Wilson 95 %)

| cella | misura | prima (20261122) | dopo c1 (20261124) |
|---|---|---|---|
| totale/att | avviso prima del frammento a 10 m | 0/59 [0; 0,061] | 59/59 [0,939; 1] |
| totale/sda | avviso prima del frammento a 10 m | 0/59 [0; 0,061] | 59/59 [0,939; 1] |
| davanti/att | avviso prima del frammento a 10 m | 27/52 [0,387; 0,649] | 51/51 [0,930; 1] |
| vira/att | avviso prima del frammento a 10 m | 19/55 [0,234; 0,477] | 58/58 [0,938; 1] |
| davanti/att | riacquisizione radar ≤ 2 s | 41/60 [0,558; 0,787] | 49/60 [0,701; 0,894] |
| vira/att | riacquisizione radar ≤ 2 s | 43/60 [0,592; 0,815] | 40/60 [0,541; 0,773] |
| totale/att | identità spurie non dichiarate | 1/60 [0,003; 0,089] | 0/60 [0; 0,060] |
| davanti/att | identità a fine passaggio | 56/60 [0,841; 0,974] | 60/60 [0,940; 1] |
| F7c/att, F7c/sda | falsi eventi o avvisi | 0/200 [0; 0,019] | 0/200 [0; 0,019] |
| tutte | continuità; «libero» | 59–60/60; 0 | 60/60; 0 |

Le righe con «prima» senza intervallo nella tabella completa le ho calcolate a mano con la stessa formula di Wilson. La
tabella completa, cella per cella, è in `tabella_c1.md`. Il margine minimo fra l'avviso e il frammento a 10 m è 0,3 s
nella cella totale e 0,4 s in davanti e vira (att).

## Critiche e limiti

1. **L'avviso (a) è prudente fino al banale.** La sfera attorno al portatore contiene sempre il percorso, quindi
   l'avviso è certo ogni volta che i due sensori saturano insieme. Arriva anche nella cella «lato», che è un evento
   reale, quindi non è un falso avviso. In compenso non localizza nulla e oscura il «libero» entro centinaia di metri
   per al più 8 s.
2. **Il test dei falsi avvisi su F7c è debole.** Nel simulatore il radar di F7c non satura mai: 0/200 dice soltanto che
   il bagliore da solo non fa scattare l'avviso. Che cosa succede se il radar satura per altre cause è «non verificato».
3. **Causa della smentita di P2 (sostenuto dai dati, osservato dopo).** I casi lenti sono a 2,0–3,6 s. Il ritardo si
   somma così: ritorno del radar, attesa di 0,5 s, 3 colpi a 5 Hz, poi la regola che dopo 1 s di perdita vieta di
   aggiornare il bersaglio con una misura singola. In vira la virata di 8 m/s² rende più facile che il criterio di
   velocità (0,7–1,3) e la porta scartino le tracce candidate.
4. **Riacquisizioni dubbie.** Le riacquisizioni dichiarate «presunta_dubbia» sono molte (davanti/att 51/60,
   totale/att 60/60). L'identità resta onesta, ma più vaga.

## Registro video e convalida

- Il passaggio 0 della cella peggiore (vira/att, seme 20261124) è in
  `/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/uscite/video_volo/registro_F7r_c1_vira.jsonl`, insieme alle
  altre varianti `registro_F7r_c1_*.jsonl`, sempre con idx 0 e configurazione att.
- Ho controllato i registri con `prove/convalida_volo.py`: 240 fotogrammi per ogni registro, 0 violazioni
  (`esito_convalida_c1.txt`).
- Nel passaggio 0 di vira/att l'avviso parte a 6,0 s e il frammento arriva a 10 m a 6,5 s.

## Proposte dopo

- **Riacquisizione rapida per vira.** Il meccanismo: riacquisire con una conferma di 2 su 3 scansioni e togliere l'attesa
  di 0,5 s quando il radar dichiara il proprio ritorno. La porta di velocità va allargata con l'inviluppo A_MAX_INV·τ e
  non con un rapporto fisso. La previsione è che vira/att salga a ≥ 51/60 senza identità spurie non dichiarate. La
  smentita sarebbe vira/att < 51/60 oppure una spuria non dichiarata su semi nuovi (es. 20261125).
- **Localizzare l'evento.** Usare la direzione del lampo nell'immagine per ridurre la sfera a un cono. Va ripetuto P4
  facendo saturare il radar anche in F7c.

Stato complessivo: **sostenuto dai dati (simulato)**. È un miglioramento netto sull'avviso (da 0/59 a 59/59) e sulle
identità spurie (da 1 a 0). Sulla riacquisizione il miglioramento è parziale e P2 è smentita.
