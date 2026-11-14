# Previsioni — sciame-prestazioni, f7, banco indipendente

Scritte alle **2026-11-14T16:10:02+01:00**, prima di scrivere una riga del banco e prima di aprire le consegne
`02-ottimizzazione` e `06-tempo-reale` e i loro script. **Che cosa avevo già letto:** contratto f7, `TRIAGE.md`
(che riporta alcuni numeri degli autori: 736/1200 e 116/160 blocchi, 2,5–3,1 ns per passo, 76–308 ms a 5 cm con tutti i
raggi, 0,50 ms polare), addendum 3–7, `promptMare.txt` §2–§4, righe B1–B2 del nucleo. Le previsioni NON sono quindi cieche
rispetto a quei numeri: lo dichiaro. Dove la mia previsione si scosta dal triage lo scrivo.

Impianto deciso prima: camera 640×480, 87°×58°, a 1,2 m, inclinata 15° in basso, profondità z in millimetri, valida
fino a 6 m; regione x 0–6, y ±2, z 0–3 m; voxel di 4 byte in tutte le strutture; raggio = da camera al ritorno, voxel
attraversati «visti liberi ora», voxel finale «occupato»; un raggio senza ritorno non scrive niente. Scena vuota = solo
pavimento, senza pareti. Tempo misurato = deproiezione + lancio dei raggi + scritture (non la generazione dell'immagine).

| N. | Misura | Previsione | Soglia di smentita |
|--|--|--|--|
| P1 | memoria densa (calcolo) | 288 000 B a 10 cm; 2 304 000 B a 5 cm | qualunque altro valore |
| P2a | hash 8³ / densa, scena vuota | 0,25–0,45 a 10 cm; 0,18–0,35 a 5 cm (meno del 67–84 % del triage, perché senza pareti i raggi alti non tornano) | fuori intervallo |
| P2b | hash 8³ / densa, scena densa con parete di fondo | 0,60–1,07 a entrambe le risoluzioni | < 0,60 |
| P3 | octree senza potatura / densa | densa: 1,3–2,5; vuota: 0,4–0,9 | fuori intervallo |
| P4 | octree con potatura a fine fotogramma | nodi a fine fotogramma ≤ 70 % del non potato; picco dentro il fotogramma ≥ 90 % del non potato; tempo ≥ 1,3 × non potato (la marca di freschezza cambia a ogni fotogramma e riespande) | una delle tre non vale |
| P5 | costo per passo di raggio, 3D | densa 2–4 ns; hash con cache dell'ultimo blocco 1,1–1,6 × densa; octree 3–8 × densa | densa < 1 o > 6 ns; rapporti fuori intervallo |
| P6 | densa, scena densa, p95 dell'aggiornamento | 5 cm tutti i raggi (307 200): 80–200 ms, cioè oltre 66,7 ms; 10 cm tutti i raggi: 35–100 ms; passo 4 (19 200 raggi): 5 cm 5–13 ms, 10 cm 2–7 ms | fuori intervallo |
| P7 | polare del nucleo (1° × 0,1 m), tutti i pixel | media 0,4–2,5 ms; a passo 4 < 0,2 ms | fuori intervallo |
| P8 | fasce (3 fasce, griglia sul piano con raggi 2D) | costo proporzionale ai raggi: rapporto tempo passo 1 / passo 8 fra 40 e 80; a 5 cm tutti i raggi 50–150 ms; a 10 cm passo 4, 1–4 ms. Lo scarto «121–140 contro 1,66 ms» del triage sarà quindi spiegabile col solo numero di raggi | rapporto fuori da 40–80 |
| P9 | carico improvviso (3 → 200 oggetti al fotogramma 150) | densa: tempo del fotogramma 150 ≤ 1,3 × mediana prima; hash e octree ≤ 2 × mediana prima; nessuna struttura supera 66,7 ms a passo 4; il tempo dopo il carico scende (raggi più corti) | una voce non vale |
| P10 | interrogazione 18 settori da 5° (tabella settore × distanza, quote 0,1–2,0 m) | polare < 5 µs; densa 10 cm 30–200 µs, 5 cm 0,3–1,5 ms; hash 1,1–2 × densa; octree 3–8 × densa; lettura nell'immagine (V-002) 0,1–1,5 ms | fuori intervallo |
| P11 | soglie del contratto (15 cicli/s = 66,7 ms; p95 ≤ 150 ms), solo aggiornamento + interrogazione | a passo ≥ 4 tutte le strutture le rispettano a 10 e a 5 cm; a passo 1 e 5 cm nessuna struttura voxel sta sotto 66,7 ms; la polare sempre | una voce non vale |
| P12 | rumore della macchina (carico medio ≈ 2 su 24 fili, altri agenti in corso) | massimo ≤ 2 × mediana per la densa a regime; se no, il massimo è dell'ambiente e lo provo ripetendo il lancio | massimo > 2 × mediana in due lanci su due |
| P13 | hash che conserva solo l'occupato (senza scrivere il libero) | memoria ≤ 25 % della densa in scena densa a 5 cm; tempo ≤ 3 ms a tutti i pixel | fuori |

Esiti (regge / smentita / non risolta): in fondo a `BENCHMARK_INDIPENDENTE.md` e qui sotto, DOPO le misure.

---

# Esiti — scritti alle 2026-11-14T16:43:19+01:00, DOPO le misure (la tabella sopra non è stata toccata)

Fonti: `tabelle.txt` (core 2), `confronto_core.txt` (core 0 e core lento 9), `risultati_python.txt`.

| N. | Esito | Misura |
|--|--|--|
| P1 | **regge** | 288 000 e 2 304 000 B |
| P2a | **smentita a 10 cm**, regge a 5 cm | 0,55 (76 blocchi su 160) e 0,33 (357 su 1 200): a 10 cm un blocco è largo 0,8 m e gonfia l'allocato |
| P2b | **regge** | 0,84 e 0,66 (116 e 724 blocchi) |
| P3 | **smentita a 5 cm** nella scena densa, regge il resto | densa: 1,31 (10 cm) e 1,17 (5 cm, atteso ≥ 1,3); vuota: 0,57 e 0,44 |
| P4 | **smentita sul tempo**; regge sul picco; sui nodi regge in 16 configurazioni su 20 | tempo 0,99–1,23 volte il non potato (atteso ≥ 1,3); picco ≥ 0,99; nodi a fine fotogramma 0,44–0,84 |
| P5 | densa **regge** (1,65–3,35 ns sul core 2); hash **smentita in parte** (1,39–1,76, atteso ≤ 1,6); octree **smentita in parte** (2,2–3,9, atteso 3–8) | più economico dell'atteso l'octree a pochi raggi |
| P6 | **smentita** (più veloce dell'atteso), salvo 10 cm a passo 4 | p95: 5 cm tutti 49,1 ms (atteso 80–200); 10 cm tutti 22,8 (35–100); passo 4: 4,35 (5–13) e 2,08 (2–7, regge) |
| P7 | **regge sulla soglia** | media 0,42 e 0,37 ms con tutti i pixel (atteso 0,4–2,5); 0,034 a passo 4 |
| P8 | **regge** | tre fasce, passo 1 / passo 8: 50,4 (10 cm) e 52,1 (5 cm); 85,5 ms a 5 cm con tutti i raggi; 3,29 ms a 10 cm passo 4. Lo scarto del triage si spiega con i raggi (21 volte) e con due strutture in un solo tempo |
| P9 | regge sui picchi (1,07–1,22; nessuna oltre 66,7 ms); **smentita** «il tempo dopo scende»: sale del 9–15 % | in una scena senza fondale gli oggetti nuovi aggiungono ritorni |
| P10 | regge per polare a 3 m (3,6 µs), densa a 10 cm (38), hash (1,2–1,8), octree (5–12 volte: **oltre l'atteso 3–8** a 5 cm con tutti i raggi), immagine (636); **smentita** per la densa a 5 cm (261 µs, atteso ≥ 300) e per la polare a 6 m (6,0 µs, atteso < 5) | |
| P11 | regge a passo ≥ 4 e per la polare; **smentita** «a passo 1 e 5 cm nessuna struttura voxel sta sotto 66,7 ms» | densa p95 49,1 ms (core 2) e 45,9 (core 0); sul core lento 67,4 |
| P12 | **regge** | densa: massimo / mediana ≤ 1,55 in tutte le configurazioni del giro principale |
| P13 | **smentita** sulla memoria, regge sul tempo | 0,55 della densa (atteso ≤ 0,25): gli oggetti mobili allocano blocchi lungo il percorso e nessuno li toglie; 1,0 ms |

Notato dopo, non previsto: (1) la scena «vuota» degli autori è una stanza chiusa; (2) il «core veloce» di un autore è un core lento; (3) la memoria residente della matrice densa nella scena vuota è quasi quella della hash (1 144 contro 1 048 kB); (4) le fasce con minimo e massimo per fascia costano più della matrice densa, le colonne di bit meno (variante aggiunta dopo il primo giro); (5) colonne di bit e matrice densa danno la stessa uscita per settori (somme uguali in 8 configurazioni su 8).
