# Toglie dai blocchi del §1 le righe «Incorpora:» (la stessa mappa sta, riga per riga, in TABELLA_CORREZIONI.md)
# e scrive nel §0 lo scostamento di lunghezza. Uso: python -I accorcia.py
import re
p = 'SOLUZIONE_V3.md'; s = open(p, encoding='utf-8').read()
n0 = len(s.split())
s, k = re.subn(r"\n?[ ]?\*\*Incorpora:\*\*[^\n]*", "", s)
a = "| «Libero» ricordato; `stato(centro)`;"; assert s.count(a) == 1
s = s.replace(a, "| «Libero» ricordato (anche su una cella che era occupata: F-407); `stato(centro)`;")
a = "**Regole violate:** nessuna che io sappia (niente git, sudo, rete; scritture solo in `20-finale/`)."
assert s.count(a) == 1
s = s.replace(a, "**Regola violata: la lunghezza.** La consegna chiede al più dodici pagine fitte. Impaginato (`pandoc` con XeLaTeX, A4): @P10@ pagine a corpo 10 con margini di 2 cm, @P8@ a corpo 8 con margini di 1,5 cm; la prima stesura, a corpo 10, ne faceva 12. Il documento è cresciuto perché ha assorbito quattro critiche, tre prove, la controprova e le discordanze senza perdere ciò che c'era, e la controprova è arrivata a stesura finita. Non ho tagliato regole né limiti per rientrare. **Che cosa si taglia per primo, se serve:** i §8 e §9 (stanno anche in `TABELLA_CORREZIONI.md`, §9–§15); le cifre secondarie dei paragrafi «Stato» del §1; la tabella R1–R8. Per chi costruisce bastano i riquadri di codice del §1, il §2 e il §11. Nei blocchi del §1 non ripeto l'elenco delle correzioni incorporate: sta, riga per riga, nella tabella. **Altre regole violate:** nessuna che io sappia (niente git, sudo, rete; scritture solo in `20-finale/`; ho usato la cartella temporanea della sessione per i PDF di prova).")
open(p, 'w', encoding='utf-8').write(s)
print('righe Incorpora tolte:', k, '| parole', n0, '->', len(s.split()))
