# Elenco dei riferimenti, aggiornamento f18: che cosa è cambiato (`sciame-redattore`, f18-documenti/04-riferimenti)

15 novembre 2026. In questa cartella ci sono le copie: `RIFERIMENTI_aggiornato.md` (393 voci) e `riferimenti.bib` (211 voci). Gli originali in `documentazione/` (332 voci, 189 voci BibTeX) **non sono stati toccati**. Il file con l'elenco ha un nome diverso da questo perché la consegna chiama `RIFERIMENTI.md` il file delle note. Il riquadro in testa al §0 dell'elenco ha il dettaglio completo; qui c'è la sintesi.

## 1. In testa

- **Regole violate:** nessuna, che io sappia: niente rete, niente git e niente sudo; nessuna cancellazione; scritture solo in `f18-documenti/` e nella cartella temporanea.
- **Scostamento principale:** le fonti nuove **non sono state riaperte**, perché la consegna non dà la rete. Lo stato di ciascuna è quello che dichiara il rapporto che la cita. Per questo nessuna voce nuova è «verificata dal curatore».

## 2. Che cosa è cambiato

1. **61 voci nuove**, da [333] a [393], in coda ai loro gruppi:
   - 8 articoli e rapporti (propagazione in nebbia, pioggia e fumo; detriti; OSDaR23);
   - 7 schede di sensori a lunga portata: Robin IRIS, Terma SCANTER 5000, Hesai AT128, Livox Tele-15, Echodyne EchoGuard, ARS 548, DJI AeroScope;
   - 7 norme: 14 CFR 91.227 e 89.310, ITU-R P.838-3 e P.840-9, FAA AC 20-128A e 90-48D, la pagina EASA della categoria aperta;
   - 7 strumenti del video: HyperFrames, GSAP, Kokoro-82M, kokoro-onnx, Piper, Inter, JetBrains Mono;
   - 11 insiemi di dati, ciascuno con la licenza dichiarata: adsb.lol (ODbL 1.0), Zenodo 18916312, TrajAir, il drone CMU e ALFA (tutti CC BY 4.0), NGSIM US-101 (CC BY-SA 3.0), digitraffic (CC BY 4.0), più quattro cercati e non usati;
   - 21 altre fonti: 10 pagine di Wikipedia; pagine sui detriti e sulle collisioni; la musica di Kevin MacLeod (CC BY 4.0, con attribuzione) e di John Bartmann (CC0, escluso dal piano); tre pagine sull'omonimia del nome «MoVi» e sul logo.
2. **Stati delle voci nuove:** 45 aperte dal ruolo, 9 viste solo nel riassunto di una ricerca, 5 non raggiungibili, 2 non verificate.
3. **Usi aggiunti a 5 voci esistenti:** [173], [191], [290], [320], [322]. Nessuno stato esistente è cambiato.
4. **Conteggi:** 204 / 58 / 23 / 66 / 15 / 10 / 17 = 393. Il programma ridà 332 sul file di prima.
5. **BibTeX:** 22 voci nuove, solo dei gruppi 1, 2 e 3, come nelle versioni precedenti. `bibtex` con lo stile plain dà 0 errori, 1 avviso atteso (`vovk2005`, già noto) e 211 voci nel `.bbl`. Ci sono 0 chiavi doppie (393 chiavi uniche nell'elenco, 211 nel `.bib`).

## 3. Critiche e dubbi per l'autore

1. **Modello Swerling 1.** Lo usano i sensori e l'attacco, ma nessun file ne cita la fonte: **manca**.
2. **Lessico fuori ambito.** La scheda IRIS e il blog di Robin Radar usano parole come «counter-drone» e «stop drones». Le voci le citano per esattezza e avvertono di non riprenderle nei testi, come chiede VERDETTO_FASE2, §6.
3. **Pagine sull'omonimia** ([391]–[393]). L'attacco al video le cita senza dire come le ha lette, e lo stato del marchio resta non verificato. È una decisione dell'utente.
4. **Voci incomplete.** Autori e titoli mancano per diverse voci, perché i rapporti non li scrivono. Non li ho completati a memoria: il campo dice «non scritto nei file».

## 4. Stati proposti

- «Il file BibTeX è ben formato»: **verificato** con bibtex, per la forma soltanto.
- «Ogni fonte con indirizzo citata in f15–f17 ha una voce»: **verificato** sull'insieme dichiarato. L'insieme è fatto dagli indirizzi e dagli identificativi estratti per programma dai file di testo, escluse le dipendenze npm e le copie dei README. Una fonte nominata solo a parole può mancare.

## 5. Che cosa propongo dopo

1. Un curatore delle fonti con la rete riapre le 61 voci, a cominciare dalle schede e dalle licenze del video. Prima della pubblicazione va riletta la licenza di GSAP.
2. Le voci [384]–[388] e [351]–[352], viste solo nel riassunto di una ricerca, si sostituiscono con le fonti primarie.
