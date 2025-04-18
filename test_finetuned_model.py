#!/usr/bin/env python3
import os
from openai import OpenAI

# 1) Load API key and model name from env
api_key    = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("FINE_TUNED_MODEL")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")
if not model_name:
    raise RuntimeError("Missing FINE_TUNED_MODEL")

# 2) Instantiate the v1 client
client = OpenAI(api_key=api_key)

# 3) Send your sample prompt
prompt = "Write a PineScript v6 snippet to plot a 20-period EMA in red."
resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150
)

# 4) Print out the result
print("=== Prompt ===")
print(prompt)
print("\n=== Response ===")
print(resp.choices[0].message.content)
