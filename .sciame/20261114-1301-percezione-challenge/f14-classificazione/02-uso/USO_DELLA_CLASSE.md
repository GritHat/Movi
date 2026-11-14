# Uso della classe e del profilo del portatore — f14, `02-uso` (`sciame-tracciamento`)

14 novembre 2026. Programma `sim_classe.py`, uscita `risultati.txt`, previsioni `PREVISIONI.md` (scritte alle 18:35:59, prima del programma; prima esecuzione 18:37:16), tutti in questa cartella. Rifare: `…/f10-dati/ambiente/venv/bin/python -I -B sim_classe.py` (seme fisso, 1 s).

## 0. In testa

**Cambi di stato proposti** (li assegna l'arbitro): (a) «un'etichetta non riduce l'avviso né produce un "libero"» → **per costruzione** con la regola del §2, **sostenuta nel mio modello** (0 uscite scoperte su 20 000 per classe dentro lo scenario dichiarato); (b) «la coerenza cinematica può convalidare un'etichetta e permettere di restringere» → **smentita** (§3: il 96 % dei carrelli lenti etichettati «pedone» non è smentibile in 3 s); (c) «non olonomo = regione più piccola» → **smentita come regola generale** (§4: vale a 1,5 m/s, si rovescia a 3 m/s).
**Esiti delle previsioni:** tr-P1 regge (0,53); tr-P2a regge (0,719 < 0,85); tr-P2b regge alla lettera (0,876 < 0,90) ma **il meccanismo è smentito**: l'etichetta giusta dà 0,879, cioè lo stesso; tr-P3 **smentita** (pedone dentro l'inviluppo «carrello»: 0,989, soglia 0,90; inviluppo giusto del carrello 0,995 a 3 s, soglia 0,999); tr-P4a regge (1,000; mediana 0,47 s); tr-P4b regge (0 su 4 000); tr-P4c regge (4,1 %); tr-P5 **smentita per metà** (carrello etichettato «pedone» scoperto nel 29 % delle uscite, non in più del 50 %; con la fascia dello scenario 0, regge); tr-P6 regge (2,11 m/s).
**Regole violate:** nessuna che io sappia (niente git, sudo, rete; scritture solo in `02-uso/`). **Scostamenti.** L'ambiente d'esecuzione chiede di non scrivere file di rapporto: la consegna chiede questo file, ho seguito la consegna. **Nessuna fonte aperta oggi da me:** tutti i valori di classi e portatori sono **ipotesi, «valori di lavoro»**, in attesa della tabella con le fonti di un altro ruolo. Letti: contratto f14; addendum 10; soluzione v3 finale §0, §1.4–1.7, §2; fascicolo dimostrazioni §3 e §8; fascicolo geometria §7. **Non letti:** verdetti sui dati e sulla continuità, fascicolo stima, `RIFERIMENTI.md`, i generatori in C (solo il rumore di misura, 5 cm, da `gen.h` r. 183). *Indipendenza:* simulatore, regole e previsioni hanno un solo autore; il «vero» e le librerie escono dallo stesso generatore con semi diversi.
**Modello dichiarato:** piano aperto (nessun ritaglio sulla maschera né su R100), soggetto puntiforme, ingresso nell'origine con rotta +x, 15 Hz, errore d'ingresso 3° e 0,06 m/s, rumore di misura 5 cm. Niente sensore, niente catena v3: è un conto sulle forme, non una prova del sistema.

## 1. Interfaccia

