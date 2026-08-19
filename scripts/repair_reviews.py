import csv
import re
from pathlib import Path

input_file = Path("data/olist_order_reviews_dataset.csv")
output_file = Path("cleaned_data/olist_order_reviews_dataset.csv")
output_file.parent.mkdir(exist_ok=True)

EXPECTED_COLS = 7

def repair_line(line: str) -> str:
    return re.sub(r'(?<!^)(?<!,)"(?!,|\r?\n|$)', '""', line)

rows = []
skipped = 0

with open(input_file, "r", encoding="utf-8", newline="") as source:
    raw_lines = source.readlines()

header_line, *data_lines = raw_lines
header = next(csv.reader([header_line]))
rows.append(header)

buffer = ""
buffered_line_count = 0

for i, line in enumerate(data_lines):
    buffer += line
    buffered_line_count += 1
    fixed = repair_line(buffer)

    try:
        parsed = next(csv.reader([fixed]))
    except csv.Error:
        if buffered_line_count > 10:  # safety valve
            print(f" Giving up on unrecoverable block near line {i}")
            skipped += 1
            buffer = ""
            buffered_line_count = 0
        continue

    if len(parsed) == EXPECTED_COLS:
        rows.append(parsed)
        buffer = ""
        buffered_line_count = 0
    elif len(parsed) < EXPECTED_COLS:
        if buffered_line_count > 10:  # safety valve — stop infinite buffering
            print(f"⚠️ Giving up on unrecoverable block near line {i}: {parsed[:2]}")
            skipped += 1
            buffer = ""
            buffered_line_count = 0
        continue
    else:
        print(f"⚠️ Skipping malformed row (>{EXPECTED_COLS} cols): {parsed[:2]}")
        skipped += 1
        buffer = ""
        buffered_line_count = 0

with open(output_file, "w", encoding="utf-8", newline="") as target:
    writer = csv.writer(target)
    writer.writerows(rows)

print(" Repair completed!")
print(f"Original rows: {len(data_lines)}")
print(f"Cleaned rows: {len(rows) - 1}")
print(f"Skipped (unrecoverable): {skipped}")
print(f"Output: {output_file}")