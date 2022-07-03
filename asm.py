#!/bin/python
from sys import stdin
from tables import *

# Read input file and convert the instructions
# to a format that is easy to handle.
instructions = dict()
srcCode = dict()
lineCount = 0
for line in stdin:
    if line == '':
        break
    else:
        codeLine = line[:-1]
        instructions[lineCount] = codeLine.split()
        srcCode[lineCount] = codeLine.split()
        lineCount += 1

# source code data
programVariables = dict()
programLabels = dict()

# machine code
machineCode = list()

# Error Handler to prevent repetition of same error printing
# in multiple functions.
errorCount = 0
def error(code, line, object = ''):
    global errorCount
    errorCount += 1
    if object != '':
        print("ERROR: " + errors[code] + " -> '" + object + "'")
    else:
        print("ERROR: " + errors[code])
    print(f"--> {line+1}: " + ' '.join(srcCode[line]))
    return 

# Parsers for instructions of type A to E
# throw errors if instructions are invalid.
def parse_typeA(line, lineNumber):
    if len(line) != 4:
        error(1, lineNumber)
    line[0] = opcodes[line[0]] + '00' # 2-bit padding
    for i in range(1, len(line)):
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
            line[2] = bin((int)(line[2][1:]))[2:].rjust(8, '0')
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
    if line[1] not in programLabels.keys():
        error(3, lineNumber)
    else:
        line[1] = programLabels[line[1]]
    return ''.join(line)

def parse_typeF(line, lineNumber):
    if len(line) != 1:
        error(1, lineNumber)
    line[0] = opcodes[line[0]].ljust(16, '0')
    return ''.join(line)

def parse_label(line, lineNumber):
    label = line[0][0:-1]
    if(label not in programLabels):
        programLabels[line[0][0:-1]] = bin(lineNumber)[2:].rjust(8, '0')
    else:
        error(3, lineNumber, label)
    return 

def assemble():
    # Variable Handling
    variableLineNumbers = list()
    for i, line in instructions.items():
        if line[0] == 'var':
            if len(line) != 2:
                error(1, i)
            else:
                programVariables[line[1]] = 'null'
                variableLineNumbers.append(i)
        else:
            break
    for lineNumber in variableLineNumbers:
        instructions.pop(variableLineNumbers[lineNumber])

    totalInstructions = len(instructions)
    variableNames = list(programVariables.keys())
    instructionLineNumbers = list(instructions.keys())
    for i in range(len(variableNames)):
        programVariables[(variableNames[i])] = bin(totalInstructions+i)[2:].rjust(8, '0')

    # Label Handling
    for i, line in instructions.items():
        if line[0][-1] == ':' :
            if len(line) > 1:
                if line[0][:-1] not in programLabels.keys():
                    programLabels[line[0][:-1]] = bin(instructionLineNumbers.index(i))[2:].rjust(8, '0') 
                    instructions[i] = line[1:]
                else:
                    error(3, i)

    # Instruction handling
    for i, line in instructions.items():
        machineInstruction = ''
        if line[0] not in opcodes.keys():
            # TODO: add error subcases.
            error(1, i)
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
        elif line[0] in instructionType['F']:
            machineInstruction = parse_typeF(line, i)
        machineCode.append(machineInstruction)
    return

if __name__ == '__main__':
    assemble()
    #print(f"Total errors: {errorCount}")
    if errorCount == 0:
        for machineInstruction in machineCode:
            print(machineInstruction)
