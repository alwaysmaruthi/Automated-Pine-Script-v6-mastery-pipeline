#!/usr/bin/env python3
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
jobs = client.fine_tuning.jobs.list().data
for job in jobs:
    print(f"ID: {job.id}   Model: {job.fine_tuned_model}   Status: {job.status}")
