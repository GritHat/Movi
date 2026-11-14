#!/usr/bin/env python3
"""Ultime correzioni, parte 2: coerenza (C-R#) e cifre (N-R#). Prima controlla tutte le sostituzioni, poi scrive."""
import pathlib, sys
base = pathlib.Path(__file__).resolve().parent.parent / "capitoli"
E = []
def sub(f, old, new, tag): E.append((f, old, new, tag))

# ================= sommario (C-R12, N-R6, D-R1)
sub("00_sommario.tex",
 r"l'avviso di possibile presenza termina solo per osservazione diretta. Nelle ipotesi dichiarate sono dimostrati che ciò che non è osservato non è mai «libero», il contenimento del soggetto nascosto nell'insieme di possibile presenza e la condizione sulla fascia di guardia. In simulazione, con modello ideale del sensore, un ostacolo fermo largo $2\unita{m}$, il bordo dell'ombra noto e un soggetto alla volta sul proprio percorso, la regione di previsione è emessa a ogni ciclo dell'occlusione, una volta riconosciuto l'ingresso nell'ombra (0 interruzioni su $23\,402$ passaggi; l'ingresso non è riconosciuto in 928 di essi, in 24 con una regola aggiuntiva), e contiene il soggetto in almeno 9 casi su 10 fino a $2\unita{s}$ e in almeno 85 su 100 fino a $3\unita{s}$; con un ostacolo largo $1\unita{m}$ la soglia di 9 su 10 non è raggiunta, e su profondità simulata dalle schede tecniche questa regola non è stata eseguita.",
 r"l'avviso di possibile presenza non termina senza osservazione diretta. Nelle ipotesi dichiarate sono dimostrati che ciò che non è osservato non è mai «libero», il contenimento del soggetto nascosto nell'insieme di possibile presenza (per una lettura esatta del suolo, senza il margine che il sistema usa) e la condizione sulla fascia di guardia. In simulazione, con modello ideale del sensore e un soggetto alla volta, la regione di previsione è emessa a ogni ciclo dell'occlusione una volta riconosciuto l'ingresso nell'ombra (0 interruzioni dopo l'ingresso su $23\,402$ passaggi nascosti; in 928 di essi la traccia si chiude prima dell'ombra e non c'è regione, e con una regola aggiuntiva, attiva solo dopo una prova d'ingresso, 24 restano senza avviso); con un ostacolo fermo largo $2\unita{m}$, il bordo dell'ombra noto e il soggetto sul proprio percorso, la regione contiene il soggetto in almeno 9 casi su 10 fino a $2\unita{s}$ e in almeno 85 su 100 fino a $3\unita{s}$; con un ostacolo largo $1\unita{m}$ la soglia di 9 su 10 non è raggiunta, e su profondità simulata dalle schede tecniche questa regola non è stata eseguita. Dietro un ostacolo fermo l'avviso resta acceso, e nella realizzazione provata resta acceso anche dopo la rimozione dell'ostacolo.", "C-R12/N-R6 sommario")

# ================= capitolo 1
I = "01_introduzione.tex"
sub(I, r"di tre camere a stereo attivo a $424\times240$ pixel, a posa nota.", r"di tre camere a stereo attivo a $424\times240$ pixel e, dove indicato, a $848\times480$, a posa nota.", "C-R14c")
sub(I, r"gli estremi superiori sono arrotondati per eccesso ($2{,}85\,\%$ è scritto $2{,}9\,\%$ e $0{,}0155\,\%$ è scritto $0{,}016\,\%$).",
 r"gli estremi superiori degli intervalli per zero eventi sono arrotondati per eccesso ($2{,}85\,\%$ è scritto $2{,}9\,\%$ e $0{,}0155\,\%$ è scritto $0{,}016\,\%$); gli altri estremi al valore più vicino, salvo l'estremo inferiore $0{,}875$ del pannello largo $1\unita{m}$, scritto $0{,}87$.", "C-R14a")
sub(I, r"Ogni riga delle tabelle dice da quale viene.",
 r"Ogni riga delle tabelle dice da quale viene. I gruppi a celle forti, le condizioni aggiuntive del riaggancio e l'avviso per le tracce chiuse vicino a un'ombra non fanno parte della configurazione di riferimento: si attivano all'avvio solo se le prove d'ingresso del \S\ref{sec:lim-salute} sono superate.", "C-R15a")
