"""Esegue un file Python dentro l'editor di Unreal aperto (esecuzione remota di PythonScriptPlugin).
Uso: python3 ue_esegui.py file.py   oppure   python3 ue_esegui.py -c "codice" """
import sys, time
sys.path.insert(0, '/home/fede/UnrealEngine/5.8.4/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python')
import remote_execution as rx
r = rx.RemoteExecution(); r.start(); time.sleep(6.0)
if not r.remote_nodes:
    print('NESSUN EDITOR TROVATO'); r.stop(); sys.exit(1)
r.open_command_connection(r.remote_nodes[0]['node_id'])
if sys.argv[1] == '-c':
    out = r.run_command(sys.argv[2], exec_mode=rx.MODE_EXEC_FILE, unattended=True)
else:
    out = r.run_command(open(sys.argv[1]).read(), exec_mode=rx.MODE_EXEC_FILE, unattended=True)
print('successo:', out.get('success'))
for o in out.get('output', []):
    print(o.get('type'), o.get('output', '').rstrip())
if out.get('result') not in (None, 'None'): print('risultato:', out.get('result'))
r.stop()
