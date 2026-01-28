import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# === Configuración ===
MODEL_PATH = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16,
    device_map="cuda",
)

sys_prompt="Eres un asistente útil, lógico y directo. Responde de forma natural y breve."

def ephemer(input):

    messages= f"<|system|>{sys_prompt}\n<|user|>{input}\n<|assistant|>"

        # Usa la plantilla de diálogo oficial del modelo
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True  # Añade el token del asistente automáticamente
    )

    #inputs = tokenizer(input, return_tensors="pt").to("cuda")
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            do_sample=True,           # 🔥 activa sampling
            temperature=0.5,           # controla creatividad
            top_p=0.3,                 # filtra por probabilidad acumulada
            repetition_penalty=1.05,
            max_new_tokens=524,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decodificar salida y limpiar
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    response = response.split("Asistente:")[-1].strip()

    return response


# === Loop interactivo ===
if __name__ == "__main__":
    print("💬 Chat con Phi-3-mini (CUDA habilitado). Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("🧠 Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        reply = ephemer(user_input)
        print(f"🤖 Phi: {reply}\n")
