from math import log2
from math import ceil

def getBytes(mem_size):
    mem_bytes = int(mem_size[0])
    size_factor = mem_size[1]
    if size_factor in ['bit', 'bits']:
        return mem_bytes * 0.125
    if size_factor in ['byte', 'bytes']:
        return mem_bytes
    exp = 0
    mul = 1
    match size_factor[0]:
        case 'K'|'k' : exp = 1
        case 'M'|'m' : exp = 2
        case 'G'|'g' : exp = 3
    match size_factor[1]:
        case 'b': mul = 8
        case 'B': mul = 1
    return mem_bytes * (1024)**exp * mul

# instruction formats.
# Type A: <Q bit opcode><-------P bit address--------><X bit register>
# Type B: <Q bit opcode><R bit filler><X bit register><X bit register>

memorySize = input("Memory size (e.g. 16 GB) : ").split()
addressableType = input("Addressable type : ")
instructionLength = int(input("Instruction length (bits) : "))
registerLength = int(input("Register length (bits) : "))

memoryBytes = getBytes(memorySize)
memoryAddressLength = ceil(log2(memoryBytes))
opcodeSize = instructionLength - (memoryAddressLength + registerLength)
fillerSize = instructionLength - (opcodeSize + (2 * registerLength))
print("="*25)
print("Minimum bits needed to represent an address : ", memoryAddressLength)
print("Bits needed for opcode : ", opcodeSize)
print("Filler bits in type 2 instruction : ", fillerSize)
print("Maxiumum number of instructions supported by ISA : ", 2**opcodeSize)
print("Maxiumum number of registers supported by ISA : ", 2**registerLength)