sub(I, r"Continuità & ideale; 12 combinazioni per 5 comportamenti; premessa: ingresso nell'ombra riconosciuto & 0 passaggi con un ciclo senza regione su $23\,402$ (6000 camminatori distinti: al più $6{,}4$ su $10\,000$); premessa mancata in 928 passaggi su $23\,402$ ($3{,}97\,\%$), in 24 ($0{,}10\,\%$) con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attiva solo dopo la prova d'ingresso sul suolo vuoto.",
 r"Continuità & ideale; 12 combinazioni (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) per 5 comportamenti; premessa: ingresso nell'ombra riconosciuto & 0 passaggi con un ciclo senza regione dopo l'ingresso, su $23\,402$ passaggi nascosti (6000 camminatori distinti: meno di 7 su $10\,000$). La premessa manca in 928 passaggi ($3{,}97\,\%$; 852 con $P_D=0{,}7$), nei quali non c'è regione: la soglia 0 della Tabella~\ref{tab:intro-requisiti} è rispettata solo fra i passaggi con l'ingresso riconosciuto. Con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attiva solo dopo la prova d'ingresso sul suolo vuoto, restano senza avviso 24 passaggi ($0{,}10\,\%$).", "N-R6/C-R10 cap1")
sub(I, r"Da scheda: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324 a 424 pixel di larghezza e in 0 su 4325 a 848, e in 0 su 3608 per risoluzione in una replica.",
 r"Da scheda, con i gruppi a celle forti e l'avviso che resta dopo il riaggancio: soggetto nascosto entro $3\unita{m}$ senza avviso in 0 fotogrammi su 4324 a 424 pixel di larghezza e in 0 su 4325 a 848 (con la configurazione di riferimento, sugli stessi 150 passaggi, in 180 e in 271), e in 0 su 3608 per risoluzione in una replica.", "C-R1/N-R2 cap1")
sub(I, r"176 su 180 $[94;\,99\,\%]$ a 424 pixel di larghezza e 174 su 180 $[93;\,98\,\%]$ a 848", r"176 su 180 $[94{,}4;\,99{,}1\,\%]$ a 424 pixel di larghezza e 174 su 180 $[92{,}9;\,98{,}5\,\%]$ a 848", "C-R14b cap1")
sub(I, r"(19 casi su 20 da scheda; 2400 su 2400 con modello ideale); l'avviso resta & \prova{S} &",
 r"(19 casi su 20 da scheda; 2400 su 2400 con modello ideale). L'avviso resta per costruzione; da scheda, in una scena con due persone, 0 fotogrammi su 336 con il primo soggetto fuori dall'avviso; con modello ideale la verifica non è stata eseguita & \prova{S}\prova{N} &", "C-R13")
sub(I, r"in 79 su 90 $[79{,}4;\,93{,}0\,\%]$, in 5 su 90 con la soglia adattata alla risoluzione;",
 r"in 79 su 90 $[79{,}4;\,93{,}0\,\%]$; in 5 su 90 con la soglia minima di punti portata da 3 a 40, non adottata perché una scatola alta $15\unita{cm}$ a $2\unita{m}$ è allora vista in 3 prove su 10;", "C-R6")
sub(I, r"uscita «osservato» con il soggetto nascosto in 8 passaggi su 90 / in 1 su 140: la soglia 0 non è rispettata & \prova{S} & \S\ref{sec:val}\\",
 r"uscita «osservato» con il soggetto nascosto in 8 passaggi su 90 in una prima serie; in una seconda, riagganci a soggetto ancora nascosto in 11 e 6 passaggi su 140 (424 e 848 pixel di larghezza) / in 1 e 1 su 140: la soglia 0 non è rispettata & \prova{S} & \S\ref{sec:sti}\\", "C-R4 cap1")
sub(I, r"portata $3\unita{m}$, avvicinamento frontale, reazione di $1{,}0\unita{s}$ ipotizzata &",
 r"portata $3\unita{m}$, avvicinamento frontale, reazione di $1{,}0\unita{s}$ ipotizzata; velocità delle classi in parte ipotizzate (\S\ref{sec:sti}) &", "N-R8a")
sub(I, r"Il simulatore da scheda produce meno pixel senza dato delle registrazioni pubbliche con cui è stato confrontato ($7{,}8\,\%$ al livello di rumore più alto, contro 24--34\,\%): le cifre al livello nominale sono ottimistiche.",
 r"Il simulatore da scheda produce meno pixel senza dato di due registrazioni pubbliche di camere a stereo attivo con cui è stato confrontato (fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$: $7{,}8\,\%$ al livello di rumore più alto, contro $24{,}1\,\%$ e $34{,}4\,\%$; camere, risoluzioni e scene diverse da quelle simulate): le cifre al livello nominale sono ottimistiche.", "N-R4 cap1")

