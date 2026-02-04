# WPflskCLEAN.py - Flask HTTP server for WhatsApp AI integration.
# Uses message queue for async processing and sends responses via HTTP callback.
# Integrates with Node.js WhatsApp bridge at localhost:3000.

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import queue, threading
from LVL2 import *   # ya lo tienes ahí

app = Flask(__name__)
CORS(app)

# memoria por usuario
histories = {}

# cola de mensajes
msg_queue = queue.Queue()

# worker que procesa la cola
def worker():
    while True:
        user_id, user_input = msg_queue.get()
        
        try:
            # ✅ detectar comandos de reinicio
            if user_input.lower() in ["reset", "reiniciar", "adiós", "goodbye", "bye", "exit", "salir"]:
                histories.pop(user_id, None)  # borra historial si existe
                print(f"🔄 Historial de {user_id} reiniciado.")
            # inicializa historial si es nuevo usuario
            if user_id not in histories:    
                histories[user_id] = []    
            #guarda la peticion en el historial
            histories[user_id].append(f"USER: {user_input}")
            #construye el prompt
            prompt = "\n".join(histories[user_id]) + f"\n[INST] {user_input} [/INST]"
            # genera respuesta con el modelo
            reply = DRCteract(prompt)
            # guarda la respuesta en el historial
            histories[user_id].append(f"AI: {reply}")
            
            #print("Historial de", user_id)
            #print("\n".join(histories[user_id]))

            # Enviar respuesta a WhatsApp a través del Node.js bridge
            try:
                r =  requests.post(           # ✅ mandar la respuesta de vuelta exactamente como Node la espera
                "http://127.0.0.1:3000/send",
                json={
                    "to": user_id,   # asegúrate que user_id tenga @c.us o @g.us
                    "message": reply
                },
                timeout=10
                )
                
                if r.ok:
                    print(f"📤 Respuesta enviada a {user_id}" )
                    print("{reply}")
                else:
                    print(f"⚠️ Error al enviar a WhatsApp: {r.text}")
            except Exception as e:
                print("❌ Error en request a Node.js:", e)

        except Exception as e:
            print(" Error en worker:", e)
        finally:
            msg_queue.task_done()

# arrancar el worker en background
threading.Thread(target=worker, daemon=True).start()


# endpoint limpio
@app.route("/msg", methods=["POST"])
def receive_msg():
    data = request.get_json()
    user_id = get_user_id(data)
    user_input = data.get("body", "")

    msg_queue.put((user_id, user_input))
    #print("📥 Recibido:", data)
    #print("➡️ user_id usado:", user_id)
    # responde rápido, no se queda esperando el modelo
    print("\033[34mPython recibió:\033[0m", user_input, "\033[34m. . . procesando . . .\033[0m")
    return jsonify({"status": "ok", "message": "Recibido, procesando...","reply": "..."})
if __name__ == "__main__":
    app.run(port=5000)
