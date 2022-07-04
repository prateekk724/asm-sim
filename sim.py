#!/bin/python
from sys import stdin

# Crate and initialize registers.
REG = {
    'R0' : '0000000000000000',
    'R1' : '0000000000000000',
    'R2' : '0000000000000000',
    'R3' : '0000000000000000',
    'R4' : '0000000000000000',
    'R5' : '0000000000000000',
    'R6' : '0000000000000000',
    'FLAGS' : '0000000000000000'
}

# Create and initialize virtual memory.
MEM = dict()
for i in range(0, 256):
    MEM[i] = '0'*16

# Initialize program counter and halt status.
PC = '00000000'
HLT = False

# Load the machine code into memory.
def initializeMEM():
    i = 0
    for line in stdin:
        if line != '':
            MEM[i] = line[:-1]
            i += 1
        else: break
    return True

def getMEM(address):
   location = int(address, 2) 
   return MEM[location]

def regFile(regName):
    return REG[regName]

def dumpPC():
    print(PC, end=' ')
    return True

def dumpRF():
    for regval in REG.values():
        print(regval, end=' ')
    print()
    return True

def execEngine(instruction):
    global HLT
    if instruction[:5] == '01010':
        HLT = True
    else:
        return (bin(int(PC, 2)+1)[2:]).rjust(8, '0')

if __name__ == "__main__":
    initializeMEM()

    while(not HLT):
        instruction = getMEM(PC)
        new_PC = execEngine(instruction)
        dumpPC()
        dumpRF()
        PC = new_PC

    for cell in MEM.values():
        print(cell)
