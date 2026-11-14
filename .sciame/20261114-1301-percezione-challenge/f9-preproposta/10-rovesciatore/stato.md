# Stato — sciame-rovesciatore, f9 (audit delle ipotesi nascoste su S3 + S4, S1, S8)

- 15:38:50 letti contratto, quinto addendum, preproposta per intero, nucleo, verdetto, v0.5, torneo parte 3, audit f5.
- 15:45:06 PREVISIONI.md (P1–P10) scritte prima del simulatore.
- 15:46:55 primo lancio di audit_imm (21 celle) -> risultati_audit_imm_lancio1.txt.
- 15:48:12 P11 e P11b aggiunte (dopo il primo lancio, dichiarato); 15:48:41 secondo lancio (24 celle, le prime 21 identiche) -> risultati_audit_imm.txt.
- 15:49 conti.py -> risultati_conti.txt.
- 15:53 CONSEGNA.md chiusa. Esiti: 13 previsioni, 7 reggono, 6 smentite (P3, P4, P6, P10, P11, P11b).
- Per rifare: gcc -O2 -o audit_imm audit_imm.c -lm && timeout 120 ./audit_imm ; timeout 60 python3 conti.py
