"""Sostituzioni esatte nella proposta v2.0 per allinearla a VERDETTO_2C e togliere il riferimento all'organizzazione interna."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding='utf-8')
S = [
("% Le righe marcate «% 2C» possono cambiare con la fase 2c (60-fase2c), non ancora chiusa a questa stesura.",
 "% Allineato a 60-fase2c/02-verdetto/VERDETTO_2C.md (verifica del 15-11-2026; copia di prima: proposta_sciame_v2.0_prima.tex)."),
("\\item \\textbf{Il «libero» può essere falso:} con il secondo radar a pannello, nella configurazione del sito, 163 passaggi su 171 hanno istanti con «libero» sul drone \\Xv; % 2C (A1 libero col pannello)\ne un edificio che manca dalla mappa apre un «libero» falso se la mappa è dichiarata completa, come fa oggi il prototipo \\Xv.",
 "\\item \\textbf{Il «libero» dipende dalla mappa:} nel sito nessuno di 171 passaggi ha «libero» sul drone, ma solo con la mappa degli ostacoli dichiarata completa, che è un'ipotesi del simulatore; se la mappa è dichiarata e sbagliata, dietro un edificio che vi manca il «libero» è falso (5 casi costruiti su 6) \\Xv. Per questo il prototipo, per impostazione, non dichiara la mappa."),
("\\item \\textbf{Eventi improvvisi:} sono dedotti, entro 2 s in 49 passaggi su 60; la zona dei detriti copre il sito e non si riduce; la fiammata è rilevata con un innesco ottimista. % 2C (E1)",
 "\\item \\textbf{Eventi improvvisi:} sono dedotti, entro 2 s in 51 passaggi su 60; la zona dei detriti è di circa 4,5 km e non si riduce guardando; l'avviso non distingue chi è in pericolo; la fiammata è rilevata con un innesco ottimista. Con le regole attuali sono rimisurati solo drone, collisione, avaria e passaggio ravvicinato; le altre cifre sono delle regole precedenti."),
("e in altri 100 su 100 ripetuti con condizioni nuove. L'avviso",
 "e in altri 100 su 100 ripetuti con condizioni nuove (regole precedenti). Con la mappa del sito dichiarata completa, in nessuno dei 171 passaggi con un drone sopra i 250 g MoVi ha detto «libero» dove il drone era. L'avviso"),
("MoVi deduce l'evento in 1,2–2,2 s (entro 2 s in 49 su 60 [0,70; 0,89]) e non chiama mai «libero» dove possono cadere i frammenti. Ma la zona dei detriti oggi è enorme (oltre 10 km in 36 su 60), non si riduce e non distingue chi è in pericolo \\Xv. % 2C (E1)",
 "MoVi deduce l'evento in 1,2–2,3 s (entro 2 s in 51 su 60 [0,74; 0,92]) e non chiama mai «libero» dove possono cadere i frammenti. La zona dei detriti è di circa 4,5 km (mai oltre 5,3 km in 60 passaggi), ma non si riduce guardando, e l'avviso non distingue chi è in pericolo \\Xv."),
("\\Xv\\ «libero» falso col pannello e con la mappa sbagliata",
 "\\Xv\\ «libero» falso con la mappa sbagliata; 0/171 col pannello solo con la mappa dichiarata"),
("\\Xv\\ entro 2 s solo in 49/60; zona dei detriti troppo larga",
 "\\Xv\\ entro 2 s solo in 51/60; zona dei detriti di km, non si riduce"),
("La prova completa (\\texttt{prova\\_tutto.sh}) termina senza errori in 665 s, e il controllo delle regole dà 0 errori sulle 20 scene \\Sv\\ (stesso codice: non indipendente; il controllo non guarda ancora il «libero» dentro l'avviso). % 2C (scene)",
 "La prova completa (\\texttt{prova\\_tutto.sh}) termina senza errori in 698 s; le 8 scene a lunga portata rifatte con le regole attuali danno 0 errori al controllo delle regole e 0 «libero» dentro l'avviso \\Sv\\ (stesso codice: non indipendente)."),
("Restringere la zona dei detriti; tenere l'avviso sul drone che si ferma; il «libero» col radar a pannello; la mappa non certificata per difetto nel prototipo; il classificatore vero; un sensore a portata maggiore per gli aerei in volo; prove su sensori fisici. % 2C (A1 libero col pannello, E1)",
 "Restringere la zona dei detriti guardando; tenere l'avviso sul drone che si ferma; convalidare la mappa con lo sfondo misurato; rimisurare con le regole attuali le altre scene; il classificatore vero; un sensore a portata maggiore per gli aerei in volo; prove su sensori fisici."),
("\\nota{\\textbf{Come è stato ottenuto.} Uno sciame di agenti specialisti: proposte cieche, falsificazione, misure, attacchi, correzioni e riconti di un arbitro. Calcoli, schede dei sensori, prove e bibliografia nell'allegato tecnico.}",
 "\\nota{\\textbf{Dove sono le prove.} Calcoli, schede dei sensori, prove e bibliografia nell'allegato tecnico.}"),
]
for i,(a,b) in enumerate(S):
    n=t.count(a)
    if n!=1: print('ERRORE',i,n); sys.exit(1)
    t=t.replace(a,b)
p.write_text(t,encoding='utf-8'); print('ok')
