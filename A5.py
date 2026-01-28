# A5.py - Direct model inference script using Phi-3-mini.
# Demonstrates direct tokenization and generation without pipeline abstraction.

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_PATH = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"
tok = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16,
    device_map="cuda",
)

inputs = tok(
    "<|system|>Eres un experto en física.<|user|>Qué es la relatividad especial?<|assistant|>",
    return_tensors="pt"
)
out = model.generate(
    **inputs,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.15,
    max_new_tokens=256,
    do_sample=True,
    pad_token_id=tok.eos_token_id
)
print(tok.decode(out[0], skip_special_tokens=True))

