# intento limpio.py - LlamaCPP inference test with GPU layer offloading.
# Tests Mistral-7B GGUF model with n_gpu_layers for CUDA acceleration.
# Interactive chat loop with basic prompt-response functionality.

import gc
from llama_cpp import Llama
import os
os.add_dll_directory(r"C:\Users\casti\llama.cpp\build\bin\Release")
gc.collect()

llm = Llama(
    model_path="D:/APPS/Models/mistral7bv0.2.Q3.gguf",  
    verbose=True, # Desactivar logs detallados
    n_ctx=5124,  # Puedes subir más si tu RAM lo permite
    n_gpu_layers=100,  # usa tu GPU
)

def ephemer(prompt):
    output = llm(f"[INST] {prompt} [/INST]",max_tokens=0)
    resp = output["choices"][0]["text"]
    print("ephemer responce: ",resp)
    return resp

while True:
    user_input = input("Tu: ")
    if user_input.lower() in ["salir", "exit", "bye"]:
        print("autoexit")
        break
    ephemer(user_input)



    

 

    
    
