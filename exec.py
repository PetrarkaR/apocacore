#!/usr/bin/env python
# instruction_handlers.py
"""
Implementation of RISC-V instruction handlers.
These functions implement the behavior of each instruction.
"""

class InstructionHandlers:
    """
    This class contains methods that implement the behavior of RISC-V instructions.
    Each method corresponds to a specific instruction and modifies the processor state.
    
    The processor state (registers, memory, etc.) is passed in from the Processor class.
    """
    def __init__(self):
        pass
    @staticmethod
    def exec_nop(processor, rd, rs1, rs2, imm):
        """Execute NOP instruction (do nothing)"""
        pass
    
    @staticmethod
    def exec_add(processor, rd, rs1, rs2, imm):
        """Execute ADD instruction: rd = rs1 + rs2"""
        if rd != 0:  # x0 is hardwired to 0
            processor.registers[rd] = processor.registers[rs1] + processor.registers[rs2]
    
    @staticmethod
    def exec_sub(processor, rd, rs1, rs2, imm):
        """Execute SUB instruction: rd = rs1 - rs2"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] - processor.registers[rs2]
    
    @staticmethod
    def exec_sll(processor, rd, rs1, rs2, imm):
        """Execute SLL instruction: rd = rs1 << rs2"""
        if rd != 0:
            shift_amount = processor.registers[rs2] & 0x1F  # Only lower 5 bits
            processor.registers[rd] = processor.registers[rs1] << shift_amount
    
    @staticmethod
    def exec_slt(processor, rd, rs1, rs2, imm):
        """Execute SLT instruction: rd = 1 if rs1 < rs2 else 0 (signed)"""
        if rd != 0:
            processor.registers[rd] = 1 if processor.registers[rs1] < processor.registers[rs2] else 0
    
    @staticmethod
    def exec_sltu(processor, rd, rs1, rs2, imm):
        """Execute SLTU instruction: rd = 1 if rs1 < rs2 else 0 (unsigned)"""
        if rd != 0:
            # Handle unsigned comparison (convert to unsigned 32-bit)
            unsigned_rs1 = processor.registers[rs1] & 0xFFFFFFFF
            unsigned_rs2 = processor.registers[rs2] & 0xFFFFFFFF
            processor.registers[rd] = 1 if unsigned_rs1 < unsigned_rs2 else 0
    
    @staticmethod
    def exec_xor(processor, rd, rs1, rs2, imm):
        """Execute XOR instruction: rd = rs1 ^ rs2"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] ^ processor.registers[rs2]
    
    @staticmethod
    def exec_srl(processor, rd, rs1, rs2, imm):
        """Execute SRL instruction: rd = rs1 >> rs2 (logical)"""
        if rd != 0:
            shift_amount = processor.registers[rs2] & 0x1F  # Only lower 5 bits
            processor.registers[rd] = (processor.registers[rs1] & 0xFFFFFFFF) >> shift_amount
    
    @staticmethod
    def exec_sra(processor, rd, rs1, rs2, imm):
        """Execute SRA instruction: rd = rs1 >> rs2 (arithmetic)"""
        if rd != 0:
            shift_amount = processor.registers[rs2] & 0x1F  # Only lower 5 bits
            # Implementation depends on how you represent signed integers
            # This assumes Python's handling of negative numbers in shifts
            processor.registers[rd] = processor.registers[rs1] >> shift_amount
    
    @staticmethod
    def exec_or(processor, rd, rs1, rs2, imm):
        """Execute OR instruction: rd = rs1 | rs2"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] | processor.registers[rs2]
    
    @staticmethod
    def exec_and(processor, rd, rs1, rs2, imm):
        """Execute AND instruction: rd = rs1 & rs2"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] & processor.registers[rs2]
    
    # I-type instructions
    @staticmethod
    def exec_addi(processor, rd, rs1, rs2, imm):
        """Execute ADDI instruction: rd = rs1 + imm"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] + imm
    
    @staticmethod
    def exec_slti(processor, rd, rs1, rs2, imm):
        """Execute SLTI instruction: rd = 1 if rs1 < imm else 0 (signed)"""
        if rd != 0:
            processor.registers[rd] = 1 if processor.registers[rs1] < imm else 0
    
    @staticmethod
    def exec_sltiu(processor, rd, rs1, rs2, imm):
        """Execute SLTIU instruction: rd = 1 if rs1 < imm else 0 (unsigned)"""
        if rd != 0:
            unsigned_rs1 = processor.registers[rs1] & 0xFFFFFFFF
            unsigned_imm = imm & 0xFFFFFFFF
            processor.registers[rd] = 1 if unsigned_rs1 < unsigned_imm else 0
    
    @staticmethod
    def exec_xori(processor, rd, rs1, rs2, imm):
        """Execute XORI instruction: rd = rs1 ^ imm"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] ^ imm
    
    @staticmethod
    def exec_ori(processor, rd, rs1, rs2, imm):
        """Execute ORI instruction: rd = rs1 | imm"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] | imm
    
    @staticmethod
    def exec_andi(processor, rd, rs1, rs2, imm):
        """Execute ANDI instruction: rd = rs1 & imm"""
        if rd != 0:
            processor.registers[rd] = processor.registers[rs1] & imm
    
    @staticmethod
    def exec_slli(processor, rd, rs1, rs2, imm):
        """Execute SLLI instruction: rd = rs1 << imm"""
        if rd != 0:
            shift_amount = imm & 0x1F  # Only lower 5 bits for 32-bit mode
            processor.registers[rd] = processor.registers[rs1] << shift_amount
    
    @staticmethod
    def exec_srli(processor, rd, rs1, rs2, imm):
        """Execute SRLI instruction: rd = rs1 >> imm (logical)"""
        if rd != 0:
            shift_amount = imm & 0x1F
            processor.registers[rd] = (processor.registers[rs1] & 0xFFFFFFFF) >> shift_amount
    
    @staticmethod
    def exec_srai(processor, rd, rs1, rs2, imm):
        """Execute SRAI instruction: rd = rs1 >> imm (arithmetic)"""
        if rd != 0:
            shift_amount = imm & 0x1F
            processor.registers[rd] = processor.registers[rs1] >> shift_amount
    
    # Load instructions
    @staticmethod
    def exec_lb(processor, rd, rs1, rs2, imm):
        """Execute LB instruction: rd = sign_extend(memory[rs1 + imm][7:0])"""
        if rd != 0:
            address = processor.registers[rs1] + imm
            value = processor.memory[address] & 0xFF
            # Sign extend from 8 bits
            if value & 0x80:
                value |= 0xFFFFFF00
            processor.registers[rd] = value
    
    @staticmethod
    def exec_lh(processor, rd, rs1, rs2, imm):
        """Execute LH instruction: rd = sign_extend(memory[rs1 + imm][15:0])"""
        if rd != 0:
            address = processor.registers[rs1] + imm
            value = processor.memory[address] & 0xFFFF
            # Sign extend from 16 bits
            if value & 0x8000:
                value |= 0xFFFF0000
            processor.registers[rd] = value
    
    @staticmethod
    def exec_lw(processor, rd, rs1, rs2, imm):
        """Execute LW instruction: rd = memory[rs1 + imm]"""
        if rd != 0:
            address = processor.registers[rs1] + imm
            processor.registers[rd] = processor.memory[address]
    
    @staticmethod
    def exec_lbu(processor, rd, rs1, rs2, imm):
        """Execute LBU instruction: rd = zero_extend(memory[rs1 + imm][7:0])"""
        if rd != 0:
            address = processor.registers[rs1] + imm
            processor.registers[rd] = processor.memory[address] & 0xFF
    
    @staticmethod
    def exec_lhu(processor, rd, rs1, rs2, imm):
        """Execute LHU instruction: rd = zero_extend(memory[rs1 + imm][15:0])"""
        if rd != 0:
            address = processor.registers[rs1] + imm
            processor.registers[rd] = processor.memory[address] & 0xFFFF
    
    # Store instructions
    @staticmethod
    def exec_sb(processor, rd, rs1, rs2, imm):
        """Execute SB instruction: memory[rs1 + imm] = rs2[7:0]"""
        address = processor.registers[rs1] + imm
        processor.memory[address] = processor.registers[rs2] & 0xFF
    
    @staticmethod
    def exec_sh(processor, rd, rs1, rs2, imm):
        """Execute SH instruction: memory[rs1 + imm] = rs2[15:0]"""
        address = processor.registers[rs1] + imm
        processor.memory[address] = processor.registers[rs2] & 0xFFFF
    
    @staticmethod
    def exec_sw(processor, rd, rs1, rs2, imm):
        """Execute SW instruction: memory[rs1 + imm] = rs2"""
        address = processor.registers[rs1] + imm
        processor.memory[address] = processor.registers[rs2]
    
    # Branch instructions
    @staticmethod
    def exec_beq(processor, rd, rs1, rs2, imm):
        """Execute BEQ instruction: if rs1 == rs2 then pc += imm"""
        if processor.registers[rs1] == processor.registers[rs2]:
            processor.pc = processor.pc + imm - 4  # -4 to compensate for the PC increment in execute
    
    @staticmethod
    def exec_bne(processor, rd, rs1, rs2, imm):
        """Execute BNE instruction: if rs1 != rs2 then pc += imm"""
        if processor.registers[rs1] != processor.registers[rs2]:
            processor.pc = processor.pc + imm - 4
    
    @staticmethod
    def exec_blt(processor, rd, rs1, rs2, imm):
        """Execute BLT instruction: if rs1 < rs2 then pc += imm (signed)"""
        if processor.registers[rs1] < processor.registers[rs2]:
            processor.pc = processor.pc + imm - 4
    
    @staticmethod
    def exec_bge(processor, rd, rs1, rs2, imm):
        """Execute BGE instruction: if rs1 >= rs2 then pc += imm (signed)"""
        if processor.registers[rs1] >= processor.registers[rs2]:
            processor.pc = processor.pc + imm - 4
    
    @staticmethod
    def exec_bltu(processor, rd, rs1, rs2, imm):
        """Execute BLTU instruction: if rs1 < rs2 then pc += imm (unsigned)"""
        unsigned_rs1 = processor.registers[rs1] & 0xFFFFFFFF
        unsigned_rs2 = processor.registers[rs2] & 0xFFFFFFFF
        if unsigned_rs1 < unsigned_rs2:
            processor.pc = processor.pc + imm - 4
    
    @staticmethod
    def exec_bgeu(processor, rd, rs1, rs2, imm):
        """Execute BGEU instruction: if rs1 >= rs2 then pc += imm (unsigned)"""
        unsigned_rs1 = processor.registers[rs1] & 0xFFFFFFFF
        unsigned_rs2 = processor.registers[rs2] & 0xFFFFFFFF
        if unsigned_rs1 >= unsigned_rs2:
            processor.pc = processor.pc + imm - 4
    
    # Jump instructions
    @staticmethod
    def exec_jal(processor, rd, rs1, rs2, imm):
        """Execute JAL instruction: rd = pc + 4; pc += imm"""
        if rd != 0:
            processor.registers[rd] = processor.pc + 4
        processor.pc = processor.pc + imm - 4
    
    @staticmethod
    def exec_jalr(processor, rd, rs1, rs2, imm):
        """Execute JALR instruction: rd = pc + 4; pc = (rs1 + imm) & ~1"""
        next_pc = (processor.registers[rs1] + imm) & ~1
        if rd != 0:
            processor.registers[rd] = processor.pc + 4
        processor.pc = next_pc - 4
    
    # U-type instructions
    @staticmethod
    def exec_lui(processor, rd, rs1, rs2, imm):
        """Execute LUI instruction: rd = imm << 12"""
        if rd != 0:
            processor.registers[rd] = imm << 12
    
    @staticmethod
    def exec_auipc(processor, rd, rs1, rs2, imm):
        """Execute AUIPC instruction: rd = pc + (imm << 12)"""
        if rd != 0:
            processor.registers[rd] = processor.pc + (imm << 12)
    @staticmethod
    def exec_vs(processor, vs3, rs1, offset, imm):
      base = processor.registers[rs1] + imm
      SEW = processor.vtype['SEW'] // 8  # bytes per element
      for i in range(processor.vl):
          value = processor.VREG[vs3][i]
          processor.write_memory(base + i * SEW, value, SEW)

