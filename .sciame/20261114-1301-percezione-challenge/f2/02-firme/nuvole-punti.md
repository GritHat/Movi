# Firme di sciame-nuvole-punti (`dfac83300259`) — lette solo le schede `nuvole-punti-1` e `nuvole-punti-2`

`nuvole-punti-1`: si perde: (a) «libero osservato» chiede anche l'assenza di ostacoli nella cella, non solo il suolo visto; (b) «niente odometria» vale solo per lo strato ricalcolato a ogni fotogramma, non per la memoria né per le tracce; (c) i 2 ms sono Python puro su scena sintetica con orientamento fisso.
Enunciato corretto:
A ogni fotogramma ogni cella di una griglia polare egocentrica (1°, 0,1 m, fino alla portata utile) riceve uno di quattro stati: *libero osservato* (suolo visto alla quota attesa E nessun ostacolo), *occupato osservato* (primo ritorno del settore fra 0,07 e 2 m di quota), *in ombra* (oltre il primo ritorno), *non osservato* (fuori campo, nessun ritorno, suolo mancante).
Memoria = ultimo stato con l'età: «libero» scade dopo margine / velocità massima (0,7 m / 1,4 m/s = 0,5 s); «occupato» resta *ricordato* finché non è smentito. Log-odds facoltativa, solo come filtro sull'occupato.
Traccia con posizione prevista in ombra o fuori campo → *prevista* (oltre soglia di covarianza *persa*, segnalata); in *libero osservato* per tre fotogrammi → chiusa.
Lo strato «osservato ora» non usa l'odometria; la memoria va compensata per la rotazione (giroscopio), altrimenti scade; il moto proprio per le tracce non è deciso da questa proposta.
Costo misurato: 2,0 ms a fotogramma in Python puro, un core, scena sintetica, tabelle per pixel a orientamento fisso; con orientamento variabile: non misurato.

`nuvole-punti-2`: si perde: (a) manca che cosa cambia se l'ipotesi sull'hackathon è falsa; (b) «terreno risolto fino a 3 m» è il solo campionamento geometrico, il rumore di profondità è a parte.
Enunciato corretto:
Una sola camera di profondità densa (almeno 240×180; meglio RGB-D stereo 640×480, classe D435, 87°×58°) inclinata verso il basso, con IMU; fuori dal suo campo tutto è «non osservato»; il 360° non si promette.
Se la demo lo vuole, lo aggiunge un LiDAR 2D (LD19: 0,8°, 5–13 Hz, 12 m), che vede i mobili su un piano (8,9 fasci su un pedone a 4 m), non il terreno.
Campionamento del terreno fino a 3 m: impronta 1,8 cm contro 87 cm del ToF 8×8 (conto geometrico, senza rumore); 7 756 pixel sul pedone a 4 m contro 5,4 zone.
Con il rumore, la separazione suolo/ostacolo a 7 cm è attesa fino a circa 3 m (calcolo con ipotesi 0,1 px e base 50 mm: non verificato sul dispositivo).
Se manca l'hardware di profondità (ipotesi sull'hackathon falsa), la stessa griglia si dimostra su registrazioni RGB-D: non verificato.
