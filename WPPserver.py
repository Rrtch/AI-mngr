from flask import Flask, request, jsonify
from flask_cors import CORS
from LVL2 import *

app = Flask(__name__)
CORS(app)  # permite que el HTML pueda llamar desde navegador

@app.route("/msg", methods=["POST"])
def receive_msg():
    data = request.get_json()
    user_msg = data.get("message", "")
    #resp= ObltrtNOapt(user_msg)
    resp=interact(user_msg)
    print("Python recibió:", user_msg, "y responde:", resp)
    return jsonify({"reply": f"AI local server: {resp}"})
    

if __name__ == "__main__":
    app.run(port=5000)
