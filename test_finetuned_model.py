#!/usr/bin/env python3
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "<your-fine-tuned-model-name>"

prompt = "Write a PineScript v6 snippet to plot a 20-period EMA in red."
resp = openai.ChatCompletion.create(
    model=MODEL_NAME,
    messages=[{"role":"user","content":prompt}],
    max_tokens=150
)
print("=== Prompt ===")
print(prompt)
print("\n=== Response ===")
print(resp.choices[0].message.content)
