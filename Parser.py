from Scanner import tokenize
from io import StringIO
import os
import sys

class Parser:
    def __init__(self, tokens, filename):
        self.tokens = tokens
        self.index = 0
        self.filename = filename

    def current(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else "EndofFile"

    def advance(self):
        self.index += 1

    def match(self, expected):
        token = self.current()
        if token.startswith(expected):
            self.advance()
        else:
            print(f"Parse Error: {expected} expected.")
            raise SyntaxError("handled")

    ## Grammar rules

    # Prg → Blk EndOfFile
    def Prg(self):
        self.Blk()
        if self.current() != "EndofFile":
            raise SyntaxError

    # Blk → Stm Blk {Identifier, PRINT, IF}
    def Blk(self):
        if self.current().startswith(("Identifier", "Print", "If")):
            self.Stm()
            self.Blk()
        else:
            return  # → ε

    # Stm → Identifier := Exp ;
    # Stm → PRINT(Arg Argfollow) ; {PRINT}
    # Stm → IF Cnd : Blk Iffollow {IF}
    def Stm(self):
        tok = self.current()

        if tok.startswith("Identifier"):
            self.advance()
            self.match("Assign")
            self.Exp()
            self.match("Semicolon")
            print("Assignment Statement Recognized")
            return

        elif tok.startswith("Print"):
            self.advance()
            self.match("LeftParen")
            self.Arg()
            self.Argfollow()
            self.match("RightParen")
            self.match("Semicolon")
            print("Print Statement Recognized")
            return

        elif tok.startswith("If"):
            print("If Statement Begins")
            self.advance()
            self.Cnd()
            self.match("Colon")
            self.Blk()
            self.Iffollow()
            print("If Statement Ends")
            return

        else:
            print("Invalid Statement")
            raise SyntaxError

    # Argfollow →, Arg Argfollow {Comma}
    # Argfollow → ε
    def Argfollow(self):
        while self.current().startswith("Comma"):
            self.advance()
            self.Arg()

    # Arg → String {String} 
    # Arg → Exp
    def Arg(self):
        if self.current().startswith("String"):
            self.advance()
        else:
            self.Exp()
            
    # Iffollow → ENDIF ; {ENDIF}
    # Iffollow → ELSE Blk ENDIF ; {ELSE}
    def Iffollow(self):
        if self.current().startswith("Endif"):
            self.advance()
            self.match("Semicolon")
        elif self.current().startswith("Else"):
            self.advance()
            self.Blk()
            self.match("Endif")
            self.match("Semicolon")
        else:
            print("Incomplete if Statement")
            raise SyntaxError

    # Exp → Trm Trmfollow
    def Exp(self):
        self.Trm()
        self.Trmfollow()

    # Trmfollow → + Trm Trmfollow {Plus}
    # Trmfollow → − Trm Trmfollow {Minus} 
    # Trmfollow → ε
    def Trmfollow(self):
        while self.current().startswith(("Plus", "Minus")):
            self.advance()
            self.Trm()

    # Trm → * Fac Facfollow {Multiply}
    # Trm → / Fac Facfollow {Divide}
    # Trm → ε
    def Trm(self):
        self.Fac()
        while self.current().startswith(("Multiply", "Divide")):
            self.advance()
            self.Fac()

    # Fac → Lit Litfollow
    def Fac(self):
        self.Lit()
        while self.current().startswith("Raise"):
            self.advance()
            self.Lit()

    # Litfollow → * * Lit Litfollow {Raise}
    # Litfollow → ε
    
    # Lit → −Val {Minus}
    # Lit → Val
    def Lit(self):
        if self.current().startswith("Minus"):
            self.advance()
            self.Val()
        else:
            self.Val()

    # Val → Identifier {Identifier}
    # Val → number {number}
    # Val → SQRT(Exp) {SQRT}
    # Val → (Exp) 
    def Val(self):
        tok = self.current()
        if tok.startswith(("Identifier", "Number")):
            self.advance()
        elif tok.startswith("Sqrt"):
            self.advance()
            self.match("LeftParen")
            self.Exp()
            self.match("RightParen")
        elif tok.startswith("LeftParen"):
            self.advance()
            self.Exp()
            self.match("RightParen")
        else:
            raise SyntaxError

    # Cnd → Exp Rel Exp
    def Cnd(self):
        self.Exp()
        if not any(self.current().startswith(x) for x in
                   ["LessThan", "Equal", "GreaterThan", "LTEqual", "GTEqual", "NotEqual"]):
            print("Missing relational operator")
            raise SyntaxError
        self.advance()
        self.Exp()

    # Rel → < {LessThan}
    # Rel → = {Equal}
    # Rel → > {GreaterThan}
    # Rel → <= {GTEqual}
    # Rel → != {NotEqual}
    # Rel → >= {LTEqual}

    def parse(self):
        try:
            self.Prg()
            print(f"{self.filename} is a valid SimpCalc program")
        except SyntaxError as e:
            if not str(e):
                print(f"{self.filename} is NOT a valid SimpCalc program")

if __name__ == "__main__":
    for file in os.listdir("."):
        if file.startswith("sample_output_scan_") and file.endswith(".txt"):
            with open(file, "r") as f:
                text = f.read().splitlines()

            tokens = [line.strip() for line in text if line.strip()]

            output_file = file.replace("scan", "parse")

            buffer = StringIO()
            sys_stdout = sys.stdout
            sys.stdout = buffer

            parser = Parser(tokens, file)
            parser.parse()

            sys.stdout = sys_stdout

            with open(output_file, "w") as out:
                out.write(buffer.getvalue())

            print(f"Processed {file} → {output_file}")
