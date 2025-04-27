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
  'SLL' :0b001,
  'SLT' :0b010,
  'SLTU' :0b011,
  'XOR' :0b100,
  'SRL_SRA' :0b101,
  'OR' :0b110,
  'AND' :0b111,
  'WORD' :0b010,
}
fp_opcodes = {
    'FADD_S': 0b1010011,  # Floating-point add single-precision
    'FSUB_S': 0b1010011,  # Floating-point subtract single-precision
    'FMUL_S': 0b1010011,  # Floating-point multiply single-precision
    'FDIV_S': 0b1010011,  # Floating-point divide single-precision
}