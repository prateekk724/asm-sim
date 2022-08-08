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
        case 'b': mul = 0.125
        case 'B': mul = 1
    return mem_bytes * (1024)**exp * mul

def getMemSize(mem_bytes):
    scaleFactor = 0
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    while(mem_bytes > 1024.0 and scaleFactor < 5):
        mem_bytes = mem_bytes / 1024
        scaleFactor = scaleFactor + 1
    return [str(mem_bytes), units[scaleFactor]]

# instruction formats.
# Type A: <Q bit opcode><-------P bit address--------><X bit register>
# Type B: <Q bit opcode><R bit filler><X bit register><X bit register>
def typeA():
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
    print("Maximum number of instructions supported by ISA : ", 2**opcodeSize)
    print("Maximum number of registers supported by ISA : ", 2**registerLength)

def typeB1():
    memorySize = input("Memory size (e.g. 16 GB) : ").split()
    addressableType = input("Addressable type : ")
    cpuBits = int(input("CPU bits : "))
    newAddressableType = input("New Addressable type : ")
    supportedAddrTypes = {"bit" : 1, "nibble" : 4, "byte" : 8, "word" : cpuBits}
    memoryBits = getBytes(memorySize) * 8 
    scaleFactor = supportedAddrTypes[addressableType] / supportedAddrTypes[newAddressableType]
    return ceil(log2(scaleFactor))

def typeB2():
    cpuBits = int(input("CPU bits : "))
    addressPins = int(input("Number of address Pins : "))
    addressableType = input("Addressable type : ")
    supportedAddrTypes = {"bit" : 1, "nibble" : 4, "byte" : 8, "word" : cpuBits}
    memorySize = 2**addressPins * supportedAddrTypes[addressableType] * 0.125
    return getMemSize(memorySize)

# Program driver
choice = int(input("Enter type: "))
if choice == 1:
    typeA()
elif choice == 2:
    subchoice = int(input("Enter subtype: "))
    if subchoice == 1:
        print("Result:", typeB1())
    elif subchoice == 2:
        print("Result:", ' '.join(typeB2()))
    else:
        print("Invalid choice!")
else:
    print("Invalid choice!")
