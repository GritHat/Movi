# Previsioni — `sciame-scene-dinamiche`, f8, fase f3 (soluzione)

Sigla: `sd`. Tutto è simulazione su CPU, a sensore fermo, soggetto puntiforme.

## Prima serie — scritta alle 2026-11-14T16:41:20+01:00 (`date -Is`), prima di ogni riga di codice mio

**Che cosa provo.** La composizione che propongo come modifica del nucleo, nei due pezzi che né il banco (`11-misure`) né il
torneo (`12-torneo`) hanno eseguito:

- **`sd-1` (composizione principale).** Regione = R90 di C-004 (fronte + scia, un solo livello) con un **pavimento**: se in un
  ciclo C-004 non emette celle, la regione è tutto il «non visto libero» dell'ombra (ombra stimata + fascia 0,20 m), segnata
  «ampio». Punto mostrato = **ibrido con attesa, senza particelle**: il punto a velocità costante del filtro finché sta su celle
  non viste libere; al primo ciclo in cui cadrebbe su una cella vista libera oltre la fascia (dopo essere entrato nell'ombra, o
  comunque dopo 8 cicli) non ci va: resta fermo dov'è per **8 cicli (0,53 s)**, poi va verso il baricentro pesato dei membri di
  C-004 non visti liberi, al più 0,167 m per ciclo, e non entra mai in una cella vista libera (se il passo ce lo porterebbe,
  resta fermo).
- **`sd-0` (ripiego).** Regione = disco da tabella di C-005 (un livello) con lo stesso pavimento; stesso punto, con il
  baricentro della regione al posto di quello dei membri.

**Parametri fissati ora, non ritoccabili dopo la prova:** attesa 8 cicli; passo massimo 0,167 m; fascia 0,20 m; lisciatura di
C-004 a 3 passate e taratura del banco (`taratura.txt`, semi 1000–1199) così come sono.

**Dati.** Codice del banco copiato (generatore `gen.h`, filtro, C-004, C-005, valutatore): condivido con il banco tutto tranne le
due regole nuove. Semi di prova **12000–12399**, mai usati da nessuno (sviluppo 5000+, taratura 1000–1199, prova del banco
9000–9399, attacchi 9500–9899); 400 passaggi per comportamento (0–6) e geometria (D, T, L), rilevamento 0,9, fascia 0,20 m.
Prova di fumo ammessa solo sui semi di sviluppo 5000–5059. C-004 e C-005 girano sugli stessi semi (confronto appaiato).

| # | Previsione | Misura | Smentita se |
|---|---|---|---|
| P-sd-1 | Con il pavimento `sd-1` non ha vuoti | passaggi con almeno un ciclo senza regione, D, T, L, comportamenti 0–6 | ≥ 1 passaggio |
| P-sd-2 | Il pavimento non abbassa la copertura | minimo di R90 sul percorso (prosegue, rallenta, sosta, torna, sosta lunga) fino a 3 s: `sd-1` ≥ C-004 cella per cella; atteso ≥ 0,90 in D, T, L | una cella sul percorso (n ≥ 30) sotto 0,85 |
| P-sd-3 | Il punto di `sd-1` non sta su celle viste libere dopo l'ingresso | cicli con il punto su cella vista libera oltre la fascia, dopo il quinto ciclo: 0; in tutto, non più di quelli del filtro nei primi 5 cicli | ≥ 1 ciclo dopo il quinto |
| P-sd-4 | Il punto non arretra su chi prosegue | passaggi «prosegue» con un passo all'indietro oltre 5 cm: < 5 % in T e L; ≤ 10 % in D (qui sono meno sicuro: ombra corta) | ≥ 5 % in T o in L |
| P-sd-5 | Il punto è efficace | «squadra», T: errore mediano ≤ 0,5 m a 1 s e ≤ 1,0 m a 2 s; nessuna cella comportamento × τ (n ≥ 30) oltre 1,5 volte la migliore base (fermo, velocità costante); atteso ≤ 1,2 | una cella oltre 1,5 |
| P-sd-6 | Il salto alla ricomparsa sta fra l'ibrido e il baricentro | salto mediano, tutti i comportamenti con ricomparsa, T: ≤ 0,6 m (banco: ibrido 0,38, baricentro 1,12, fantasma 1,32) | > 1,0 m |
| P-sd-7 | Il ripiego `sd-0` non ha vuoti dopo 5 cicli e copre come C-005 | passaggi con un vuoto dopo il quinto ciclo: 0; minimo sul percorso fino a 3 s ≥ 0,85 | 1 passaggio con un vuoto dopo il quinto ciclo, o una cella sotto 0,85 |
| P-sd-8 | Il costo in più è trascurabile | tempo per ciclo e traccia di `sd-1` oltre C-004, 95º percentile, 1 e 10 tracce: < 0,05 ms e < 0,5 ms | > 1 ms con 10 tracce |
| P-sd-9 | La prima misura cade vicino alla regione | prima misura entro 0,40 m da R90 di `sd-1`: ≥ 0,99 in D, T, L | < 0,95 |
| P-sd-10 | Nessun passo lungo | passaggi con un passo del punto oltre 0,167 m: 0 | ≥ 1 |

