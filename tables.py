opcodes = {
#   opcode  : instrxn   type    syntax                  semantic
    'add' : '10000',    # A     add reg1 reg2 reg3      reg3 = reg1 + reg2
    'sub' : '10001',    # A     sub reg1 reg2 reg3      reg3 = reg1 - reg2
    'mov' : '10010',    # B     mov reg1 $Imm           reg1 = $Imm
    'mov' : '10011',    # C     mov reg1 reg2           reg2 = reg1
    'ld'  : '10100',    # D     ld reg1 mem_addr        reg1 = [mem_addr]
    'st'  : '10101',    # D     st reg1 mem_addr        [mem_addr] = reg1
    'mul' : '10110',    # A     mul reg1 reg2 reg3      reg3 = reg1 * reg2
    'div' : '10111',    # C     div reg3 reg4           R0 = reg3 / reg4, R1 = reg3 % reg4
    'rs'  : '11000',    # B     rs reg1 $Imm            reg1 = reg1 >> $Imm
    'ls'  : '11001',    # B     ls reg1 $Imm            reg1 = reg1 << $Imm
    'xor' : '11010',    # A     xor reg1 reg2 reg3      reg3 = reg1 XOR reg2
    'or'  : '11011',    # A     or reg1 reg2 reg3       reg3 = reg1 OR reg2
    'and' : '11100',    # A     and reg1 reg2 reg3      reg3 = reg1 AND reg2
    'not' : '11101',    # C     not reg1 reg2           reg2 = NOT reg1
    'cmp' : '11110',    # C     cmp reg1 reg2           FLAGS = reg1 CMP reg2
    'jmp' : '11111',    # E     jmp mem_addr
    'jlt' : '01100',    # E     jlt mem_addr
    'jgt' : '01101',    # E     jgt mem_addr
    'je'  : '01111',    # E     je mem_addr
    'hlt' : '01010'     # F     hlt
}

instructionType = {
    'A' : ['add', 'sub', 'mul', 'or', 'xor', 'and'],
    'B' : ['mov', 'rs', 'ls'],
    'C' : ['mov', 'div', 'not', 'cmp'],
    'D' : ['ld', 'st'],
    'E' : ['jmp', 'jlt', 'jgt', 'je'],
    'F' : ['hlt']
}

registers = {
#   addr  : name
    'R0' : '000',
    'R1' : '001',
    'R2' : '010',
    'R3' : '011',
    'R4' : '100',
    'R5' : '101',
    'R6' : '110',
   'FLAGS' : '111'
}

errors = {
    1 : 'Typo/misuse of instruction name or register.',
    2 : 'Use of undefined variable.',
    3 : 'Use of undefined label.',
    4 : 'Illegal use of FLAG register.',
    5 : 'Illegal immediate value (more than 8 bits).',
    6 : 'Misuse of label as variable or vice versa.',
    7 : 'Variables not declared at the beginning.',
    8 : 'Missing hlt instruction.',
    9 : 'Last instruction is not hlt.',
    10: 'Illegal use of variable or Label name',
    11: 'Assembly code cannot be accomodated in memory'
}

keywords = ['add', 'sub', 'mul', 'or', 'xor', 'and', 'mov', 'rs', 'ls', 'mov', 'div', 'not', 'cmp', 'ld', 'st', 'jmp', 'jlt', 'jgt', 'je', 'hlt', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']
