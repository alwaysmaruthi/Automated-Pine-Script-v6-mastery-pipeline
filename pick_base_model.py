#!/usr/bin/env python3
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Set OPENAI_API_KEY in env")

client = OpenAI(api_key=api_key)

# 1. Fetch all models
all_models = client.models.list().data

# 2. Filter only fine‑tunable ones
ft_models = []
for m in all_models:
    info = client.models.retrieve(m.id)
    if getattr(info, "fine_tunable", False):
        ft_models.append(m.id)

print("Fine‑tunable models:")
for m in ft_models:
    print(" ‑", m)

# 3. Choose the “best” GPT‑3.5 variant (16k context if available)
preferred = "gpt-3.5-turbo-16k" if "gpt-3.5-turbo-16k" in ft_models else "gpt-3.5-turbo"
print("\nSelected base model:", preferred)
