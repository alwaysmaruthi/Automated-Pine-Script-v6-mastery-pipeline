import os, re, requests
from bs4 import BeautifulSoup

SRC_FILE = "community_sources.txt"
OUT_DIR   = "community"
os.makedirs(OUT_DIR, exist_ok=True)

with open(SRC_FILE, "r", encoding="utf-8") as src:
    urls = [u.strip() for u in src if u.strip() and not u.startswith("#")]

for url in urls:
    try:
        r = requests.get(url, timeout=15); r.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}"); continue

    soup = BeautifulSoup(r.text, "html.parser")
    ta = soup.find("textarea", {"class": "code-block"})
    if not ta or not ta.text.strip():
        print(f"⚠️  No code at {url}"); continue

    parts = url.rstrip("/").split("/")
    if len(parts) >= 5 and parts[3]=="script":
        sid, slug = parts[4], parts[5] if len(parts)>=6 else parts[4]
        fname = f"{sid}_{re.sub(r'\\W+','_',slug)}.pine"
    else:
        fname = re.sub(r"[\\W]+","_",parts[-1]) + ".pine"

    with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
        f.write(ta.text)
    print(f"✅ Saved {url} → {OUT_DIR}/{fname}")
