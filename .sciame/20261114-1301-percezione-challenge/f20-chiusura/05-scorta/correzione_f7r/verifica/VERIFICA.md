# Verifica avversaria della correzione F7r-c1 (sciame-avversario, 15-11-2026, 06:43–06:48)

Tutto **simulato**. Solo osservazione e avviso. Indipendenza: ho riusato lo stesso simulatore e lo stesso codice
(`scorta_f7r.py`, `scorta_f7r_c1.py`). I miei script ricontano e attaccano, ma condividono con la correzione la fisica,
la verità generata e l'autore del modello. Quindi coprono solo gli errori di conteggio, di confronto e di logica della
correzione, non quelli del modello fisico.

## In testa: cambi di stato e regole

- **Dove scrivo.** La consegna chiede `correzione_f7r/VERIFICA.md`, ma le regole ammettono scritture solo in
  `correzione_f7r/verifica/`. Ho scritto qui, in `verifica/VERIFICA.md`. Nessun file è stato cancellato o sovrascritto,
  e niente git né rete.
- **Previsioni.** Le ho scritte prima delle prove: `PREVISIONI_VERIFICA.md` alle 06:44:13 e `PREVISIONI_VERIFICA_2.md`
  alle 06:45:50 circa, prima dell'attacco.
- **Avviso prima del frammento: è un miglioramento percettibile e significativo.** Sostenuto dai dati (simulato),
  anche nel confronto appaiato.
- **Riacquisizione ≤ 2 s:** il miglioramento è piccolo; P2 resta **smentita**. In davanti/att è significativo solo nel
  test appaiato; in vira/att non è significativo.
- **Nuovo controesempio (smentisce la robustezza dell'avviso c1 ai falsi avvisi).** In F7c il radar viene saturato
  1 s per un'altra causa, con il bagliore naturale della camera. La correzione dà **11/200 falsi avvisi
  [0,031; 0,096]**; l'originale ne dava 0/200 [0; 0,019].

## Critiche numerate, con le prove

1. **Verità e informazioni future.** Ho letto tutte le righe nuove (diff fra `scorta_f7r.py` e `scorta_f7r_c1.py`).
   - Le righe nuove decidono con la posa stimata `pce` e con le bandiere di saturazione dei sensori (`saturata`,
     `radar_cieco`: il sensore stesso dichiara la saturazione, come in F7r). Usano anche gli istanti passati
     `cam_ultima_sat` e `rad_ultima_sat`. Le etichette vere `fonti` servono solo a contare. Il volume si apre a `t-0,1`:
     non c'è alcuna informazione futura.
   - Restano due usi della verità **già presenti nell'originale**: la velocità vera del portatore
     (`vce = W["Vc"][i]`, riga 498) e la posizione vera nella regione del candidato (`tb.regione(t, W["Pc"][i])`,
     riga 560). Per l'avviso c1 la velocità è irrilevante, perché la sfera è centrata sul portatore e quindi a s=0 lo
     contiene sempre.
   - Stato: **verificato** sulle righe nuove.
2. **I semi.**
   - Valutazione su 20261124, sviluppo su 20261123 (anche `sv2`). I semi usati prima: 20261120 e 20261121 (F7),
     20261122 e 20261123 (F7r).
   - Con `grep` su `.sciame` e `prototipo` (esclusi i `.jsonl`), 20261124 compare solo nei file di c1 e nei miei.
   - Il seme è nuovo: **verificato**.
3. **Il riconteggio dalle uscite grezze** (`riconto.txt`, con `riconta.py` sui due `passaggi_*.jsonl`): ogni cifra di
   CORREZIONE.md coincide, Wilson compreso. **Verificato.**
4. **Confronto appaiato.** Non era nella correzione, l'ho aggiunto io.
   - Ho ripetuto il codice F7r originale sul seme 20261124 (`appaiata.py`, file `orig_seme20261124.jsonl`). La verità
     generata è identica in 60/60 passaggi per ogni cella (stessa `interseca_t`, stessa `d_rad`). I risultati sono in
     `confronto.txt`:

     | cella (att) | misura | originale @24 | c1 @24 | migliora/peggiora | McNemar esatto | Fisher |
     |---|---|---|---|---|---|---|
     | totale | avviso prima del frammento | 0/59 [0; 0,061] | 59/59 [0,939; 1] | 59/0 | p = 3,5e-18 | p = 8,2e-35 |
     | davanti | avviso prima del frammento | 22/51 [0,305; 0,567] | 51/51 [0,930; 1] | – | p = 3,7e-9 | p = 1,3e-11 |
     | vira | avviso prima del frammento | 28/58 [0,359; 0,608] | 58/58 [0,938; 1] | – | p = 1,9e-9 | p = 1,1e-11 |
     | davanti | riacquisizione ≤ 2 s | 42/60 [0,575; 0,801] | 49/60 [0,701; 0,894] | 8/1 | p = 0,039 | p = 0,20 |
     | vira | riacquisizione ≤ 2 s | 35/60 [0,457; 0,699] | 40/60 [0,541; 0,773] | 5/0 | p = 0,0625 | p = 0,45 |
     | vira | identità spurie | 1/60 [0,003; 0,089] | 0/60 [0; 0,060] | – | – | p = 1 |
     | totale | riacquisizione ≤ 2 s | 60/60 [0,940; 1] | 59/60 [0,911; 0,997] | 0/1 | p = 1 | – |

   - Sulla riacquisizione gli intervalli di Wilson si sovrappongono. L'«1 → 0 spurie» non è significativo.
5. **P3 vale in parte per costruzione.** `dub_` include `ev_nl is not None`, e `ev_nl` non torna mai `None`. Dopo un
   evento con doppia saturazione, quindi, ogni riacquisizione è «dubbia» e una spuria «non dichiarata» non può esistere.
   Il dato utile è un altro: in c1 le spurie, dichiarate o no, sono **0** in ogni cella (0/60 [0; 0,060]).
6. **L'avviso immediato è prudente fino al banale; ho misurato quanto costa** (`costo.txt`; 240 passaggi con evento,
   att).
   - **Durata.** La sfera non localizzata resta attiva da 3 a 8 s, con mediana **8 s**: l'evento localizzato è
     dichiarato solo in 81/240 passaggi.
   - **Ampiezza.** Il raggio orizzontale è 219 m a 1 s, 345 m a 3 s e **565 m** a 8 s (mediana 565 m, circa 7,6e8 m³).
   - **Tempo d'avviso.** L'avviso parte nel ciclo stesso della doppia saturazione (scarto 0,0 s), con margine sul
     frammento a 10 m di almeno 0,3 s e in mediana 0,7–1,3 s.
   - **Avvisi «inutili».** L'avviso è acceso in **71/71 [0,949; 1]** dei passaggi con evento ma senza frammenti entro
     10 m, cioè quasi tutta la cella lato. Nell'originale (att) lato aveva 0/60 avvisi. Non sono falsi avvisi, perché
     l'evento c'è, ma la regola non discrimina il pericolo.
   - **Contro un avviso sempre acceso.** Non è banale: un avviso fisso darebbe 200/200 falsi in F7c, mentre c1 ne dà
     0/200 [0; 0,019]. Il motivo però è che nel simulatore la doppia saturazione equivale all'evento: in F7c,
     `d_rad = 0` per costruzione.
