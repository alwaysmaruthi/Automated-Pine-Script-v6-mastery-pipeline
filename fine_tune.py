#!/usr/bin/env python3
import os
import subprocess
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

# 1) Dynamically pick the base model
# Runs the helper script and captures its last line
res = subprocess.run(
    ["python", "pick_base_model.py"],
    capture_output=True, text=True, check=True
)
base_model = res.stdout.strip().splitlines()[-1].split()[-1]
print(f"[✔] Using base model: {base_model}")

# 2) Init client
client = OpenAI(api_key=api_key)

# 3) Upload dataset
print("Uploading training file…")
upload = client.files.create(
    file=open("finetune_dataset.jsonl", "rb"),
    purpose="fine-tune"
)
file_id = upload.id
print(f"📁 Uploaded file ID: {file_id}")

# 4) Kick off fine‑tune
print("Starting fine‑tune job…")
ft_job = client.fine_tuning.jobs.create(
    training_file=file_id,
    model=base_model
)
print(f"🛠 Fine‑tune created: {ft_job.id}")
print(f"🎯 Model endpoint: {ft_job.fine_tuned_model}")
