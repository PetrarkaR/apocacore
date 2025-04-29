#!/usr/bin/env python

""" ALL OF THE ISA CODES WILL BE IN HERE"""

opCodes = {
  'LUI'     :0b0110111,
  'AUIPC'   :0b0010111,
  'JAL'     :0b1101111,
  'JALR'    :0b1100111,
  'BRANCH'  :0b1100011,
  'LOAD'    :0b0000011,
  'STORE'   :0b0100011,
  'ALU_IMM' :0b0010011,
  'ALU_REG' :0b0110011,
}

funct3_codes={
  'ADD_SUB' :0b000,
  'SLL'     :0b001,
  'SLT'     :0b010,
  'SLTU'    :0b011,
  'XOR'     :0b100,
  'SRL_SRA' :0b101,
  'OR'      :0b110,
  'AND'     :0b111,
  'WORD'    :0b010,
  'BYTE'    :0B000,
  'HALF'    :0B001,
  'BYTE_U'  :0B100,
  'HALF_U'  :0B101,
  'BEQ'     :0B000,
  'BNE'     :0B001,
  'BLT'     :0B100,
  'BGE'     :0B101,
  'BLTU'    :0B110,
  'BGEU'    :0B111,
}
funct7_codes={
  'STANDARD':0b0000000,
  'SUB'     :0b0100000,
  'SRA'     :0b0100000,
  'MUL'     :0b0000001,
}
fp_opcodes = {
    'FADD_S': 0b1010011,  # Floating-point add single-precision
    'FSUB_S': 0b1010011,  # Floating-point subtract single-precision
    'FMUL_S': 0b1010011,  # Floating-point multiply single-precision
    'FDIV_S': 0b1010011,  # Floating-point divide single-precision
}
instruction_map = {
    # R-type instructions (ALU operations with registers)
    'ADD': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['ADD_SUB'], 'funct7': funct7_codes['STANDARD']},
    'SUB': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['ADD_SUB'], 'funct7': funct7_codes['SUB']},
    'SLL': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLL'], 'funct7': funct7_codes['STANDARD']},
    'SLT': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLT'], 'funct7': funct7_codes['STANDARD']},
    'SLTU': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLTU'], 'funct7': funct7_codes['STANDARD']},
    'XOR': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['XOR'], 'funct7': funct7_codes['STANDARD']},
    'SRL': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SRL_SRA'], 'funct7': funct7_codes['STANDARD']},
    'SRA': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SRL_SRA'], 'funct7': funct7_codes['SRA']},
    'OR': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['OR'], 'funct7': funct7_codes['STANDARD']},
    'AND': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['AND'], 'funct7': funct7_codes['STANDARD']},
    
    # R-type instructions (M extension)
    'MUL': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['ADD_SUB'], 'funct7': funct7_codes['MUL']},
    'MULH': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLL'], 'funct7': funct7_codes['MUL']},
    'MULHSU': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLT'], 'funct7': funct7_codes['MUL']},
    'MULHU': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SLTU'], 'funct7': funct7_codes['MUL']},
    'DIV': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['XOR'], 'funct7': funct7_codes['MUL']},
    'DIVU': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['SRL_SRA'], 'funct7': funct7_codes['MUL']},
    'REM': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['OR'], 'funct7': funct7_codes['MUL']},
    'REMU': {'opcode': opCodes['ALU_REG'], 'funct3': funct3_codes['AND'], 'funct7': funct7_codes['MUL']},
    
    # I-type instructions (ALU operations with immediates)
    'ADDI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['ADD_SUB']},
    'SLTI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['SLT']},
    'SLTIU': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['SLTU']},
    'XORI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['XOR']},
    'ORI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['OR']},
    'ANDI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['AND']},
    'SLLI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['SLL'], 'funct7': funct7_codes['STANDARD']},
    'SRLI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['SRL_SRA'], 'funct7': funct7_codes['STANDARD']},
    'SRAI': {'opcode': opCodes['ALU_IMM'], 'funct3': funct3_codes['SRL_SRA'], 'funct7': funct7_codes['SRA']},
    
    # I-type instructions (Loads)
    'LB': {'opcode': opCodes['LOAD'], 'funct3': funct3_codes['BYTE']},
    'LH': {'opcode': opCodes['LOAD'], 'funct3': funct3_codes['HALF']},
    'LW': {'opcode': opCodes['LOAD'], 'funct3': funct3_codes['WORD']},
    'LBU': {'opcode': opCodes['LOAD'], 'funct3': funct3_codes['BYTE_U']},
    'LHU': {'opcode': opCodes['LOAD'], 'funct3': funct3_codes['HALF_U']},
    
    # I-type instructions (JALR)
    'JALR': {'opcode': opCodes['JALR'], 'funct3': 0b000},
    
    # S-type instructions (Stores)
    'SB': {'opcode': opCodes['STORE'], 'funct3': funct3_codes['BYTE']},
    'SH': {'opcode': opCodes['STORE'], 'funct3': funct3_codes['HALF']},
    'SW': {'opcode': opCodes['STORE'], 'funct3': funct3_codes['WORD']},
    
    # B-type instructions (Branches)
    'BEQ': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BEQ']},
    'BNE': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BNE']},
    'BLT': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BLT']},
    'BGE': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BGE']},
    'BLTU': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BLTU']},
    'BGEU': {'opcode': opCodes['BRANCH'], 'funct3': funct3_codes['BGEU']},
    
    # U-type instructions
    'LUI': {'opcode': opCodes['LUI']},
    'AUIPC': {'opcode': opCodes['AUIPC']},
    
    # J-type instructions
    'JAL': {'opcode': opCodes['JAL']},
}
