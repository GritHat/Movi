#!/usr/bin/env python3
"""Ultime correzioni, parte 1: dimostrazioni (sigla D-R#). Ogni sostituzione deve trovare il testo una volta sola."""
import pathlib, sys
base = pathlib.Path(__file__).resolve().parent.parent / "capitoli"
n_ok = 0
def sub(f, old, new, tag):
    global n_ok
    p = base / f; s = p.read_text(encoding="utf-8")
    c = s.count(old)
    if c != 1:
        print(f"ERRORE {tag} {f}: {c} occorrenze di: {old[:70]!r}"); sys.exit(1)
    p.write_text(s.replace(old, new), encoding="utf-8"); n_ok += 1

# ---- D-R1 contenimento
sub("05_occlusione.tex",
 r"Sia $\Oss(t)$ l'insieme dei punti del suolo il cui raggio è letto come suolo da un pixel valido del fotogramma $t$ (lettura per punto). Sotto le ipotesi (i), (iv) e (v), a posa esatta ($\varepsilon_p=0$), ogni punto del suolo su cui poggia, al fotogramma $t$, un oggetto più alto del margine di lettura \eqref{eq:map-margine} (punto \emph{occupato}) appartiene a $\Pres(t)$.",
 r"Sia $\Oss(t)$ l'insieme dei punti del suolo il cui raggio, nel fotogramma $t$, è letto da un pixel valido alla profondità attesa del suolo (lettura per punto \emph{esatta}: margine di lettura nullo nella \eqref{eq:map-margine} e tolleranza di misura nulla nella (i)). Sotto le ipotesi (i), (iv) e (v), a posa esatta ($\varepsilon_p=0$), ogni punto interno all'impronta al suolo di un oggetto al fotogramma $t$ (punto \emph{occupato}) appartiene a $\Pres(t)$.", "D-R1a")
sub("05_occlusione.tex",
 r"Con posa nota entro $\varepsilon_p$ (ipotesi (iii)) l'enunciato vale nel riferimento stimato;",
 r"Con posa nota entro $\varepsilon_p$ (ipotesi (iii), intesa come spostamento nel piano del suolo, come nel Lemma~\ref{lem:map-posa}) l'enunciato vale nel riferimento stimato;", "D-R1b")
sub("05_occlusione.tex",
 r"è contenuto nel libero stimato $\hat{\Oss}(t)$ (Lemma~\ref{lem:map-posa}). \prova{D}",
 r"è contenuto nel libero stimato $\hat{\Oss}(t)$. \prova{D}", "D-R1c")
sub("05_occlusione.tex",
 r"Per (i) e (v) il raggio che legge il suolo in un punto è privo di superfici fino al suolo, a meno del margine di lettura, quindi un punto occupato non è letto come suolo: $x\notin\Oss(t)$.",
 r"Per (i) e (v) un raggio letto alla profondità attesa del suolo è privo di superfici fino al suolo; il raggio diretto a un punto interno all'impronta incontra invece l'oggetto prima del suolo, quindi un punto occupato non è letto come suolo: $x\notin\Oss(t)$.", "D-R1d")
sub("05_occlusione.tex",
 r"Per la regola della cella (Definizione~\ref{def:map-libero}) il passo «un punto occupato non è letto come suolo» non è dimostrato: una cella può essere «libero» con meno di metà dell'impronta coperta da un oggetto. La Proposizione è quindi dimostrata per la lettura per punto \prova{D}; con la mappa a celle il contenimento poggia sulla verifica in simulazione del \S\ref{sec:map-banco} \prova{S}.",
 r"Con il margine di lettura $m>0$ della \eqref{eq:map-margine} il passo «un punto occupato non è letto come suolo» cade su una striscia dell'impronta: il raggio diretto a un punto che sta a distanza $\delta$, in pianta, dietro la faccia vista dell'oggetto incontra la faccia alla profondità $z_0\,(1-\delta/\rho)$ e, se $\delta\le\rho\,m(z_0)/z_0$, è letto come suolo, qualunque sia l'altezza dell'oggetto (sull'asse del campo, con $k=0{,}004$: $11\unita{cm}$ a $2{,}5\unita{m}$ e $14\unita{cm}$ a $3\unita{m}$ \prova{C}). Nemmeno per la regola della cella (Definizione~\ref{def:map-libero}) il passo è dimostrato: una cella può essere «libero» con meno di metà dell'impronta coperta da un oggetto. La Proposizione è quindi dimostrata per la lettura per punto esatta \prova{D}; con il margine di lettura e con la mappa a celle il contenimento dell'intera impronta non è dimostrato e poggia sulla verifica in simulazione del \S\ref{sec:map-banco} \prova{S}.", "D-R1e")
