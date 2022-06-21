from tables import *

INPUT_FILE = "input.txt"

typeA_instructions = ['add', 'sub', 'mul', 'or', 'xor', 'and']
typeB_instructions = ['mov', 'rs', 'ls']
typeC_instructions = ['mov', 'div', 'not', 'cmp']
typeD_instructions = ['ld', 'st']
typeE_instructions = ['jmp', 'jlt', 'jgt', 'je']

# Read input file and convert the instructions
# to a format that is easy to handle.
instructions = list()
with open(INPUT_FILE, 'r') as file:
    text = file.read()
    codeLines = text.split("\n")
    for line in codeLines:
        instructions.append(line.split())
    instructions.pop()

lineCount = 0
totalLines = len(instructions) 
programVariables = list()

while(instructions[lineCount][0] == "var"):
    if(len(instructions[lineCount]) != 2):
        print("ERROR: Illegal variable declaration.")
        print(f"--> {lineCount+1}: " + codeLines[lineCount])
    programVariables.append(instructions[lineCount][1])
    lineCount += 1

# Check program halt
if(instructions[-1][0] != "hlt" or len(instructions[-1]) != 1):
    print("ERROR: Last instruction is not 'hlt'")
    
def parse_typeE(line, lineNumber):
    if len(line) != 2:
        print("ERROR: mem_addr or instruction type mismatch.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    if line[1] != 'mem_addr':
        # TODO: add mem_addr type.
        pass
    return

def parse_typeB(line, lineNumber):
    return

def parse_typeC(line, lineNumber):
    return

def parse_typeD(line, lineNumber):
    return

def parse_typeA(line, lineNumber):
    if len(line) != 4:
        print("ERROR: Register count or instruction type mismatch.")
    for i in range(1, 4):
        if line[i] not in registers.values():
            print(f"ERROR: Invalid register usage -> '{line[i]}'.")
            print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    return

# Check opcodes first
for i in range(lineCount, totalLines):
    line = instructions[i]
    if len(line) > 0 and line[0] not in opcodes.values():
        print(f"ERROR: opcode '{line[0]}' is invalid.")
        print(f"--> {i+1}: " + codeLines[i])
    elif line[0] in typeA_instructions:
        parse_typeA(line, i)
    elif line[0] in typeB_instructions:
        parse_typeB(line, i)
    elif line[0] in typeC_instructions:
        parse_typeC(line, i)
    elif line[0] in typeD_instructions:
        parse_typeD(line, i)
    elif line[0] in typeE_instructions:
        parse_typeE(line, i)
