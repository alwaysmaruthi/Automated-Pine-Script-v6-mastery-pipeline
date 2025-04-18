#!/usr/bin/env python3
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

print("Uploading training file…")
upload = client.files.create(
    file=open("finetune_dataset.jsonl", "rb"),
    purpose="fine-tune"
)
file_id = upload.id
print(f"📁 Uploaded file ID: {file_id}")

print("Starting fine‑tune job…")
ft_job = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)
print(f"🛠 Fine‑tune created: {ft_job.id}")
print(f"🎯 Model endpoint: {ft_job.fine_tuned_model}")
