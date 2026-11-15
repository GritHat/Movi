"""MoVi (gruppo SDMs) — prototipo SIMULATO di percezione che dichiara ciò che non ha osservato.

Nessun sensore fisico: i dati sono simulati dalle schede tecniche o presi da archivi pubblici; le etichette di classe
sono assegnate a mano da file (il classificatore è supposto esistente e lasciato ai lavori futuri).
Ambito: osservazione, monitoraggio, ispezione, navigazione sicura e avviso. Nessuna uscita è un comando.

Forma del pacchetto: vedi README.md e ARCHITETTURA.md (f16-prototipo/01-architettura)."""

VERSIONE = "0.3-corto-lungo"

# I tre principi: nessun modulo, interruttore o etichetta li può scavalcare (li controlla registro.valida_riga).
PRINCIPI = (
    "ciò che non è osservato non è mai dichiarato libero",
    "l'avviso di possibile presenza si toglie solo guardando",
    "nessuna etichetta di classe riduce un avviso",
)