**Dove mi aspetto di sbagliare.** P-sd-4 in D; P-sd-5 a 5 s su «torna» e «sosta» (l'attesa di 0,53 s ritarda il rientro del
punto); P-sd-3 se il baricentro dei membri attraversa una rientranza vista libera (il punto resta fermo: regge, ma l'errore sale).

## Esiti della prima serie

Lanci alle 16:42:59 (`ris/prova_{D,T,L}.tsv`, lettura in `ris/LETTURA.txt`; tempi in `ris/tempi.txt`). Codice congelato prima
dei lanci (`CONGELATO.txt`, 16:42:42) e non toccato dopo. Prova di fumo: 60 semi di sviluppo in T, vista prima; nessun
parametro cambiato. Passaggi validi: 2716 (D), 2800 (T), 2798 (L).

| # | Esito | Numeri |
|---|---|---|
| P-sd-1 | **regge** (per costruzione, ricontato) | passaggi con un vuoto: 0 / 0 / 0 (C-004 sugli stessi semi: 23 / 14 / 0); cicli in cui scatta il pavimento: 473 / 15 / 0 |
| P-sd-2 | **smentita in D** per un millesimo, regge in T e L | `sd-1` = C-004 cella per cella (questa metà regge); ma il minimo sul percorso fino a 3 s è 0,849 in D («prosegue» a 3 s, 101 su 119, Wilson 0,774–0,902): **sotto 0,85 di un millesimo e sotto lo 0,90 atteso**. T 0,962 (252/262), L 0,920 (357/388). A 5 s: 0,737 (D, 42/57), 0,927 (T, 51/55), 0,858 (L, 259/302) |
| P-sd-3 | **smentita** | punto su celle viste libere dopo il quinto ciclo: 13 (D), 0 (T), 23 (L) cicli; in tutto 434 / 397 / 355 (il filtro nei primi 5 cicli: 434 / 403 / 344; per tutta l'occlusione 22 192 / 38 367 / 13 541). Causa probabile, non verificata: i cicli 6–8 concessi prima dell'ingresso |
| P-sd-4 | **regge** in T e L, **attesa mancata in D** | «prosegue» con un passo indietro: 4,0 % (T, 16/400), 3,5 % (L, 14/400), **18,2 % (D, 70/385)**; fantasma di C-004 54–68 %, baricentro dei membri 19–38 %, ibrido del banco 11,5–23,6 % |
| P-sd-5 | **regge** | «squadra», T: 0,182 m a 1 s, 0,386 m a 2 s (0,597 a 3 s, 0,921 a 5 s); peggior rapporto con la migliore base 1,22 (D, «torna» a 5 s: sopra l'1,2 atteso), 1,00 (T), 1,01 (L) |
| P-sd-6 | **mista**; la mediana d'insieme non l'ho calcolata (l'uscita dà le mediane per comportamento) | T: prosegue 0,366, rallenta 0,527, lontano 0,539, sosta lunga 0,315 m (reggono); svolta 0,991; **sosta 1,295 e torna 1,410 m (oltre 1,0)** |
| P-sd-7 | **regge** | `sd-0`: vuoti dopo il quinto ciclo 0 / 0 / 0 (C-005: 61 / 19 / 0); minimo sul percorso fino a 3 s 0,866 (D, 103/119), 0,911 (T), 0,953 (L). Ma l'area sul percorso da 2 s è 1,06–1,54 volte l'ombra, e il suo punto supera 1,5 volte la base in D («torna» a 5 s: 1,57) |
| P-sd-8 | **regge** | in più di C-004, 95º percentile: 0,005 e 0,051 ms (T, 1 e 10 tracce), 0,008 e 0,074 ms (L). C-004 sugli stessi lanci: 0,078 e 0,63 ms (T), 0,15 e 1,34 ms (L). In C, macchina condivisa |
| P-sd-9 | **smentita come scritta, regge sul percorso** | prima misura entro 0,40 m da R90: su tutti i comportamenti 0,988 / **0,939** / 0,951; sul percorso 0,989 (1136/1149) / 0,998 (1044/1046) / 0,990 (503/508); per chi svolta o esce lontano 0,979 / 0,646 (135/209) / 0,721 (62/86) |
| P-sd-10 | **regge** | 0 passaggi con un passo oltre 0,167 m |

**Notato dopo, non previsto.** (a) In D la copertura di C-004 su «prosegue» scende a 0,861 a 2 s e 0,849 a 3 s (sono i passaggi
lenti, ancora nascosti a 2–3 s): il banco dava 0,935 come minimo in D e il torneo 0,898, su altri semi. (b) Su «giurato» il punto
di `sd-1` a 2–3 s è peggiore del baricentro dei membri (T: 0,465 e 0,687 contro 0,421 e 0,611 m): l'attesa di 0,53 s ha un prezzo
su chi si ferma. (c) Soglia «ampio» all'80 % dell'ombra: 50,4 % dei cicli in D, 0,0 % in T e L.

## Seconda serie — previsioni per l'attacco successivo, scritte alle 2026-11-14T16:48:57+01:00, senza prova mia

Nessuna di queste è stata eseguita. Le smentisce chi attacca `MODIFICHE_CONTINUITA.md`.

| # | Previsione | Smentita se |
|---|---|---|
| A-sd-1 | Riga d'ingresso di B5 riscritta **insieme** a `sd-1` (mai provate insieme), rilevamento 0,9, geometria T: copertura sul percorso fino a 3 s ≥ 0,90 e non più di 20 passaggi su 2800 con un ciclo nascosto senza traccia pendente | una cella sul percorso sotto 0,85, o più di 20 passaggi |
| A-sd-2 | Corpo largo 0,45 m **messo nella griglia** (le celle del corpo tagliato sono «occupato osservato», non «libero»), ombra a −20 cm e rilevamento 0,7 insieme: `sd-1` sul percorso ≥ 0,85 a 1 e 2 s; a 3 s mi aspetto che ceda (0,60–0,85); R100 al 100 % | sotto 0,80 a 2 s, o un passaggio fuori da R100 |
| A-sd-3 | Con il pavimento, nessun ciclo senza regione in nessun braccio (ombra stretta, rilevamento 0,7, corpo largo), finché l'ombra ha almeno una cella | un passaggio con un vuoto |
| A-sd-4 | Portando da 8 a 5 i cicli concessi al punto prima dell'ingresso, i cicli con il punto su celle viste libere dopo il quinto vanno a 0, su semi nuovi | un ciclo |
| A-sd-5 | Geometria della demo, semi nuovi (né 9000–9399 né 12000–12399): R90 di `sd-1` su «prosegue» sta ≥ 0,93 a 1 s e fra 0,80 e 0,93 a 3 s | sotto 0,90 a 1 s, o fuori da 0,80–0,93 a 3 s |
| A-sd-6 | Due tracce pendenti nella stessa ombra: nessun riaggancio con identità (regola del nucleo), due regioni indipendenti, ciascuna ≥ 0,85 sul percorso fino a 2 s | un riaggancio con identità, o una cella sotto 0,80 |
| A-sd-7 | `sd-1` in Python puro: 95º percentile ≤ 6,7 ms per ciclo con 3 tracce pendenti (l'autore di C-004 misurava 0,48 ms a traccia e 4,3 ms all'ingresso) | oltre 20 ms |
| A-sd-8 | Sosta di 30 s: `sd-1` resta ≥ 0,90 fino a 3 s e passa ad «ampio» (orizzonte dichiarato), dove contiene il nascosto nel 100 % dei cicli | un ciclo «ampio» con il nascosto fuori dalla regione e dentro la griglia |
