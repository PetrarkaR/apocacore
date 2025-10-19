#!/usr/bin/env python
from constants import *
import typing
from exec import InstructionHandlers
class ApocaCore:
  def __init__(self,memory_size=1024,debug=False):
    self.registers = [0]*16
    self.f_registers =[0.0]*16 
    self.pc=0
    self.memory=[0]*memory_size
    self.debug = debug
    self.build_map()
    self.VLEN = 256
    self.MAX_SEW=8
    self.LMUL=1
    self.vl=8
    self.vtype = {'SEW':32,'LMUL':1}
    self.vreg= [[0]*(self.VLEN//self.vtype['SEW']) for _ in range(16)]
    self.next_address=0
    self.jump_adress= {}


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

            (opCodes_vector['VECTOR_LOAD'], 0, 0): handlers.exec_vl,
            (opCodes_vector['VECTOR_STORE'], 0, 0): handlers.exec_vs,
            (opCodes_vector['VECTOR_ADD'], funct3_codes['ADD_SUB'], funct6_codes['VADD']): handlers.exec_vadd,
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
            address = base_address + (i * len(vector) + j) * 4  # each value is 8 bytes
            self.write_memory(address, int(val, 0) if isinstance(val, str) else val, 8)

  def load_program(self,program):
    self.memory[:len(program)] = program
    self.program_length = len(program)

  def fetch(self):
    instruction = self.memory[self.pc]
    self.pc+=1
    return instruction
  def decode(self, instruction):
    """default decoding"""
    opcode = instruction & 0x7F
    rd = (instruction >> 7) & 0x1F
    funct3_codes = (instruction >> 12) & 0x7
    rs1 = (instruction >> 15) & 0x1F
    rs2 = (instruction >> 20) & 0x1F
    funct7 = (instruction >> 25) & 0x7F
    
    if opcode in opCodes_vector.values():
        funct6 = (instruction >> 26) & 0x3F
        vm = (instruction >> 25) & 0x1
        rs2 = (instruction >> 20) & 0x1F  # vs2 or could be part of immediate
        rs1 = (instruction >> 15) & 0x1F  # vs1 / base register
        funct3 = (instruction >> 12) & 0x7
        rd = (instruction >> 7) & 0x1F    # vd
        if opcode == opCodes_vector['VECTOR_LOAD'] or opcode == opCodes_vector['VECTOR_STORE']:
            # Extract immediate from bits [31:20] like scalar loads
            imm = (instruction >> 20) & 0xFFF
            # Sign extend from 12 bits
            if imm & 0x800:
                imm |= 0xFFFFF000
            
            funct6 = 0  # Not used for load/store
            vm = 1      # Default mask
            return ('vector_mem', opcode, rd, funct3, rs1, imm, funct6, vm)

        # For vector load/store, extract immediate
        # Format: imm[11:0] = {funct6[5:0], vm, rs2[4:0]}
        imm = (funct6 << 6) | (vm << 5) | rs2
        # Sign extend from 12 bits
        if imm & 0x800:
            imm |= 0xFFFFF000
        
        return ('vector_arith', opcode, rd, funct6, funct3, rs1, rs2, vm)

    if opcode == opCodes['ALU_IMM'] or opcode == opCodes['LOAD'] or opcode == opCodes['JALR']:
        imm = (instruction >> 20) if (instruction >> 31) == 0 else (instruction >> 20) | 0xFFFFF000
    elif opcode == opCodes['STORE']:
        imm_11_5 = (instruction >> 25) & 0x7F
        imm_4_0 = (instruction >> 7) & 0x1F
        imm = (imm_11_5 << 5) | imm_4_0
        if (imm_11_5 >> 6) & 1:  # Sign extend
            imm |= 0xFFFFF000
    elif opcode == opCodes['BRANCH']:
        imm = (instruction >> 20) & 0xFFF  # Get 12 bits
        
        # Shift left by 1 (branches are 2-byte aligned, bit 0 is implicit 0)
        imm = imm << 1
        
        # Sign extend from bit 12
        if imm & 0x1000:  # Check if bit 12 is set (sign bit)
            imm |= 0xFFFFE000  # Sign extend to 32 bits
        opcode = instruction & 0x7F  # Bits [6:0] - unchanged
        funct3 = (instruction >> 7) & 0x7  # Bits [9:7] - unchanged
        rs1 = (instruction >> 10) & 0x1F  # Bits [14:10] - CHANGED (was 15)
        rs2 = (instruction >> 15) & 0x1F  # Bits [19:15] - CHANGED (was 20)
        return ('branch',opcode,imm,rs1,rs2,funct3)
    else:
        # Default case (includes LUI, AUIPC which have upper immediate)
        imm = instruction >> 20
        
    return ('scalar',opcode, rd, funct3_codes, rs1, rs2, funct7, imm)
  def execute(self, *decoded):
    if self.debug==True:
        print(decoded,(self.pc*4)-4)
    instruction_type = decoded[0]
    if( instruction_type == 'vector_arith'):
        _, opcode,rd,funct6,funct3,rs1,rs2,vm =decoded
        key=(opcode,funct3,funct6)
        if key in self.dispatch:
            self.dispatch[key](self, rd, rs1,rs2 )  # ← Pass imm correctly
    elif instruction_type == 'vector_mem':
        _, opcode, rd, funct3, rs1, imm, funct6, vm = decoded  # ← Changed rs2 to imm
        key = (opcode, funct3, funct6)

        if key in self.dispatch:
            self.dispatch[key](self, rd, rs1, imm, vm)  # ← Pass imm correctly
        else:
            raise Exception(f"Unknown vector instruction: opcode=0x{opcode:02x}, funct3=0x{funct3:x}, funct6=0x{funct6:x}")
    
    

    elif instruction_type == 'scalar':
        _, opcode, rd, funct3, rs1, rs2, funct7, imm = decoded
        
        if opcode in [opCodes['ALU_REG']]:
            key = (opcode, funct3, funct7)
        else:
            key = (opcode, funct3, None)
        
        if key in self.dispatch:
            self.dispatch[key](self, rd, rs1, rs2, imm)
        else:
            raise Exception(f"Unknown instruction SCALAR: opcode=0x{opcode:02x}, funct3=0x{funct3:x}")
        
    elif(instruction_type=='branch'):
       _,opcode,imm,rs1,rs2,funct3=decoded
       key=(opcode,funct3,None)
       if key in self.dispatch:
            self.dispatch[key](self, rs1,rs2,imm )  # ← Pass imm correctly
  def examine_all_registers(self):
    # group into rows of 8 registers
    for base in range(0, 16, 8):
        row = " ".join(f"x{j:02}={self.registers[j]:>3}" 
                        for j in range(base, base+8))
        print(row)
  def read_memory(self, address, size):
      value = 0
      for i in range(size):
          value |= self.memory[address + i] << (i * 8)
      return value  # <-- ADD THIS!
    
  def write_memory(self, address,value,size):
    for i in range(size):
      self.memory[address+i] = (value >> (i*8)) & 0xFF
  def dump_memory(self, start, length):
      print(f"\n=== Memory Dump: {start} to {start + length - 1} ===")
      for i in range(start, start + length, 4):
          word = self.read_memory(i, 4)
          print(f"  [{i:04d}] = 0x{word:08x} ({word})")
      print()

  def dump_vector_registers(self):
      print("\n=== Vector Registers ===")
      for i, vreg in enumerate(self.vreg):
          non_zero = [val for val in vreg if val != 0]
          if non_zero:
              print(f"  v{i}: {non_zero[:8]}")  # Show first 8 elements
      print()
