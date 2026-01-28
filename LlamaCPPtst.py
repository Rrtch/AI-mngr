# LlamaCPPtst.py - Interactive chat test script using LlamaCPP with Mistral-7B.
# Features conversation history, streaming output, and execution time tracking.

from llama_cpp import Llama

#para cronometrar
from FuncionesTime import *
time_start = time.time()

# Ruta al modelo GGUF — asegúrate de que termine en el archivo correcto
model_path="C:/Users/casti/.lmstudio/models/lmstudio-community/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"  # Carga el modelo solo 1 vez

# Cargar el modelo s
llm = Llama(
    model_path=model_path,
    verbose=False, # Desactivar logs detallados
    n_ctx=5124  # Puedes subir más si tu RAM lo permite
)

# Historial de conversación (lista de strings)
historial = []

system_prompt = (                           #traduccion
    "あなたは役立つアシスタントです。"          #Eres un asistente útil.
    "短く自然な日本語で会話してください。"      #Habla en japonés breve y natural.
    "繰り返しや冗長な表現は避けてください。"    #Evita repeticiones y expresiones redundantes.    
)

# Añadir el system prompt al historial como la primera instrucción
historial.append(f"[INST] {system_prompt} [/INST]")

# Prompt (entrada) para el modelo
def armar_prompt(historial, user_input):
    """Construye el prompt concatenando el historial con la nueva entrada"""
    # Conversación previa + nueva entrada
    prompt = "".join(historial) + f"[INST] {user_input} [/INST]"
    return prompt

# Generación en streaming
while True:
    user_input = input()
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("Saliendo...")
        break
    prompt = armar_prompt(historial, user_input)
    respuesta = ""
    for chunk in llm(prompt, max_tokens=0, stream=True):
        token = chunk["choices"][0]["text"]
        print(token, end="", flush=True)
        respuesta += token
    print("")
    historial.append(f"[INST] {user_input} [/INST]{respuesta}")
   
time_end=time.time()-(time_start)   #calculo del tiempo de finalizacion    
#time_end=Tpss(time_start)          #sacado de FuncionesTime, mismo paso
print("\ntiempo de ejecucion: ",int(time_end))    