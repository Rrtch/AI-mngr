import socket
import threading
import json
from LVL2 import *

histories = {}

def process(user_id, user_input):
    if user_input.lower() in ["reset", "reiniciar", "adiós", "goodbye", "bye", "exit", "salir"]:
        histories.pop(user_id, None)
    if user_id not in histories:
        histories[user_id] = []
    histories[user_id].append(f"USER: {user_input}")
    prompt = "\n".join(histories[user_id]) + f"\n[INST] {user_input} [/INST]"
    reply = interact(prompt, P3)
    histories[user_id].append(f"AI: {reply}")
    return reply

def handle_client(conn, addr):
    with conn:
        try:
            data = conn.recv(4096).decode()
            msg = json.loads(data)
            user_id = msg.get("from")
            body = msg.get("body")
            reply = process(user_id, body)

            response = {"to": user_id, "reply": reply}
            conn.sendall(json.dumps(response).encode())
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode())

def start_server(host="127.0.0.1", port=5053):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"🐍 Python TCP server escuchando en {host}:{port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