# ================= capitolo 3
sub("03_mappa.tex", r"dichiarano lo stesso principio (\S\ref{sec:cos-correlati})", r"dichiarano un principio analogo (\S\ref{sec:cos-correlati})", "C-R18a")

# ================= capitolo 4
S = "04_stima.tex"
sub(S, r"con quota $y\in[0{,}07;\,2]\unita{m}$ ed è il primo ritorno lungo il suo azimut.",
 r"con quota $y\in[0{,}07;\,2]\unita{m}$, anche se sta oltre la prima cella occupata del suo azimut (è la definizione del \S\ref{sec:map}).", "N-R5")
sub(S, r"Prova singola: valori del calcolo d'origine con la Proposizione~\ref{prop:sti-mobile}; con la curva severa sovrastima, perché la regola usa la maggiore delle distanze \emph{misurate}, che il rumore gonfia. Rifacendo il conto con $T_w=0{,}867\unita{s}$ e lo scarto tipo a $3\unita{m}$ si ottengono $0{,}815$ e $0{,}389$ per le curve pessimista e severa: lo scarto dai valori in tabella non è spiegato.",
 r"Prova singola \prova{C}: probabilità che scatti la sola prova alla finestra massima $T_w=0{,}867\unita{s}$ (Proposizione~\ref{prop:sti-mobile}), con la soglia \eqref{eq:sti-soglia} alla distanza di partenza e lo scarto tipo alle distanze dei due capi della finestra ($2{,}97$ e $2{,}53\unita{m}$); con lo scarto tipo a $3\unita{m}$ a entrambi i capi si ottengono $0{,}815$ e $0{,}389$ per le curve pessimista e severa. Con la curva severa la prova singola sovrastima la simulazione, perché la regola usa la maggiore delle distanze \emph{misurate}, che il rumore gonfia.", "N-R3")
sub(S, r"acc. / frenata (m/s$^2$)", r"acc. / frenata massime (m/s$^2$)", "N-R8b")
sub(S, r"176 passaggi su 180 (94--99\,\%) a 424 pixel di larghezza e in 174 su 180 (93--98\,\%) a 848", r"176 passaggi su 180 (94,4--99,1\,\%) a 424 pixel di larghezza e in 174 su 180 (92,9--98,5\,\%) a 848", "C-R14b cap4")

# ================= capitolo 5
sub("05_occlusione.tex",
 r"I 23\,402 passaggi della prova su semi nuovi vengono da 6\,000 camminatori distinti: il limite superiore al 95\,\% è «meno di 6,4 passaggi su 10\,000», non quello che si otterrebbe trattando i passaggi come indipendenti. La premessa è l'ingresso: nella stessa prova la traccia è chiusa prima dell'ombra in 928 passaggi su 23\,402 (3,97\,\%);",
 r"I 23\,402 passaggi nascosti della prova su semi nuovi (12 combinazioni: 3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) vengono da 6\,000 camminatori distinti: il limite superiore al 95\,\% è «meno di 7 passaggi su 10\,000» (6,4 se ogni camminatore ha almeno un passaggio con l'ingresso riconosciuto, 6,8 nel caso peggiore), non quello che si otterrebbe trattando i passaggi come indipendenti. La premessa è l'ingresso: nella stessa prova la traccia è chiusa prima dell'ombra in 928 passaggi su 23\,402 (3,97\,\%: 76 su 11\,701 con $P_D=0{,}9$ e 852 su 11\,701 con $P_D=0{,}7$), e lo zero vale per i 22\,474 restanti;", "N-R6 cap5")

# ================= capitolo 6
V = "06_valutazione.tex"
sub(V, r"con i semi riparati il rapporto torna a $0{,}94$.", r"con lo stato iniziale mescolato il rapporto torna a $0{,}94$.", "C-R17d1")
sub(V, r"non sono stati rifatti con semi riparati 71\,671", r"non sono stati ripetuti con lo stato iniziale mescolato 71\,671", "C-R17d2")
sub(V, r"Il soggetto è \emph{puntiforme} nelle prove di base e un \emph{corpo esteso} (disco di $0{,}45\unita{m}$, misura nel baricentro della parte visibile) nelle prove d'insieme.",
 r"Il soggetto è \emph{puntiforme} nelle prove di base; nelle prove d'insieme è un \emph{corpo esteso} (disco di $0{,}45\unita{m}$, misura nel baricentro della parte visibile) in metà delle configurazioni e puntiforme nelle altre, con $P_D=0{,}9$ o $0{,}7$.", "C-R11a")
