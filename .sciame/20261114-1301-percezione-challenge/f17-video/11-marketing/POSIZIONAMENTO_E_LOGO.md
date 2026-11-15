# Posizionamento, marchio e titoli del video MoVi: `sciame-marketing`, f17-video/11

Inizio 2026-11-15T00:22+01:00, fine circa alle 00:40. Lavoro di preproduzione: qui non c'è nessuna cifra di risultato, e dove ne serve una c'è il segnaposto `[CIFRA: …]` da riempire con il verdetto `f15-lunga-portata/30-verdetto/VERDETTO_FASE2.md` (alle 00:24 il file non esiste ancora).

## 0. Cambi di stato e regole

- **Nessun file cancellato.** I tre `movi_wordmark*.svg` sono stati riscritti nella versione 2, dopo averne salvato la versione 1 accanto, come `movi_wordmark*_v1.svg` (addendum 13: «accanto a una copia della precedente»). La tavola v1 resta.
- **Richieste in rete:** `uv` ha scaricato da PyPI i pacchetti `fonttools` 4.68.0 e `pillow`, senza nessun dato del progetto.
- **Controlli fatti:** tutti i 12 SVG passano `xmllint`. Nessuno contiene `<image>`, `href`, `<text>` o font. Sulla tavola v2 ci sono 0 pixel verdi (tinta fra 90° e 160°, saturazione oltre 0,3). Niente git, niente sudo. Ho scritto solo in `f17-video/11-marketing/` e in `video/marchio/`.
- **Previsioni:** non le ho scritte prima delle prove visive, quindi i giudizi di §5 sono osservazioni fatte dopo, non previsioni confermate.
- **Indipendenza:** sono io sia l'autore del marchio sia chi l'ha controllato sulla tavola. I due motori di disegno (Chrome 152 e librsvg) sono indipendenti fra loro, ma non da me. Serve un lettore critico esterno (§7).

## 1. Posizionamento

**A chi parla.** Tre pubblici, con il bisogno che hanno prima di conoscere MoVi:

| Pubblico | Che cosa gli importa | Che cosa MoVi gli dà (stato) |
|---|---|---|
| Operatori di sorveglianza di piazzali, aeroporti minori e aree di prova | Sapere se uno schermo vuoto vuol dire «niente» o «non lo so», quando fumo, nebbia o detriti tolgono la vista | Ogni oggetto seguito ha sempre uno stato dichiarato: vista, non vista con una zona, ignoto. Ciò che non è osservato non è mai «visto libero» (per regola; nel prototipo `[CIFRA: fotogrammi senza «visto libero» in zona non osservata, E1–E5]`) |
| Gestori di sistemi senza equipaggio (droni, piattaforme di prova) | Sapere quando i dati di percezione non bastano più per decidere | La perdita di affidabilità è dichiarata con la sua causa («affidabilità persa: radar»), e la portata utile ridotta si dichiara per sensore e per classe (per regola EV-C ed EV-D; tempo di dichiarazione `[CIFRA]`). Il messaggio verso un autopilota resta «in progetto, mai generato» |
| Sicurezza industriale e di sito | Un avviso che non si spegne da solo e che si può rileggere dopo un evento | L'avviso di «possibile presenza» resta acceso finché non si torna a guardare. Il registro scrive per ogni fotogramma che cosa è osservato e che cosa è dedotto (per regola; formato del registro in `f16-prototipo/01-architettura/ARCHITETTURA.md`) |

**Bisogno comune:** i veicoli veloci (aerei, droni) si muovono di decine di metri al secondo, e un evento improvviso (una collisione con detriti, un motore in fiamme, una colonna di fumo, la nebbia) toglie la vista proprio quando serve. Il rischio non è solo non vedere: è credere che dove non si vede non ci sia niente.

**Posizionamento in una frase**
- EN: *For people who monitor aprons, test ranges and industrial sites where aircraft and drones move fast and visibility can collapse in a second, MoVi is a simulated multi-sensor perception prototype that states, for every tracked object, whether it is seen, not seen but within a declared zone, or unknown, and never presents what it has not observed as clear.*
- IT: *Per chi sorveglia piazzali, aree di prova e siti industriali dove aerei e droni si muovono veloci e la visibilità può crollare in un attimo, MoVi è un prototipo simulato di percezione multisensore che dichiara, per ogni oggetto seguito, se lo vede, se non lo vede ma indica una zona dove può essere, o se non lo sa; e ciò che non ha osservato non lo presenta mai come libero.*