```
traccia.etichetta = (classe, fiducia in [0,1], origine in {a_mano, simulata, modello}, t_etichetta, smentita: bool)
classe in {pedone, corsa, carrello, auto, treno, aereo, multirotore, non_classificato}
PROFILO[classe] = (v_max, a_max, b_max, modello di moto, gradi di libertà, k_max o binario, libreria)   # tabella fissa
configurazione d'avvio (deterministica, entra in I11): SCENARIO = classi ammesse -> v_scen = max v_max;
   PORTATORE = (v_ego, T_r, b_ego, gradi di libertà)
```
Il classificatore è **asincrono**: senza etichetta, con etichetta vecchia (età oltre 1 s, *scelto*) o con fiducia sotto soglia la classe è `non_classificato`. Nel prototipo l'origine è sempre `a_mano` o `simulata`, e la riga fissa dello schermo lo dice.

| Classe (valori di lavoro, **ipotesi**) | v_max m/s | a / frenata m/s² | Gradi di libertà, modello | w(v_max) m | d_serve m (stazione fissa, T_r 1 s) | Nel dominio di 3 m? |
|---|---|---|---|---|---|---|
| pedone a piedi | 1,8–2,5 | 2,5 / 2,5 | 2, olonomo; si ferma e inverte | 0,64–0,89 | 2,56–3,56 | sì fino a 2,11 m/s |
| persona di corsa | 6 | 3 / 3 | 2, olonomo | 2,13 | 8,53 | **no** |
| carrello elevatore | 5 | 1 / 2 | 2, non olonomo, raggio ≥ 2 m | 1,77 | 7,11 | solo sotto 2,1 m/s |
| auto in area di lavoro | 8 | 2,5 / 6 | 2, non olonomo, raggio ≥ 5 m | 2,84 | 11,38 | **no** |
| treno in manovra | 5 | 0,3 / 0,5 | 1, sul binario (linea nota in configurazione) | 1,77 | 7,11 | solo sotto 2,1 m/s |
| aereo in rullaggio | 15 | 1 / 2 | 2, non olonomo, grande raggio | 5,32 | 21,33 | **no** |
| multirotore lento | 3 (ipotesi) | — | 3 + imbardata, non sta sul suolo | 1,06 | 4,27 | **no: la mappa del suolo non lo rappresenta** |
| non classificato | v_scen | massimi dello scenario | 2, olonomo | w(v_scen) | — | — |

w(v) = ε_Ω + v·(a + τ + Δ) con 0,133 + 0,155 + 0,067 = 0,355 s e ε_Ω = 0 (fascicolo dimostrazioni, prop. 8). d_serve = v·(t_conf + τ + T_r) = v·1,422 s (§5). **Il dominio provato (camera ferma, 3 m) dà un avviso tempestivo solo a ciò che va a meno di 2,1 m/s**: per tutte le classi di veicolo alla loro velocità massima la portata non basta, e va detto così (L-5).

## 2. La regola di sicurezza sull'uso dell'etichetta

**Decisione: non esiste una condizione accettabile per restringere.** Tre ragioni, ognuna con la sua prova.
1. *L'avviso è dello spazio non osservato; l'etichetta è di una traccia.* La proposizione 2 del fascicolo dimostrazioni vale «senza alcuna ipotesi sul numero dei soggetti né sull'esistenza di una traccia»: la v_max dell'ipotesi 4 deve limitare **ogni** oggetto che può stare nell'ombra, non quello etichettato. Dalla stessa ombra può uscire un altro (il controesempio dell'estraneo, v3 §1.7).
2. *La coerenza cinematica smentisce, non conferma* (§3): un carrello a 1–2,2 m/s etichettato «pedone» resta coerente nel 95,9 % delle tracce di 3 s.
3. *Il costo misurato dell'etichetta che restringe* (regola C: w dalla v_max dell'etichetta; 20 000 uscite per classe, direzione entro ±60° dalla normale al bordo):

