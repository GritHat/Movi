Canarino: sciame-canarino-55f6adcfa718b00e

# Parere di dominio sull'estensione f7 — `sciame-esperto-dominio`, corsia A

**Campo in cui parlo:** monitoraggio e ispezione in ambienti aerospaziali e industriali, e percezione per piattaforme senza equipaggio, dal lato delle mappe volumetriche. Non è un parere di sicurezza funzionale né legale. Sigle: **[A]** pagina aperta oggi, **[R]** solo risultato di ricerca, **NV** non verificato, **[inf.]** inferenza mia.

## 1. Scostamenti, regole violate, previsioni smentite

- **Lancio fallito.** Il primo lancio di `griglia_densa` è stato fermato da `timeout 120` senza uscita; rilanciato con meno fotogrammi nelle righe a piena risoluzione (`PREVISIONI.md`).
- **Previsioni** (scritte alle 15:06:07 e 15:08:44, prima delle prove). **Smentita P8:** aspettavo il 45–70 % dei voxel toccati, sono l'8,5–20,9 %. **Smentite in parte P5** (la scatola da 0,5 m posta a 2 m fa ombra fino a 3,43 m, cioè fino al bordo) **e P6** (a piena risoluzione 148–198 ms, non 50–150; il caso peggiore è la parete vicina, non la stanza vuota). **Non risolta P3:** nessuna fonte trovata che misuri uno stereo attivo in nebbia o fumo. Reggono P1 (salvo OpenVDB, oggi Apache 2.0), P2, P4, P7.
- **Fonti.** Le pagine le riassume un modello ausiliario: le frasi fra «» vanno ricontrollate dal curatore. Non aperte: la circolare FAA (403; letta in una fonte secondaria), la licenza di nvblox (404), l'articolo sulla polvere (403).
- **Indipendenza.** Programma, scena e autore della misura sono miei; la scena è sintetica: vale per l'ordine di grandezza del costo, non per il sensore né per il prototipo.
- **Lunghezza:** tre pagine, misurate con pandoc e xelatex (A4, corpo 10, margini 1,8 cm).

## 2. Critiche, ciascuna con la prova

**C1. «Sparsa» è la premessa sbagliata a questa scala.** La regione 6 × 4 × 3 m, densa, con 4 byte per voxel, occupa **2,20 MB a 5 cm** (576 000 voxel) e **0,27 MB a 10 cm** (`risultati_griglia_densa.txt`). Una struttura sparsa risparmierebbe un fattore 5–12, ma su una memoria che sta già nella cache. Le librerie sparse nascono per mappe illimitate: Bonxai si dice «Sparse» e «Unbounded» [A, S4]; nel volo la mappa locale tipica è invece una griglia densa che scorre con il veicolo, «an occupancy grid stored in a three-dimensional circular buffer» [A, S7].

**C2. Il costo misurato regge solo con la decimazione.** Aggiornamento della sola mappa, un processo, 200 fotogrammi: con un raggio ogni 4 pixel per lato (25 440 raggi) il 95° percentile è **9,7–13,3 ms a 5 cm** (massimo 15,5) e 5,1–7,2 ms a 10 cm; a piena risoluzione (407 040 raggi) sale a **148–198 ms** e 76–107 ms, oltre i 66 ms del ciclo. Rifare: `gcc -O2 -o griglia_densa griglia_densa.c -lm && timeout 100 ./griglia_densa`. Non è la catena intera.

