import os,re,gc
from llama_cpp import Llama

def read_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='latin-1') as file:
            return file.read()
    return "[Error] File not found."

B1 = read_file_content('B1.txt')    

def ephemer(prompt,Temp=0.5,TopP=0.3,rep=1.1,MaxT=0,Nctx=5124):
    gc.collect()
    # Cargar el modelo una vez
    llm = Llama(
        model_path="D:/APPS/Models/Mistral7Bv0.3.gguf",  
        verbose=False,      # Desactivar logs detallados
        temperature=Temp,    # Ajusta la creatividad de las respuestas (default: 0.8)
        top_p=TopP,          # Ajusta la diversidad de las respuestas (default: 0.95)
        repetition_penalty=rep,     #
        n_ctx=Nctx  # Puedes subir más si tu RAM lo permite
    )
    output = llm(prompt,max_tokens=MaxT)
    resp = output["choices"][0]["text"].strip()
    # Descargar/liberar memoria del modelo
    print("ai: ",resp)
    del llm
    gc.collect()
    return resp


# Crear carpeta de logs
os.makedirs("logs", exist_ok=True)

def generate_response(prompt, tem, toP, rep):
    # Construir el prompt completo
    #prompt=f"[INST] {system_prompt} [/INST][INST] {system_input} [/INST]"  #
    prompt=f"[INST] {prompt} [/INST]"
    # Ejecutar modelo y guardar la respuesta
    output = ephemer(prompt,tem,toP,rep)
    return output

temperature_values = [0.2, 0.4, 0.6, 0.8]
top_p_values = [0.3, 0.6, 0.9]
rep_values = [1.0, 1.25, 1.5]

prompt = "hola"

with open("logs/all_results.txt", "w", encoding="utf-8") as log:
    log.write(f"Prompt: {prompt}\n")
    for temp in temperature_values:
        for top_p in top_p_values:
            for rep in rep_values:
                response = generate_response(prompt, temp, top_p, rep)
                log.write("=== Nueva combinación ===\n")
                log.write(f"temperature={temp}, top_p={top_p}, repetition_penalty={rep}\n")
                log.write("Respuesta: ")
                log.write(response + "\n\n")

print("Resultados guardados en logs/all_results.txt")


#prompt=f"[INST] {system_input} [/INST]\n[INST] {system_prompt} [/INST]\n"          #
#prompt=f"[INST] {system_input} [/INST]\n[INST] {system_prompt} [/INST]"            #
#prompt=f"[INST] {system_input} [/INST][INST] {system_prompt} [/INST]"              #
#prompt="[INST] "+system_input+" [/INST]\n"+"<<SYS>> "+system_prompt+" <</SYS>>\n"  #
#prompt="[INST] "+system_input+" [/INST]\n"+"<<SYS>> "+system_prompt+" <</SYS>>"    # 
#prompt="[INST] "+system_input+" [/INST]"+"<<SYS>> "+system_prompt+" <</SYS>>"      #
#prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]\n"     #
#prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]"       #
#prompt="<<SYS>> "+system_prompt+" <</SYS>>[INST] "+system_input+" [/INST]"         #
#prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]\n"          #
#prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]"            #
#print ("00",ephemer()
#print("EnD")
    

 

    
    
