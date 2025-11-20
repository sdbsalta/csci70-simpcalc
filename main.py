from Scanner import tokenize
from Parser import Parser
from io import StringIO
import os
import sys
import re

def run_pipeline(input_file):
    # ---------- SCANNING ----------
    with open(input_file, "r") as f:
        text = f.read()

    tokens = tokenize(text)

    # produce scan output filename
    match = re.search(r'_(\d+)\.txt$', input_file)
    if match:
        number = match.group(1)
        scan_output = f"sample_output_scan_{number}.txt"
    else:
        scan_output = input_file.replace(".txt", "_output_scan.txt")

    # write scanner output
    with open(scan_output, "w") as f:
        for t in tokens:
            f.write(t + "\n")

    print(f"Scanner: {input_file} → {scan_output}")

    # ---------- PARSING ----------
    # remove blank lines & keep token strings
    parser_tokens = [t.strip() for t in tokens if t.strip()]

    # generate parse output filename
    parse_output = scan_output.replace("scan", "parse")

    buffer = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    parser = Parser(parser_tokens, scan_output)
    parser.parse()

    sys.stdout = sys_stdout

    with open(parse_output, "w") as f:
        f.write(buffer.getvalue())

    print(f"Parser: {scan_output} → {parse_output}")
    print("Pipeline complete.\n")


def main():
    for file in os.listdir("."):
        if "input" in file.lower() and file.endswith(".txt"):
            run_pipeline(file)


if __name__ == "__main__":
    main()
