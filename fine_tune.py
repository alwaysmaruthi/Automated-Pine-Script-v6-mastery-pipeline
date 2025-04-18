# fine_tune.py
import os
import openai

# 1) Read your API key from env
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Missing OPENAI_API_KEY")

# 2) Upload the JSONL dataset you generated
print("Uploading training file…")
upload_resp = openai.File.create(
    file=open("finetune_dataset.jsonl", "rb"),
    purpose="fine-tune"
)
file_id = upload_resp.id
print(f"📁 Uploaded file ID: {file_id}")

# 3) Create the fine-tune job
print("Starting fine-tune job…")
ft = openai.FineTune.create(
    training_file=file_id,
    model="gpt-4o-mini"       # or another suitable base
)
print("🛠 Fine-tune created:", ft.id)
print("Status endpoint:", ft.fine_tuned_model)
