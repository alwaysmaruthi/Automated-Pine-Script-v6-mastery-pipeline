#!/usr/bin/env python3
import os
import sys
import difflib

SPEC_DIR = "specs"
# find all snapshots named pine_v6_spec_YYYY-MM-DD.html
files = sorted(f for f in os.listdir(SPEC_DIR) if f.startswith("pine_v6_spec_") and f.endswith(".html"))
if len(files) < 2:
    print("Only one spec snapshot; skipping diff check.")
    sys.exit(0)

prev, curr = files[-2], files[-1]
with open(os.path.join(SPEC_DIR, prev), encoding="utf-8") as f_old, \
     open(os.path.join(SPEC_DIR, curr), encoding="utf-8") as f_new:
    old_lines = f_old.readlines()
    new_lines = f_new.readlines()

diff = list(difflib.unified_diff(
    old_lines, new_lines,
    fromfile=prev, tofile=curr, lineterm=""
))
if diff:
    print(f"📘 Pine v6 spec changes detected between {prev} and {curr}:")
    for line in diff:
        print(line.rstrip())
    sys.exit(1)
else:
    print("No changes detected in Pine v6 spec.")
    sys.exit(0)