**C3. La sicurezza industriale usa tre stati per fotogramma, non una probabilità con memoria.** Un sistema 3D per la sorveglianza di velocità e separazione classifica i volumi in «empty (something can be seen behind it), occupied, or unknown», e ciò che nessun sensore vede è «treated as occupied for SSM purposes» [A, S8: l'autrice è del costruttore]. La distanza di protezione della ISO/TS 15066 somma percorsi nel caso peggiore e incertezze di posizione [A, S9]. I sensori 3D certificati lavorano a campi di protezione [R, S10]. Quindi lo strato a log-odds di `promptMare.txt` §4 può solo *informare* («occupato ricordato»): il «libero» resta dell'osservazione corrente. 
| Libreria | Struttura | Licenza | Prestazione dichiarata | «Sconosciuto» |
|---|---|---|---|---|
| OctoMap [A, S1] | octree, log-odds | BSD (visualizzatore GPL) | nessun numero in pagina | implicito: «Unknown areas… are implicitly encoded» |
| Voxblox [A, S2] | distanza con segno troncata, a strati | BSD-3 | «runs in real-time on a single CPU core» | NV |
| UFOMap [A, S3] | octree | BSD-2 | «real-time (2 Hz) at 2 mm» | **esplicito**: «occupied, free, and unknown» |
| OpenVDB [A, S5] | albero gerarchico sparso | Apache 2.0 (era MPL 2.0) | NV | NV |
| Bonxai [A, S4] | gerarchica, solo intestazioni | MPL-2.0 | creazione 1165 µs contro 25 522 di OctoMap («preliminary») | nessuna semantica: puntatore nullo |
| nvblox [A, S6] | distanza con segno, su GPU | NV | «up to a 177x speed-up» | NV; chiede la GPU: fuori dai vincoli |

Un non addetto prenderebbe una di queste librerie con i valori predefiniti: solo una delle sei dichiara lo sconosciuto.

**C4. Senza una superficie dietro non c'è «libero».** Nella stanza vuota da 6 m il **44,2 % dei raggi non ha ritorno** e non aggiorna nulla: i voxel toccati sono al più il 20,9 %. In un hangar (decine di metri) una camera da 6 m lascia quasi tutto il volume «sconosciuto». Il nucleo funziona perché il suolo fa da superficie di fondo; in quota quel fondo manca. Va detto alla giuria.

**C5. Lo scenario «nebbia» (§8-A) come azzeramento casuale prova la logica, non la nebbia.** Si sa, per sensori vicini: in fumo denso «LIDAR and visual stereo vision fail», radar e infrarosso termico reggono [A, S11]; la profondità delle camere RGB-D in polvere è «heavily distorted» [R, S12]. Sullo stereo attivo non ho trovato misure. L'azzeramento casuale non contiene i ritorni falsi vicini, la dipendenza dalla distanza, le chiazze. È onesto dire: «con misure mancanti il sistema non produce mai un libero e dichiara l'affidabilità persa sotto soglia». **Critica al nucleo:** B2 si dichiara invalido sotto il 95 % di suolo valido e l'allarme di B8 scatta sotto metà delle celle valide (`SOLUZIONE_V2.md`): fra le due soglie il sistema non è né provato né in allarme [inf.: l'equivalenza fra le due misure è NV].

**C6. «Detriti e frammenti»: i limiti di osservabilità** (`risultati_osservabilita.txt`). Impronta di un pixel: 6,7 mm a 3 m, 13,4 mm a 6 m. Con almeno 5 pixel di lato (criterio mio): **3,4 cm a 3 m, 6,7 cm a 6 m**; un oggetto di 1 cm si vede solo entro 0,89 m. Velocità: attraversando il campo a 3 m restano 4–5 fotogrammi fino a **17–21 m/s a 15 fotogrammi al secondo** (34–43 a 30); ma la porta del nucleo è tarata su 2,5 m/s (16,7 cm per fotogramma) e un oggetto caduto da 2 m viaggia a 6,3 m/s (42 cm per fotogramma). Risposta corretta: **«non osservabile»**; al più un voxel occupato transitorio senza traccia, mai una previsione. Conseguenza di dominio: gli oggetti estranei di riferimento sulle piste (sfera di 4,3 cm, cilindro di 3 × 3,8 cm [A, S13, fonte secondaria]) stanno sotto i 7 cm di quota minima del nucleo: **il prototipo non rileva oggetti estranei al suolo**, e non va detto.

**C7. Il cuneo fino al bordo sbaglia solo per ostacoli bassi e vicini, e dal lato prudente.** Con il sensore a 1,2 m l'ombra al suolo finisce a d·h/(h − a): scatola da 0,3 m a 1,3 m → 1,73 m (il 25,5 % del cuneo è davvero in ombra); da 0,5 m a 1,5 m → 2,57 m (71,4 %); da 0,5 m a 2 m → 3,43 m (cuneo esatto). Il caso tipico dell'hangar è l'opposto: l'ostacolo **sospeso** (ala, piano di coda, carico): solo una rappresentazione in quota dice «libero fino a quota q» [inf.].

**C8. Posa (§7).** Un grado d'errore d'assetto sposta un punto di **5,2 cm a 3 m** (un voxel da 5 cm) e di 10,5 cm a 6 m (`conti_a_mano.txt`): su una mappa nel riferimento del mondo l'oscillazione del volo stazionario diventa falso «libero» ai bordi (prova 6). In hangar il GNSS manca; i droni da ispezione si guidano con il LiDAR [R, S15]. Una mappa nel riferimento del sensore, rifatta a ogni fotogramma, non chiede la posa (`MOTO_PROPRIO.md`, f6). A un velivolo la mappa in quota **serve** (la prevenzione delle collisioni per settori è solo orizzontale: f6, S18), ma senza posa misurata si trasferisce la struttura, non le garanzie.