| Vero (velocità m/s) | base v3, w 0,40 | C, etichetta «pedone» (0,89) | C, etichetta «carrello» (1,77) | **A, scenario a 6 m/s (2,13)** | scarto massimo oltre w(«pedone») |
|---|---|---|---|---|---|
| pedone (0,3–1,8) | 0,130 | 0 | 0 | **0** | 0 |
| corsa (3–6) | 0,999 | 0,681 | 0,024 | **0** | 1,23 m |
| carrello (1–5) | 0,800 | **0,291** | 0 | **0** | 0,86 m |
| auto (2–8), **fuori dallo scenario dichiarato** | 0,983 | 0,681 | 0,143 | **0,048** | 1,91 m |

Quota di uscite dall'ombra con almeno un istante fuori dall'avviso. La colonna A è 0 per costruzione dentro lo scenario; l'ultima riga mostra il punto debole vero: **lo scenario dichiarato male**, non l'etichetta. La prima colonna ritrova il limite già scritto in v3 (0,40 m copre 1,13 m/s).

```
all'avvio:  v_scen <- max v_max delle classi dello SCENARIO;  w_scen <- max(0,40, eps_ombra + (v_scen + v_ego)*(a + tau + Delta))
            se w_scen > 1,3 m (metà del campo utile, scelto): riga fissa «avviso tempestivo NON dichiarato per: <classi>»
a ogni ciclo, per ogni ombra con uno strato d'avviso:
   w_ombra <- max(w_ombra, w_scen, w(v_max di ogni classe NON smentita entrata in quell'ombra))    # solo allarga
   R100 <- cuneo + w_ombra;   rilascio: SOLO cella vista libera 3 fotogrammi e oltre w_ombra dall'ombra corrente
«libero» (1.2), insieme di possibile presenza, rilascio: nessun argomento è un'etichetta
R90 <- regione del PROFILO[classe] (§4), ritagliata su maschera e su R100;  livello numerico solo con libreria provata
classe fuori dallo SCENARIO -> evento «classe fuori scenario», w_ombra cresce, non torna indietro
```
**Invariante (`tr-I15`).** Per ogni coppia di esecuzioni sugli stessi fotogrammi che differiscono **solo** nelle etichette: le celle «libero» e i rilasci sono identici; R100 con etichette è un soprainsieme di R100 senza etichette. Controllo: la stessa sequenza con le etichette permutate a caso, differenze a soglia 0 (**non eseguito** sui banchi di v3: lì nessuna funzione prende ancora un'etichetta). *Costo:* nello scenario «solo pedoni» w passa da 0,40 a 0,64–0,89 m; con una classe da 5–6 m/s diventa 1,8–2,1 m e l'avviso copre quasi tutto il campo: è il dominio, non un difetto della regola. **Questo tocca w, che v3 tiene a un solo valore (AT-10): è una contraddizione da portare all'arbitro**; l'alternativa minima è lasciare 0,40 m e scrivere per ogni classe la velocità non coperta.

## 3. Coerenza cinematica

```
dal 4° ciclo di misura; scatta se in 4 degli ultimi 6 cicli vale una di:
  c1  |v| - 2*sigma_v > v_max(classe)
  c2  (1 grado) distanza dal binario > 0,30 m + 2*sigma_pos
  c3  (non olonomo) curvatura stimata su 0,4 s > 1,5*k_max con |v| > 0,5 m/s + 2*sigma_v, oppure inversione del verso in meno di 1 s
quando scatta: classe <- non_classificato; smentita <- vero (non torna per quella traccia); profilo dello scenario;
   R90 <- disco sd-0 senza cifre; evento «etichetta smentita dalla cinematica»; R100 e w non si restringono
```
Soglie *scelte*, non tarate. Filtro a velocità quasi costante, q = 0,2 (1,0 per il carrello, ipotesi); 4 000 tracce per riga.

| Caso | Smentite | Ritardo mediano / 95° (s) |
|---|---|---|
| pedone, carrello, treno veri con l'etichetta giusta, 3 s | 0 / 1 / 0 su 4 000 | — |
| «persona» a 6 m/s costanti in linea retta | 1,000 | 0,47 / 0,47 |
| «persona» a 3,5 m/s; a 2,8 m/s (1 s in vista) | 1,000; 0,106 | 0,47; 0,67 / 0,93 |
| «treno» che esce dal binario a 10°, 2 m/s | 1,000 | 1,40 / 1,53 |
| pedone etichettato «treno», a 20° dal binario; lungo il binario | 0,866; 0,395 | 1,20; 1,93 |
| **carrello lento (1–2,2 m/s) etichettato «pedone»** | **0,041** | 2,33 |
| **pedone etichettato «carrello»** | **0,052** | 1,80 |

Lettura. (i) 0,47 s è il minimo della regola (4 cicli d'avvio più 4 di finestra): a 6 m/s sono **2,8 m, quasi tutta la portata**; il controllo arriva quando l'oggetto è già passato. (ii) Gli scatti falsi (0 su 4 000, limite superiore al 95 % circa 1 per mille) sono un **limite inferiore**: il «vero» rispetta i limiti della classe per costruzione. (iii) Le due righe in grassetto: il controllo non vede quasi mai l'errore fra classi lente. Serve a togliere un'etichetta palesemente falsa, **non** a fidarsi di una.

## 4. Modello di moto per classe

**Nel filtro:** velocità quasi costante per tutti, con q della classe **mai sotto** quello di base (q <- max(0,2, q_classe)) e porta d'associazione mai più stretta: in meno di 3 m e a 15 Hz rotta e velocità d'imbardata non si osservano da un punto, e un modello vincolato sbagliato perde l'associazione. Nessun confronto con più modelli interagenti: **non verificato**. **Nella previsione** entra il modello della classe: pedone, libreria con chi prosegue, si ferma, inverte, svolta (in v3: 200 proseguono, 200 si fermano); non olonomo, biciclo a curvatura limitata (prosegue, frena, svolta, accelera; mai di lato); treno, un grado lungo la linea.

Regione al 90 % (celle da 0,1 m più dense; 6 000 membri) e inviluppo cinematico (60 000 controlli estremi a caso: **stima per difetto**), piano aperto:

| Ingresso 1,5 m/s | area R90 a 1 / 2 / 3 s (m²) | lungo la rotta a 3 s (m) | larghezza a 1 / 2 / 3 s (m) | inviluppo a 2 s (m²) | «fermi» dentro R90 a 3 s |
|---|---|---|---|---|---|
| pedone | 0,41 / 2,76 / 8,36 | da −1,3 a 5,2 | 1,0 / 2,6 / 5,3 | 46,1 | 0,992 |
| carrello | 0,16 / 1,47 / 5,94 | da 0,5 a 7,3 | 0,5 / 1,6 / 5,4 | 30,3 | 0,967 |
| treno | 0,03 / 0,16 / 0,39 | da 3,1 a 5,4 | 0,1 / 0,3 / 0,3 | 0,8 | 0 (fermi: 0,7 %) |
| disco prudente a 2,5 e 5 m/s | 19,6 / 78,5 / 176,7 e 78,5 / 314 / 707 | | | | |

A 3 m/s d'ingresso il carrello ha R90 di 0,41 / 5,53 / 24,7 m², **più grande** di quella del pedone (0,40 / 2,74 / 8,95 con la velocità tagliata a 2,5): più lunga (fino a 13 m a 3 s) e a 3 s anche più larga (11,9 m). Dunque: più stretta di lato a 1–2 s e a bassa velocità, più lunga in avanti sempre; l'area non è «più piccola» in generale. La regione del pedone contiene «fermo» e «tornato indietro»; quella del treno **non contiene il treno fermo** (va aggiunto a mano: frenata massima dal punto d'ingresso).

**Copertura con l'etichetta sbagliata** (quota del vero dentro la regione dell'etichetta; 6 000 prove):

| Vero → etichetta | R90 a 1 / 2 / 3 s | inviluppo a 1 / 2 / 3 s |
|---|---|---|
| pedone → pedone; carrello → carrello; treno → treno (1,5 m/s) | 0,90 / 0,90 / 0,88; 0,90 / 0,89 / 0,88; 0,92 / 0,92 / 0,90 | 1,000; 1,000 / 1,000 / 0,999; 1,000 |
| pedone → «carrello» (1,5 m/s) | **0,704 / 0,719 / 0,739** | 0,998 / 0,989 / 0,970 |
| pedone → «treno» (1,5 m/s) | **0,239 / 0,233 / 0,108** | 0,646 / 0,360 / 0,239 |
| carrello → «pedone» (1,5 m/s) | 0,963 / 0,928 / 0,876 | 1,000 / 0,998 / 0,980 |
| carrello → «pedone» (3 m/s; c1 scatterebbe prima) | **0,022 / 0,050 / 0,097** | 0,037 / 0,099 / 0,185 |
| carrello → «treno» (1,5 m/s) | 0,321 / 0,345 / 0,201 | 0,833 / 0,473 / 0,290 |

Le righe «giuste» valgono 0,9 **per costruzione** (stesso generatore): non misurano niente. **Sull'avviso l'effetto è nullo** (R100 non prende l'etichetta, §2). Sulla regione mostrata l'effetto è grande: quindi (`tr-I17`) **nessun livello numerico si dichiara per una classe senza libreria provata**, e con etichette a mano il livello è «condizionato all'etichetta giusta»; oggi l'unica libreria con cifre è quella dei pedoni di v3. Per `non_classificato`: disco sd-0 senza cifre.

## 5. Il profilo di chi porta il sensore

Configurazione fissa (v_ego, T_r, b, gradi di libertà). Anticipo e distanza che servono:
**T_ant = t_conf + τ + T_r + v_ego/b**;  **d_serve = (v_obj + v_ego)·(t_conf + τ + T_r) + v_ego²/(2b) + v_obj·v_ego/b + C**, con t_conf = 0,267 s (conferma 3 su 5), τ = 0,155 s (stimata), C margine (0 oppure 0,5 m, *scelto*). Fascia in moto: **w = ε_Ω + (v_scen + v_ego)·(a + τ + Δ)**. Livello «attenzione»: distanza ≤ d_serve calcolata con v_obj = velocità d'avvicinamento stimata più 2σ per una traccia in vista, **v_scen per un'ombra con avviso** (mai la v_max dell'etichetta, se è più bassa); la classe può solo anticipare (v_obj <- min(v_max, v + a_max·T_ant)).

| Profilo (valori di lavoro, **ipotesi**) | v_ego m/s | T_r s | b m/s² | T_ant s | d_serve m per v_obj 1,4 / 2,5 / 5 / 8 (C = 0) | v_obj coperta con 3 m (C = 0; 0,5) | w a v_scen 2,5 |
|---|---|---|---|---|---|---|---|
| stazione fissa con operatore | 0 | 1,0 | — | 1,42 | 1,99 / 3,56 / 7,11 / 11,4 | 2,11; 1,76 | 0,89 |
| veicolo terrestre lento, arresto automatico | 0,5 | 0,3 | 1,0 | 1,22 | 2,20 / 3,54 / 6,60 / 10,3 | 2,06; 1,65 | 1,06 |
| veicolo terrestre lento, operatore remoto | 0,5 | 1,5 | 1,0 | 2,42 | 4,48 / 7,14 / 13,2 / 20,5 | 0,79; 0,58 | 1,06 |
| persona non vedente ferma | 0 | 1,5 | — | 1,92 | 2,69 / 4,81 / 9,61 / 15,4 | 1,56; 1,30 | 0,89 |
| persona non vedente in cammino | 1,0 | 1,5 | 2,0 | 2,42 | 5,56 / 8,23 / 14,3 / 21,6 | **0,34; 0,14** | 1,24 |

**Che cosa si usa già a sensore fermo:** solo T_r di chi riceve l'avviso (e t_conf, τ): le righe con v_ego = 0. Il veicolo senza equipaggio resta **fermo**, come in v3: il suo profilo entra come T_r del destinatario. **Che cosa resta analisi:** ogni riga con v_ego > 0. A sensore in moto nessuna soglia è provata: l'ombra si sposta, cade «occlusore fermo» della proposizione 8, entra l'errore di posa. La tabella dice già che con 3 m una persona in cammino riceve un avviso utile solo da oggetti quasi fermi (0,34 m/s): serve più portata, non un'altra soglia. T_r di 1,0 s è il valore del fascicolo geometria §7; 1,5 s, frenate e 0,3 s **non hanno fonte**.

## 6. Che cosa cambia nei blocchi di v3, e invarianti nuovi

| Blocco | Cambio |
|---|---|
| 1 sorgente e avvio | la configurazione porta SCENARIO e PORTATORE; calcola v_scen, w_scen, T_ant; dichiara le classi senza avviso tempestivo |
| nuovo: classificatore | componente **richiesto, qui simulato**: dà (classe, fiducia, origine, età) per traccia; nelle prove l'etichetta è a mano |
| 2 mappa, «libero» | **nessuno**: nessun argomento è un'etichetta |
| 3 gruppi, «mobile» | nessuno; la regola «mobile» non usa la classe |
| 4 associazione e filtro | q <- max(0,2, q_classe); porta mai più stretta; l'etichetta viaggia con la traccia e non con il gruppo |
| 5 ciclo di vita | campo etichetta; controllo di coerenza (§3); evento «etichetta smentita»; al riaggancio l'etichetta è «presunta» come l'identità |
| 6 previsione R90 | libreria o modello della classe; cifra solo con libreria provata; non classificato → sd-0 |
| 7 avviso R100 | w_ombra <- max(w_scen, classi entrate): solo allarga; rilascio invariato |
| 8 riaggancio | la classe **non** entra nel candidato (non restringe la porta); una classe diversa al ritorno è un indizio, non una prova |
| 9 salute del sensore | invariato; scavalca anche l'etichetta |
| 10 regole e uscite | «attenzione» con d_serve del portatore; testo con classe e origine («carrello · etichetta a mano») |
| 11 registro | etichetta, origine, età, smentita, scenario e portatore in ogni riga |
| 12 precisione sul posto | per classe, e solo per le classi con libreria |

**Invarianti nuovi (provvisori).** `tr-I15` (§2): stesse celle «libero» e stessi rilasci al variare delle sole etichette; R100 con etichette ⊇ R100 senza. `tr-I16`: una classe può solo allargare w e alzare il livello d'attenzione, mai il contrario. `tr-I17`: ogni uscita che usa la classe porta classe, origine, età; nessun livello numerico senza libreria provata. `tr-I18`: un'etichetta smentita non torna per quella traccia. `tr-I19`: scenario e portatore fissati all'avvio (estende I11); con v_ego > 0 l'uscita dice «soglie non provate in moto». I5 si estende: fra le cose che non producono un «libero» e non tolgono un avviso entra **l'etichetta**.

## 7. Limiti e che cosa propongo dopo

Limiti: un autore, un modello, valori senza fonte; piano aperto (il ritaglio su maschera e R100 cambierebbe le aree, non la regola); il generatore dei pedoni è mio, non quello di f8; l'inviluppo è per difetto; nessuna prova con la catena v3 né con un sensore. Dopo: (1) l'arbitro decide su w (0,40 fisso con velocità non coperta dichiarata, oppure w_scen); (2) la prova di `tr-I15` sul banco `insieme.c` appena una funzione prende l'etichetta; (3) sostituire i valori di lavoro con la tabella con le fonti e rifare le tabelle con un comando; (4) aggiungere «fermo» alla regione del treno.
