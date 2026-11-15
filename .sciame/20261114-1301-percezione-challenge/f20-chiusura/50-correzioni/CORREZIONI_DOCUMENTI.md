# Correzioni del documento tecnico v3 e della proposta (`sciame-redattore`)

Scritto il 15-11-2026, dalle 07:02 alle 07:12 circa (`date -Is`). Fonte delle correzioni: `40-commissario/COMMISSARIO.md`.

## 0. In testa

**Esito.**
- Il documento tecnico ricompilato ha **108 pagine** e zero «??» (`pdftotext | grep -c "??"` = 0). Il log non ha riferimenti né citazioni indefinite e nessun Overfull.
- La proposta è passata a **v3.1**: **2 pagine** (`pdfinfo`), zero «??», nessun Overfull.

**Regole.**
- Non ho cancellato nulla.
- Prima di modificare ho fatto queste copie:
  - `allegato_tecnico/allegato_tecnico_pre_correzioni.pdf`;
  - `allegato_tecnico/capitoli/versioni_precedenti/pre_correzioni_v3/` (tutti i capitoli, `allegato.bib`, `allegato_tecnico.tex`, `preambolo.tex`);
  - `proposta/proposta_sciame_pre_correzioni.pdf` e `.tex`;
  - `50-correzioni/VERSIONI_pre_correzioni.md`.
- Una regola l'ho violata per errore: un `sed -i.bak_tmp` ha creato `capitoli/11_volo_alta_velocita.tex.bak_tmp`. L'ho spostato con `mv -n` fra le copie (`pre_correzioni_v3/11_volo_alta_velocita_prima_ref.tex`), senza cancellare nulla.
- Niente git, rete o sudo.

**Scelta di versione.** La proposta corretta è la **v3.1**, non una v3.0 riscritta. La v3.0 ha già le sue copie (`proposta_sciame_v3.0.*`) e resta intatta. In `VERSIONI.md` ho aggiunto una riga v3.1 e lasciato com'è la riga v3.0. Copie nuove: `proposta_sciame_v3.1.pdf` e `.tex`.

## 1. Correzioni fatte

**D-1: la correzione c1.**
- Allegato, nuovo paragrafo «Correzione provata (c1)» a p. 87, con le cifre di CORREZIONE.md e VERIFICA.md ricontrollate sui file:
  - 59/59 [0,939; 1], McNemar p = 3,5·10⁻¹⁸; 51/51 e 58/58;
  - 0/200 nel controllo, detto debole perché lì il radar non satura;
  - 11/200 [0,031; 0,096], e 200/200 con il bagliore forzato;
  - sfera di 565 m, mediana 8 s;
  - riacquisizione 49/60 e 40/60 sotto la soglia di 51/60.
- Allegato, tab. 2 (`01_introduzione`), limiti (`08_limiti`) e conclusioni: «fino a 0/59; con c1 59/59, ma non localizzato e con 11/200 falsi avvisi».
- Allegato, tab. 58: lo stato diventa «c1 applicata in simulazione», con il passo dopo (localizzare l'avviso) e le soglie.
- Proposta: limiti e § 4 (forma breve, «vedi i limiti»), e la riga del § 9.

**D-2: il sensore in moto.** § 1.7 e conclusioni distinguono il corto raggio (analisi dei requisiti, § 8.11) dalla lunga portata (simulata nel § 10.7).

**D-3: quale formula misura la copertura.**
- Allegato p. 83: la (32) vale per un regime nel piano; la copertura viene dalla sfera (k₀,₉ = 2,500), dalla miscela e dalla ricalibrazione.
- Proposta § 3: lo stesso, in forma breve.

**D-4: σ_rif.** Aggiunto che la copertura è misurata rispetto alla posizione ADS-B, e che con un'altra verità di riferimento σ_rif va rifissato (tappa 2, § 11.2).

**D-5: la copertura sui 43 aerei.**
- In tab. 4, § 10.9 e conclusioni c'è ora la stessa cifra della tab. di § 9.6: 0,95 / 0,93 / 0,93 a 2 / 10 / 30 s, con il bootstrap per mezzo e Wilson su n = 43 mezzi ≥ 0,83.
- Nota: è un intervallo per mezzo, non per passaggio, come nella fonte.
- La frase del commissario «zona d'avviso» l'ho corretta in «zona prevista con quantile conforme, non regione al 90 % della formula chiusa»: il § 9.5 dice che quella zona «non è l'avviso».

**D-6 e D-7.** Proposta § 8: «59–60 su 60 … col radar rotante 39 su 60 L». § 2: «Col nucleo adottato, nessun falso evento».

**D-8.**
- Tolto «fase 4» da `\statodoc`.
- Bibliografia: le note di lavoro ridotte a «consultata il 15-11-2026», «testo intero non consultato» o «dato del produttore». Tolti «Aperta il», PMC, IEEE Xplore, MDPI 403, «risultato di ricerca» e «lette solo le accuratezze»; restano le sole avvertenze di contenuto (analogia, ipotesi).

**D-10: i parametri del drone seguito.** Aggiunti per B σ₀ᵥ = 4,44 m²/s (da `05-scorta/curva_F7.json`; il commissario lo stimava 4,6), q = 80 m²/s³ e l'insieme r = 4,59σ₀ + 3σᵥτ + aτ²/2 con a = 10 m/s² (da `curva_f7.py`).

**D-11: la costante 0,75 s.** Scritta la provenienza: è il primo avviso su CPU in SENSORI_E_HARDWARE.md. Con i 0,70 s della tab. 57 si avrebbero 3300 m. La cifra 3312 non l'ho cambiata (decide l'arbitro).

**D-12.**
- (a) Aggiunto il simbolo «τ (§10): tempo dall'ultima misura».
- (b) «76 violazioni» ora indica i registri F2, F3 ed F5 e dice che il denominatore non è riportato, quindi **non verificato**; l'insieme è diverso dai 1440 passi della taratura.
- (c)–(g) Fatte nella proposta. Per (g): 0,96 [0,94; 0,98] dalla tab. 51; 0,905 «(stima)», perché l'intervallo non c'è.
- (h) Sommario: «se l'errore iniziale è entro r₀».

**D-13.**
- Il punto doppio dopo «s.d.»: `year = {s.d}` in 23 voci, e ora nel PDF non compare più «s.d..».
- Lo spazio prima del punto nella voce [101].
- «L'89,5 %» in due punti.

**Aggiunta in Appendice B.** `scorta_f7r_c1.py` fra i programmi.

## 2. Correzioni non fatte

- **D-9.** Non ho copiato i programmi in `prototipo/prove/volo/`: la consegna non mi autorizza a scrivere in `prototipo/`. Serve il sì del coordinatore.
- **D-13, «RealSense.Post-processing».** Nel `.bbl` lo spazio c'è (`\newblock`). Probabilmente è un artefatto dell'estrazione del testo. **Non verificato** a vista.
- **D-14.** Facoltativa, non fatta: la struttura cambierebbe troppo a fine lavoro.

## 3. Stati

- Nessuna cifra nuova inventata. Tutte vengono dal verdetto finale, da CORREZIONE.md e VERIFICA.md, da `curva_F7.json` o dalle tabelle dell'allegato stesso.
- La c1 resta **simulata, non adottata**.

## 4. Dopo

- L'arbitro decide su D-11 e su D-9.
- Il video EN v3 (173,856 s, dentro i 176 s) non contiene c1. Se lo si aggiorna, il limite di 176 s resta vincolante.