sub("01_introduzione.tex",
 r"suolo piano; lettura per punto; velocità al più $\vmax$ & proposizioni; con la mappa a celle il contenimento poggia sulla simulazione",
 r"suolo piano; lettura per punto esatta (margine di lettura nullo); velocità al più $\vmax$ & proposizioni; con il margine di lettura e con la mappa a celle il contenimento poggia sulla simulazione", "D-R1f")
sub("09_conclusioni.tex",
 r"su suolo piano e con la lettura per punto; con la mappa a celle il contenimento poggia sulla verifica in simulazione \prova{S}.",
 r"su suolo piano e con la lettura per punto esatta, senza margine di lettura; con il margine e con la mappa a celle il contenimento poggia sulla verifica in simulazione \prova{S}.", "D-R1g")

# ---- D-R2 fascia
sub("05_occlusione.tex",
 r"un soggetto fuori dall'ombra, in campo e in portata, è rilevato entro un tempo $t_a$.",
 r"un soggetto che è fuori dall'ombra, in campo e in portata da un tempo $t_a$ è riportato come osservato.", "D-R2a")
sub("05_occlusione.tex",
 r"Sotto le ipotesi (ii) e (iv), se" + "\n" + r"\begin{equation}\label{eq:occ-fascia}",
 r"Sotto le ipotesi (ii) e (iv), con la (ii) riferita al centro del soggetto ($c\notin\Omb$), se" + "\n" + r"\begin{equation}\label{eq:occ-fascia}", "D-R2b")
sub("05_occlusione.tex",
 r"Per contenere l'intero corpo di raggio $r_c$ si aggiunge $r_c$ al secondo membro. \prova{D}",
 r"Per contenere l'intero corpo di raggio $r_c$ si aggiunge $r_c$ al secondo membro; se la (ii) vale solo quando tutto il corpo è fuori dall'ombra, se ne aggiunge un altro. \prova{D}", "D-R2c")
sub("05_occlusione.tex",
 r"nel quale il soggetto non è rilevato. Poiché il soggetto è nel campo e in portata in tutto $[t-t_a,t]$ e non è rilevato in $t$, per (ii) esiste $t'\in[t-t_a,t]$ con $c(t')\in\Omb$: altrimenti sarebbe fuori dall'ombra da più di $t_a$ e sarebbe rilevato.",
 r"che non lo riporta come osservato. Poiché il soggetto è nel campo e in portata in tutto $[t-t_a,t]$ e non è riportato come osservato in $t$, per (ii) esiste $t'\in[t-t_a,t]$ con $c(t')\in\Omb$: altrimenti il centro sarebbe fuori dall'ombra da un tempo $t_a$ e il soggetto sarebbe riportato come osservato.", "D-R2d")
sub("05_occlusione.tex",
 r"e $t_a=0{,}133\unita{s}$ (due cicli) è un valore assunto \prova{N}.",
 r"e $t_a=0{,}133\unita{s}$ (due cicli) è un valore assunto \prova{N}: con $P_D<1$ nessun tempo finito è un limite certo, e la (ii) è un'idealizzazione (\S\ref{sec:sti-porta}).", "D-R2e")
sub("05_occlusione.tex",
 r"si allontana dall'ombra alla velocità massima senza essere rilevato per tutto il tempo $t_a$.",
 r"si allontana dall'ombra alla velocità massima senza essere riportato come osservato per tutto il tempo $t_a$.", "D-R2f")

