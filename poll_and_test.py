#!/usr/bin/env python3
import os, time
from openai import OpenAI

# 1) Load config
api_key = os.getenv("OPENAI_API_KEY")
job_id  = os.getenv("FINE_TUNE_JOB_ID")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")
if not job_id:
    raise RuntimeError("Missing FINE_TUNE_JOB_ID")

# 2) Init client
client = OpenAI(api_key=api_key)

# 3) Poll until done
print(f"Polling job {job_id}…")
while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    status = job.status
    print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
    if status == "succeeded":
        break
    if status in ("failed", "cancelled"):
        raise RuntimeError(f"Job ended with status '{status}'")
    time.sleep(60)

model_name = job.fine_tuned_model
print(f"📦 Fine‑tuned model ready: {model_name}")

# 4) Send test prompt
prompt = "Write a PineScript v6 snippet to plot a 20-period EMA in red."
print("\n=== Prompt ===\n" + prompt + "\n")
resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role":"user","content":prompt}],
    max_tokens=150
)
print("=== Response ===\n" + resp.choices[0].message.content)
