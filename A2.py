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

sys_prompt="eres un asistente virtual"

def ephemer(input_text):
    messages = [
        {"role": "system", "content": "Eres un asistente útil, lógico y directo. Responde de forma natural y breve."},
        {"role": "user", "content": input_text},
    ]

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


# === Loop interactivo ===
if __name__ == "__main__":
    print("💬 Chat con Phi-3-mini (CUDA habilitado). Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("🧠 Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        reply = ephemer(user_input)
        print(f"🤖 Phi: {reply}\n")

