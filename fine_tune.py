# fine_tune.py
#!/usr/bin/env python3
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY") or ""
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

print("Uploading training file…")
t = client.files.create(file=open("training_dataset.jsonl","rb"), purpose="fine-tune")
print("Uploading validation file…")
v = client.files.create(file=open("validation_dataset.jsonl","rb"), purpose="fine-tune")

print("Starting fine‑tune job…")
job = client.fine_tuning.jobs.create(
    training_file  = t.id,
    validation_file= v.id,
    model          = "gpt-3.5-turbo",      # or your chosen base
    hyperparameters= {"n_epochs":10}
)

print(f"🛠 Fine‑tune created: {job.id}")
print(f"🎯 Model endpoint: {job.fine_tuned_model}")