**Rispetto a che cosa.** L'alternativa è uno schermo di tracce che mostra solo ciò che rileva: una traccia che sparisce non dice se l'oggetto se n'è andato o se il sensore è accecato. La differenza di MoVi sta nel **formato dell'uscita**, non in una prestazione misurata contro un altro sistema. **Nessun confronto numerico è ammesso:** non abbiamo misurato nessun sistema concorrente. Il principio della traccia che prosegue senza misura («coasting») esiste già nella sorveglianza aerea. Lo si cita come ispirazione, non come superiorità.

## 2. Promessa e ragioni per crederci

**L'unica promessa:** *MoVi non tace ciò che non vede: lo dichiara, e tiene acceso l'avviso finché non si torna a guardare.*

| # | Affermazione (EN / IT) | Prova e dove sta | Stato |
|---|---|---|---|
| A1 | Every tracked object is always *seen*, *not seen (zone)* or *unknown* / Ogni oggetto seguito è sempre «visto», «non visto (zona)» o «ignoto» | Formato del registro e controllo `valida_riga` (ARCHITETTURA §2); conteggio sui registri E1–E5 `[CIFRA]` | Per regola; nel prototipo, da misurare |
| A2 | What is not observed is never shown as clear / Ciò che non è osservato non è mai mostrato libero | Regola scritta e `valida_riga` («con affidabilità persa nessuna cella libera»); criteri E3 ed E4 «0 celle libere oltre la portata utile / dentro o dietro la nube» (REGOLE_E_SCENARI_EVENTI.md) | Per regola; risultato `[CIFRA]` |
| A3 | A "possible presence" warning stays until the area is looked at again / L'avviso di possibile presenza resta finché non si torna a guardare | Decisione chiusa dell'utente (addendum 11); regola dell'avviso | Per regola; nel prototipo `[CIFRA]` |
| A4 | Loss of reliability is declared, with its cause / La perdita di affidabilità è dichiarata, con la causa | EV-C ed EV-D; scenario E3(c), «affidabilità persa: radar» | Per regola; tempo di dichiarazione `[CIFRA]` |
| A5 | A smoke cloud is not mistaken for a break-up / Una nube non viene scambiata per una frammentazione | Criterio di E4 «0 eventi»; E5 «0 falsi eventi su 1000» (limite al 95 % 0,3 %) | Atteso: criterio scritto, esito `[CIFRA]` |
| A6 | Radar, LiDAR, electro-optical and thermal cameras, cooperative surveillance / Radar, LiDAR, camere elettro-ottiche e termiche, sorveglianza cooperativa | SENSORI_LUNGA_PORTATA.md: modelli dalle schede tecniche | Simulati dalle schede; nessun sensore fisico |
| A7 | Rules decide; class labels are assigned by hand / Decidono regole scritte; le etichette di classe sono messe a mano | Addendi 10 e 11 | Dichiarazione di limite, da dire in voce |

**Che cosa non si può dire, e perché.**

| Non dire | Perché | Al suo posto |
|---|---|---|
| sees through smoke / vede attraverso il fumo | Le camere elettro-ottiche lì sono «non osservato, causa nube» (E4) | "the radar still measures it; the cameras declare the cloud" / «il radar lo misura ancora; le camere dichiarano la nube» |
| predicts where it will be / prevede dove sarà | La zona è una regione dichiarata, non una posizione | "indicates a zone where it can be" / «indica una zona dove può essere» |
| detects drones at X km | Le portate sono calcoli dalle schede, non misure | "by calculation, from datasheets" / «per calcolo, dalle schede» |
| real-time, low latency (come risultato) | Non misurato su hardware | `[CIFRA: ms per ciclo, in simulazione]`, oppure niente |
| detect and avoid, threat, target, intercept, counter-drone / minaccia, bersaglio, contrasto | Perimetro: solo osservazione e avviso | "observe and warn", "attention", "unverified zone" / «osserva e avvisa», «attenzione», «zona non verificata» |
| AI recognises aircraft / l'IA riconosce gli aerei | Il classificatore è richiesto ma non realizzato | "labels assigned by hand" / «etichette messe a mano» |
| safe, certified, compliant, guaranteed / sicuro, certificato, conforme, garantito | Nessuna norma letta né applicata | "inspired by" / «ispirato a» |
| clear, all clear, go / libero, via libera | Regola 9 del video | "seen clear up to d metres" / «visto libero fino a d metri», solo dove il registro lo dice |
| debris cleared / detriti assenti | Al suolo è solo ispezione (EV-E) | "possible debris: inspect" / «possibili detriti: ispezionare» |

