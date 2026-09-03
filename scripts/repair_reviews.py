import csv
import re
from pathlib import Path

EXPECTED_COLS = 7


def _repair_line(line: str) -> str:
    return re.sub(r'(?<!^)(?<!,)"(?!,|\r?\n|$)', '""', line)


def repair_reviews(input_path: str, output_path: str) -> dict:
    """
    Repairs the malformed olist_order_reviews CSV (embedded unescaped quotes
    breaking row boundaries) and writes a cleaned copy.

    Returns a summary dict: {output_path, original_rows, cleaned_rows, skipped}
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(input_file, "r", encoding="utf-8", newline="") as source:
        raw_lines = source.readlines()

    header_line, *data_lines = raw_lines
    header = next(csv.reader([header_line]))
    rows = [header]

    buffer = ""
    buffered_line_count = 0
    skipped = 0

    for i, line in enumerate(data_lines):
        buffer += line
        buffered_line_count += 1
        fixed = _repair_line(buffer)

        try:
            parsed = next(csv.reader([fixed]))
        except csv.Error:
            if buffered_line_count > 10:
                print(f"Giving up on unrecoverable block near line {i}")
                skipped += 1
                buffer = ""
                buffered_line_count = 0
            continue

        if len(parsed) == EXPECTED_COLS:
            rows.append(parsed)
            buffer = ""
            buffered_line_count = 0
        elif len(parsed) < EXPECTED_COLS:
            if buffered_line_count > 10:
                print(f"Giving up on unrecoverable block near line {i}: {parsed[:2]}")
                skipped += 1
                buffer = ""
                buffered_line_count = 0
            continue
        else:
            print(f"Skipping malformed row (>{EXPECTED_COLS} cols): {parsed[:2]}")
            skipped += 1
            buffer = ""
            buffered_line_count = 0

    with open(output_file, "w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerows(rows)

    summary = {
        "output_path": str(output_file),
        "original_rows": len(data_lines),
        "cleaned_rows": len(rows) - 1,
        "skipped": skipped,
    }
    print("Repair completed!")
    print(summary)
    return summary


if __name__ == "__main__":
    # Local CLI usage: assumes repo-root-relative paths
    repair_reviews("data/olist_order_reviews_dataset.csv",
                    "cleaned_data/olist_order_reviews_dataset.csv")