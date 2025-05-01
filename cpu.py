#!/usr/bin/env python
from constants import *
import typing
from exec import InstructionHandlers
class ApocaCore:
  def __init__(self,memory_size=1024):
    self.registers = [0]*16
    self.f_registers =[0.0]*16 
    self.pc=0
    self.memory=[0]*memory_size
    self.build_map()
    self.VLEN = 64
    self.MAX_SEW=8
    self.LMUL=1
    self.vl=0
    self.vtype = {'SEW':32,'LMUL':1}
    self.vreg= [[0]*(self.VLEN//self.vtype['SEW']) for _ in range(16)]
    self.next_address=0


  def build_map(self):
    handlers=InstructionHandlers()
    self.dispatch = {
            # Special case for NOP
            (0, 0, 0): handlers.exec_nop,
            
            # R-type instructions
            # ALU operations
            (opCodes['ALU_REG'], funct3_codes['ADD_SUB'], funct7_codes['STANDARD']): handlers.exec_add,
            (opCodes['ALU_REG'], funct3_codes['ADD_SUB'], funct7_codes['SUB']): handlers.exec_sub,
            (opCodes['ALU_REG'], funct3_codes['SLL'], funct7_codes['STANDARD']): handlers.exec_sll,
            (opCodes['ALU_REG'], funct3_codes['SLT'], funct7_codes['STANDARD']): handlers.exec_slt,
            (opCodes['ALU_REG'], funct3_codes['SLTU'], funct7_codes['STANDARD']): handlers.exec_sltu,
            (opCodes['ALU_REG'], funct3_codes['XOR'], funct7_codes['STANDARD']): handlers.exec_xor,
            (opCodes['ALU_REG'], funct3_codes['SRL_SRA'], funct7_codes['STANDARD']): handlers.exec_srl,
            (opCodes['ALU_REG'], funct3_codes['SRL_SRA'], funct7_codes['SRA']): handlers.exec_sra,
            (opCodes['ALU_REG'], funct3_codes['OR'], funct7_codes['STANDARD']): handlers.exec_or,
            (opCodes['ALU_REG'], funct3_codes['AND'], funct7_codes['STANDARD']): handlers.exec_and,
            
            # I-type instructions
            # ALU operations with immediates
            (opCodes['ALU_IMM'], funct3_codes['ADD_SUB'], None): handlers.exec_addi,
            (opCodes['ALU_IMM'], funct3_codes['SLT'], None): handlers.exec_slti,
            (opCodes['ALU_IMM'], funct3_codes['SLTU'], None): handlers.exec_sltiu,
            (opCodes['ALU_IMM'], funct3_codes['XOR'], None): handlers.exec_xori,
            (opCodes['ALU_IMM'], funct3_codes['OR'], None): handlers.exec_ori,
            (opCodes['ALU_IMM'], funct3_codes['AND'], None): handlers.exec_andi,
            
            # Shifts with immediates (these might have funct7 values in some implementations)
            (opCodes['ALU_IMM'], funct3_codes['SLL'], None): handlers.exec_slli,
            (opCodes['ALU_IMM'], funct3_codes['SRL_SRA'], 0b0000000): handlers.exec_srli,
            (opCodes['ALU_IMM'], funct3_codes['SRL_SRA'], 0b0100000): handlers.exec_srai,
            
            # Load instructions
            (opCodes['LOAD'], funct3_codes['BYTE'], None): handlers.exec_lb,
            (opCodes['LOAD'], funct3_codes['HALF'], None): handlers.exec_lh,
            (opCodes['LOAD'], funct3_codes['WORD'], None): handlers.exec_lw,
            (opCodes['LOAD'], funct3_codes['BYTE_U'], None): handlers.exec_lbu,
            (opCodes['LOAD'], funct3_codes['HALF_U'], None): handlers.exec_lhu,
            
            # Store instructions
            (opCodes['STORE'], funct3_codes['BYTE'], None): handlers.exec_sb,
            (opCodes['STORE'], funct3_codes['HALF'], None): handlers.exec_sh,
            (opCodes['STORE'], funct3_codes['WORD'], None): handlers.exec_sw,
            
            # Branch instructions
            (opCodes['BRANCH'], funct3_codes['BEQ'], None): handlers.exec_beq,
            (opCodes['BRANCH'], funct3_codes['BNE'], None): handlers.exec_bne,
            (opCodes['BRANCH'], funct3_codes['BLT'], None): handlers.exec_blt,
            (opCodes['BRANCH'], funct3_codes['BGE'], None): handlers.exec_bge,
            (opCodes['BRANCH'], funct3_codes['BLTU'], None): handlers.exec_bltu,
            (opCodes['BRANCH'], funct3_codes['BGEU'], None): handlers.exec_bgeu,
            
            # Jump instructions
            (opCodes['JAL'], None, None): handlers.exec_jal,
            (opCodes['JALR'], 0b000, None): handlers.exec_jalr,
            
            # U-type instructions
            (opCodes['LUI'], None, None): handlers.exec_lui,
            (opCodes['AUIPC'], None, None): handlers.exec_auipc,

            (opCodes['VECTOR'], funct3_codes['WORD'], funct6_codes['STORE']): handlers.exec_vs
        }
  def run(self):
    for i in range(1024):  # Safety limit
      while self.pc < self.program_length:
            ins = self.fetch()
            decoded = self.decode(ins)
            self.execute(*decoded)
  def load_memory(self, memory_vectors):
    base_address = 512
    for i, vector in enumerate(memory_vectors):  # each vector is a list of values
        for j, val in enumerate(vector):
            address = base_address + (i * len(vector) + j) * 8  # each value is 8 bytes
            self.write_memory(address, int(val, 0) if isinstance(val, str) else val, 8)

  def load_program(self,program):
    self.memory[:len(program)] = program
    self.program_length = len(program)

  def fetch(self):
    instruction = self.memory[self.pc]
    self.pc+=1
    return instruction
  def decode(self, instruction):
    opcode = instruction & 0x7F
    rd = (instruction >> 7) & 0x1F
    funct3_codes = (instruction >> 12) & 0x7
    rs1 = (instruction >> 15) & 0x1F
    rs2 = (instruction >> 20) & 0x1F
    funct7 = (instruction >> 25) & 0x7F
    
    if opcode == opCodes['ALU_IMM'] or opcode == opCodes['LOAD'] or opcode == opCodes['JALR']:
        imm = (instruction >> 20) if (instruction >> 31) == 0 else (instruction >> 20) | 0xFFFFF000
    elif opcode == opCodes['VECTOR']:
        # vector-format: funct6[31:26], vs2[20:16], vs1[15:11], vm[25], vd[11:7], funct3[14:12]
        funct6 = (instruction >> 26) & 0x3F
        vs2     = (instruction >> 20) & 0x1F
        vs1     = (instruction >> 15) & 0x1F
        vm      = (instruction >> 25) & 0x1
        vd      = (instruction >> 7)  & 0x1F
        funct3  = (instruction >> 12) & 0x7
        return (opcode, vd, vs1, vs2, vm, funct6, funct3)
    elif opcode == opCodes['STORE']:
        imm_11_5 = (instruction >> 25) & 0x7F
        imm_4_0 = (instruction >> 7) & 0x1F
        imm = (imm_11_5 << 5) | imm_4_0
        if (imm_11_5 >> 6) & 1:  # Sign extend
            imm |= 0xFFFFF000
    elif opcode == opCodes['BRANCH']:
        imm_12 = (instruction >> 31) & 0x1
        imm_11 = (instruction >> 7) & 0x1
        imm_10_5 = (instruction >> 25) & 0x3F
        imm_4_1 = (instruction >> 8) & 0xF
        imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
        if imm_12:  # Sign extend
            imm |= 0xFFFFE000
    else:
        # Default case (includes LUI, AUIPC which have upper immediate)
        imm = instruction >> 20
        
    return opcode, rd, funct3_codes, rs1, rs2, funct7, imm
  def execute(self, opcode, rd, funct3, rs1, rs2, funct7, imm):
    if opcode in [opCodes['ALU_REG']]:
        key = (opcode, funct3, funct7)
    else:
        key = (opcode, funct3, None)
    
    if key in self.dispatch:
        self.dispatch[key](self,rd, rs1, rs2, imm)
    else:
        raise Exception(f"Unknown instruction: opcode=0x{opcode:02x}, funct3=0x{funct3:x}")
  def examine_all_registers(self):
    # group into rows of 8 registers
    for base in range(0, 16, 8):
        row = " ".join(f"x{j:02}={self.registers[j]:>3}" 
                        for j in range(base, base+8))
        print(row)
  def read_memory(self, address,size):
    value = 0
    for i in range(size):
      value |= self.memory[address+i] <<(i*8)
    return value
  def write_memory(self, address,value,size):
    for i in range(size):
      self.memory[address+i] = (value >> (i*8)) & 0xFF

