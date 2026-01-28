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
    #n_ctx=5124  # Puedes subir más si tu RAM lo permite
)

# Generación en streaming
while True:
    user_input = input()
    #prompt = f"<s>[INST] {user_input} [/INST]</s>" # Formato para modelos instruct
    #prompt = f"[INST] {user_input} [/INST]" # Formato para modelos instruct sin etiquetas de inicio y fin
    prompt = f"[INST] {user_input} [/INST]" #
    if prompt.lower() in ["exit", "quit", "salir"]:
        print("Saliendo...")
        break
    for chunk in llm(prompt, max_tokens=0, stream=True):
        print(chunk["choices"][0]["text"], end="", flush=True)
    print("\n")
   
time_end=time.time()-(time_start)   #calculo del tiempo de finalizacion    
#time_end=Tpss(time_start)          #sacado de FuncionesTime, mismo paso
print("\ntiempo de ejecucion: ",int(time_end))     

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
    #n_ctx=5124  # Puedes subir más si tu RAM lo permite
)

# Prompt (entrada) para el modelo
prompt = "Hola"

# Ejecutar modelo y guardar la respuesta
output = llm(prompt, max_tokens=100)

# Extraer solo el texto generado y limpiarlo
respuesta = output["choices"][0]["text"].strip()

# Mostrar solo la respuesta, sin estadísticas ni logs
print("Respuesta generada:\n")
print(respuesta)

time_end=time.time()-(time_start)   #calculo del tiempo de finalizacion    
#time_end=Tpss(time_start)          #sacado de FuncionesTime, mismo paso
print("tiempo de ejecucion: ",int(time_end))     