sub(V, r"Traccia chiusa prima dell'ombra (avviso non acceso) & senza / con l'avviso mantenuto per le tracce chiuse entro $0{,}75\unita{m}$ dall'ombra & 928 / 24 & 23\,402 passaggi & quote: 3,97\,\% / 0,10\,\% & I \prova{S}\\",
 r"Traccia chiusa prima dell'ombra (avviso non acceso) & senza / con l'avviso mantenuto per le tracce chiuse entro $0{,}75\unita{m}$ dall'ombra; 3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme & 928 / 24 & 23\,402 passaggi nascosti (11\,701 per valore di $P_D$) & quote: 3,97\,\% / 0,10\,\%; con $P_D=0{,}9$: 76 / 2; con $P_D=0{,}7$: 852 / 22 & I \prova{S}\\", "N-R6 cap6a")
sub(V, r"4324 e 4325 fotogrammi (3921 e 3922 senza la disposizione in cui il soggetto si allontana nell'ombra); replica: 0 su 3608 per risoluzione",
 r"4324 e 4325 fotogrammi in 150 passaggi (3921 e 3922 tolti i 10 passaggi al livello limite, 106 fotogrammi, e i 10 in cui il soggetto si allontana nell'ombra e non ricompare, 297); replica: 0 su 3608 per risoluzione", "N-R1")
sub(V, r"idem, prove d'insieme & corpo esteso; 12 configurazioni $\times$ 5 comportamenti & 0 & 23\,402 passaggi (6000 soggetti distinti) & 0–0,064\,\% (su 6000)\\",
 r"idem, prove d'insieme & 12 configurazioni (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme) $\times$ 5 comportamenti; vuoti contati dopo l'ingresso nell'ombra & 0 & 23\,402 passaggi nascosti (6000 soggetti distinti); traccia entrata nell'ombra in 22\,474 & 0–0,07\,\% per soggetto (0,064 se tutti i 6000 hanno un passaggio con la traccia entrata)\\", "N-R6/C-R11 cap6b")
sub(V, r"Ostacolo entro 15 cm dalla posizione vera, casi limite &",
 r"Ostacolo fermo entro 15 cm dalla posizione vera & cassa alta $1\unita{m}$ a $1{,}68\unita{m}$; scatola di 15 cm a $2{,}0\unita{m}$ & 84; 10 & 84; 10 fotogrammi (una sequenza ciascuno) & — & II \prova{S}\\" + "\n" + r"Ostacolo entro 15 cm dalla posizione vera, casi limite &", "C-R5")
sub(V, r"confrontato con registrazioni pubbliche, sottostima i pixel senza dato (7,8\,\% al livello limite contro 24–34\,\% osservati).",
 r"confrontato con due registrazioni pubbliche di camere a stereo attivo, sottostima i pixel senza dato. Fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$, nei primi 60 fotogrammi, i pixel senza dato sono 1,7\,\% al livello nominale e 7,8\,\% al livello limite, contro 24,1\,\% in una sequenza al chiuso con una persona \cite{depthtrack} e 34,4\,\% in una registrazione di esempio del costruttore di una delle camere; una registrazione con un sensore a luce strutturata \cite{tum-rgbd} dà 6,3\,\%. Camere, risoluzioni e scene non sono quelle simulate: il confronto dà il verso dello scarto, non la sua misura.", "N-R4 cap6")

# ================= capitolo 7
sub("07_costo.tex", r"La terza riga è riportata senza ricalcolo dai dati per ciclo.", r"La terza riga non è stata ricalcolata dai dati per ciclo.", "C-R17e")

# ================= capitolo 8
L = "08_limiti.tex"
sub(L, r"La frase per settori è una regola di progetto: l'ordine fra i primi due livelli non è stato provato \prova{N}.",
 r"La frase per settori è una regola di progetto: non è stata generata in alcuna prova, e l'ordine fra i primi due livelli non è stato provato \prova{N}.", "C-R3")
