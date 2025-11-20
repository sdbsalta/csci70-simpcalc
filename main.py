from Scanner import tokenize
from Parser import Parser
from io import StringIO
import os
import sys
import re

def make_output_name(input_file, mode):  # mode = "scan" or "parse"
    # Remove .txt
    base = input_file[:-4]

    # Replace the first "input" with "output"
    if "input" in base:
        base = base.replace("input", "output", 1)

    # Check if filename ends with _number
    match = re.search(r'_(\d+)$', base)
    if match:
        number = match.group(1)
        base_no_number = base[:-(len(number) + 1)]  # remove _X
        return f"{base_no_number}_{mode}_{number}.txt"

    # No trailing number
    return f"{base}_{mode}.txt"


def run_pipeline(input_file):
    # ---------- SCANNING ----------
    with open(input_file, "r") as f:
        text = f.read()

    tokens = tokenize(text)

    # Scanner output file
    scan_output = make_output_name(input_file, "scan")

    # write scanner output
    with open(scan_output, "w") as f:
        for t in tokens:
            f.write(t + "\n")

    print(f"Scanner: {input_file} → {scan_output}")

    # ---------- PARSING ----------
    parser_tokens = [t.strip() for t in tokens if t.strip()]

    parse_output = make_output_name(input_file, "parse")

    buffer = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    # Pass original input filename to parser so messages reflect input file
    parser = Parser(parser_tokens, input_file)
    parser.parse()

    sys.stdout = sys_stdout

    with open(parse_output, "w") as f:
        f.write(buffer.getvalue())

    print(f"Parser: {input_file} → {parse_output}")
    print("Pipeline complete.\n")


def main():
    # Process only .txt files containing "input"
    for file in os.listdir("."):
        if "input" in file.lower() and file.endswith(".txt"):
            run_pipeline(file)


if __name__ == "__main__":
    main()
