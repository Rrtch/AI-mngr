import time, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = r"D:\DB\ENVS\LMS\Phi3mini4Kinst"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map="cuda")

prompt = "El sol se alza sobre las montañas y"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.inference_mode():
    start = time.time()
    output = model.generate(
        **inputs,
        max_new_tokens=64,
        use_cache=True,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1
    )
    end = time.time()

text = tokenizer.decode(output[0], skip_special_tokens=True)
tokens = output.shape[-1]
print(f"⏱️ {tokens/(end-start):.2f} tokens/segundo")
print(text)