# ---- D-R3 t_a nei simboli e in appendice
sub("00_simboli.tex", r"$t_a$ & età del dato più vecchio usato da un'uscita\\",
 r"$t_a$ & tempo entro cui un soggetto fuori dall'ombra, in campo e in portata, è riportato come osservato\\", "D-R3a")
sub("00_simboli.tex", r"allargamento dell'ombra che copre l'età del dato, la latenza e l'errore del bordo",
 r"allargamento dell'ombra che copre il tempo $t_a$, la latenza, la tenuta di un ciclo e l'errore del bordo", "D-R3b")
sub("A_parametri.tex", r"con età $0{,}133\unita{s}$,", r"con $t_a=0{,}133\unita{s}$ (assunto),", "D-R3c")

# ---- D-R4 zero di «fuori da W»
sub("06_valutazione.tex",
 r"Lo zero della prima riga è dimostrato solo nelle ipotesi della Proposizione~\ref{prop:occ-fascia} (bordo dell'ombra esatto, ingresso riconosciuto, un solo soggetto per ombra, ostacolo fermo); altrove è un conteggio.",
 r"Lo zero della prima riga vale per costruzione dove l'ingresso è riconosciuto, l'ostacolo è fermo e l'ombra stimata coincide con la vera: allora $W=\dilata(\hat\Omb,w)\supseteq\Omb$ (Definizione~\ref{def:occ-avviso}) e il centro di un soggetto nascosto sta in $\Omb$; altrove è un conteggio. Non discende dalla Proposizione~\ref{prop:occ-fascia}, che riguarda il soggetto uscito dall'ombra e la cui condizione copre $1{,}13\unita{m/s}$, meno delle velocità d'ingresso di queste prove (fino a $1{,}8\unita{m/s}$).", "D-R4")

# ---- D-R5 etichetta
sub("05_occlusione.tex", r"i rilasci con etichette sono un sottoinsieme di quelli senza. \prova{D}",
 r"l'insieme di rilascio $L(t)$ con etichette è contenuto in quello senza. \prova{D}", "D-R5a")
FRASE = r"Un'etichetta non produce un «libero» né riduce un avviso acceso; può cambiare l'esito di un riaggancio, e quindi gli ingressi successivi (\S\ref{sec:occ-classe})."
sub("04_stima.tex", r"La sicurezza delle indicazioni non dipende dall'etichetta (\S\ref{sec:occ}).", FRASE, "D-R5b")
sub("09_conclusioni.tex", r"(0 riduzioni dell'avviso su $20\,000$ sequenze di etichette, due volte). La sicurezza delle indicazioni non dipende dall'etichetta.",
 r"(0 riduzioni dell'avviso su $20\,000$ sequenze di etichette, due volte). " + FRASE, "D-R5c")
sub("01_introduzione.tex", r"Nessuna classe diversa da «persona» è stata simulata nella catena completa. La sicurezza delle indicazioni non dipende dall'etichetta.",
 r"Nessuna classe diversa da «persona» è stata simulata nella catena completa. " + FRASE, "D-R5d")
sub("08_limiti.tex", r"La sicurezza delle indicazioni non dipende dall'etichetta (invarianti 5 e 15).",
 r"Un'etichetta non produce un «libero» e non toglie né restringe un avviso acceso (invarianti 5 e 15); può cambiare l'esito di un riaggancio, e quindi gli ingressi successivi (\S\ref{sec:occ-classe}).", "D-R5e")
sub("04_stima.tex", r"non entra nel costo d'associazione né nella porta;",
 r"non entra nel costo d'associazione né nella porta di validazione; entra, attraverso la forma della regione di previsione, nella porta del riaggancio (\S\ref{sec:occ-classe});", "D-R5f")
sub("08_limiti.tex", r"celle «libero» e distanze identiche; avviso con etichette non più stretto;",
 r"celle «libero» e distanze identiche; per ogni ingresso riconosciuto in entrambe le esecuzioni, avviso con etichette non più stretto;", "D-R5g")

