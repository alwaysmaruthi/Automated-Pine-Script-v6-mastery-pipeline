#!/usr/bin/env python3
import os
from openai import OpenAI

# 1) Read your API key from env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

# 2) Instantiate the v1 client
client = OpenAI(api_key=api_key)

# 3) Upload the JSONL dataset
print("Uploading training file…")
upload = client.files.create(
    file=open("finetune_dataset.jsonl", "rb"),
    purpose="fine-tune"
)
file_id = upload.id
print(f"📁 Uploaded file ID: {file_id}")

# 4) Create the fine‑tune job with more epochs
print("Starting fine‑tune job…")
ft_job = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo",
    n_epochs=10       # ← run 10 full passes over your data
)
print(f"🛠 Fine‑tune created: {ft_job.id}")
print(f"🎯 Model endpoint: {ft_job.fine_tuned_model}")
