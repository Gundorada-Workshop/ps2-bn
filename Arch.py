from __future__ import annotations
from typing import Optional
from .ps2.decode import decode
from .ps2.instruction import Instruction, InstructionType
from .ps2.ee.registers import gpr as EERegisters
from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 4
    max_instr_length = 8 # Branch + Branch delay slot

    regs = {r: RegisterInfo(r, 16) for r in EERegisters.values()}

    stack_pointer = '$sp'
    link_register = '$ra'
    operand_separator = ', '

    def get_instruction_info(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = decode(data[0:4], addr)
        IT = InstructionType

        result = InstructionInfo()
        result.length = 4

        if instruction.type == IT.Branch:
            result.branch_delay = 1
            match instruction.name:
                case "jr":
                    if EERegisters[instruction.dest] == EmotionEngine.link_register:
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
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EERegisters[instruction.dest]))
                if instruction.source1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EERegisters[instruction.source1]))
                if instruction.source2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EERegisters[instruction.source2]))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str(instruction.operand)))
            case IT.Branch:
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EERegisters[instruction.dest]))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, str(instruction.operand)))

        if len(tokens) == 2:
            # Remove spaces from instruction only text
            del tokens[1]

        return tokens, 4
    
    def get_instruction_low_level_il(self, data: bytes, addr: int, il) -> Optional[int]:
        if len(data) < 4:
            return None
        instruction = decode(data[0:4], addr)
        if instruction.il_func is None:
            il.append(il.unimplemented())
            return 4
        
        instruction.il_func(instruction, il)
        return 4
