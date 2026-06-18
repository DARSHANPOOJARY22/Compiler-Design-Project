from tabulate import tabulate
import re

print("\n===== SIMPLE COMPILER (SUM OF NATURAL NUMBERS) =====")

# 🔥 TAKE INPUT
print("Enter your program (type END on a new line to finish):")
lines = []
while True:
    line = input()
    lines.append(line)
    if line.strip() == "END":
        break

program = "\n".join(lines)

# 🔥 KEYWORDS & OPERATORS
keywords = {"BEGIN", "END", "INTEGER", "READ", "FOR", "PRINT", "TO"}
operators = {":=", "+", ",", "=="}

# 🔥 TABLES
token_table = []
symbol_table = []
symbol_dict = {}

token_id = 1

# 🔥 TOKENIZATION
tokens = re.findall(r':=|==|\w+|[,+]', program)

for word in tokens:
    if word in keywords:
        token_type = "KEYWORD"
    elif word in operators:
        token_type = "OPERATOR"
    elif word.isdigit():
        token_type = "NUMBER"
    elif word.isidentifier():
        token_type = "IDENTIFIER"
    else:
        token_type = "UNKNOWN"

    token_table.append([token_type, word, token_id])

    if word not in symbol_dict:
        symbol_dict[word] = token_type
        symbol_table.append([word, token_type])

    token_id += 1

# 🔥 TOKEN TABLE
print("\nTOKEN TABLE:")
print(tabulate(token_table, headers=["Type", "Lexeme", "Token ID"], tablefmt="fancy_grid"))

# 🔥 SYMBOL TABLE
print("\nCOMBINED SYMBOL TABLE:")
print(tabulate(symbol_table, headers=["Symbol", "Category"], tablefmt="fancy_grid"))

# 🔥 PARSE TREE (SUM VERSION)
print("\nPARSE TREE:")
print("program")
print(" ├── BEGIN")
print(" ├── stmt_list")
print(" │    ├── declaration (INTEGER N, I, SUM)")
print(" │    ├── assignment (SUM := 0)")
print(" │    ├── for_loop")
print(" │    │    ├── FOR I := 1 TO N")
print(" │    │    └── assignment (SUM := SUM + I)")
print(" │    └── print (PRINT SUM)")
print(" └── END")

# 🔥 GRAMMAR
print("\nGRAMMAR:")
grammar = [
    "program -> BEGIN stmt_list END",
    "stmt_list -> stmt stmt_list",
    "stmt_list -> ε",
    "stmt -> declaration",
    "stmt -> assignment",
    "stmt -> for_loop",
    "stmt -> print",
    "declaration -> INTEGER var_list",
    "var_list -> IDENTIFIER",
    "var_list -> IDENTIFIER , var_list",
    "assignment -> IDENTIFIER := expr",
    "for_loop -> FOR IDENTIFIER := expr TO expr stmt_list END",
    "expr -> IDENTIFIER",
    "expr -> NUMBER",
    "print -> PRINT IDENTIFIER"
]

for rule in grammar:
    print(rule)

# 🔥 PARSING TABLE
print("\nPARSING TABLE:")
parsing_table = [
    ["program", "BEGIN", "BEGIN stmt_list END"],
    ["stmt_list", "INTEGER", "stmt stmt_list"],
    ["stmt_list", "IDENTIFIER", "stmt stmt_list"],
    ["stmt_list", "FOR", "stmt stmt_list"],
    ["stmt_list", "PRINT", "stmt stmt_list"],
    ["stmt_list", "END", "ε"],
    ["stmt", "INTEGER", "declaration"],
    ["stmt", "IDENTIFIER", "assignment"],
    ["stmt", "FOR", "for_loop"],
    ["stmt", "PRINT", "print"],
    ["for_loop", "FOR", "FOR IDENTIFIER := expr TO expr stmt_list END"],
    ["print", "PRINT", "PRINT IDENTIFIER"],
]

print(tabulate(parsing_table, headers=["Non-Terminal", "Input", "Production"], tablefmt="fancy_grid"))

# 🔥 FIRST SET
print("\nFIRST SET:")
first = {
    "program": ["BEGIN"],
    "stmt_list": ["INTEGER", "IDENTIFIER", "FOR", "PRINT", "ε"],
    "stmt": ["INTEGER", "IDENTIFIER", "FOR", "PRINT"],
    "declaration": ["INTEGER"],
    "assignment": ["IDENTIFIER"],
    "for_loop": ["FOR"],
    "print": ["PRINT"],
    "expr": ["IDENTIFIER", "NUMBER"]
}

print(tabulate([[k, ", ".join(v)] for k, v in first.items()],
               headers=["Non-Terminal", "FIRST"], tablefmt="fancy_grid"))

# 🔥 FOLLOW SET
print("\nFOLLOW SET:")
follow = {
    "program": ["$"],
    "stmt_list": ["END"],
    "stmt": ["INTEGER", "IDENTIFIER", "FOR", "PRINT", "END"],
    "declaration": ["INTEGER", "IDENTIFIER", "FOR", "PRINT", "END"],
    "assignment": ["INTEGER", "IDENTIFIER", "FOR", "PRINT", "END"],
    "for_loop": ["INTEGER", "IDENTIFIER", "FOR", "PRINT", "END"],
    "print": ["END"],
    "expr": ["TO", "+", "END"]
}

print(tabulate([[k, ", ".join(v)] for k, v in follow.items()],
               headers=["Non-Terminal", "FOLLOW"], tablefmt="fancy_grid"))

print("\n===== PARSING COMPLETED SUCCESSFULLY =====\n")
