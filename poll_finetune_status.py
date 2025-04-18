#!/usr/bin/env python3
import os, time
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

# Replace with the ID you saw in your fine‑tune logs
FINE_TUNE_ID = "<your-fine-tune-job-id>"

def poll_status(ft_id, interval=60):
    while True:
        resp = openai.FineTune.retrieve(ft_id)
        status = resp.status
        print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
        if status in ("succeeded", "failed", "cancelled"):
            return resp
        time.sleep(interval)

if __name__ == "__main__":
    result = poll_status(FINE_TUNE_ID, interval=120)
    print("Final job info:\n", result)
