#!/usr/bin/env python3
import os
import time
from openai import OpenAI

# 1) Load API key and Fine‑tune ID
api_key = os.getenv("OPENAI_API_KEY")
ft_id   = os.getenv("FINE_TUNE_ID")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")
if not ft_id:
    raise RuntimeError("Please set the FINE_TUNE_ID environment variable")

# 2) Instantiate v1 client
client = OpenAI(api_key=api_key)

# 3) Poll loop
def poll_status(job_id, interval=60):
    while True:
        resp = client.fine_tuning.jobs.retrieve(job_id)
        status = resp.status
        print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
        if status in ("succeeded", "failed", "cancelled"):
            return resp
        time.sleep(interval)

if __name__ == "__main__":
    result = poll_status(ft_id, interval=120)
    print("Final job info:\n", result)
