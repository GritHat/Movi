# Chiusura dell'anomalia «Pd 0,9, ombra a −20 cm» — H-012, f4 (`sciame-validazione`)

**Previsioni, scritte alle 2026-11-14T14:49:49+01:00 (`date -Is`), prima del codice e di ogni lancio.**

- **Previsione registrata** (è quella di `MISURE_V2.md`): con `validazione-4` i falliti con Pd = 0,9 scendono a **0 su 4800** a −20 cm e restano 0 a 0 e +20 cm. **La smentisce un solo passaggio fallito.** Il braccio «prima», sugli stessi semi, deve ridare **13 su 4800**: se non li ridà, la prova non vale.
- **Dubbio scritto ora, prima del lancio:** ragionando sul codice mi aspetto che `validazione-4` da sola **non** arrivi a 0. Due motivi: (a) nei 3 fotogrammi di «non confermato» lo strato 1 non c'è ancora, e la striscia di 20 cm si attraversa in 2–3 fotogrammi; (b) nel mio simulatore una traccia chiusa non rinasce, quindi una chiusura a più di 1 m dall'ombra resta scoperta. Attesi 3–13 falliti residui con la sola `validazione-4`; aggiungo, dichiarandoli, due bracci: «la traccia chiusa rinasce alla prima rilevazione» e la variante «ingresso SUBITO se l'ultima rilevazione è a meno di 1 m da un'ombra». Per la variante «subito» con rinascita attendo **0 falliti**.
- **Costo atteso (strati 1 a vuoto).** Senza pannello: 0, per costruzione (non c'è ombra da cui farli nascere; non simulato). Con il pannello, passaggio davanti al pannello senza entrare nell'ombra: `validazione-4` 0,1–0,6 ogni 100 passaggi; variante «subito» 80–100 ogni 100 passaggi. In tutti e due i casi lo strato a vuoto **non si rilascia più** (C1 non riaggancia a più di 0,40 m dall'ombra e non c'è tetto di tempo).
- **P2a** (riaggancio): atteso invariato, 99,7–100 %. **P3b** (falsi «mobile»): invariato per costruzione, la regola «mobile» non legge lo strato 1; non la rieseguo.
- **Limite P2b** (secondo soggetto che esce dalla stessa ombra, riaggancio sbagliato, strato 1 rilasciato con il primo ancora nascosto): le celle del cuneo stimato restano «in ombra» in tutti i passaggi (per costruzione, pannello fermo). Attendo però passaggi falliti **a −20 cm**, dove il primo soggetto attraversa la striscia che il sistema crede libera: quasi tutti in «sosta» e «torna», quasi nessuno in «lontano»; 0 a 0 e +20 cm.

## Esito: l'anomalia NON è chiusa

Lanci fra le 14:52 e le 14:55 (`date -Is`). Pd = 0,9, 36 celle principali, 400 passaggi per cella, **stessi semi** di `v2_R8_pd09.txt`. Unità: il passaggio. Limiti superiori al 95 % (Poisson) calcolati da me.

| Braccio | Falliti a −20 cm (su 4800) | A 0 e +20 cm | Strati 1 rimasti accesi a fine passaggio, soggetto visibile (su 4800) | Primo riaggancio |
|---|---|---|---|---|
| **prima** (regola della versione 2) | **13** (limite 0,43 %): riprodotto | 0 e 0 | 613–686 | 99,97–100 % |
| prima + la traccia chiusa rinasce | 3 | 0 e 0 | 615–687 | 99,97–100 % |
| **`validazione-4`** | **8** (limite 0,30 %) | 0 e 0 | 616–690; nati dalla regola: 4–8 | 99,92–99,97 % |
| `validazione-4` + rinascita | **2** (limite 0,13 %) | 0 e 0 | 616–691; nati dalla regola: 4–8 | 99,92–99,97 % |
| ingresso subito entro 1 m | 6 | 0 e 0 | 2521–2695 | 50,3–55,0 % |
| ingresso subito entro 1 m + rinascita | **0** (limite 0,06 %) | 0 e 0 | 2523–2700 | 50,3–55,0 % |

- **La previsione registrata (0 su 4800) è smentita:** con `validazione-4` restano 8 passaggi falliti, 2 se la traccia chiusa rinasce. Il dubbio scritto prima del lancio regge (attesi 3–13): la regola agisce dopo la chiusura, mentre il soggetto attraversa la striscia durante i fotogrammi di «non confermato».
- **La riproduzione fallisce prima (13) e non passa dopo (8, oppure 2).** Passa solo con «ingresso subito entro 1 m» più rinascita, come previsto, ma a un costo che la esclude (sotto).
- **P2a:** il riaggancio non cambia con `validazione-4` (99,92–99,97 % contro 99,97–100 %). **P3b:** non rieseguita; invariata per costruzione, la regola «mobile» non legge lo strato 1.

**Costo, strati 1 a vuoto** (`bis_DAVANTI.txt`, N = 4000 per riga). Senza pannello: 0 per costruzione, non simulato. Passaggio a 0,5 m davanti al pannello, senza entrare nell'ombra: prima 0,0 ogni 100 passaggi; `validazione-4` **0,1–0,2**, tutti rimasti accesi (previsto 0,1–0,6); «subito entro 1 m» **94–95 nati, 83–85 rimasti accesi** (previsto 80–100). Senza tetto di tempo e con C1, uno strato a vuoto non si rilascia più.

**Notato dopo, senza previsione.** Già con la regola della versione 2 e Pd = 0,9, nel 12,8–14,3 % dei passaggi (613–686 su 4800) resta acceso uno strato 1 con il soggetto visibile: un rilevamento mancato vicino all'ombra apre lo strato, e C1 non riaggancia se la rilevazione successiva è oltre la fascia. È un costo della coppia «C1 + nessun tetto», non di `validazione-4`.

## Le due domande

1. **La variante «entra subito nello strato 1 entro 1 m» non è equivalente.** È migliore su R8 (0 falliti contro 2–8, se la traccia chiusa rinasce; 6 senza) e molto peggiore sul resto: strati a vuoto in oltre metà dei passaggi e primo riaggancio al 50–55 %. Non la propongo.
2. **Il limite P2b tocca R8 solo insieme all'errore della maschera d'ombra.** Dopo il riaggancio sbagliato le celle del cuneo stimato restano «in ombra», mai «libero», in **7198 passaggi su 7198** (per costruzione, a pannello fermo). A 0 e +20 cm: 0 passaggi falliti su 4799, quindi cade solo l'avviso legato alla traccia. A −20 cm il primo soggetto, senza misura, sta in una cella «libero» dopo il rilascio in **800 su 800** (sosta), **799 su 799** (torna), 17 su 800 (lontano): è la striscia di 20 cm che il sistema crede visibile (`bis_FURTO.txt`, Pd = 1, furto a 1,0 s dall'ingresso).

