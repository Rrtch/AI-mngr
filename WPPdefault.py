from LVL2 import *  
import socket
import threading
import json
from multiprocessing import Process, Queue

print(BLU+"WPPclean.py in"+RES)

HOST = "127.0.0.1"
PORT = 5050

# Historial por usuario: { user_id: ["USER: ...", "AI: ...", ...] }
histories = {}

# Jobs activos por usuario: { user_id: (proc, queue) }
active_jobs = {}

# Comandos para resetear historial
RESET_COMMANDS = {"reset", "reiniciar", "adiós", "goodbye", "bye", "exit", "salir"}

#A3.load_model()

def generate(H,ID,qst, queue):
    """
    Ejecuta la inferencia (en un proceso hijo).
    Recibe el prompt ya construido (string) y devuelve la respuesta por queue.
    """
    try:
        #reply = DRCteract(qst,H,ID)
        reply = A3.Histeract(qst,H)
        queue.put({"reply": reply})
    except Exception as e:
        queue.put({"error": str(e)})


def handle_client(conn, addr):
    """
    Maneja una conexión entrante desde Node.
    Lee el JSON entrante, actualiza historial, cancela proceso viejo si existe,
    arranca un nuevo proceso con el prompt (pasado como string), espera la respuesta
    y la envía por la misma conexión antes de cerrarla.
    """
    try:
        raw = conn.recv(8192).decode()
        if not raw:
            return

        # Por seguridad, strip y parse
        raw = raw.strip()
        print(BLU+"FROM"+RES, raw)

        try:
            data = json.loads(raw)
        except Exception as e:
            err = {"error": f"JSON parse error: {e}"}
            conn.sendall((json.dumps(err) + "\n").encode())
            print("❌ JSON parse error:", e)
            return

        user_id = data.get("from")
        body = data.get("body", "")

        if not user_id:
            err = {"error": "Missing 'from' field"}
            conn.sendall((json.dumps(err) + "\n").encode())
            print("❌ Missing 'from' in payload")
            return

        # Manejar comando de reset: si es reset, borrar historial y cancelar job activo
        if body.strip().lower() in RESET_COMMANDS:
            histories.pop(user_id, None)
            # cancelar job si existe
            if user_id in active_jobs:
                old_proc, old_q = active_jobs.pop(user_id)
                try:
                    if old_proc.is_alive():
                        old_proc.join(timeout=2)
                        print(f"⚠️ Job viejo cancelado por reset para {user_id}")
                        old_proc.terminate()
                except Exception as e:
                    print("⚠️ Error cancelando job viejo en reset:", e)

            # responder confirmación de reset
            resp = {"to": user_id, "reply": "Historial reiniciado."}
            conn.sendall((json.dumps(resp) + "\n").encode())
            print(BLU+"RESET"+RES, resp)
            return

        # Asegurar historial inicial
        if user_id not in histories:
            histories[user_id] = []

        # Añadir mensaje del usuario al historial (persistente)
        histories[user_id].append(f"USER: {body}")

        # Construir prompt final que se pasará al proceso hijo
        # (Usamos el historial acumulado + final instruction con el mismo body)
        #prompt = "\n".join(histories[user_id]) + f"\n[INST] {body} [/INST]"

        # Si hay un job activo para este usuario, terminarlo (sin borrar historial)
        if user_id in active_jobs:
            old_proc, old_q = active_jobs.pop(user_id)
            try:
                if old_proc.is_alive():
                    old_proc.terminate()
                    old_proc.join(timeout=2)
                    print(f"⚠️ Job viejo cancelado para {user_id}")
            except Exception as e:
                print("⚠️ Error cancelando job viejo:", e)

        # Preparar nueva cola y proceso
        q = Queue()
        proc = Process(target=generate, args=(histories[user_id],user_id,body,q))
        #proc = Process(target=generate, args=(prompt, q))
        proc.start()

        # Guardar job activo
        active_jobs[user_id] = (proc, q)

        # Esperar la respuesta final del proceso (bloqueante aquí, por conexión TCP)
        result = q.get()  # {'reply': '...'} o {'error': '...'}
        # Limpieza del job activo (si corresponde)
        try:
            stored = active_jobs.get(user_id)
            if stored and stored[0] is proc:
                active_jobs.pop(user_id, None)
        except Exception:
            pass

        # Si hubo error en el proceso hijo, enviar error
        if "error" in result:
            resp = {"to": user_id, "error": result["error"]}
            try:
                conn.sendall((json.dumps(resp) + "\n").encode())
            except Exception as e:
                print(RED+"❌ Error enviando error a Node:"+RES, e)
            print(RED+"❌ Error en proceso hijo:"+RES, result["error"])
            return

        # Respuesta final OK: añadirla al historial y enviar al socket
        reply_text = result.get("reply", "")
        histories[user_id].append(f"AI: {reply_text}")

        resp = {"to": user_id, "reply": reply_text}
        try:
            conn.sendall((json.dumps(resp) + "\n").encode())
            print(BLU+"PARA"+RES, user_id)
        except Exception as e:
            print(RED+"❌ Error enviando a Node:"+RES, e)

    except Exception as e:
        # Manejo general de errores
        try:
            conn.sendall((json.dumps({"error": str(e)}) + "\n").encode())
        except:
            pass
        print("❌ Error en handle_client:", e)
    finally:
        try:
            conn.close()
        except:
            pass


def start_server(host=HOST, port=PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reusar puerto rápido si se reinicia (útil en dev)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(BLU+"🐍 Python TCP server escuchando en "+RES+f"{host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            # Cada conexión la maneja un thread (que a su vez lanza el proceso hijo)
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
