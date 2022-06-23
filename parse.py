from tables import *

INPUT_FILE = "input.txt"

# Read input file and convert the instructions
# to a format that is easy to handle.
instructions = list()
with open(INPUT_FILE, 'r') as file:
    text = file.read()
    codeLines = text.split("\n")
    for line in codeLines:
        instructions.append(line.split())
    instructions.pop()

# source code data
totalLines = len(instructions) 
programVariables = list()
programLabels = list()

def error(code, line, object = ''):
    if object != '':
        print("ERROR: " + errors[code] + " -> '" + object + "'")
    else:
        print("ERROR: " + errors[code])
    print(f"--> {line+1}: " + codeLines[line])
    return 

    
def parse_typeA(line, lineNumber):
    if len(line) != 4:
        print("ERROR: Register count or instruction type mismatch.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    for i in range(1, 4):
        if line[i] not in registers.values():
            print(f"ERROR: Invalid register usage -> '{line[i]}'.")
            print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    return

def parse_typeB(line, lineNumber):
    if len(line) != 3:
        print("ERROR: Register count or instruction type mismatch")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    if line[1] not in registers.values():
        print("ERROR: Register count or instruction type mismatch")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
        # parse_typeC(line, lineNumber)
    if line[2][0] == '$': 
        if int(line[2][1:]) > 255:
            print("ERROR: Immediate value greater than 255")
            print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
        elif int(line[2][1:]) < 0:
            print("ERROR: Immediate value less than 0")
            print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    elif line[0] == 'mov':
        parse_typeC(line, lineNumber)
    return

def parse_typeC(line, lineNumber):
    if len(line) != 3:
        print("ERROR: mem_addr/register or instruction type mismatch.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    for i in range(1, 3):
        if line[i] not in registers.values():
            print(f"ERROR: Invalid register usage -> '{line[i]}'.")
            print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    return

def parse_typeD(line, lineNumber):
    if len(line) != 3:
        print("ERROR: Instruction type mismatch.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    if line[1] not in registers.values():
        print(f"ERROR: Invalid register usage -> '{line[1]}'.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    if line[2] not in programVariables:
        print("ERROR: Illegal variable access -> '{line[2]}'")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    return

def parse_typeE(line, lineNumber):
    if len(line) != 2:
        print("ERROR: mem_addr or instruction type mismatch.")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    if line[1][0:-1] not in programLabels:
        print("ERROR: Illegal label access -> '{line[2]}'")
        print(f"--> {lineNumber+1}: " + codeLines[lineNumber])
    return

def parse_label(line, linenumber):
    programLabels.append(line[0][0:-1])
    return 

def parse():
    lineCount = 0;
    while(instructions[lineCount][0] == "var"):
        if(len(instructions[lineCount]) != 2):
            print("ERROR: Illegal variable declaration.")
            print(f"--> {lineCount+1}: " + codeLines[lineCount])
        programVariables.append(instructions[lineCount][1])
        lineCount += 1

    if(instructions[-1][0] != "hlt" or len(instructions[-1]) != 1):
        error(9, totalLines-1, '')

    for i in range(lineCount, totalLines-1):
        line = instructions[i]
        if len(line) == 1 and line[0][-1] == ':':
            parse_label(line, i)
        elif len(line) > 0 and line[0] not in opcodes.values():
            print(f"ERROR: opcode '{line[0]}' is invalid.")
            print(f"--> {i+1}: " + codeLines[i])
        elif line[0] in instructionType['A']:
            parse_typeA(line, i)
        elif line[0] in instructionType['B']:
            parse_typeB(line, i)
        elif line[0] in instructionType['C']:
            parse_typeC(line, i)
        elif line[0] in instructionType['D']:
            parse_typeD(line, i)
        elif line[0] in instructionType['E']:
            parse_typeE(line, i)
    return

parse()
