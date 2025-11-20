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
    line = 1  # iya feat: keep track of line number for error messages

    while i < n:
        c = text[i]

        if c.isspace():
            if c == "\n":
                line += 1  # increment line count
            i += 1
            continue
        
        # Check if "//" for comments
        if c == "/" and i + 1 < n and text[i+1] == "/":
            i += 2
            while i < n and text[i] != "\n":
                i += 1
            continue

        # Check if String
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
                tokens.append(f"Lexical Error (line {line}): Unterminated string")
                tokens.append("Error")
            continue

        # Check if Digit
        if c.isdigit():
            start = i
            has_dot = False
            i += 1
            while i < n and (text[i].isdigit() or text[i] == "."):
                if text[i] == ".":
                    if has_dot:
                        tokens.append(f"Lexical Error (line {line}): Invalid number format")
                        tokens.append("Error")
                        break
                    has_dot = True
                    if i + 1 >= n or not text[i+1].isdigit():
                        tokens.append(f"Lexical Error (line {line}): Invalid number format")
                        tokens.append("Error")
                        i += 1
                        break
                i += 1
            else:
                if i < n and text[i].lower() == "e":
                    i += 1
                    if i < n and text[i] in "+-":
                        i += 1
                    if i >= n or not text[i].isdigit():
                        tokens.append(f"Lexical Error (line {line}): Invalid number format")
                        tokens.append("Error")
                        i += 1
                        continue
                    while i < n and text[i].isdigit():
                        i += 1
                tokens.append(f"Number          {text[start:i]}")
                continue
            i += 1
            continue

        # Check if Identifier
        if c.isalpha() or c == "_":
            start = i
            i += 1
            while i < n and (text[i].isalnum() or text[i] == "_"):
                i += 1
            lex = text[start:i]
            if lex in KEYWORDS:
                tokens.append(f"{KEYWORDS[lex]:<15} {lex}")
            else:
                tokens.append(f"Identifier      {lex}")
            continue

        # Check for multi-character operators first
        matched = False
        for op in MULTI_OPS:
            if text.startswith(op, i):
                tokens.append(f"{OPERATORS[op]:<15} {op}")
                i += len(op)
                matched = True
                break
        if matched:
            continue

        # Check single-character operators
        if c in OPERATORS:
            tokens.append(f"{OPERATORS[c]:<15} {c}")
            i += 1
            continue

    
        tokens.append(f"Lexical Error (line {line}): Illegal character/character sequence")
        tokens.append("Error")
        i += 1

        # iya feat: if it encounters an illegal char & there's a letter/digit beside it, skip the adjacent char
        if c == "!" and i < n and (text[i].isdigit() or text[i].isalpha()):
            i += 1

        continue

    tokens.append("EndofFile")
    return tokens


class Lexer:
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.index = 0

    def gettoken(self):
        # Returns the next token from the input
        if self.index < len(self.tokens):
            tok = self.tokens[self.index]
            self.index += 1
            return tok
        else:
            return "EndofFile"
