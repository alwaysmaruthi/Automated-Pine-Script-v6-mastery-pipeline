#!/usr/bin/env python3
import os, json, random, math
from bs4 import BeautifulSoup

SPEC_DIR        = "specs"
TESTS_DIR       = "tests"
SNAPSHOT_PREFIX = "pine_v6_spec_"
MAX_SAMPLES     = 500
MIN_TRAIN       = 10

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
        if desc_tag and desc_tag.get_text(strip=True):
            entries.append((func, desc_tag.get_text(strip=True)))
        if len(entries) >= MAX_SAMPLES:
            break
    return entries

def parse_tests():
    samples = []
    for fname in os.listdir(TESTS_DIR):
        if not fname.endswith(".pine"):
            continue
        func = fname.replace("test_", "").replace(".pine", "")
        code = open(os.path.join(TESTS_DIR, fname), encoding="utf-8").read().strip()
        samples.append((func, code))
        if len(samples) >= MAX_SAMPLES:
            break
    return samples

def build_dataset(spec_entries, test_entries):
    for func, desc in spec_entries:
        yield {"messages":[
            {"role":"user",      "content":f"What does PineScript function `{func}` do?"},
            {"role":"assistant", "content":f"{desc}\n\nExample:\n```pinescript\n{func}(...)\n```"}
        ]}
    for func, code in test_entries:
        yield {"messages":[
            {"role":"user",      "content":f"Write a PineScript v6 snippet using `{func}`"},
            {"role":"assistant", "content":f"```pinescript\n{code}\n```"}
        ]}

def main():
    spec_entries = parse_spec(latest_spec_file())
    test_entries = parse_tests()
    samples      = list(build_dataset(spec_entries, test_entries))
    if not samples:
        raise RuntimeError("No samples generated; check your spec/tests directories")

    random.shuffle(samples)
    split = int(0.8 * len(samples))
    train, val = samples[:split], samples[split:]

    # Ensure at least MIN_TRAIN examples in training set
    if len(train) < MIN_TRAIN:
        times = math.ceil(MIN_TRAIN / len(train))
        train = (train * times)[:MIN_TRAIN]

    # Write out training and validation files
    with open("training_dataset.jsonl", "w", encoding="utf-8") as f:
        for s in train:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open("validation_dataset.jsonl", "w", encoding="utf-8") as f:
        for s in val:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"[✔] Wrote {len(train)} training and {len(val)} validation samples")

if __name__ == "__main__":
    main()
