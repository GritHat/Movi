# Firme di sciame-lidar (f2)

Lette solo le schede `lidar-1` e `lidar-2` (righe 20–32 di `f2/01-traduzione/SCHEDE.md`).

`lidar-1`: si perde: l'enunciato è fedele, ma nei rischi due numeri sono attribuiti alla camera sbagliata. «Nero a portata dimezzata» è il dato del LiDAR 2D RPLIDAR C1 (12 m al 70 %, 6 m al 10 %), non della camera stereo: per la stereo l'effetto del nero non è quantificato (non verificato; lo misura P10). «330–417 $» vale per Gemini 335 e D455; la D435i l'ho letta fra 362 e 550 $. Manca anche che un buco nella profondità è «nessun dato», mai «libero».
Versione corretta:
Un solo sensore frontale: camera stereo attiva con IMU (D455, D435i, Gemini 335, o quella già posseduta), circa 87°×58°, 30 fps. Fuori campo è «sconosciuto» per costruzione; i 360° si dichiarano come limite. 42–56 pixel su una persona a 4 m contro 1,3 zone di un ToF 8×8; un cavo USB, nessuna interferenza, nessuna calibrazione estrinseca.
Rischi: niente retro; portata utile 3–6 m; il vetro non compare e una griglia a lancio di raggi segna «libero» una porta; un buco è «nessun dato», mai «libero»; sul nero la resa cala di una quantità non verificata per la stereo (da misurare con P10); sole pieno non verificato; 330–550 $ secondo il modello.

`lidar-2`: fedele
