from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_PATH = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"
tok = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16,
    device_map="cuda",
)

chat = pipeline("text-generation", model=model, tokenizer=tok)

prompt = "<|system|>Eres un asistente útil.<|user|>Explica el principio de Arquímedes.<|assistant|>"

resp = chat(
    prompt,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repetition_penalty=1.1,
    max_new_tokens=1000,
    do_sample=True
)

print(resp[0]["generated_text"])
