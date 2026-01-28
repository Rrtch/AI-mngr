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

def ephemer(input_text, system_prompt="Eres un asistente útil y conciso."):
    prompt = f"{system_prompt}\nUsuario: {input_text}\nAsistente:"

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=524,         # aumenta si quieres respuestas más largas
            repetition_penalty=1.05,    # suaviza repeticiones sin dañar coherencia
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decodificar y limpiar
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    # Cortar el texto para quedarse solo con la parte del asistente
    if "Asistente:" in text:
        text = text.split("Asistente:")[-1].strip()
    return text


# === Loop interactivo ===
if __name__ == "__main__":
    print("💬 Chat con Phi-3-mini (CUDA habilitado). Escribe 'salir' para terminar.\n")
    while True:
        user_input = input("🧠 Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break
        reply = ephemer(user_input)
        print(f"🤖 Phi: {reply}\n")