## Scostamenti, stato, dopo

- **Regola violata:** il primo lancio ha superato i 120 s ed è stato fermato da `timeout` a cinque bracci su sei (`bis_R8_lancio_interrotto.txt`, conservato). L'ho diviso in due lanci (57 e 64 s) e rifatto tutto: i cinque bracci danno gli stessi numeri.
- `sim_v2bis.py` importa `sim_v2.py` e ne ripete `pass_v2` con quattro interruttori; nessun file consegnato è stato toccato. I due bracci in più (rinascita, «subito») sono dichiarati nelle previsioni.
- **Stato proposto.** R8 con Pd = 0,9 e ombra a −20 cm: resta **smentita** la soglia «0 falliti»; con `validazione-4` e rinascita il tasso scende a 2 su 4800. `validazione-4`: **smentita** come chiusura, sostenuta come riduzione (13 → 8 → 2).
- **Che cosa lo deciderebbe** (`validazione-5`, non provata): strato 1 provvisorio già durante «non confermato» quando l'ultima rilevazione è entro 1 m da un'ombra, rilasciato dal primo rilevamento in porta e non da C1. Previsione: 0 falliti e strati a vuoto come con `validazione-4`. La smentisce questa stessa corsa.
- Per rifare: `sh /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f4/H-012/03-validazione/rifai_v2bis.sh` (quattro lanci, il più lungo 64 s; risultati in `bis_*.txt`).
