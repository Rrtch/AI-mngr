# download_pipeline_defaults.py
from transformers import pipeline

tasks = [
    "text-generation",
    "text-classification",
    "token-classification",
    "question-answering",
    "summarization",
    "translation_en_to_fr",
    "fill-mask",
    "feature-extraction",
    "zero-shot-classification",
]

for task in tasks:
    print(f"Descargando modelo default para: {task} ...")
    try:
        pipe = pipeline(task)
        _ = pipe.tokenizer
        _ = pipe.model
        print(f"✅  {task} descargado correctamente.\n")
    except Exception as e:
        print(f"⚠️  Error en {task}: {e}\n")