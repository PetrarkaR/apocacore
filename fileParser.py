#!/usr/bin/env python

"""PARSER FOR EASIER USER PROGRAMMING"""

import re
import argparse
from constants import *
from cpu import *
class Parser():
  def __init__(self):
      self.core = ApocaCore()
      self.filename = None
      self.errors = 0 
      self.lines = []
      self.commands = []
      self.symbols = {}
      self.debug = False
      self.var_dict = []
      self.opcode_map = instruction_map
      self.data_name= None
      self.data = []
  def arguments(self):
    parser =argparse.ArgumentParser(description='parser for the assembly of the custom processor')
    parser.add_argument('-f',required=True,help='Input file')
    parser.add_argument('-r',required=False,help='Run mode')
    parser.add_argument('-d',required=False,help='debug')
    args = parser.parse_args()
    self.run =args.r
    self.debug =args.d
    return args.f
  def load(self, filename):
    self.filename = filename
    with open(filename , 'r') as f:
      self.lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    if self.debug=='debug':
      print(f"loaded {len(self.lines)} lines from {filename}")
  
  def first_pass(self):
    pc=0
    i=0
    for line in self.lines:
      i=i+1
      section =re.match(r"data:",line)
      m = re.match(r"^(\w+):",line)
      if section:
        section = m.group(1)
        self.parse_data(line, int(i))
      if m:
        label =m.group(1)
        self.symbols[label] = pc
        if self.debug=='debug':
          print(f"label {label} at addres {pc}")
      else:
        pc+=4
  def second_pass(self):
    pc = 0
    for line in self.lines:
      if re.match(r"^\w+:",line):
        continue
      word = self.parse_line(line,pc)
      self.commands.append(word)
      pc+=4
    if self.debug=='debug':
            for addr, cmd in enumerate(self.commands):
                print(f"{addr*4:04x}: {cmd:08x}")
  def parse_data(self, line, i):
    parts = [tok for tok in re.split(r"[,\s()]+", line) if tok]
    self.data_name= parts[0]
    self.data = parts[1:]
    self.data.pop(0)
    self.var_dict.append(self.data)




  def parse_line(self, line, pc):
        # split tokens, filter empties
        parts = [tok for tok in re.split(r"[,\s()]+", line) if tok]
        mnemonic = parts[0].upper()
        args = parts[1:]

        info = self.opcode_map.get(mnemonic)
        if not info:
            raise ValueError(f"Unknown instruction '{mnemonic}' at PC {pc}")

        # I-type: ADDI, LW, add more later, vectors probably
        if mnemonic == 'ADDI' or mnemonic == 'LW':
            rd = args[0]
            # offset(base)
            if mnemonic == 'LW':
                # args: rd, offset, base
                offset, base = args[1], args[2]
            else:
                # ADDI args: rd, rs, imm
                base = args[1]; offset = args[2]
            return self.encode_i_type(int(rd[1:]), int(base[1:]), int(offset), info['funct3'], info['opcode'])

        # R-type: ADD, need to add more later
        if mnemonic == 'ADD':
            rd, rs1, rs2 = args
            return self.encode_r_type(int(rd[1:]), int(rs1[1:]), int(rs2[1:]), info['funct3'], info['funct7'], info['opcode'])

        # S-type: SW
        if mnemonic == 'SW':
            rs2 = args[0]
            offset = args[1]
            rs1 = args[2]
            return self.encode_s_type(int(rs2[1:]), int(rs1[1:]), int(offset), info['funct3'], info['opcode'])
        
                # Vector instructions: LV, SV, etc.
        if mnemonic == 'LV' or mnemonic == 'SV':
                # LV v1, 512(x0) -> args = ['v1', '512', 'x0']
                vs3 = args[0]
                offset = args[1]
                rs1 = args[2]

                vs3_num = int(vs3[1:])  # v1 -> 1
                rs1_num = int(rs1[1:])  # x0 -> 0
                imm = int(offset)       # 512 -> 512
                
                print(f"[ASSEMBLER] {mnemonic} v{vs3_num}, {imm}(x{rs1_num})")

                # Use I-type encoding for vector load/store
                return self.encode_i_type(vs3_num, rs1_num, imm, info['funct3'], info['opcode'])





        raise NotImplementedError(f"Encoding for '{mnemonic}' not implemented at PC {pc}")

  def encode_r_type(self, rd, rs1, rs2, funct3, funct7, opcode):
      # [funct7][rs2][rs1][funct3][rd][opcode]
      return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
  def encode_i_type(self, rd, rs1, imm, funct3, opcode):
      # [imm[11:0]][rs1][funct3][rd][opcode]
      imm12 = imm & 0xfff
      return (imm12 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
  def encode_s_type(self, rs2, rs1, imm, funct3, opcode):
      # [imm[11:5]][rs2][rs1][funct3][imm[4:0]][opcode]
      imm11_5 = (imm >> 5) & 0x7f
      imm4_0 = imm & 0x1f
      return (imm11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm4_0 << 7) | opcode
  def encode_v_type(self, vs3, rs1, imm, funct3, funct6, opcode):
    # For vector load/store, use I-type format like scalar loads:
    # [imm[11:0]][rs1][funct3][vd][opcode]
    # This matches how your decoder extracts the immediate
    
    imm12 = imm & 0xFFF  # 12-bit immediate (supports up to 4095)
    
    return (imm12 << 20) | (rs1 << 15) | (funct3 << 12) | (vs3 << 7) | opcode

  def assemble(self, filename):
      self.load(filename)
      self.first_pass()
      self.second_pass()
      return self.commands, self.var_dict

  def parse(self, filename):
      if(filename.endswith('.apo')==True):
        with open(filename,'r') as parsed:
          lines = parsed.readlines()
          numLines=len(lines)
          print(f"File started successfully!\nTotal number of lines : {numLines}")
          if(lines[0].strip()=='#apocacore'):
            print("\nDone parsing")
      else:
        print("Invalid file format!")
  


"""if __name__=="__main__":
  main()
"""

