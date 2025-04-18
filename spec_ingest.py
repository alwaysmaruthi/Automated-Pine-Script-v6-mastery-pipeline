import requests, os, datetime

BASE_URL = "https://www.tradingview.com/pine-script-reference/"
OUT_DIR  = "specs"

os.makedirs(OUT_DIR, exist_ok=True)
today = datetime.date.today().isoformat()
resp = requests.get(BASE_URL)
resp.raise_for_status()

fname = os.path.join(OUT_DIR, f"pine_v6_spec_{today}.html")
with open(fname, "w", encoding="utf-8") as f:
    f.write(resp.text)

print(f"[✔] Saved spec to {fname}")