7. **L'attacco ai falsi avvisi** (`attacco_f7c_2.py`, `attacco_f7c_orig.py`; seme 20261125, F7c/att, 200 passaggi).
   Il radar è saturato 1 s a 6 s per un'altra causa.
   - Con il bagliore naturale: c1 dà **11/200 [0,031; 0,096]** falsi avvisi, l'originale 0/200 [0; 0,019].
   - Con il bagliore forzato a 6 s: c1 dà **200/200 [0,981; 1]**, l'originale 0/200.
   - In entrambi i casi la continuità resta 200/200 e «libero» 0.
   - Ho trovato e corretto un mio errore: la prima versione (`attacco_f7c.py`) applicava una sola modalità per
     processo, quindi l'uscita `attacco_f7c.txt` non vale.

## Esiti delle mie previsioni

- **A1 (il riconteggio coincide): regge.**
- **A2:** la parte «per costruzione» è dimostrata dal codice. La parte «riacq_spurie ≥ 1 in totale/att c1» è
  **smentita**: le spurie sono 0.
- **A3 (originale @24 in totale con 0/n avvisi prima del frammento): regge**, 0/59.
- **A4: regge.** Davanti +7 (soglia ≥ +5). Vira +5, dentro la banda [-5; +5] e non significativo.
- **A5: smentita in parte.** La durata è sempre ≥ 3 s, ma il raggio minimo è 345 m, non più di 400 m.
- **A6: regge.** Ho misurato 11/200 falsi avvisi, contro circa 17 attesi.

## Stati proposti

- **Avviso prima del frammento nella cella totale:** sostenuto dai dati (simulato), miglioramento percettibile e
  significativo (Wilson disgiunti; test esatti come in tabella).
- **P2:** resta smentita. Il miglioramento in davanti è incoraggiante (p = 0,039, appaiato); in vira non è risolto.
- **Robustezza ai falsi avvisi:** smentita sotto interferenza radar (critica 7).

## Frasi per la giuria

**Permessa (classe «strada promettente», con il suo limite).**

- IT: «In simulazione, quando radar e camere si accecano insieme, MoVi avvisa subito il portatore e dichiara un volume
  prudente non localizzato, mai "libero". Nello scenario di accecamento totale l'avviso arriva prima del primo
  frammento in 59 passaggi su 59, contro 0 su 59 senza la correzione (stessi semi). È una strada promettente: il volume
  è ampio (fino a circa 500 m per alcuni secondi) e la riacquisizione del bersaglio migliora solo in parte.»
- EN: «In simulation, when radar and cameras are blinded together, MoVi warns the carrier at once and declares a
  conservative, unlocalised volume, never "free". In the total-blinding scenario the warning comes before the first
  fragment in 59 of 59 runs, against 0 of 59 without the fix (same seeds). It is a promising direction: the volume is
  large (up to about 500 m for a few seconds), and target reacquisition improves only partly.»

**Non permesse:**
- «risolto» o «validato»;
- «riacquisizione entro 2 s» (P2 è smentita);
- «zero falsi avvisi» (11/200 sotto interferenza);
- «nessuna identità spuria» come fatto generale (1 → 0 non è significativo).

## Che cosa propongo dopo

- Accendere l'avviso non localizzato solo se la saturazione della camera e un altro indizio indipendente (salto di
  echi, convergenza) cadono entro 0,5 s.
  - **Previsione:** l'attacco della critica 7 scende a ≤ 2/200 e l'avviso nella cella totale resta ≥ 0,9.
  - **Smentita:** l'avviso nella cella totale scende sotto 0,9.
- Ripetere P4 con questo attacco su un seme nuovo.
