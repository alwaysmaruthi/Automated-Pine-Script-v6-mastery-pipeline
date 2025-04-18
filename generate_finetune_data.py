#!/usr/bin/env python3
import os
import json
from bs4 import BeautifulSoup

SPEC_DIR        = "specs"
TESTS_DIR       = "tests"
OUTPUT_FILE     = "finetune_dataset.jsonl"
SNAPSHOT_PREFIX = "pine_v6_spec_"
MAX_SAMPLES     = 500

def latest_spec_file():
    files = sorted(
        f for f in os.listdir(SPEC_DIR)
        if f.startswith(SNAPSHOT_PREFIX) and f.endswith(".html")
    )
    return os.path.join(SPEC_DIR, files[-1])

def parse_spec(html_path):
    entries = []
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    for h2 in soup.find_all("h2"):
        func = h2.get("id", "").strip()
        if not func:
            continue
        desc_tag = h2.find_next_sibling("p")
        if desc_tag:
            desc = desc_tag.get_text(strip=True)
            entries.append((func, desc))
        if len(entries) >= MAX_SAMPLES:
            break
    return entries

def parse_tests():
    samples = []
    for fname in os.listdir(TESTS_DIR):
        if not fname.endswith(".pine"):
            continue
        func = fname.replace("test_", "").replace(".pine", "")
        with open(os.path.join(TESTS_DIR, fname), encoding="utf-8") as f:
            code = f.read().strip()
        samples.append((func, code))
        if len(samples) >= MAX_SAMPLES:
            break
    return samples

def build_dataset(spec_entries, test_entries):
    for func, desc in spec_entries:
        prompt = f"What does PineScript function `{func}` do?"
        completion = (
            f"{desc}\n\nExample:\n```pinescript\n{func}(...)\n```"
        )
        yield {
            "messages": [
                {"role": "user",      "content": prompt},
                {"role": "assistant", "content": completion}
            ]
        }
    for func, code in test_entries:
        prompt = f"Write a PineScript v6 snippet using `{func}`"
        completion = f"```pinescript\n{code}\n```"
        yield {
            "messages": [
                {"role": "user",      "content": prompt},
                {"role": "assistant", "content": completion}
            ]
        }

def main():
    spec_path    = latest_spec_file()
    spec_entries = parse_spec(spec_path)
    test_entries = parse_tests()
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for sample in build_dataset(spec_entries, test_entries):
            out.write(json.dumps(sample, ensure_ascii=False) + "\n")
            count += 1
    print(f"[✔] Wrote {count} chat‑style samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
