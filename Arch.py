from __future__ import annotations
from typing import Optional
from .ps2.decode import decode
from .ps2.instruction import Instruction, InstructionType
from .ps2.ee.registers import registers as EERegisters
from .ps2.ee.registers import HI_REG, LO_REG, PC_REG, SA_REG, RA_REG, SP_REG
from .ps2.fpu.registers import registers as FPURegisters
from .ps2.vu0f.registers import registers as VU0FRegisters
from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 4
    max_instr_length = 8 # Branch + Branch delay slot

    regs = {name: RegisterInfo(name, size) for name, size in EERegisters} | \
           {name: RegisterInfo(name, size) for name, size in FPURegisters} | \
           {name: RegisterInfo(name, size) for name, size in VU0FRegisters}

    stack_pointer = SP_REG
    link_register = RA_REG
    operand_separator = ', '

    def get_instruction_info(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = decode(data[0:4], addr)
        IT = InstructionType

        if instruction is None:
            print(f"INSTRUCTION NONE {bytes}")

        result = InstructionInfo()
        result.length = 4

        if instruction.type == IT.Branch:
            result.branch_delay = 1
            match instruction.name:
                case "jr":
                    if instruction.reg1 == EmotionEngine.link_register:
                        result.add_branch(BranchType.FunctionReturn)
                    else:
                        result.add_branch(BranchType.IndirectBranch)
                # TODO other branches

        return result
    
    def get_instruction_text(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = decode(data[0:4], addr)
        IT = InstructionType
        tokens = []

        if instruction.type == IT.UNDEFINED:
            return None
        
        # Instruction name + spaces
        pad = 7 # Spaces will be padded to a *multiple* of this length
        spaces = " " * ((pad - len(instruction.name)) % pad + 1)
        tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, instruction.name))
        tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, spaces))

        match instruction.type:
            case IT.GenericInt:
                if instruction.reg1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg1))
                if instruction.reg2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg2))
                if instruction.reg3 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg3))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str(instruction.operand)))
            case IT.Branch:
                if instruction.reg1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg1))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, str(instruction.operand)))

        if len(tokens) == 2:
            # Remove spaces from instruction only text
            del tokens[1]

        return tokens, 4
    
    def get_instruction_low_level_il(self, data: bytes, addr: int, il) -> Optional[int]:
        if len(data) < 4:
            return None
        
        length = 4

        instruction1 = decode(data[0:4], addr)        
        instruction1.arch = EmotionEngine
        if instruction1.il_func is None:
            il.append(il.unimplemented())
            return 4
        
        instruction2 = None
        if instruction1.type == InstructionType.Branch:
            assert len(data) >= 8, "Branch at end of file??"
            instruction2 = decode(data[4:8], addr + 4)
            length += 4

        if instruction2 is not None:
            instruction2.arch = EmotionEngine
            if instruction2.il_func is None:
                # Command in branch delay slot unimplemented...
                length -= 4
            else:
                pass
                #instruction2.il_func(instruction2, addr, il)
        
        #instruction1.il_func(instruction1, addr, il)
        il.append(il.unimplemented()) # TEMP
        return length
