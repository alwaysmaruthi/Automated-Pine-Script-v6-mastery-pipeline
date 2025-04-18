#!/usr/bin/env python3
import os
import json
from bs4 import BeautifulSoup
import math

SPEC_DIR        = "specs"
TESTS_DIR       = "tests"
OUTPUT_FILE     = "finetune_dataset.jsonl"
SNAPSHOT_PREFIX = "pine_v6_spec_"
MIN_EXAMPLES    = 10

def latest_spec_file():
    files = sorted(
        f for f in os.listdir(SPEC_DIR)
        if f.startswith(SNAPSHOT_PREFIX) and f.endswith(".html")
    )
    return os.path.join(SPEC_DIR, files[-1])

def parse_spec(html_path, max_samples=500):
    entries = []
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    for h2 in soup.find_all("h2"):
        func = h2.get("id", "").strip()
        if not func:
            continue
        desc_tag = h2.find_next_sibling("p")
        if desc_tag and desc_tag.get_text(strip=True):
            desc = desc_tag.get_text(strip=True)
            entries.append((func, desc))
        if len(entries) >= max_samples:
            break
    return entries

def parse_tests(max_samples=500):
    samples = []
    for fname in os.listdir(TESTS_DIR):
        if not fname.endswith(".pine"):
            continue
        func = fname.replace("test_", "").replace(".pine", "")
        code = open(os.path.join(TESTS_DIR, fname), encoding="utf-8").read().strip()
        samples.append((func, code))
        if len(samples) >= max_samples:
            break
    return samples

def build_chat_samples(spec_entries, test_entries):
    for func, desc in spec_entries:
        prompt = f"What does PineScript function `{func}` do?"
        completion = f"{desc}\n\nExample:\n```pinescript\n{func}(...)\n```"
        yield {"messages":[
            {"role":"user","content":prompt},
            {"role":"assistant","content":completion}
        ]}
    for func, code in test_entries:
        prompt = f"Write a PineScript v6 snippet using `{func}`"
        completion = f"```pinescript\n{code}\n```"
        yield {"messages":[
            {"role":"user","content":prompt},
            {"role":"assistant","content":completion}
        ]}

def main():
    spec_path     = latest_spec_file()
    spec_entries  = parse_spec(spec_path)
    test_entries  = parse_tests()
    samples       = list(build_chat_samples(spec_entries, test_entries))
    
    # If too few examples, repeat until we have at least MIN_EXAMPLES
    if len(samples) < MIN_EXAMPLES and samples:
        repeat = math.ceil(MIN_EXAMPLES / len(samples))
        samples = (samples * repeat)[:MIN_EXAMPLES]
    elif not samples:
        raise RuntimeError("No examples found in spec or tests; cannot build dataset")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for sample in samples:
            out.write(json.dumps(sample, ensure_ascii=False) + "\n")
    print(f"[✔] Wrote {len(samples)} chat‑style samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
