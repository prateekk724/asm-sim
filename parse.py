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
        error(1, lineNumber)
    for i in range(1, 4):
        if line[i] not in registers.values():
            error(1, lineNumber, line[i])
    return

def parse_typeB(line, lineNumber):
    if len(line) != 3:
        error(1, lineNumber)
    if line[1] not in registers.values():
        error(1, lineNumber, line[1])
    if line[2][0] == '$': 
        if int(line[2][1:]) > 255:
            error(5, lineNumber, line[2])
        elif int(line[2][1:]) < 0:
            error(5, lineNumber, line[2])
    elif line[0] == 'mov':
        parse_typeC(line, lineNumber)
    return

def parse_typeC(line, lineNumber):
    if len(line) != 3:
        error(3, lineNumber)
    for i in range(1, 3):
        if line[i] not in registers.values():
            error(1, lineNumber, line[i])
    return

def parse_typeD(line, lineNumber):
    if len(line) != 3:
        error(1, lineNumber)
    if line[1] not in registers.values():
        error(1, lineNumber, line[1])
    if line[2] not in programVariables:
        error(1, lineNumber, line[2])
    return

def parse_typeE(line, lineNumber):
    if len(line) != 2:
        error(1, lineNumber)
    if line[1][0:-1] not in programLabels:
        error(3, lineNumber)
    return

def parse_label(line, lineNumber):
    label = line[0][0:-1];
    if(label not in programLabels):
        programLabels.append(line[0][0:-1])
    else:
        error(3, lineNumber, label)
    return 

def parse():
    lineCount = 0
    while(instructions[lineCount][0] == "var"):
        if(len(instructions[lineCount]) != 2):
            error(2, lineCount)
        programVariables.append(instructions[lineCount][1])
        lineCount += 1

    if(instructions[-1][0] != "hlt" or len(instructions[-1]) != 1):
        error(9, totalLines-1, '')

    for i in range(lineCount, totalLines-1):
        line = instructions[i]
        if line[0][-1] == ':':
            parse_label(line, i)
        if len(line) > 0 and line[0] not in opcodes.values():
            error(1, lineCount)
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
print(programLabels)