sub(L, r"(5) sul suolo vuoto, in $30\unita{s}$, non devono nascere gruppi né tracce confermate. Se cade una delle prime quattro prove il sistema non parte; se cade la quinta restano spenti l'avviso senza traccia e l'identità al ritorno, e l'uscita lo dichiara.",
 r"(5) sul suolo vuoto, in $30\unita{s}$, non devono nascere gruppi né tracce confermate; la prova si esegue nella configurazione che si vuole attivare, con i gruppi a celle forti (\S\ref{sec:sti-mobile}): con i gruppi per componenti connesse della configurazione di riferimento, su profondità simulata dalle schede tecniche, sul suolo vuoto nascono 137 e 206 tracce confermate in 9 sequenze, e la prova non sarebbe superata \prova{S}. Se cade una delle prime quattro prove il sistema non parte; se cade la quinta restano spenti i gruppi a celle forti, le condizioni aggiuntive del riaggancio, l'avviso senza traccia e l'identità al ritorno, e l'uscita lo dichiara.", "C-R2")
sub(L, r"Con $T_r=1{,}0\unita{s}$ la velocità coperta è $1{,}44\unita{m/s}$: una persona a passo normale rientra nel dominio con $6\unita{cm}$ di margine sulla distanza, il passo svelto no.",
 r"Con $T_r=1{,}0\unita{s}$ la velocità coperta dall'avviso tempestivo è $1{,}44\unita{m/s}$: una persona a passo normale ($1{,}4\unita{m/s}$) vi rientra con $6\unita{cm}$ di margine sulla distanza, il passo svelto no. È una grandezza diversa dalla velocità coperta dalla fascia di guardia ($1{,}13\unita{m/s}$, \S\ref{sec:lim-validita}), che il passo normale supera: a $1{,}4\unita{m/s}$ l'avviso è tempestivo per calcolo, ma il contenimento nella fascia non è dimostrato (\S\ref{sec:occ}).", "C-R8")
sub(L, r"8 passaggi su 90 con la configurazione di riferimento su profondità simulata dalle schede tecniche, 1 su 140 con i gruppi a celle forti",
 r"8 passaggi su 90 e, in una seconda serie, riagganci a soggetto ancora nascosto in 11 e 6 passaggi su 140, con la configurazione di riferimento su profondità simulata dalle schede tecniche; 1 e 1 su 140 con i gruppi a celle forti", "C-R4 cap8")
sub(L, r"Per una persona alta $1{,}70\unita{m}$ servono $1{,}61\unita{m}$ d'ostacolo nella geometria provata.",
 r"Per una persona alta $1{,}70\unita{m}$ a $2{,}3\unita{m}$ dal sensore servono da $1{,}57$ a $1{,}61\unita{m}$ d'ostacolo con il pannello fra $1{,}7$ e $1{,}9\unita{m}$ (Tabella~\ref{tab:geo-amin}).", "C-R7a")
sub(L, r"Dietro un ostacolo più basso di circa $1{,}65\unita{m}$ il sistema",
 r"Dietro un ostacolo più basso dell'altezza minima della Tabella~\ref{tab:geo-amin} (circa $1{,}65\unita{m}$ per una statura di $1{,}75\unita{m}$ con il pannello a $1{,}9\unita{m}$) il sistema", "C-R7b")
sub(L, r"in 10 prove su 10, (72--100\,\%),", r"in 10 prove su 10 (72--100\,\%),", "C-R18b")
sub(L, r"e l'avviso che resta, l'identità tiene in 176 passaggi su 180 [94--99\,\%] a 424 pixel e in 174 su 180 [93--98\,\%] a 848,",
 r"e l'avviso che resta (regole attive solo dopo le prove d'ingresso, \S\ref{sec:lim-salute}), l'identità tiene in 176 passaggi su 180 [94,4--99,1\,\%] a 424 pixel e in 174 su 180 [92,9--98,5\,\%] a 848,", "C-R14b/C-R15 cap8")
sub(L, r"Il simulatore sottostima i pixel senza dato ($7{,}8\,\%$ al livello limite contro 24--34\,\% in registrazioni pubbliche \prova{P}): le cifre al rumore nominale sono ottimistiche.",
 r"Il simulatore sottostima i pixel senza dato ($7{,}8\,\%$ al livello limite contro $24{,}1\,\%$ e $34{,}4\,\%$ in due registrazioni pubbliche di camere a stereo attivo, fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$ \prova{P}; \S\ref{sec:val}): le cifre al rumore nominale sono ottimistiche.", "N-R4 cap8")