**C9. Lessico.** «UAV», «drone», «beneficio misurabile per applicazioni UAV» restringono l'ambito oltre la traccia; «detriti», «frammenti», «perturbazione improvvisa» si prestano a una lettura d'ingaggio. Da dire: oggetti caduti o estranei, ingresso simultaneo di più persone e mezzi.

## 3. `promptMare.txt`: utile, inutile, sbagliato (per il mio campo)

- **Utile:** §4, storia contro garanzia corrente (è la prassi della sicurezza, C3); §5, le cinque classi di voxel; §7, moto condizionato alla posa e nessun 360°; §8, il divieto di confondere l'azzeramento con la nebbia e la risposta «non osservabile»; §10, prove 1, 2, 6, 8, 9; §3, alternative A (densa scorrevole) e D (ibrida).
- **Inutile a questa scala:** §3, B e C, CSR e COO (C1); §6, stato a sei componenti e IMM (nessun bersaglio in volo nella prima demo); §12 e §13 (già detto dal contratto).
- **Sbagliato o da correggere:** la sparsità come fonte d'efficienza (C1, misurato); lo scenario A letto come nebbia (C5); il criterio «beneficio per applicazioni UAV» (§14: non è nella traccia).

## 4. La traccia: che cosa vuol dire «monitoraggio di attività e oggetti»