**Punto aperto per il coordinatore e il comunicatore.** Le regole 15 e 24–25 della versione a corto raggio vietano «in volo», «drone» e «UAV». Con il nuovo caso centrale, aerei e droni sono gli **oggetti osservati**, e nominarli è inevitabile. Propongo di tenere il divieto solo per il **sensore** e per la piattaforma che lo porta («ferma» oppure «configurata, non provata»), e di dire l'ambito sempre con le parole della traccia: «monitoraggio di attività e oggetti in ambienti aerospaziali e industriali». Va deciso prima del copione.

## 3. Tagline: tre alternative e la scelta

| | EN | IT | Prova | Rischio |
|---|---|---|---|---|
| T1 | **Seen, unseen, unknown: always declared.** | **Visto, non visto, non so: sempre dichiarato.** | A1: è il formato dell'uscita, tenuto da un controllo su ogni riga | «always» vale per costruzione del formato. Se la `[CIFRA]` di A1 non fosse 100 %, si scende a T3 |
| T2 | What it cannot see, it never calls clear. | Ciò che non vede, non lo chiama mai libero. | A2 | Usa «clear» e «libero» da soli, in conflitto con la regola 9 (nessun «via libera» suggerito). È anche la promessa più esposta a un controesempio |
| T3 | The unseen stays on screen until someone looks again. | Ciò che non si vede resta a schermo finché non si torna a guardare. | A3 | Lunga, e più debole come ricordo |

**Scelta: T1.** È la più forte fra quelle che le prove reggono. Promette una **dichiarazione**, non una prestazione: dice di sé solo ciò che il formato del registro impone a ogni fotogramma. Ripete i tre stati che il video mostra. Non contiene «libero», né superlativi, né cifre. Si chiude con il marchio, che dice la stessa cosa in forma: il pieno, il tratteggiato, il segno che resta. Il sottotitolo ufficiale resta accanto al titolo: *A prototype that declares what it has not observed* / *Un prototipo che dichiara ciò che non ha osservato*.

## 4. Titolo del video e titoli di coda

