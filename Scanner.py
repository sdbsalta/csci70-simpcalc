import os

'''
I implemented a state-based approach where the program transitions between valid states 
as it processes each character in the input. The make_tokens function checks the 
current state and the character being read. Based on the character, it either transitions 
to the next valid state—like if it's a digit or an operator—or outputs the 
corresponding token. If the character doesn't fit any of the accepted states, an error 
message is generated, and the program stops reading further characters. This ensures 
that only valid tokens are added to the output file, and any invalid input is immediately flagged.
'''

# DFA Accepted states
assign = "ASSIGN"
plus = "PLUS"
minus = "MINUS"
digit = "NUM"
error = "ERROR"
start = "START"
in_num = "IN_NUM"

# Function to convert content of input to tokens with DFA states
def make_tokens(text: str):
    list_tokens = []
    current_state = start  # Start state
    i = 0
    len_text = len(text)

    while i < len_text:
        char = text[i]
        
        if char.isspace():
            i += 1
            continue

        '''
        This is for the initial setup. So we start in the start state (current_state == start).
        Then the program starts to read each char from the input. It checks the current state
        then determines the next state based on the char being processed at that moment.
        '''
        # Transitioning based on current_state
        if current_state == start:
            if char == '=':
                # Checks if next char is =
                if i + 1 < len_text and text[i+1] == '=':
                    list_tokens.append((assign, "=="))
                    i += 2
                else:
                    list_tokens.append(f'Lexical Error reading character "="')
                    break  # Stop processing on a single = error
            elif char == '+':
                list_tokens.append((plus, "+"))
                i += 1
                current_state = start  # Back to start
                continue
            elif char == '-':
                list_tokens.append((minus, "-"))
                i += 1
                current_state = start  # Back to start
                continue
            elif char.isdigit():
                current_state = in_num  # Start processing a digit
            else:
                list_tokens.append(f'Lexical Error reading character "{char}"')
                break
        
        # If the program encountered a digit, it will start processing the 
        # sequence of digits to extract the complete number
        elif current_state == in_num:
            j = i + 1
            while j < len_text and text[j].isdigit():
                j += 1
            lexeme = text[i:j]
            list_tokens.append((digit, lexeme))
            i = j
            current_state = start  # Back to start after reading a number
            continue
    
    return list_tokens

# Function that writes the output(s)
def create_output(input_path: str) -> str:
    directory, base = os.path.split(input_path)
    name, ext = os.path.splitext(base)
    new_name = name.replace("input", "output_scan", 1) # switch input -> output_scan in filename
    return os.path.join(directory, new_name + ext)

# Function that reads the input(s)
def write_tokens(output_path: str, items):
    lines = []

    for item in items:
        if isinstance(item, str):
            lines.append(item)  # already an error string
        else:
            token_type, lexeme = item
            # for column alignment formatting
            lines.append(f"{token_type:<10} {lexeme:<20}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

        
if __name__ == "__main__":
    input_file = "sample_input.txt"  # change here
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    token_list = make_tokens(text)
    output_file = create_output(input_file)
    write_tokens(output_file, token_list)
    print(f"Created {output_file}")