Nel campo vuol dire sapere **chi e che cosa si muove in un'area di lavoro dichiarata, dov'è, e quando non lo si sa più**. Tre casi documentati:
1. **Area attorno a un velivolo, in hangar o sul piazzale.** Il danno a terra potrebbe arrivare a «nearly $10 billion by 2035»; nastri, caricatori, scale e pontili causano il «40% of total incidents»; i mezzi con «anti-collision and inching technology» lo ridurrebbero del 42 % [A, S14: stima dell'associazione]. Qui l'occlusione è la regola: il velivolo e i mezzi nascondono le persone.
2. **Area condivisa fra persone e robot o mezzi:** sorveglianza di velocità e separazione, dove il non visto vale occupato (C3).
3. **Ispezione visiva con drone in hangar,** accettata dall'autorità statunitense per un vettore e approvata dai due maggiori costruttori [A, S16]: la piattaforma porta il sensore e ha bisogno di una localizzazione propria.

**Racconto di demo più fedele [inf.]:** «una stazione fissa sorveglia l'area attorno a un velivolo o a una macchina: segue persone e mezzi (le attività) e gli ostacoli fermi (gli oggetti); quando un carrello ne nasconde uno dice *possibile presenza dietro l'ostacolo, da n secondi*, non *area vuota*; a sensore coperto dice *affidabilità persa*». **La piattaforma senza equipaggio** sta lì in due modi: è uno dei mezzi osservati, ed è uno dei modi di portare il sensore (ferma equivale alla stazione; in moto resta condizionata alla posa).

## 5. Stati proposti

- **Sostenuto dai dati** (una macchina, scena sintetica): memoria densa 2,20 e 0,27 MB; aggiornamento ≤ 13,3 ms al 95° percentile con 25 440 raggi; oltre 66 ms a piena risoluzione.
- **Smentito:** «lo sparso è necessario per la memoria» alla scala 6 × 4 × 3 m; «il cuneo sovrastima sempre l'ombra degli ostacoli bassi» (per la scatola da 0,5 m a 2 m è esatto).
- **Dimostrato** (geometria della camera a foro, 848 × 480, 87°): i limiti di C6 e l'ombra di C7.
- **Non risolto:** l'effetto di nebbia e fumo sullo stereo attivo (lo decide una misura della quota di profondità valida in aerosol, o una fonte); il vetro (un raggio che attraversa una lastra segna «libero» anche in 3D: prova 8 non superata [inf.]).
- **Q1, voto di corsia:** **NO** alla mappa *sparsa e probabilistica* come garanzia; **SÌ CONDIZIONATO** a una griglia 3D *densa e locale* in affiancamento, se la demo ne mostra un beneficio (proposta 2). **Q2:** primo ambito detto come al §4.

## 6. Proposte

**`esperto-dominio-1` — Zone dichiarate a quattro esiti, con registro degli eventi.** L'operatore dichiara una o più zone sul piano (per esempio la fascia attorno al velivolo). A ogni ciclo ogni zona esce in un solo stato: «occupata, osservato»; «possibile presenza»; «non verificabile» (almeno una cella non osservata o in ombra); «vuota, osservato» (tutte le celle libere negli ultimi 3 fotogrammi). «Affidabilità persa» prevale. Ogni cambio va in un registro con ora, stato ed età. *Guadagno:* copre «monitoraggio di attività e oggetti», che `SOLUZIONE_V2.md` §7 dichiara non coperto, senza toccare il nucleo. *Vincoli:* zone fra 1,24 e 3 m; non è un dispositivo di sicurezza. *Chi la prova:* validazione, sul simulatore esistente. *Falsificatore (5 minuti):* nell'atto 4, con la persona nascosta dentro la zona, contare i fotogrammi «vuota, osservato». **Atteso: 0** (smentita: 1). Braccio di utilità: una zona di 1 × 1 m in campo aperto fra 1,5 e 2,5 m deve uscire «vuota, osservato» in circa il **96,6 %** dei fotogrammi con suolo valido 0,95 (75,6 % con 0,90); sotto il 90 % la zona non informa.

**`esperto-dominio-2` — Se 3D, allora griglia densa locale nel riferimento del sensore, a tre stati più l'età.** Regione 6 × 4 × 3 m a 5 cm, un raggio ogni 4 pixel per lato. Un voxel è «libero osservato» solo se attraversato, nel fotogramma (o negli ultimi 3), da un raggio con ritorno valido oltre di esso; mai toccato vuol dire «sconosciuto»; il log-odds resta informativo. La colonna si proietta sulla griglia del nucleo come «libero fino a quota q». *Guadagno:* ombre corrette per ostacoli bassi e vicini (25–71 % del cuneo restituito nei casi di C7), ostacoli sospesi, struttura pronta per una piattaforma in quota. *Vincoli:* sensore fermo; vetro non risolto; nessuna garanzia in moto. *Chi la prova:* strutture dati e visione. *Costo:* nessun hardware in più; integrazione stimata 6–10 ore [stima mia, NV]. *Falsificatore (5 minuti):* `timeout 100 ./griglia_densa` sul portatile della squadra. **Atteso:** riga «parete a 2 m, 5 cm, 25 440 raggi» con 95° percentile ≤ 20 ms (smentita: > 66 ms). Sulla scatola da 0,5 m a 1,5 m: celle di suolo «libero osservato» fra 2,57 e 3 m (smentita: nessuna, oppure un voxel mai attraversato che risulta libero).

## 7. Che cosa propongo dopo

Al curatore le citazioni [A] e i tre documenti non aperti. Alla validazione il falsificatore di `esperto-dominio-1`. Al metrologo una misura di dieci minuti con la camera vera e un aerosol innocuo (vapore): quota di profondità valida e ritorni falsi, per chiudere P3. Nel documento: togliere ogni accenno agli oggetti estranei al suolo e dichiarare C4.

## Fonti

S1 https://octomap.github.io/ · S2 https://github.com/ethz-asl/voxblox (BSD-3; TSDF; «runs in real-time on a single CPU core», https://arxiv.org/abs/1611.03631) · S3 https://arxiv.org/abs/2003.04749 e https://github.com/UnknownFreeOccupied/ufomap (BSD-2) · S4 https://github.com/facontidavide/Bonxai (MPL-2.0) · S5 https://github.com/AcademySoftwareFoundation/openvdb (Apache 2.0) · S6 https://arxiv.org/abs/2311.00626 (nvblox: GPU; licenza NV) · S7 https://arxiv.org/abs/1703.01416 · S8 https://www.therobotreport.com/advanced-vision-future-robot-safety-manufacturing/ · S9 https://pmc.ncbi.nlm.nih.gov/articles/PMC5117641 · S10 https://www.sick.com/in/en/c/g568562 · S11 https://vtechworks.lib.vt.edu/items/d7fdffcf-494d-40bb-a54a-6315de467ef3/full · S12 https://www.sciencedirect.com/science/article/pii/S0926580524005867 · S13 https://flightsafety.org/asw-article/clean-sweep/ (sulla circolare FAA AC 150/5220-24) · S14 https://www.iata.org/en/pressroom/2022-releases/2022-12-06-04/ · S15 https://www.journal-aviation.com/en/news/37578-donecle-sets-its-drone-to-work-for-maintenance-with-afi-klm-e-m · S16 https://aviationweek.com/mro/emerging-technologies/aircraft-inspections-drones-accelerate-toward-next-evolution
