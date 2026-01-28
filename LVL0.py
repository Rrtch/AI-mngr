# LVL0.py - Core LlamaCPP-based functions module using Mistral-7B model.
# Provides ephemer, interact, boolteract, Histeract, and keyword extraction.
# Lower-level implementation for GGUF model inference.

import os,re,gc
from llama_cpp import Llama
YEL = "\x1b[33m"
RES = "\x1b[0m"
print(YEL+"LVL0.py in"+RES)
MAG = "\x1b[35m"
RED = "\x1b[31m"
GRE = "\x1b[32m"
RNG = "\x1b[38;5;166m"
BLU = "\x1b[34m"

def ephemer(prompt,Temp=0.5,TopP=0.3,rep=1.1,MaxT=0,Nctx=5124):
    gc.collect()
    llm = Llama(
        model_path="D:/APPS/Models/Mistral-7BQ4_K_M.gguf",  
        verbose=False,      # Desactivar logs detallados
        temperature=Temp,    # Ajusta la creatividad de las respuestas (default: 0.8)
        top_p=TopP,          # Ajusta la diversidad de las respuestas (default: 0.95)
        repetition_penalty=rep,     #
        n_ctx=Nctx  # Puedes subir más si tu RAM lo permite
    )
    output = llm(prompt,max_tokens=MaxT)
    
    resp = output["choices"][0]["text"]
    print(YEL+"ephemer responce: "+RES,resp)
    try:
        del llm  # intenta eliminar la variable del modelo
        gc.collect()  # fuerza la recolección de basura
    except Exception:
        pass  # ignora si 'llm' no existe o ya fue liberado
    return resp

def read_file_content(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='latin-1') as file:
            return file.read()
    return "[Error] File not found."

B1 = read_file_content('B1.txt')    
P3 = read_file_content('P3.txt')

# Prompt (entrada) para el modelo

def build_prompt(history, user_input, system_general, system_specific):
    prompt = ""

    # 1. Instrucciones generales al inicio
    prompt += f"[INST] {system_general} [/INST]\n"

    # 2. Historial acumulado
    if history:
        prompt += "\n".join(history) + "\n"

    # 3. Nuevo input
    prompt += f"[INST] {user_input} [/INST]\n"

    # 4. Instrucciones precisas al final
    if system_specific:
        prompt += f"[INST] {system_specific} [/INST]\n"

    return prompt
                    
def interact(system_input,system_prompt=P3):
    # Construir el prompt completo 

    #prompt=f"[INST] {system_input} [/INST]\n[INST] {system_prompt} [/INST]\n"          #
    #prompt=f"[INST] {system_input} [/INST]\n[INST] {system_prompt} [/INST]"            #
    #prompt=f"[INST] {system_input} [/INST][INST] {system_prompt} [/INST]"              #

    #prompt="[INST] "+system_input+" [/INST]\n"+"<<SYS>> "+system_prompt+" <</SYS>>\n"  #
    #prompt="[INST] "+system_input+" [/INST]\n"+"<<SYS>> "+system_prompt+" <</SYS>>"    # 
    #prompt="[INST] "+system_input+" [/INST]"+"<<SYS>> "+system_prompt+" <</SYS>>"      #

    #-----------------------------------------------------------------------------------#
    #prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]\n"     #
    #prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]"       #
    #prompt="<<SYS>> "+system_prompt+" <</SYS>>[INST] "+system_input+" [/INST]"         #

    #prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]\n"          #
    #prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]"            #
    #prompt=f"[INST] {system_prompt} [/INST][INST] {system_input} [/INST]"              #
    # Ejecutar modelo y guardar la respuesta
    
    prompt=f"[INST] {system_input} [/INST]"              #
    output = ephemer(prompt)
    # Extraer solo el texto generado y limpiarlo
    #print(user_input,YEL+"interact:"+RES,respuesta)
    
    return output

def ObltrtNOapt(q):     #No 1 word? No return cicle - filter
    brk=0
    while brk!=1:
        I=interact(q+" return a word.",B1)
        brk=len(I.split())
        #print(q,YEL+"ObltrtNOapt:"+RES,I)  #DEBUG
    return I

def Histeract(user_input,history="",system_specific=P3, system_general="" ):
    prompt = ""

    # 1. Instrucciones generales al inicio
    if system_general:
        prompt += f"\n<<DATA>> {system_general} <</DATA>>"
    # 2. Historial acumulado
    if history:
        prompt += "\n".join(history)
    # 4. Instrucciones precisas al final
    if system_specific:
        prompt += f"\n<<SYS>> {system_specific} <</SYS>>"

    # 3. actual user input
    prompt += f"\n[INST] {user_input} [/INST]"
    
    #print("prompt en histeract",prompt)

    # Ejecutar modelo y guardar la respuesta
    output = ephemer(prompt)
    # Extraer solo el texto generado y limpiarlo
    #print(user_input,YEL+"interact:"+RES,respuesta)
    return output

def SelFromList(lst, q):
    lst.append("other")
    lst_str = " , ".join(lst)
    return ObltrtNOapt(f"Classify the expression '{q}' into one of the following topics: {lst_str} ")

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

def Summarize(Ex):

    I=interact(Ex+"return a word.",B1)
    res=interact(Ex)

    return res

while False:

    #system_prompt = read_file_content('SR.txt')
    system_input = input("Tu: ")
    if system_input.lower() in ["salir", "exit", "bye"]:
        print("autoexit")
        break
    respuesta = interact(system_input)
    print("AI: ",respuesta) 
                                                                                    #lineas en response            
   #prompt=f"[INST] {system_input} [/INST][INST] {system_prompt} [/INST]"              #1 s
   #print ("00",ephemer(prompt))

   #prompt="[INST] "+system_input+" [/INST]<<SYS>> "+system_prompt+" <</SYS>>"         #2 s j    
   #print ("01",ephemer(prompt))

   ##-------------------------------------------------------------------#
   #prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]\n"     #2 s j 
   #print ("02",ephemer(prompt))
   #prompt="<<SYS>> "+system_prompt+" <</SYS>>\n[INST] "+system_input+" [/INST]"       #1 m
   #print ("03",ephemer(prompt))
   #prompt="<<SYS>> "+system_prompt+" <</SYS>>[INST] "+system_input+" [/INST]"         #1 s
   #print ("04",ephemer(prompt))

   #prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]\n"          #3 xs j
   #print ("05",ephemer(prompt))
   #prompt=f"[INST] {system_prompt} [/INST]\n[INST] {system_input} [/INST]"            #1 xs
   #print ("06",ephemer(prompt))
   #prompt=f"[INST] {system_prompt} [/INST][INST] {system_input} [/INST]"              #2 s j
   #print ("07",ephemer(prompt))

    #test00 = user_imput
    #test01 = f"summarize the expresion '{user_imput}'"
    #test00 = "ready to ("+user_imput+")"
    #test00 = "ready to ("+user_imput+")"
    
    #interact(test00,SR)
    #interact(test01,SR)
    
    #print ("00",ephemer()

#print("EnD")
    

 

    
    
