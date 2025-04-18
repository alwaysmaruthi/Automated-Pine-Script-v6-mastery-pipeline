#!/usr/bin/env python3
import os, time
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
jobs = client.fine_tuning.jobs.list().data

# assume the first entry is the most recent
latest_job = jobs[0].id
print("Latest fine‑tune job ID:", latest_job)
# 1) Load config
api_key = os.getenv("OPENAI_API_KEY")
job_id  = os.getenv("FINE_TUNE_JOB_ID")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")
if not job_id:
    raise RuntimeError("Missing FINE_TUNE_JOB_ID")

# 2) Init client
client = OpenAI(api_key=api_key)

# 3) Poll until done or failed
print(f"Polling job {job_id}…")
while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    status = job.status
    print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
    if status == "succeeded":
        break
    if status in ("failed", "cancelled"):
        print("\n⚠️ Job did not succeed. Fetching failure events:")
        events = client.fine_tuning.jobs.list_events(job_id)
        for ev in events.data:
            ts = ev.created_at or ev.timestamp
            print(f"- {ts} | {ev.level.upper()} | {ev.message}")
        raise RuntimeError(f"Fine‑tune job ended with status '{status}'")
    time.sleep(60)

model_name = job.fine_tuned_model
print(f"\n✅ Fine‑tuned model ready: {model_name}\n")

# 4) Send test prompt
prompt = "Write a PineScript v6 snippet to plot a 20-period EMA in red."
print("=== Prompt ===\n" + prompt + "\n")
resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role":"user","content":prompt}],
    max_tokens=150
)
print("=== Response ===\n" + resp.choices[0].message.content)