**Titolo (apertura, 0:00–0:04; etichetta «Schematic» non necessaria: è un titolo, non una scena)**
- Wordmark MoVi largo 1080 px. Sotto, in Inter 600 da 44 px: **A prototype that declares what it has not observed** / *Un prototipo che dichiara ciò che non ha osservato*.
- Riga piccola (JetBrains Mono, 24 px, #8A97A8): `SDMs · The Big Hack 2026 · Simulation and schematics only` / `SDMs · The Big Hack 2026 · Solo simulazioni e schemi`.
- Nome del file e titolo di caricamento: **MoVi: a prototype that declares what it has not observed (SDMs, The Big Hack 2026)**.

**Cartello dei limiti (prima dei titoli di coda, 4 s, letto anche in voce)**
- EN: *Every scene is a simulation or a schematic. No physical sensor was used: sensors are modelled from public datasheets. Class labels are assigned by hand. MoVi observes and warns; no output is a command.*
- IT: *Ogni scena è una simulazione o uno schema. Nessun sensore fisico è stato usato: i sensori sono modellati dalle schede tecniche pubbliche. Le etichette di classe sono messe a mano. MoVi osserva e avvisa; nessuna uscita è un comando.*

**Chiusura (2:44–2:48):** logo SDMs alto 96 px; tagline T1 in inglese, con l'italiano nei sottotitoli.

**Titoli di coda (2:48–2:51,5; a scorrimento lento o in due cartelli; i testi fra parentesi quadre vanno scelti prima dell'esportazione)**

```
MoVi
A prototype that declares what it has not observed
Un prototipo che dichiara ciò che non ha osservato

Team SDMs
Ignazio Crocchiolo · Federico Dellini · Danilo Amalfitano
Emanuele Ciotola · Pierfrancesco Amendola

The Big Hack 2026 · Codemotion · Città della Scienza, Napoli

Music / Musica
[SE USATO] "Dreams Become Real" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
[SE USATO] "Ossuary 5 - Rest" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
[SE USATO] "above the clouds" John Bartmann, CC0 1.0 (attribution not required)
[SE USATO] Ambient pad generated by the team / Tappeto sonoro generato dal gruppo

Voice / Voce: synthetic, Kokoro-82M (Apache-2.0), voice bm_george [it: im_nicola]
Fonts: Inter (SIL OFL 1.1, The Inter Project Authors)
       JetBrains Mono (SIL OFL 1.1, The JetBrains Mono Project Authors)
Animation / Animazione: HyperFrames (Apache-2.0), GSAP (GreenSock Standard License)
Sensor models from public datasheets; sources in the technical report
Modelli dei sensori dalle schede tecniche pubbliche; fonti nella relazione tecnica

Logo and visual identity: original work by SDMs
Logo e identità visiva: opera originale di SDMs
© 2026 SDMs
```

Le fonti delle licenze sono in `00-strumenti/STRUMENTI.md` §1.1, §3.5 e §4.1. La formula di MacLeod è quella standard del sito; il generatore di crediti della pagina non è stato letto (**non verificato**, come in STRUMENTI.md). La città «Napoli» per Città della Scienza è un dato pubblico non ricontrollato qui: **non verificato**. Nei titoli si usa solo il nome «Codemotion», nessun logo di terzi.

## 5. Il marchio (dettagli in `video/marchio/GUIDA_MARCHIO.md`)

- **Simbolo SDMs:** un disco pieno ciano #3DD6E8 (visto) e una zona tratteggiata ambra #F5A524 con dentro un anello vuoto (non visto, il segno che resta). Accanto, «SDMs» in Inter SemiBold convertito in tracciati, colore #E8EDF2.
- **MoVi:** la «o» è l'anello tratteggiato ambra; il punto della «i» è il disco ciano.
- Ci sono la versione a colori, la monocroma bianca e la monocroma scura; fondo trasparente. Niente verde: le tinte sono 186° e 37°, fuori dalla fascia 90°–160° del controllo Q11. I contrasti su #0B0F17 sono 10,9:1, 9,4:1 e 16,3:1 (calcolati qui con la formula WCAG).
- **Controllo visivo** (`video/marchio/tavola_controllo_v2.png`, guardata con lo strumento di lettura delle immagini; più un taglio a 64 px fatto con librsvg):
  - **v1:** a 64 px la «o» a 6 tratti, con il vuoto in alto e in basso, si leggeva come due punti («M:Vi»). Smentita e rifatta.
  - **v2:** con 8 tratti al 70 % la «o» a 64 px si legge come «o» in entrambi i motori.
  - Il logo SDMs si legge fino a 24 px. Per MoVi la grandezza minima dichiarata è 32 px, perché a 24 px il tratteggio si impasta.
- **Licenza:** opera originale del gruppo. Inter è sotto OFL 1.1 e le lettere sono convertite in tracciati. La ricerca di anteriorità su marchi simili **non è stata fatta**.

## 6. Stati proposti

| Enunciato | Stato |
|---|---|
| Il marchio si legge a 64 px e a 1080 px, senza verde | Verificato su Chrome 152 e librsvg, sulla tavola v2 (controllo dell'autore) |
| T1 è vera per il prototipo | Per regola (formato del registro); il risultato attende la `[CIFRA]` del verdetto |
| MoVi è migliore di uno schermo di tracce tradizionale | **Non provato**: non entra nel messaggio |

## 7. Proposte e passi successivi

1. **Test dei cinque secondi** su 3–5 persone fuori dal gruppo. Si mostra il logo e si chiede «che cosa vuol dire?».
   - Previsione: almeno 3 su 5 nominano «visto / non visto» o «traccia».
   - Smentita: 2 o meno. In quel caso si aggiunge sotto il simbolo, nel solo titolo d'apertura, la riga «seen · unseen».
2. **Taglio di T1 dopo il verdetto.** Se la `[CIFRA]` di A1 o di A2 non fosse piena, si passa a T3 senza «always».
3. Il **videomaker** usa l'animazione del logo descritta nella guida (§7), e la usa anche come transizione «visto → non visto» del racconto.
4. Il **lettore critico** rilegge §2 e il cartello dei limiti contro il copione.
5. Il **coordinatore** decide il lessico «drone, in volo» (§2, punto aperto).
