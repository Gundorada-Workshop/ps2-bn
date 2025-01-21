from __future__ import annotations
from .ps2.decode import decode, InstructionType
from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 4
    max_instr_length = 8 # Branch + Branch delay slot

    gpr = {
        0: "$zero",
        1: "$at",
        2: "$v0",
        3: "$v1",
        4: "$a0",
        5: "$a1",
        6: "$a2",
        7: "$a3",
        8: "$t0",
        9: "$t1",
        10: "$t2",
        11: "$t3",
        12: "$t4",
        13: "$t5",
        14: "$t6",
        15: "$t7",
        16: "$s0",
        17: "$s1",
        18: "$s2",
        19: "$s3",
        20: "$s4",
        21: "$s5",
        22: "$s6",
        23: "$s7",
        24: "$t8",
        25: "$t9",
        26: "$k0",
        27: "$k1",
        28: "$gp",
        29: "$sp",
        30: "$fp",
        31: "$ra",
    }
    regs = {r: RegisterInfo(r, 16) for r in gpr.values()}

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
                    if EmotionEngine.gpr[instruction.dest] == EmotionEngine.link_register:
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
        
        tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, f"{instruction.name:7s} "))

        match instruction.type:
            case IT.GenericInt:
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.gpr[instruction.dest]))
                if instruction.source1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.gpr[instruction.source1]))
                if instruction.source2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.gpr[instruction.source2]))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str(instruction.operand)))
            case IT.Branch:
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.gpr[instruction.dest]))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, str(instruction.operand)))

        return tokens, 4