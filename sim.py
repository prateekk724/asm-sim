#!/bin/python
from sys import stdin
from tables import *

# Crate and initialize registers.
reg = {
    '000' : '0000000000000000',
    '001' : '0000000000000000',
    '010' : '0000000000000000',
    '011' : '0000000000000000',
    '100' : '0000000000000000',
    '101' : '0000000000000000',
    '110' : '0000000000000000',
    '111' : '0000000000000000'
}

# Create and initialize virtual memory.
mem = dict()
for i in range(0, 256):
    mem[i] = '0'*16

# Initialize program counter and halt status.
# pc = '00000000'
halt = False

# Load the machine code into memory.
def initializemem():
    i = 0
    for line in stdin:
        if line != '':
            mem[i] = line[:-1]
            i += 1
        else: break
    return True

def getmem(address):
   location = int(address, 2) 
   return mem[location]

def regFile(regName):
    return reg[regName]

def dumppc():
    print(pc, end=' ')
    return True

def dumpRF():
    for regval in reg.values():
        print(regval, end=' ')
    print()
    return True

def execEngine(instruction):
    global halt
    opcode = instruction[:5]
    if opcode in instructionOpcode['A']:
        overflow = 0
        reg1 = regFile(instruction[7:10])
        reg2 = regFile(instruction[10:13])
        reg3 = instruction[13:]
        if opcode == '10000': # add
            sum = int(reg1, 2) + int(reg2, 2)
            if sum > 2**17-1:
                sum = 2**17-1
                overflow = 1
            reg[reg3] = bin(sum)[2:].rjust(16, '0')
        elif opcode == '10001': # sub
            sub = int(reg1, 2) - int(reg2, 2)
            if sub < 0:
                sub = 0
                overflow = 1
            reg[reg3] = bin(sub)[2:].rjust(16, '0')
        elif opcode == '10110': # mul
            mul = int(reg1, 2) * int(reg2, 2)
            if mul > 2**17-1:
                mul = 2**17-1
                overflow = 1
            reg[reg3] = bin(mul)[2:].rjust(16, '0')
        elif opcode == '11011': # or
            resor = int(reg1, 2) | int(reg2, 2)
            reg[reg3] = bin(resor)[2:].rjust(16, '0')
        elif opcode == '11010': # xor
            resxor = int(reg1, 2) ^ int(reg2, 2)
            reg[reg3] = bin(resxor)[2:].rjust(16, '0')
        elif opcode == '11100': # and
            resand = int(reg1, 2) & int(reg2, 2)
            reg[reg3] = bin(resand)[2:].rjust(16, '0')
        if overflow:
            reg['111'] = reg['111'][0:12] + '1' + reg['111'][13:]
        else:
            reg['111'] = reg['111'][0:12] + '0' + reg['111'][13:]
    elif opcode in instructionOpcode['B']:
        reg1 = instruction[5:8]
        imm = int(instruction[8:], 2)
        if opcode == '10010': # mov
            reg[reg1] = instruction[8:].rjust(16, '0')
        elif opcode == '11000': # rs
            if imm >= 16:
                reg[reg1] = '0000000000000000'
            else:
                reg[reg1] = reg[reg1][:-imm].rjust(16, '0')
        elif opcode == '11001': # ls
            if imm >= 16:
                reg[reg1] = '0000000000000000'
            else:
                reg[reg1] = reg[reg1][imm:].ljust(16, '0')
    elif opcode in instructionOpcode['C']:
        reg1 = regFile(instruction[10:13])
        reg2 = regFile(instruction[13:])
        if opcode == '10011': # mov
            reg[instruction[13:]] =  reg1
        elif opcode == '10111': # div
            reg['000'] = bin(int((int(reg1, 2) / int(reg2, 2))))[2:].rjust(16, '0')
            reg['001'] = bin((int(reg1, 2) % int(reg2, 2)))[2:].rjust(16, '0')
        elif opcode == '11101': # not 
            reg[instruction[13:]] = bin((~ int(reg1, 2)))[2:].rjust(16, '0')
        elif opcode == '11110': #cmp
            if int(reg1, 2) < int(reg2, 2):
                reg['111'] = reg['111'][0:13] + '100'
            elif int(reg1, 2) > int(reg2, 2):
                reg['111'] = reg['111'][0:13] + '010'
            else:
                reg['111'] = reg['111'][0:13] + '001'
    elif opcode in instructionOpcode['D']:
        addr = int(instruction[8:], 2)
        if opcode == '10110': # ld
            reg[instruction[5:8]] = getmem(addr)
        elif opcode == '10101': # st
            mem[addr] = reg[instruction[5:8]]
    elif opcode in instructionOpcode['E']:
        addr = instruction[8:].rjust(8, '0')
        if opcode == '11111': # jmp
            return addr
        elif opcode == '01100' and reg['111'][13] == '1':   # jlt
            return addr
        elif opcode == '01101' and reg['111'][15] == '1':   # jgt
            return addr
        elif opcode == '01111' and reg['111'][14] == '1':   # je
            return addr
    elif opcode in instructionOpcode['F']:
        halt = True

    return bin(int(pc, 2) + 1)[2:].rjust(8, '0')

if __name__ == "__main__":
    initializemem()
    global pc
    pc = '00000000'
    while(not halt):
        instruction = getmem(pc)
        new_pc = execEngine(instruction)
        dumppc()
        dumpRF()
        pc = new_pc

    for cell in mem.values():
        print(cell)
