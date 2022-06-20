from tables import *

INPUT_FILE = "input.txt"

# Read input file and convert the instructions
# to a format that is easy to handle.
instructions = list()
with open(INPUT_FILE, 'r') as file:
    text = file.read()
    text = text.split("\n")
    for line in text:
        instructions.append(line.split())

lineCount = 0
totalLines = len(instructions) 

# Check opcodes first
for i in range(totalLines):
    line = instructions[i]
    if len(line) > 0:
        if(line[0] == "var"):
            # Handle variable declaration.
            pass
        else:
            if(line[0] != 'hlt' and line[0] not in opcodes.values()):
                print(f"ERROR: opcode '{line[0]}' is invalid.")

