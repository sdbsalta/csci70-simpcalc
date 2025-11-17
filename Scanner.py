import os

KEYWORDS = {
    "PRINT": "Print",
    "IF": "If",
    "ELSE": "Else",
    "ENDIF": "Endif",
    "SQRT": "Sqrt",
    "AND": "And",
    "OR": "Or",
    "NOT": "Not"
}

OPERATORS = {
    ":=": "Assign",
    "<=": "LTEqual",
    ">=": "GTEqual",
    "!=": "NotEqual",
    "**": "Raise",
    ";": "Semicolon",
    ":": "Colon",
    ",": "Comma",
    "(": "LeftParen",
    ")": "RightParen",
    "+": "Plus",
    "-": "Minus",
    "*": "Multiply",
    "/": "Divide",
    "<": "LessThan",
    "=": "Equal",
    ">": "GreaterThan",
}

MULTI_OPS = ["<=", ">=", "!=", ":=", "**"]


def tokenize(text):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        c = text[i]

        if c.isspace():
            i += 1
            continue

        if c == "/" and i + 1 < n and text[i+1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue

        if c == '"':
            i += 1
            start = i
            while i < n and text[i] not in ['"', "\n"]:
                i += 1
            if i < n and text[i] == '"':
                lex = '"' + text[start:i] + '"'
                tokens.append(f"String           {lex}")
                i += 1
            else:
                tokens.append("Lexical Error: Unterminated string")
                tokens.append("Error")
            continue

        if c.isdigit():
            start = i
            has_dot = False
            i += 1
            while i < n and (text[i].isdigit() or text[i] == "."):
                if text[i] == ".":
                    if has_dot:
                        tokens.append("Lexical Error: Invalid number format")
                        tokens.append("Error")
                        break
                    has_dot = True
                i += 1
            else:
                if i < n and text[i].lower() == "e":
                    i += 1
                    if i < n and text[i] in "+-":
                        i += 1
                    if i >= n or not text[i].isdigit():
                        tokens.append("Lexical Error: Invalid number format")
                        tokens.append("Error")
                        continue
                    while i < n and text[i].isdigit():
                        i += 1
                tokens.append(f"Number           {text[start:i]}")
                continue
            i += 1
            continue

        if c.isalpha() or c == "_":
            start = i
            i += 1
            while i < n and (text[i].isalnum() or text[i] == "_"):
                i += 1
            lex = text[start:i]
            if lex in KEYWORDS:
                tokens.append(f"{KEYWORDS[lex]:<15} {lex}")
            else:
                tokens.append(f"Identifier       {lex}")
            continue

        matched = False
        for op in MULTI_OPS:
            if text.startswith(op, i):
                tokens.append(f"{OPERATORS[op]:<15} {op}")
                i += len(op)
                matched = True
                break
        if matched:
            continue

        if c in OPERATORS:
            tokens.append(f"{OPERATORS[c]:<15} {c}")
            i += 1
            continue

        tokens.append("Lexical Error: Illegal character/character sequence")
        tokens.append("Error")
        i += 1

    tokens.append("EndofFile")
    return tokens


def process_file(filename):
    with open(filename, "r") as f:
        text = f.read()

    tokens = tokenize(text)

    output = filename.replace(".txt", "_output_scan.txt")

    with open(output, "w") as f:
        for t in tokens:
            f.write(t + "\n")

    print(f"Processed {filename} -> {output}")


if __name__ == "__main__":
    for file in os.listdir("."):
        if file.endswith(".txt"):
            process_file(file)
