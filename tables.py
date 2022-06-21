opcodes = {
#   opcode  : instrxn   type    syntax                  semantic
    '10000' : 'add',    # A     add reg1 reg2 reg3      reg3 = reg1 + reg2
    '10001' : 'sub',    # A     sub reg1 reg2 reg3      reg3 = reg1 - reg2
    '10010' : 'mov',    # B     mov reg1 $Imm           reg1 = $Imm
    '10011' : 'mov',    # C     mov reg1 reg2           reg2 = reg1
    '10100' : 'ld',     # D     ld reg1 mem_addr        reg1 = [mem_addr]
    '10101' : 'st',     # D     st reg1 mem_addr        [mem_addr] = reg1
    '10110' : 'mul',    # A     mul reg1 reg2 reg3      reg3 = reg1 * reg2
    '10111' : 'div',    # C     div reg3 reg4           R0 = reg3 / reg4, R1 = reg3 % reg4
    '11000' : 'rs',     # B     rs reg1 $Imm            reg1 = reg1 >> $Imm
    '11001' : 'ls',     # B     ls reg1 $Imm            reg1 = reg1 << $Imm
    '11010' : 'xor',    # A     xor reg1 reg2 reg3      reg3 = reg1 XOR reg2
    '11011' : 'or',     # A     or reg1 reg2 reg3       reg3 = reg1 OR reg2
    '11100' : 'and',    # A     and reg1 reg2 reg3      reg3 = reg1 AND reg2
    '11101' : 'not',    # C     not reg1 reg2           reg2 = NOT reg1
    '11110' : 'cmp',    # C     cmp reg1 reg2           FLAGS = reg1 CMP reg2
    '11111' : 'jmp',    # E     jmp mem_addr
    '01100' : 'jlt',    # E     jlt mem_addr
    '01101' : 'jgt',    # E     jgt mem_addr
    '01111' : 'je',     # E     je mem_addr
    '01010' : 'hlt'     # F     hlt
}

instructionType = {
    'A' : ['add', 'sub', 'mul', 'or', 'xor', 'and'],
    'B' : ['mov', 'rs', 'ls'],
    'C' : ['mov', 'div', 'not', 'cmp'],
    'D' : ['ld', 'st'],
    'E' : ['jmp', 'jlt', 'jgt', 'je'],
}

registers = {
#   addr  : name
    '000' : 'R0',
    '001' : 'R1',
    '010' : 'R2',
    '011' : 'R3',
    '100' : 'R4',
    '101' : 'R5',
    '110' : 'R6',
    '111' : 'FLAGS'
}

errors = {
    '01' : 'Typo in instruction name or register.',
    '02' : 'Use of undefined variable.',
    '03' : 'Use of undefined label.',
    '04' : 'Illegal use of FLAG register.',
    '05' : 'Illegal immediate value (more than 8 bits).',
    '06' : 'Misuse of label as variable or vice versa.',
    '07' : 'Variables not declared at the beginning.',
    '08' : 'Missing hlt instruction.',
    '09' : 'Last instruction is not hlt.'
}
