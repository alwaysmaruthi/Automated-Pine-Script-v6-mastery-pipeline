# generate_finetune_data.py
import os
import json
from bs4 import BeautifulSoup

SPEC_DIR        = "specs"
TESTS_DIR       = "tests"
OUTPUT_FILE     = "finetune_dataset.jsonl"
SNAPSHOT_PREFIX = "pine_v6_spec_"
MAX_SAMPLES     = 500

def latest_spec_file():
    files = sorted(f for f in os.listdir(SPEC_DIR)
                   if f.startswith(SNAPSHOT_PREFIX) and f.endswith(".html"))
    return os.path.join(SPEC_DIR, files[-1])

def parse_spec(html_path):
    """
    Extract (function_name, description) pairs from the spec HTML.
    Assumes function sections are <h2 id="func"> followed by <p>desc</p>.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    entries = []
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
    """
    For each test_xxx.pine, use the function name from the filename
    and the code as the completion.
    """
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
    """
    Build prompt-completion pairs:
    - Spec: prompt "What does PineScript function <func> do?"
      completion: "<desc>\nExample:\n<func>(...)\n"
    - Tests: prompt "Write a PineScript v6 snippet using <func>"
      completion: "<code>"
    """
    for func, desc in spec_entries:
        prompt = f"What does PineScript function `{func}` do?"
        completion = f"{desc}\nExample usage:\n```pinescript\n{func}(...)\n```"
        yield {"prompt": prompt, "completion": completion}
    for func, code in test_entries:
        prompt = f"Write a PineScript v6 snippet using `{func}`"
        completion = f"```pinescript\n{code}\n```"
        yield {"prompt": prompt, "completion": completion}

def main():
    spec_path    = latest_spec_file()
    spec_entries = parse_spec(spec_path)
    test_entries = parse_tests()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for sample in build_dataset(spec_entries, test_entries):
            out.write(json.dumps(sample, ensure_ascii=False) + "\n")
    print(f"[✔] Wrote {len(spec_entries)+len(test_entries)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
