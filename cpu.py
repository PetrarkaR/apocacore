#!/usr/bin/env python

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
}
fp_opcodes = {
    'FADD_S': 0b1010011,  # Floating-point add single-precision
    'FSUB_S': 0b1010011,  # Floating-point subtract single-precision
    'FMUL_S': 0b1010011,  # Floating-point multiply single-precision
    'FDIV_S': 0b1010011,  # Floating-point divide single-precision
}

class apocacore:
  def __init__(self,memory_size=1024):
    self.registers = [0]*32
    self.f_registers =[0.0]*32
    self.pc=0
    self.memory=[0]*memory_size
  def run(self):
    for i in range(1024):  # Safety limit
        if self.pc >= len(self.memory):
            break
        ins = self.fetch()
        decoded = self.decode(ins)
        self.execute(decoded[0], decoded[1], decoded[2], decoded[3], decoded[4], decoded[5], decoded[6])
  def load_program(self,program):
    self.memory[:len(program)]=program
  def fetch(self):
    instruction = self.memory[self.pc]
    self.pc+=1
    return instruction
  def decode(self, instruction):
    opcode = instruction & 0x7F
    rd = (instruction >> 7) & 0x1F
    funct3 = (instruction >> 12) & 0x7
    rs1 = (instruction >> 15) & 0x1F
    rs2 = (instruction >> 20) & 0x1F
    funct7 = (instruction >> 25) & 0x7F
    
    # Different immediate formats based on instruction type
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
        
    return opcode, rd, funct3, rs1, rs2, funct7, imm
  def execute(self,opcode, rd, funct3,rs1,rs2,funct7, imm):
    if(opcode ==opCodes['LUI']):
      self.registers[rd] =imm<<12
    elif( opcode == opCodes['ALU_IMM']):
      if ( funct3==funct3_codes['ADD_SUB']):
        self.registers[rd] = self.registers[rs1] +imm
    elif (opcode ==opCodes['ALU_REG']):
      if(funct7 ==0b0000000):
        self.registers[rd] = self.registers[rs1]+self.registers[rs2]
      elif(funct7==0b0100000):
        self.registers[rd] = self.registers[rs1]-self.registers[rs2]
    elif(opcode==opCodes['LOAD']):
      if funct3==0b010:
        self.registers[rd]=self.read_memory(self.registers[rs1]+imm, 4)
    elif(opcode == opCodes['STORE']):
      if funct3==0b010:
        self.write_memory(self.registers[rs1] + imm, self.registers[rs2],4)
    elif (opcode == opCodes['BRANCH']):
      offset = (imm<<1)
      if funct3==0b000:
        if self.registers[rs1] ==self.registers[rs2]:
          self.pc +=offset
      if funct3==0b001:
        if self.registers[rs1] !=self.registers[rs2]:
          self.pc +=offset
  def read_memory(self, address,size):
    value = 0
    for i in range(size):
      value |= self.memory[address+i] <<(i*8)
    return value
  def write_memory(self, address,value,size):
    for i in range(size):
      self.memory[address+i] = (value >> (i*8)) & 0xFF
      
program = [
    0x00A00513,  # ADDI x10, x0, 5    # Set x10 = 5
    0x00600593,  # ADDI x11, x0, 6    # Set x11 = 6
    0x00b50633,  # ADD x12, x10, x11  # Set x12 = x10 + x11 = 11
    0x00c02023,  # SW x11, 0(x0)      # Store x11 at memory address 0+x0
    0x00002083,  # LW x1, 0(x0)       # Load into x1 from memory address 0+x0
]
if __name__ == '__main__':
    emulator = apocacore()
    emulator.load_program(program)
    emulator.run()
    # Check results
    print(f'Register x12 (should be 11): {emulator.registers[12]}')
    print(f'Register x1 (loaded from memory): {emulator.registers[1]}')