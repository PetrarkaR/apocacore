#!/usr/bin/env python
from fileParser import Parser
from constants import *
import typing

class ApocaCore:
  def __init__(self,memory_size=1024):
    self.registers = [0]*16
    self.f_registers =[0.0]*16 
    self.pc=0
    self.memory=[0]*memory_size

    self._dispatch = {
            (0, 0, None):      self._exec_nop,
            # R-type :   (opcode, funct3_codes, funct7) → handler
            (opCodes['ALU_REG'], funct3_codes['ADD_SUB'], 0b0000000): self._exec_add,
            (opCodes['ALU_REG'], funct3_codes['ADD_SUB'], 0b0100000): self._exec_sub,
            # I-type:
            (opCodes['ALU_IMM'], funct3_codes['ADD_SUB'], None):      self._exec_addi,
            (opCodes['LOAD'   ], funct3_codes['WORD'   ], None):      self._exec_load,
            # S-type:
            (opCodes['STORE'  ], funct3_codes['WORD'   ], None):         self._exec_store
            # …load, store, branch entries…
        }

  def run(self):
    for i in range(1024):  # Safety limit
      while self.pc < self.program_length:
            ins = self.fetch()
            decoded = self.decode(ins)
            self.execute(*decoded)

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
    
    if key in self._dispatch:
        self._dispatch[key](rd, rs1, rs2, imm)
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
  def _exec_add(self, rd, rs1, rs2, imm):
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
  def _exec_sub(self, rd, rs1, rs2, imm):
      self.registers[rd] = self.registers[rs1] - self.registers[rs2]
  def _exec_addi(self, rd, rs1, rs2, imm):
        self.registers[rd] = self.registers[rs1] + imm
  def _exec_load(self, rd, rs1, rs2, imm):
        self.registers[rd]=self.read_memory(self.registers[rs1]+imm, 4)
  def _exec_store(self, rd, rs1, rs2, imm):
        self.write_memory(self.registers[rs1] + imm, self.registers[rs2],4)
  def _exec_beq(self, rd, rs1, rs2, imm):
        if self.registers[rs1] ==self.registers[rs2]:
          self.pc +=(imm<<1)
  def _exec_bne(self, rd, rs1, rs2, imm):
        if self.registers[rs1] !=self.registers[rs2]:
          self.pc +=(imm<<1)
  def _exec_nop(self, rd, rs1, rs2, imm):
        # do nothing
        pass
program = [
    0x00A00513,  # ADDI x10, x0, 5    # Set x10 = 5
    0x00600593,  # ADDI x11, x0, 6    # Set x11 = 6
    0x00b50633,  # ADD x12, x10, x11  # Set x12 = x10 + x11 = 11
    0x00c02023,  # SW x11, 0(x0)      # Store x11 at memory address 0+x0
    0x00002083,  # LW x1, 0(x0)       # Load into x1 from memory address 0+x0
]
if __name__ == '__main__':
    parser=Parser()
    filename = parser.arguments()
    machine = parser.assemble(filename)
    if(parser.debug=='Run'):
      emulator = ApocaCore()
      emulator.load_program(machine)
      emulator.run()
      emulator.examine_all_registers()
    # Check results
    #print(f'Register x12 (should be 16): {emulator.registers[12]}')
    #print(f'Register x1 (loaded from memory): {emulator.registers[1]}')