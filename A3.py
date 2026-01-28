import torch,os,re
from transformers import AutoTokenizer, AutoModelForCausalLM

YEL = "\x1b[33m"
RES = "\x1b[0m"
print(YEL+"A3.py in"+RES)
MAG = "\x1b[35m"
RED = "\x1b[31m"
GRE = "\x1b[32m"
RNG = "\x1b[38;5;166m"
BLU = "\x1b[34m"

# === Configuración ===

MODEL_PATH = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"

model = None
tokenizer = None
"""Carga el modelo una sola vez (en el proceso principal)."""

if model is None:
    print("🔹 Cargando modelo (una sola vez)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.float16,
        device_map="cuda"
    )
print("✅ Modelo cargado correctamente")      

def ephemer(input_text):
    '''messages = [
        {"role": "system", "content": "Eres un asistente útil, lógico y directo. Responde de forma natural y breve."},
        {"role": "user", "content": input_text},
    ]'''

    messages=input_text
    # Usa la plantilla de diálogo oficial del modelo
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True  # Añade el token del asistente automáticamente
    )

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            do_sample=True,
            temperature=0.5, 
            top_p=0.3,
            max_new_tokens=524,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extraer solo la respuesta del asistente
    # El modelo genera todo el diálogo, así que tomamos el texto tras la última línea del usuario
    if messages[-1]["content"] in response:
        response = response.split(messages[-1]["content"])[-1]
    response = response.strip()

    return response

def read_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='latin-1') as file:
            return file.read()
    return "[Error] File not found."

B1 = read_file_content('sbB1.txt')    
P3 = read_file_content('sbP3.txt')

def interact(system_input,system_prompt=P3):
     
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": system_input},
    ]

    output = ephemer(prompt)
    return output

def ObltrtNOapt(q):     #No 1 word? No return cicle - filter
    brk=0
    while brk!=1:
        I=interact(q+" return a word.",B1)
        brk=len(I.split())
        #print(q,YEL+"ObltrtNOapt:"+RES,I)  #DEBUG
    return I

def Histeract(user_input,history="",system_specific=P3, system_general="" ):
    
     # 1. Instrucciones generales al inicio
    if system_general:
        prompt += {"role": "system", "content": system_general}
    # 2. Historial acumulado
    if history:
        prompt += {"role": "history", "content": history}
    # 4. Instrucciones precisas al final
    if system_specific:
        prompt += {"role": "system", "content": system_specific}

    # 3. actual user input
    prompt += {"role": "user", "content": user_input}
    
    '''
    prompt = [
        {""}
        {"role": "system", "content": system_specific},
        {"role": "user", "content": user_input},
    ]'''

    #print("prompt en histeract",prompt)

    # Ejecutar modelo y guardar la respuesta
    output = ephemer(prompt)
    # Extraer solo el texto generado y limpiarlo
    #print(user_input,YEL+"interact:"+RES,respuesta)
    return output

def boolteract(system_input):
    # orden del sistema
    system_prompt = B1

    # Construir el prompt completo
    prompt=f"[INST] {system_input} [/INST]"+f"[INST] {system_prompt} [/INST]"
    #prompt="".join(f"[INST] {system_input} [/INST]")+ f"[INST] {system_prompt} [/INST]"
    #prompt=f"<<SYS>> {system_prompt} <</SYS>>\n"+f"[INST] {system_input} [/INST]\n"
    
    # Ejecutar modelo y guardar la respuesta
    output = ephemer(prompt)

    # Extraer solo el texto generado y limpiarlo

    Rspnc = output.lower()
    keywordsT = [r"\btrue\b", r"\byes\b", r"\baffirmative\b"]
    keywordsF = [r"\bfalse\b", r"\bno\b", r"\bnegative\b"]
    print(system_input,YEL+"boolteract:"+RES,Rspnc)  #DEBUG
    if any(re.search(pattern, Rspnc) for pattern in keywordsT):
        return True
    elif any(re.search(pattern, Rspnc) for pattern in keywordsF):
        return False
    else:
        return None

def ObltrtNObooL(q):    #No bool? No return cicle - filter 
    brk=None
    while brk==None:
        brk=boolteract(q+" return a boolean.")
        #print(q,YEL+"ObltrtNObooL:"+RES,brk)  #DEBUG
    return brk

def Surelias(quest,tms=10): #4 boolean petit
    S=0
    for i in range(tms):
        if(ObltrtNObooL(quest)):S+=1
    return S                #a list of bools

def Keypier(q,tms=3): #4 keywords petit
    RL=[]
    kqst =  "keyword for ("+q+")"
    for i in range(tms):
        RL.append(ObltrtNOapt(kqst))
    return str(RL)             #a list of keywords

def SelFromList(lst, q):
    lst.append("other")
    lst_str = " , ".join(lst)
    return ObltrtNOapt(f"Classify the expression '{q}' into one of the following topics: {lst_str} ")


# === Loop interactivo ===
if __name__ == "__main__":
    print("💬 Chat con Phi-3-mini (CUDA habilitado). Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("🧠 Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        #reply = ephemer(user_input)
        reply = interact(user_input)
        print(f"🤖 Phi: {reply}\n")

