"""Sostituzioni esatte (una occorrenza ciascuna) nei capitoli della copia v2 dell'allegato, per allinearla a VERDETTO_2C."""
import sys, pathlib
C = pathlib.Path(sys.argv[1])
R = {}
R['00_sommario.tex'] = [
(" % 2C: le cifre della frase seguente (pannello, collisione) possono cambiare.\nLe simulazioni mostrano anche dove il sistema cede: il «libero» è falso con un radar a pannello nella configurazione del sito e con una mappa degli ostacoli sbagliata; dopo una collisione fra droni la zona dei detriti è troppo ampia per essere utile.",
 "\nLe simulazioni mostrano anche dove il sistema cede. Il «libero» dipende dalla mappa degli ostacoli: con la mappa del sito dichiarata completa (un'ipotesi del simulatore) nessuno di 171 passaggi ha un «libero» sul drone, ma con una mappa dichiarata e sbagliata il «libero» dietro un edificio che non vi compare è falso; per questo, per impostazione, la mappa non è dichiarata completa. Quando il drone rallenta o si ferma l'avviso lo perde per qualche ciclo in 12 passaggi su 200. Dopo una collisione fra droni l'evento è dedotto entro $2\\unita{s}$ in 51 passaggi su 60, e la zona dei detriti è di alcuni chilometri e non si riduce guardando."),
]
R['01_introduzione.tex'] = [
("tempestivo in 200 passaggi su 200 $[0{,}981;\\,1]$, e in 100 su 100 con semi nuovi; con",
 "tempestivo in 200 passaggi su 200 $[0{,}981;\\,1]$, e in 100 su 100 con semi nuovi e la versione precedente delle regole; con"),
("«Libero» con il radar a pannello & configurazione del sito & falso in 163 passaggi su 171 $[0{,}910;\\,0{,}976]$: limite & \\prova{S} & \\S\\ref{sec:lp-smentiti}\\\\\n% 2C: la riga sopra e la riga sotto possono cambiare.\nCollisione fra droni & evento dedotto; 60 passaggi & entro $2\\unita{s}$ in 49 su 60 $[0{,}701;\\,0{,}894]$; zona dei detriti oltre $10\\unita{km}$ in 36 su 60 & \\prova{S} & \\S\\ref{sec:lp-eventi}\\\\",
 "«Libero» sul drone con il radar a pannello & configurazione del sito; ritenuta del ritorno per $5\\unita{s}$; mappa del sito dichiarata completa (ipotesi) & 0 passaggi su 171 $[0;\\,0{,}022]$ con «libero» sul drone; con una mappa dichiarata ma sbagliata «libero» falso in 5 casi costruiti su 6: limite & \\prova{S} & \\S\\ref{sec:lp-smentiti}\\\\\nCollisione fra droni & evento dedotto; 60 passaggi & entro $2\\unita{s}$ in 51 su 60 $[0{,}739;\\,0{,}919]$; zona dei detriti di $3{,}1$--$5{,}3\\unita{km}$, che non si riduce guardando & \\prova{S} & \\S\\ref{sec:lp-eventi}\\\\"),
("mappa degli ostacoli corretta. Per gli aerei in volo",
 "mappa degli ostacoli corretta e, per il «libero» sul drone nel sito, dichiarata completa. Per gli aerei in volo"),
]
R['08_limiti.tex'] = [
("% 2C: cifra del «libero» con il pannello.\n\\item \\textbf{«Libero» falso.} Con il radar a pannello, nella configurazione del sito, in 163 passaggi su 171; con una mappa degli ostacoli dichiarata completa ma sbagliata, dietro l'edificio che non vi compare.",
 "\\item \\textbf{Il «libero» dipende dalla mappa.} Nel sito, nessuno di 171 passaggi ha un «libero» sul drone solo con la mappa degli ostacoli dichiarata completa, che è un'ipotesi del simulatore; con una mappa dichiarata completa ma sbagliata il «libero» dietro l'edificio che non vi compare è falso (5 casi costruiti su 6). Per impostazione la mappa non è dichiarata completa; la sua convalida con lo sfondo misurato non è usata nel simulatore."),
("Con il solo radar per droni l'avviso perde il drone che rallenta o si ferma in 12 passaggi su 200; con il filtro Doppler a bordo in 9 su 100.\n% 2C: cifre della collisione.\n\\item \\textbf{Eventi improvvisi.} La collisione è dedotta entro $2\\unita{s}$ in 49 passaggi su 60; la zona dei detriti copre il sito e non si riduce; la fiammata è riconosciuta con un innesco ottimista.",
 "Con il solo radar per droni l'avviso perde il drone che rallenta o si ferma in 12 passaggi su 200; con il filtro Doppler a bordo in 9 su 100, con la versione precedente delle regole.\n\\item \\textbf{Eventi improvvisi.} La collisione è dedotta entro $2\\unita{s}$ in 51 passaggi su 60; la zona dei detriti è di circa $4{,}5\\unita{km}$ e non si riduce guardando; l'avviso non distingue chi è in pericolo (circa 96 tracce avvisate nell'avaria); la fiammata è riconosciuta con un innesco ottimista.\n\\item \\textbf{Cifre non rimisurate.} Con le regole attuali (ritenuta del ritorno, origine dei detriti dalle sole tracce recenti) sono rimisurati solo il drone dietro un edificio, la collisione, l'avaria e il passaggio ravvicinato; le altre scene hanno le cifre della versione precedente, e le ripetizioni con semi nuovi non sono rifatte. Il prezzo della ritenuta, cioè le chiusure tardive dell'avviso, non è misurato."),
]
R['09_conclusioni.tex'] = [
(" % 2C: i limiti seguenti (pannello, collisione) possono cambiare.\nRestano limiti dichiarati: per gli aerei in volo l'avviso non è tempestivo; il «libero» è falso con un radar a pannello nella configurazione del sito e con una mappa sbagliata; dopo una collisione fra droni la zona dei detriti è troppo ampia per essere utile;",
 "\nRestano limiti dichiarati: per gli aerei in volo l'avviso non è tempestivo; il «libero» sul drone nel sito regge solo con la mappa degli ostacoli dichiarata completa, ed è falso con una mappa dichiarata e sbagliata; l'avviso perde per qualche ciclo il drone che rallenta o si ferma (12 passaggi su 200); dopo una collisione fra droni la zona dei detriti è di alcuni chilometri e non si riduce guardando;"),
]
R['10_lunga_portata.tex'] = [
("Un sensore in perdita di affidabilità rende tutta la sua griglia «non osservata».\n",
 "Un sensore in perdita di affidabilità rende tutta la sua griglia «non osservata». Un ritorno recente di un radar vieta il «libero» attorno al punto misurato per $5\\unita{s}$: una sola passata mancata non basta ad aprirlo. Il prezzo di questa ritenuta, cioè le chiusure tardive dell'avviso, non è misurato.\n"),
("è un controesempio, e nel prototipo provato la mappa è dichiarata completa per impostazione (\\S\\ref{sec:lp-smentiti}).",
 "è un controesempio (5 casi costruiti su 6). Per questo nel prototipo, per impostazione, la mappa non è dichiarata completa, e nei sei casi la cella dietro l'edificio resta «non osservata» \\prova{S}. La convalida della mappa con lo sfondo misurato non è ancora usata nel simulatore (\\S\\ref{sec:lp-smentiti})."),
("\\item \\emph{Collisione fra droni.} % 2C: le cifre di questo punto possono cambiare con le correzioni sulla collisione.\nL'evento è dedotto in $1{,}2$--$2{,}2\\unita{s}$; entro $2\\unita{s}$ in 49 passaggi su 60 $[0{,}701;\\,0{,}894]$ e in 24 su 30 $[0{,}627;\\,0{,}905]$ con semi nuovi \\prova{S}. La soglia di progetto, entro $2\\unita{s}$ in ogni passaggio, non è raggiunta. I frammenti stanno nel volume in una quota di $0{,}9973$, sotto il $0{,}999$ richiesto. Nessuna cella è dichiarata «libera» su un frammento: 0 passaggi su 60 $[0;\\,0{,}06]$, per costruzione. L'impronta dei detriti, però, è enorme: il suo raggio supera $10\\unita{km}$ in 36 passaggi su 60 $[0{,}474;\\,0{,}714]$ (20 su 30 con semi nuovi), con mediana di $42\\unita{km}$ e massimo di $74\\unita{km}$; non si riduce, perché manca l'ispezione, e l'avviso resta acceso su tutte le tracce. In un passaggio su 60 una «separazione» falsa è dichiarata $12{,}5\\unita{s}$ prima dell'urto.",
 "\\item \\emph{Collisione fra droni.} L'evento è dedotto da $1{,}2$ a $2{,}3\\unita{s}$ dopo l'urto (mediana $1{,}8\\unita{s}$); entro $2\\unita{s}$ in 51 passaggi su 60 $[0{,}739;\\,0{,}919]$, e con il tipo giusto («contatto») in 50 su 60 $[0{,}720;\\,0{,}907]$: in due passaggi è dedotto come «separazione» \\prova{S}. La soglia di progetto, entro $2\\unita{s}$ in ogni passaggio, non è raggiunta. Nessuna cella è dichiarata «libera» su un frammento: 0 passaggi su 60 $[0;\\,0{,}06]$, per costruzione. L'origine dei detriti è presa solo dalle tracce viste negli ultimi $3\\unita{s}$: il raggio residuo della zona dei detriti va da $3{,}1$ a $5{,}3\\unita{km}$ (mediana $4{,}5\\unita{km}$), mai oltre $10\\unita{km}$ (0 su 60 $[0;\\,0{,}06]$). La zona non si riduce guardando: l'ispezione non ha tolto punti in nessun passaggio (0 su 60), e l'avviso resta su tutte le tracce dentro la zona. Nessun evento è dichiarato prima dell'urto (0 su 60 $[0;\\,0{,}06]$), ma la regola delle tracce recenti è stata scritta dopo aver esaminato un passaggio con un evento falso prima dell'urto: questo esito non è una previsione. Con la versione precedente delle regole i frammenti stavano nel volume in una quota di $0{,}9973$, sotto il $0{,}999$ richiesto; con le regole attuali la ripetizione con semi nuovi non è rifatta."),
("Il mezzo in pista è avvisato a non meno di $140\\unita{m}$ dai frammenti veri in 60 passaggi su 60;",
 "Con le regole attuali le camere sono dichiarate non affidabili entro 3 cicli anche in 30 passaggi su 30. Il mezzo in pista è avvisato a non meno di $140\\unita{m}$ dai frammenti veri in 60 passaggi su 60, e con le regole attuali entra davvero nell'impronta in 30 su 30;"),
("l'avviso è giusto e non distingue chi è in pericolo.",
 "l'avviso è giusto e non distingue chi è in pericolo: tocca una mediana di 96 tracce."),
("e 0 su 30 con quello di $210\\unita{m/s}$ \\prova{S}.",
 "e 0 su 30 con quello di $210\\unita{m/s}$, anche con le regole attuali (0 su 30 $[0;\\,0{,}114]$) \\prova{S}."),
("in 100 su 100 $[0{,}963;\\,1]$ con semi nuovi; fuori avviso 0 su 200",
 "in 100 su 100 $[0{,}963;\\,1]$ con semi nuovi e la versione precedente delle regole; fuori avviso 0 su 200"),
("e in 9 su 100 $[0{,}048;\\,0{,}162]$ con semi nuovi\\\\",
 "e in 9 su 100 $[0{,}048;\\,0{,}162]$ con semi nuovi e la versione precedente delle regole\\\\"),
("Due precisazioni. L'avviso perde il drone che rallenta o si ferma in circa il $6\\,\\%$ dei passaggi con il solo radar: la causa non è stata accertata. E con il radar a pannello il «libero» sull'oggetto non regge (\\S\\ref{sec:lp-smentiti}): la tempestività di questa tabella non dice che il «libero» sia corretto.",
 "Tre precisazioni. L'avviso perde il drone che rallenta o si ferma in circa il $6\\,\\%$ dei passaggi con il solo radar: la causa non è stata accertata. Il «libero» sull'oggetto con il radar a pannello regge solo con la mappa del sito dichiarata completa (\\S\\ref{sec:lp-smentiti}): la tempestività di questa tabella non dice che il «libero» sia corretto in ogni caso. Con le regole attuali è rimisurato solo il drone dietro un edificio (200 passaggi per configurazione); il rullaggio e il drone sotto la copertura hanno le cifre della versione precedente."),
("\\item \\textbf{Il «libero» può essere falso con il radar a pannello.} % 2C: cifra da allineare se cambia la configurazione del sito.\nNella configurazione del sito hanno istanti con «libero» sulla cella del drone 163 passaggi su 171 $[0{,}910;\\,0{,}976]$, e 85 su 85 $[0{,}957;\\,1]$ con semi nuovi \\prova{S}: il ritorno cade nella cella vicina.",
 "\\item \\textbf{Il «libero» con il radar a pannello dipende dalla mappa.} Nella configurazione del sito, con la regola precedente, una sola passata mancata apriva un «libero» sulla cella del drone in 163 passaggi su 171 $[0{,}910;\\,0{,}976]$: il ritorno cadeva nella cella vicina, e legare la finestra alla velocità massima, da solo, non lo toglieva. Con la ritenuta del ritorno per $5\\unita{s}$ e con la mappa del sito dichiarata completa, che è un'ipotesi del simulatore, nessun passaggio su 171 ha istanti con «libero» sul drone $[0;\\,0{,}022]$ \\prova{S}; la ripetizione con semi nuovi non è rifatta."),
("\\item \\textbf{Mappa dichiarata completa ma sbagliata.} Un edificio che non compare in una mappa dichiarata completa apre un «libero» falso dietro di sé \\prova{S}; nel prototipo provato la mappa è dichiarata completa per impostazione.",
 "\\item \\textbf{Mappa dichiarata completa ma sbagliata.} Un edificio che non compare in una mappa dichiarata completa apre un «libero» falso dietro di sé, in 5 casi costruiti su 6 \\prova{S}; per questo il prototipo, per impostazione, non dichiara la mappa completa, e lì la cella dietro l'edificio è «non osservata» (6 su 6)."),
("con il filtro Doppler a bordo, in 9 su 100.\n\\item \\textbf{Classi",
 "con il filtro Doppler a bordo, in 9 su 100, con la versione precedente delle regole.\n\\item \\textbf{Classi"),
("La collisione non è dedotta entro $2\\unita{s}$ in ogni passaggio (49 su 60); la zona dei detriti copre il sito e non si riduce;",
 "La collisione non è dedotta entro $2\\unita{s}$ in ogni passaggio (51 su 60); la zona dei detriti è di alcuni chilometri e non si riduce guardando; l'avviso non distingue chi è in pericolo;"),
("\\item \\textbf{Mappa degli ostacoli corretta,} oppure sfondo misurato; senza l'una o l'altro non c'è «libero».",
 "\\item \\textbf{Mappa degli ostacoli corretta,} oppure sfondo misurato; senza l'una o l'altro non c'è «libero». Le cifre del «libero» sul drone nel sito valgono con la mappa dichiarata completa, che è un'ipotesi."),
]
R['B_riproducibilita.tex'] = [
("% 2C: i nomi e gli esiti delle scene possono cambiare.\n", ""),
("ha dato esito senza errori in $665\\unita{s}$.", "ha dato esito senza errori in $698\\unita{s}$."),
]
err = 0
for f, lst in R.items():
    p = C / f; t = p.read_text(encoding='utf-8')
    for i, (a, b) in enumerate(lst):
        n = t.count(a)
        if n != 1:
            print(f'ERRORE {f} #{i}: {n} occorrenze'); err += 1; continue
        t = t.replace(a, b)
    if not err: p.write_text(t, encoding='utf-8')
    print(f, 'ok' if not err else 'non scritto')
sys.exit(1 if err else 0)
