from __future__ import annotations
from enum import Enum, auto, unique
from typing import Optional
from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 4

    regs = {
        '$zero': RegisterInfo('$zero', 16),
        '$at':   RegisterInfo('$at', 16),
        '$v0':   RegisterInfo('$v0', 16),
        '$v1':   RegisterInfo('$v1', 16),
        '$a0':   RegisterInfo('$a0', 16),
        '$a1':   RegisterInfo('$a1', 16),
        '$a2':   RegisterInfo('$a2', 16),
        '$a3':   RegisterInfo('$a3', 16),
        '$t0':   RegisterInfo('$t0', 16),
        '$t1':   RegisterInfo('$t1', 16),
        '$t2':   RegisterInfo('$t2', 16),
        '$t3':   RegisterInfo('$t3', 16),
        '$t4':   RegisterInfo('$t4', 16),
        '$t5':   RegisterInfo('$t5', 16),
        '$t6':   RegisterInfo('$t6', 16),
        '$t7':   RegisterInfo('$t7', 16),
        '$s0':   RegisterInfo('$s0', 16),
        '$s1':   RegisterInfo('$s1', 16),
        '$s2':   RegisterInfo('$s2', 16),
        '$s3':   RegisterInfo('$s3', 16),
        '$s4':   RegisterInfo('$s4', 16),
        '$s5':   RegisterInfo('$s5', 16),
        '$s6':   RegisterInfo('$s6', 16),
        '$s7':   RegisterInfo('$s7', 16),
        '$t8':   RegisterInfo('$t8', 16),
        '$t9':   RegisterInfo('$t9', 16),
        '$k0':   RegisterInfo('$k0', 16),
        '$k1':   RegisterInfo('$k1', 16),
        '$gp':   RegisterInfo('$gp', 16),
        '$sp':   RegisterInfo('$sp', 16),
        '$fp':   RegisterInfo('$fp', 16),
        '$ra':   RegisterInfo('$ra', 16),
    }
    registers = {
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

    stack_pointer = '$sp'
    link_register = '$ra'
    operand_separator = ', '

    @unique
    class InstructionType(Enum):
        UNDEFINED = auto()
        GenericInt = auto()

    class Instruction:
        type: EmotionEngine.InstructionType
        name: Optional[str]
        dest: Optional[int]
        source1: Optional[int]
        source2: Optional[int]
        operand: Optional[str]

        def __init__(self):
            self.type = EmotionEngine.InstructionType.UNDEFINED
            self.name = None
            self.dest = None
            self.source1 = None
            self.source2 = None
            self.operand = None

    @staticmethod
    def _decode_special(opcode: int, addr: int) -> Optional[Instruction]:
        instruction = EmotionEngine.Instruction()
        IT = EmotionEngine.InstructionType

        op = opcode & 0x3F
        match op:
            case 0x0:
                # sll
                instruction.type = IT.GenericInt

                dest = (opcode >> 11) & 0x1F
                source = (opcode >> 16) & 0x1F
                operand = (opcode >> 6) & 0x1F
                if dest == 0:
                    # nop
                    instruction.name = "nop"
                    return instruction
                
                instruction.name = "sll"
                instruction.dest = dest
                instruction.source1 = source
                instruction.operand = operand
                return instruction
            case _:
                return None

    @staticmethod
    def decode(data: bytes, addr: int) -> Optional[Instruction]:
        opcode = int.from_bytes(data, "little")
        op = opcode >> 26
        instruction = EmotionEngine.Instruction()

        match op:
            case 0x00:
                return EmotionEngine._decode_special(opcode, addr)
            case _:
                return None

    def get_instruction_info(self, data: bytes, addr: int):
        result = InstructionInfo()
        result.length = 4
        return result
    
    def get_instruction_text(self, data: bytes, addr: int):
        instruction = self.decode(data, addr)
        IT = EmotionEngine.InstructionType
        tokens = []

        match instruction.type:
            case IT.GenericInt:
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, instruction.name))
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, " "))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.registers[instruction.dest]))
                if instruction.source1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.registers[instruction.source1]))
                if instruction.source2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, EmotionEngine.registers[instruction.source2]))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str(instruction.operand)))
            case _:
                tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "???")]

        return tokens, 4