# ---- D-R6 regione di ripiego
sub("05_occlusione.tex",
 r"se questo insieme è vuoto, $\Reg_\alpha(t)=W(t)\setminus\Oss(t)$, cioè tutto il non visto libero dell'ombra e della sua fascia (\emph{regione di ripiego}), con lo stato «previsto ampio».",
 r"se questo insieme è vuoto, e in ogni altro caso di «previsto ampio», $\Reg_\alpha(t)=\bigl(\hat\Omb(t)\setminus\Oss(t)\bigr)\cap W(t)$, cioè tutto il non visto libero dell'ombra (\emph{regione di ripiego}).", "D-R6a")
sub("05_occlusione.tex",
 r"con l'ostacolo fermo, $\hat\Omb\subseteq W(t_0)=W(t)$; quindi $W(t)\setminus\Oss(t)\supseteq\hat\Omb\neq\emptyset$.",
 r"con l'ostacolo fermo e l'ombra stimata costante, $\hat\Omb\subseteq W(t_0)=W(t)$; quindi la regione di ripiego è $\hat\Omb\neq\emptyset$, e negli altri casi $C_\alpha(t)\cap W(t)\neq\emptyset$.", "D-R6b")

# ---- D-R7 riquadro del cap. 3
sub("03_mappa.tex",
 r"parte (b) dimostrata nel modello; regola della cella verificata in simulazione, con modello ideale del sensore, su 300 condizioni dichiarate.",
 r"parte (b) dimostrata nel modello a posa esatta; regola della cella, e tenuta con errore d'inclinazione entro $0{,}5^\circ$, verificate in simulazione, con modello ideale del sensore, su 300 condizioni dichiarate, non dimostrate.", "D-R7")

# ---- D-R8 + C-R9 conclusioni, fascia
sub("09_conclusioni.tex",
 r"La fascia di guardia $w$ contiene il soggetto se vale la condizione~\eqref{eq:occ-fascia}, l'ostacolo è fermo e il soggetto resta nel campo e in portata; con $w=0{,}40\unita{m}$ la velocità coperta, per calcolo, è $1{,}13\unita{m/s}$, e $0{,}56\unita{m/s}$ se il bordo dell'ombra sbaglia di $0{,}20\unita{m}$ (Proposizione~\ref{prop:occ-fascia}) \prova{C}.",
 r"La fascia di guardia $w$ contiene il centro del soggetto se vale la condizione~\eqref{eq:occ-fascia}, l'ostacolo è fermo, il soggetto resta nel campo e in portata ed è riportato come osservato entro $t_a$ da quando il suo centro è fuori dall'ombra; con $w=0{,}40\unita{m}$ la velocità coperta, per calcolo, è $1{,}13\unita{m/s}$, e $0{,}56\unita{m/s}$ se il bordo dell'ombra sbaglia di $0{,}20\unita{m}$; per l'intero corpo, di raggio $r_c$, la condizione chiede $r_c$ in più (Proposizione~\ref{prop:occ-fascia}) \prova{C}.", "D-R8/C-R9a")
sub("01_introduzione.tex", r"ostacolo fermo & copre $\vmax=1{,}13\unita{m/s}$;", r"ostacolo fermo & copre, per il centro del soggetto, $\vmax=1{,}13\unita{m/s}$;", "C-R9b")
sub("08_limiti.tex", r"e tenuta di un ciclo $0{,}067\unita{s}$: $0{,}40/0{,}355=1{,}13\unita{m/s}$;", r"e tenuta di un ciclo $0{,}067\unita{s}$, per il centro del soggetto: $0{,}40/0{,}355=1{,}13\unita{m/s}$;", "C-R9c")

# ---- D-R9 tabella di sintesi, prima riga
sub("01_introduzione.tex", r"regola di scrittura unica; per l'inverso: profondità valida corretta,",
 r"regola di scrittura unica; per l'inverso, limitato ai raggi dei pixel che leggono il suolo e a meno del margine di lettura: profondità valida corretta,", "D-R9")
print("parte 1: sostituzioni applicate", n_ok)
