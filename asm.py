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
programVariables = dict()
programLabels = dict()
totalInstructions = totalLines - len(programVariables)

# machine code
machineCode = list()

# Error Handler to prevent repetition of same error printing
# in multiple functions.
def error(code, line, object = ''):
    if object != '':
        print("ERROR: " + errors[code] + " -> '" + object + "'")
    else:
        print("ERROR: " + errors[code])
    print(f"--> {line+1}: " + codeLines[line])
    return 

# Parsers for instructions of type A to E
# throw errors if instructions are invalid.
def parse_typeA(line, lineNumber):
    if len(line) != 4:
        error(1, lineNumber)
    line[0] = opcodes[line[0]] + '00' # 2-bit padding
    for i in range(1, 4):
        if line[i] not in registers.keys():
            error(1, lineNumber, line[i])
        else:
            line[i] = registers[line[i]]
    return ''.join(line)

def parse_typeB(line, lineNumber):
    if len(line) != 3:
        error(1, lineNumber)
    if line[2][0] == '$': 
        if line[0] == 'mov':
            line[0] = '10010'
        else:
            line[0] = opcodes[line[0]]
        if line[1] not in registers.keys():
            error(1, lineNumber, line[1])
        else:
            line[1] = registers[line[1]]
        if int(line[2][1:]) > 255:
            error(5, lineNumber, line[2])
        elif int(line[2][1:]) < 0:
            error(5, lineNumber, line[2])
        else:
            line[2] = bin((int)(line[2][1:]))[2:].zfill(8)
        return ''.join(line)
    elif line[0] == 'mov':
        return parse_typeC(line, lineNumber)

def parse_typeC(line, lineNumber):
    if len(line) != 3:
        error(3, lineNumber)
    line[0] = opcodes[line[0]] + '00000' # 5-bit padding
    for i in range(1, 3):
        if line[i] not in registers.keys():
            error(1, lineNumber, line[i])
        else:
            line[i] = registers[line[i]]
    return ''.join(line)

def parse_typeD(line, lineNumber):
    if len(line) != 3:
        error(1, lineNumber)
    line[0] = opcodes[line[0]]
    if line[1] not in registers.keys():
        error(1, lineNumber, line[1])
    else:
        line[1] = registers[line[1]];
    if line[2] not in programVariables.keys():
        error(1, lineNumber, line[2])
    else:
        line[2] = programVariables[line[2]]
    return ''.join(line)

def parse_typeE(line, lineNumber):
    if len(line) != 2:
        error(1, lineNumber)
    line[0] = opcodes[line[0]] + '000' # 3-bit padding
    if line[1][0:-1] not in programLabels.keys():
        error(3, lineNumber)
    else:
        line[1] = programLabels[line[1]]
    return ''.join(line)

def parse_label(line, lineNumber):
    label = line[0][0:-1];
    if(label not in programLabels):
        programLabels[line[0][0:-1]] = bin(lineNumber)[2:].zfill(8)
    else:
        error(3, lineNumber, label)
    return 

def assemble():
    lineCount = 0
    while(instructions[lineCount][0] == "var"):
        if(len(instructions[lineCount]) != 2):
            error(2, lineCount)
        else:
            programVariables[instructions[lineCount][1]] = bin(lineCount+totalInstructions-1)[2:].zfill(8)
        lineCount += 1
    for i in range(lineCount, totalLines-1):
        line = instructions[i]
        if line[0][-1] == ':':
            parse_label(line, i)
        machineInstruction = ''
        if len(line) > 0 and line[0] not in opcodes.keys():
            error(1, lineCount)
        elif line[0] in instructionType['A']:
            machineInstruction = parse_typeA(line, i)
        elif line[0] in instructionType['B']:
            machineInstruction = parse_typeB(line, i)
        elif line[0] in instructionType['C']:
            machineInstruction = parse_typeC(line, i)
        elif line[0] in instructionType['D']:
            machineInstruction = parse_typeD(line, i)
        elif line[0] in instructionType['E']:
            machineInstruction = parse_typeE(line, i)
        # TODO: check and impliment if machineInstruction validation is necessary
        machineCode.append(machineInstruction)
    if(instructions[-1][0] != "hlt" or len(instructions[-1]) != 1):
        error(9, totalLines-1, '')
    else:
        machineCode.append(opcodes[instructions[-1][0]].ljust(16, '0'))
    return True

assemble()
for machineInstruction in machineCode:
    print(machineInstruction)
