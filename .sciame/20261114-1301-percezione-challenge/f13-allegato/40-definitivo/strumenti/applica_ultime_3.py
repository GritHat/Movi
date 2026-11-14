#!/usr/bin/env python3
"""Ultime correzioni, parte 3: accorcia i testi introdotti dalle parti 1 e 2 (stesso contenuto, meno parole) e
lascia flottare due tabelle che lasciavano mezza pagina bianca. Prima controlla tutto, poi scrive."""
import pathlib, sys
base = pathlib.Path(__file__).resolve().parent.parent / "capitoli"
E = []
def sub(f, old, new, tag): E.append((f, old, new, tag))
sub("06_valutazione.tex",
 r"sottostima i pixel senza dato. Fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$, nei primi 60 fotogrammi, i pixel senza dato sono 1,7\,\% al livello nominale e 7,8\,\% al livello limite, contro 24,1\,\% in una sequenza al chiuso con una persona \cite{depthtrack} e 34,4\,\% in una registrazione di esempio del costruttore di una delle camere; una registrazione con un sensore a luce strutturata \cite{tum-rgbd} dà 6,3\,\%. Camere, risoluzioni e scene non sono quelle simulate: il confronto dà il verso dello scarto, non la sua misura.",
 r"sottostima i pixel senza dato: fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$, 1,7\,\% al livello nominale e 7,8\,\% al livello limite, contro 24,1\,\% (una sequenza al chiuso con una persona \cite{depthtrack}) e 34,4\,\% (una registrazione di esempio del costruttore di una delle camere); una registrazione con un sensore a luce strutturata \cite{tum-rgbd} dà 6,3\,\%. Camere, risoluzioni e scene non sono quelle simulate: il confronto dà il verso dello scarto, non la misura.", "N-R4 cap6 breve")
sub("08_limiti.tex",
 r"contro $24{,}1\,\%$ e $34{,}4\,\%$ in due registrazioni pubbliche di camere a stereo attivo, fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$ \prova{P}; \S\ref{sec:val})",
 r"contro $24{,}1\,\%$ e $34{,}4\,\%$ in due registrazioni pubbliche di camere a stereo attivo \prova{P}; \S\ref{sec:val})", "N-R4 cap8 breve")
sub("01_introduzione.tex",
 r"(fra i pixel in cui la scena sta fra $0{,}5$ e $3\unita{m}$: $7{,}8\,\%$ al livello di rumore più alto, contro $24{,}1\,\%$ e $34{,}4\,\%$; camere, risoluzioni e scene diverse da quelle simulate)",
 r"($7{,}8\,\%$ al livello di rumore più alto, contro $24{,}1\,\%$ e $34{,}4\,\%$; camere e scene diverse da quelle simulate, \S\ref{sec:val})", "N-R4 cap1 breve")
sub("08_limiti.tex",
 r"la prova si esegue nella configurazione che si vuole attivare, con i gruppi a celle forti (\S\ref{sec:sti-mobile}): con i gruppi per componenti connesse della configurazione di riferimento, su profondità simulata dalle schede tecniche, sul suolo vuoto nascono 137 e 206 tracce confermate in 9 sequenze, e la prova non sarebbe superata \prova{S}.",
 r"la prova si esegue con i gruppi a celle forti (\S\ref{sec:sti-mobile}): con quelli della configurazione di riferimento, su profondità simulata dalle schede tecniche, nascono 137 e 206 tracce confermate in 9 sequenze e la prova non sarebbe superata \prova{S}.", "C-R2 breve")
sub("08_limiti.tex",
 r"È una grandezza diversa dalla velocità coperta dalla fascia di guardia ($1{,}13\unita{m/s}$, \S\ref{sec:lim-validita}), che il passo normale supera: a $1{,}4\unita{m/s}$ l'avviso è tempestivo per calcolo, ma il contenimento nella fascia non è dimostrato (\S\ref{sec:occ}).",
 r"Non è la velocità coperta dalla fascia di guardia ($1{,}13\unita{m/s}$, \S\ref{sec:lim-validita}), che il passo normale supera: a $1{,}4\unita{m/s}$ il contenimento nella fascia non è dimostrato.", "C-R8 breve")
sub("09_conclusioni.tex",
 r"su $23\,402$ passaggi nascosti, da 6000 soggetti distinti (3 disposizioni, $P_D=0{,}9$ e $0{,}7$, corpo esteso e puntiforme); la premessa",
 r"su $23\,402$ passaggi nascosti, da 6000 soggetti distinti; la premessa", "N-R6 cap9 breve")
sub("01_introduzione.tex",
 r"I gruppi a celle forti, le condizioni aggiuntive del riaggancio e l'avviso per le tracce chiuse vicino a un'ombra non fanno parte della configurazione di riferimento: si attivano all'avvio solo se le prove d'ingresso del \S\ref{sec:lim-salute} sono superate.",
 r"I gruppi a celle forti, le condizioni aggiuntive del riaggancio e l'avviso per le tracce chiuse vicino a un'ombra si attivano all'avvio solo se le prove d'ingresso del \S\ref{sec:lim-salute} sono superate.", "C-R15a breve")
sub("01_introduzione.tex",
 r"La premessa manca in 928 passaggi ($3{,}97\,\%$; 852 con $P_D=0{,}7$), nei quali non c'è regione: la soglia 0 della Tabella~\ref{tab:intro-requisiti} è rispettata solo fra i passaggi con l'ingresso riconosciuto. Con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra, regola attiva solo dopo la prova d'ingresso sul suolo vuoto, restano senza avviso 24 passaggi ($0{,}10\,\%$).",
 r"La premessa manca in 928 passaggi ($3{,}97\,\%$; 852 con $P_D=0{,}7$), senza regione: la soglia 0 della Tabella~\ref{tab:intro-requisiti} è rispettata solo dove l'ingresso è riconosciuto. Con l'avviso acceso anche per le tracce chiuse entro $0{,}75\unita{m}$ da un'ombra (regola attiva solo dopo la prova d'ingresso sul suolo vuoto) restano senza avviso 24 passaggi ($0{,}10\,\%$).", "N-R6 cap1 breve")
# tabelle che lasciavano mezza pagina bianca: da [H] a [!htb]
sub("05_occlusione.tex", "\\begin{table}[H]\\centering\\footnotesize\n\\caption{Quota di istanti con il soggetto dentro", "\\begin{table}[!htb]\\centering\\footnotesize\n\\caption{Quota di istanti con il soggetto dentro", "impaginazione tab. dominio")
sub("06_valutazione.tex", "\\begin{table}[H]\\centering\\footnotesize\n\\caption{Etichetta «in movimento», ostacoli fermi, tracce spurie.", "\\begin{table}[!htb]\\centering\\footnotesize\n\\caption{Etichetta «in movimento», ostacoli fermi, tracce spurie.", "impaginazione tab. mobili")
bad = 0
for f, old, new, tag in E:
    c = (base / f).read_text(encoding="utf-8").count(old)
    if c != 1:
        print(f"ERRORE {tag} {f}: {c} occorrenze di: {old[:80]!r}"); bad += 1
if bad: sys.exit(1)
for f, old, new, tag in E:
    p = base / f; s = p.read_text(encoding="utf-8"); p.write_text(s.replace(old, new), encoding="utf-8")
print("parte 3: sostituzioni applicate", len(E))
