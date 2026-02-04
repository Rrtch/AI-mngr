# A9.py - Advanced conversation handler with message compression for Phi-3-mini.
# Features automatic message summarization when context grows too large.
# Includes Conversa function for building formatted conversation prompts.

import torch,os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# === Configuración ===
MODEL_PATH = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16,
    device_map="cuda",
)

def ephemer(input_text,MAX=1000):
    messages=input_text
    print("!dsds&",messages)
    # Usa la plantilla de diálogo oficial del modelo
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True  # Añade el token del asistente automáticamente
    )
    print("!#$%&",prompt)
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            do_sample=True,
            temperature=0.7, 
            top_p=0.5,
            max_new_tokens=MAX,
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
        with open(path, 'r', encoding='utf-8-sig') as file:
            return file.read()
    return "[Error] File not found."

SYS= read_file_content('sbSY.txt')
P3 = read_file_content('sbP3.txt')
SR = read_file_content('sbSR.txt')
def interact(system_input,system_prompt=P3):
     
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": system_input},
    ]

    output = ephemer(prompt,512)
    return output


def summarizer(texto,system_prompt=SR.replace('\n',' ')):
     
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "reply{texto}compressed"}
    ]
    
    output = ephemer(prompt,250)
    print(output)
    return output

def summy(texto,system_prompt=SR.replace('\n',' ')):
    print("aaa: ",texto)
    prompt = [
        {"role": "system", "content": system_prompt},
        
            {"role": "user", "content": "from [{text}] output concisest"}
    ]
    
    output = ephemer(prompt,64)
    #print(output)
    return output

def msgCompress(mess):
    """
    valida si debe comprimir los msgs.
    """
    # 1️⃣ Construir el prompt
    usermsgs= ""
    asismsgs= ""
    formatted= []
    for msg in mess:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            formatted.append({"role": "system", "content": content})
        elif role == "user":
            usermsgs += f"{content}\n "
        elif role == "assistant":
            asismsgs += f"{content}\n "
    #print("user:",usermsgs)
    #print("asis:",asismsgs)
    
    if ( len(usermsgs) / 3.8)>=150 or ( len(asismsgs) / 3.8)>=150:
        print("compress msgs!")
        formatted.append({"role": "user", "content": summarizer(usermsgs)})
        formatted.append({"role": "assistant", "content": summarizer(asismsgs)})
        #print (formatted)
        return formatted
    else:return mess

def Conversa(messages):
    # 0 Analiza la longitud
    mess=[]
    mess=messages.copy()
    #messages=msgCompress(messages)
    mess.insert(0,{"role": "system", "content": SYS.replace('\n',' ')})
    mess.insert(1,{"role": "assistant", "content": "Ok, ¡I'll never forget it!"})
    mess.insert(len(mess)-1,{"role": "system", "content": P3.replace('\n',' ')})
    # 1️⃣ Construir el prompt
    formatted= ""
    for msg in mess:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            formatted += f"\n{content}\n"
        elif role == "user":
            formatted += f"\n{content}\n"
        elif role == "assistant":
            formatted += f"\n{content}\n"
    mess.clear()
    formatted +="<|assistant|>" 
    #print (formatted)
    return formatted

def EphConv(cntxt):
    print(cntxt)
    # 2️⃣ Tokenizar e inferir
    inputs = tokenizer(cntxt, return_tensors="pt").to(model.device)
    output = model.generate(
        **inputs,
        do_sample=True,
        temperature=0.5, 
        top_p=0.1,
        max_new_tokens=524,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    # 3️⃣ Decodificar y limpiar
    decoded = tokenizer.decode(output[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    return decoded.strip()

chat_history = []
#chat_history.insert(0,{"role": "system", "content": SYS.replace('\n',' ')})
# === Loop interactivo ===
if __name__ == "__main__":
    print("💬 Chat con Phi-3-mini (CUDA habilitado). Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit", "bye"]:
            break
        usi= summy(user_input.lower())
        print("usi: ",usi)
        chat_history.append({"role": "user", "content":"UserContentReply"+user_input})
        respuesta = EphConv(Conversa(chat_history))
        #respuesta = interact(input)
        print(f"Phi: {respuesta}\n")
        #res=summy(respuesta)
        chat_history.append({"role": "assistant", "content": respuesta})
        chat_history=msgCompress(chat_history)
        print("-------------------------------------------------")
        

