#!/usr/bin/env python3
import os, time
from openai import OpenAI

# ─── Config ──────────────────────────────────────────────────────────────────
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY")

# ─── Init client ──────────────────────────────────────────────────────────────
client = OpenAI(api_key=API_KEY)

# ─── Pick the latest fine‑tune job ────────────────────────────────────────────
jobs = client.fine_tuning.jobs.list().data
if not jobs:
    raise RuntimeError("No fine‑tune jobs found in your account")
latest = jobs[0]
job_id = latest.id
print(f"[✔] Polling latest fine‑tune job: {job_id}")

# ─── Poll until completion ────────────────────────────────────────────────────
while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    status = job.status
    print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
    if status == "succeeded":
        break
    if status in ("failed", "cancelled"):
        print("\n⚠️ Job did not succeed. Fetching events:")
        events = client.fine_tuning.jobs.list_events(job_id).data
        for ev in events:
            ts = ev.created_at or ev.timestamp
            print(f"- {ts} | {ev.level.upper()} | {ev.message}")
        raise RuntimeError(f"Fine‑tune job ended with status '{status}'")
    time.sleep(60)

model_name = job.fine_tuned_model
print(f"\n✅ Fine‑tuned model ready: {model_name}\n")

# ─── Run your sample prompt ───────────────────────────────────────────────────
prompt = "Write a PineScript v6 snippet to plot a 20-period EMA in red."
print("=== Prompt ===\n" + prompt + "\n")

resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150
)

print("=== Response ===\n" + resp.choices[0].message.content)
