# Dimostrazione 3D di MoVi in Unreal Engine 5.8

Scena «scorta»: un drone porta MoVi e segue un drone più avanti. Accanto, due droni collidono: lampo, fumo, detriti
mossi dal motore fisico (Chaos). Radar e camera simulati vengono accecati. MoVi tiene la regione del bersaglio con
la confidenza che cala, avvisa subito, poi riprende il bersaglio. Il tempo rallenta all'urto, con la scala a schermo.
Tutto è simulato: nessun sensore fisico.

| File | Che cosa fa |
|---|---|
| `movi_core.py` | nucleo MoVi in Python puro (porto compatto delle regole del prototipo: Kalman, regione al 90 %, confidenza, avviso) |
| `movi_scena.py` | costruisce il livello nell'editor: droni, cielo, detriti, fumo, zone di MoVi |
| `movi_demo.py` | avvia la simulazione e collega la scena al nucleo a ogni passo |
| `init_unreal.py` | da copiare in `<progetto>/Content/Python/`: apre la «cassetta» per eseguire script nell'editor aperto |
| `ue.sh` | `sh ue.sh file.py`: esegue un file nell'editor tramite la cassetta |

## Uso

1. Progetto Unreal 5.8 con il plugin «Python Editor Script Plugin» attivo; copiare `init_unreal.py` in
   `<progetto>/Content/Python/` (correggere il percorso `D` se la cartella è diversa) e aprire l'editor.
2. `sh ue.sh movi_scena.py` costruisce la scena.
3. `sh ue.sh movi_demo.py` avvia la dimostrazione (circa 25 s). Per salvare i fotogrammi: impostare `FOTO` in `movi_demo.py`.

## Server MCP (unreal-mcp)

Il plugin `UnrealMCP` non compilava con Unreal 5.8 per due costrutti non più accettati:
`FindObject<UClass>(ANY_PACKAGE, …)` va sostituito con `FindFirstObject<UClass>(…)`, e il ciclo sui parametri JSON va
scritto con `const auto&`. Dopo la correzione il plugin compila e ascolta su `127.0.0.1:55557`.
In Claude Code il server si registra con:

    claude mcp add unrealMCP -s user -- uv --directory /percorso/unreal-mcp/Python run unreal_mcp_server.py