# ================= capitolo 9
C = "09_conclusioni.tex"
sub(C, r"La regione è emessa a ogni ciclo dell'occlusione: 0 passaggi con un'interruzione su $23\,402$, da 6000 soggetti distinti; la premessa, cioè l'ingresso nell'ombra riconosciuto, manca in 928 passaggi su $23\,402$ ($3{,}97\,\%$), e in 24 ($0{,}10\,\%$) con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attivata solo dopo la prova d'ingresso sul suolo vuoto (\S\ref{sec:lim-salute}).",
 r"La regione è emessa a ogni ciclo dell'occlusione dopo l'ingresso: 0 passaggi con un'interruzione su $23\,402$ passaggi nascosti, da 6000 soggetti distinti (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme); la premessa, cioè l'ingresso nell'ombra riconosciuto, manca in 928 passaggi ($3{,}97\,\%$; 76 con $P_D=0{,}9$ e 852 con $P_D=0{,}7$), nei quali non c'è regione; con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attivata solo dopo la prova d'ingresso sul suolo vuoto (\S\ref{sec:lim-salute}), restano senza avviso 24 passaggi ($0{,}10\,\%$; 2 e 22).", "N-R6 cap9")
sub(C, r"\emph{Su profondità simulata dalle schede tecniche.} Un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324 a 424 pixel di larghezza e 0 su 4325 a 848, e 0 su 3608 per risoluzione in una replica).",
 r"\emph{Su profondità simulata dalle schede tecniche.} Con i gruppi a celle forti e l'avviso che resta dopo il riaggancio, un soggetto nascosto entro $3\unita{m}$ non resta senza avviso (0 fotogrammi su 4324 a 424 pixel di larghezza e 0 su 4325 a 848, e 0 su 3608 per risoluzione in una replica); con la configurazione di riferimento, sugli stessi passaggi, resta senza avviso in 180 e in 271 fotogrammi.", "C-R1/N-R2 cap9")
sub(C, r"entro $2{,}6\unita{m}$, rumore nominale (\S\ref{sec:sti}, \S\ref{sec:val}).",
 r"entro $2{,}6\unita{m}$, rumore nominale (\S\ref{sec:sti}, \S\ref{sec:val}). Queste regole non fanno parte della configurazione di riferimento: si attivano all'avvio solo se le prove d'ingresso sono superate (\S\ref{sec:lim-salute}).", "C-R15b")

# ================= appendici
A = "A_parametri.tex"
sub(A, r"intervallo utile della camera; da misurare & scelto\\", r"intervallo utile della camera; non misurato & scelto\\", "C-R17c1")
sub(A, r"modello del rumore del sensore; da misurare sul suolo & stimato\\", r"modello del rumore del sensore; non misurato sul suolo & stimato\\", "C-R17c2")
sub(A, r"dato del costruttore; da misurare & stimato\\", r"dato del costruttore; non misurato & stimato\\", "C-R17c3")
sub(A, r"--- & libreria di taratura dei percorsi & almeno 200 percorsi, due persone, tre andature & \S\ref{sec:val} & scelto\\",
 r"--- & libreria di percorsi ricavata da camminate di persone (non realizzata) & almeno 200 percorsi, due persone, tre andature & requisito di progetto; nelle prove la libreria è di 400 percorsi simulati (\S\ref{sec:occ}) & scelto\\", "N-R7")
sub(A, r"da rifissare con $60\unita{s}$ di conteggio a vuoto e sotto carico", r"valore di progetto, non misurato; va fissato con $60\unita{s}$ di conteggio a vuoto e sotto carico", "C-R17a")
sub(A, r"il legame fra i due numeri non è documentato", r"il legame fra i due numeri non è derivato in questo documento", "C-R17b")
sub("B_riproducibilita.tex", r"che non contengono profondità, e sequenze di profondità registrate \cite{tum-rgbd,depthtrack}.",
 r"che non contengono profondità, sequenze di profondità registrate \cite{tum-rgbd,depthtrack} e una registrazione di esempio distribuita dal costruttore di una delle camere, usata solo per il confronto dei pixel senza dato (\S\ref{sec:val}).", "N-R4 appB")

bad = 0
for f, old, new, tag in E:
    c = (base / f).read_text(encoding="utf-8").count(old)
    if c != 1:
        print(f"ERRORE {tag} {f}: {c} occorrenze di: {old[:80]!r}"); bad += 1
if bad: sys.exit(1)
for f, old, new, tag in E:
    p = base / f; s = p.read_text(encoding="utf-8"); assert s.count(old) == 1, tag
    p.write_text(s.replace(old, new), encoding="utf-8")
print("parte 2: sostituzioni applicate", len(E))
