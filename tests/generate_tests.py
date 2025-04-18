import os

# List out the Pine functions you want to test (expand this list over time)
FUNCTIONS = [
    ("ta.highest", "ta.highest(close, 10)"),
    ("ta.lowest",  "ta.lowest(close, 10)"),
    # add more tuples like ("namespace.func", "func(args)") here
]

TEMPLATE = """//@version=6
indicator("Test {name}")
plot({call})
"""

os.makedirs("tests", exist_ok=True)
for name, call in FUNCTIONS:
    code = TEMPLATE.format(name=name, call=call)
    fname = f"tests/test_{name.replace('.', '_')}.pine"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(code)
print("[✔] Generated test scripts in tests/ directory")
