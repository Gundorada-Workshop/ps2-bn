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
    def _decode_special(opcode: int, addr: int) -> Instruction:
        instruction = EmotionEngine.Instruction()
        IT = EmotionEngine.InstructionType

        op = opcode & 0x3F
        match op:
            case 0x00:
                # sll
                instruction.type = IT.GenericInt

                dest = (opcode >> 11) & 0x1F
                if dest == 0:
                    # nop
                    instruction.name = "nop"
                else:   
                    instruction.name = "sll"
                    instruction.dest = dest
                    instruction.source1 = (opcode >> 16) & 0x1F
                    instruction.operand = (opcode >> 6) & 0x1F
            case 0x02:
                # srl
                instruction.type = IT.GenericInt
                instruction.name = "srl"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x03:
                # sra
                instruction.type = IT.GenericInt
                instruction.name = "sra"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x04:
                # sllv
                instruction.type = IT.GenericInt
                instruction.name = "sllv"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x06:
                # srlv
                instruction.type = IT.GenericInt
                instruction.name = "srlv"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x07:
                # srav
                instruction.type = IT.GenericInt
                instruction.name = "srav"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x08:
                # jr
                instruction.type = IT.GenericInt # TODO: Different instruction type
                instruction.name = "jr"
                instruction.dest = (opcode >> 21) & 0x1F
            case 0x09:
                # jalr
                instruction.type = IT.GenericInt # TODO: Different instruction type
                instruction.name = "jalr"
                instruction.dest = (opcode >> 21) & 0x1F
            case 0x0A:
                # movz
                instruction.type = IT.GenericInt
                instruction.name = "movz"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x0B:
                # movn
                instruction.type = IT.GenericInt
                instruction.name = "movn"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x0C:
                # syscall
                instruction.type = IT.GenericInt
                instruction.name = "syscall"
            case 0x0D:
                # break
                instruction.type = IT.GenericInt
                instruction.name = "break"
            case 0x0F:
                # sync
                instruction.type = IT.GenericInt
                instruction.name = "sync"
            case 0x10:
                # mfhi
                instruction.type = IT.GenericInt
                instruction.name = "mfhi"
                instruction.dest = (opcode >> 11) & 0x1F
            case 0x11:
                # mthi
                instruction.type = IT.GenericInt
                instruction.name = "mthi"
                instruction.dest = (opcode >> 21) & 0x1F
            case 0x12:
                # mflo
                instruction.type = IT.GenericInt
                instruction.name = "mflo"
                instruction.dest = (opcode >> 11) & 0x1F
            case 0x13:
                # mtlo
                instruction.type = IT.GenericInt
                instruction.name = "mtlo"
                instruction.dest = (opcode >> 21) & 0x1F
            case 0x14:
                # dsllv
                instruction.type = IT.GenericInt
                instruction.name = "dsllv"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x16:
                # dsrlv
                instruction.type = IT.GenericInt
                instruction.name = "dsrlv"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x17:
                # dsrav
                instruction.type = IT.GenericInt
                instruction.name = "dsrav"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x18:
                # mult
                instruction.type = IT.GenericInt
                instruction.name = "mult"
                instruction.dest = (opcode >> 16) & 0x1F
                instruction.source1 = (opcode >> 21) & 0x1F
            case 0x19:
                # multu
                instruction.type = IT.GenericInt
                instruction.name = "multu"
                instruction.dest = (opcode >> 16) & 0x1F
                instruction.source1 = (opcode >> 21) & 0x1F
            case 0x1A:
                # div
                instruction.type = IT.GenericInt
                instruction.name = "div"
                instruction.dest = (opcode >> 16) & 0x1F
                instruction.source1 = (opcode >> 21) & 0x1F
            case 0x1B:
                # divu
                instruction.type = IT.GenericInt
                instruction.name = "divu"
                instruction.dest = (opcode >> 16) & 0x1F
                instruction.source1 = (opcode >> 21) & 0x1F
            case 0x20:
                # add
                instruction.type = IT.GenericInt
                instruction.name = "add"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x21:
                # addu
                instruction.type = IT.GenericInt
                instruction.name = "addu"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x22:
                # sub
                instruction.type = IT.GenericInt
                instruction.name = "sub"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x23:
                # subu
                instruction.type = IT.GenericInt
                instruction.name = "subu"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x24:
                # and
                instruction.type = IT.GenericInt
                instruction.name = "and"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x25:
                # or
                instruction.type = IT.GenericInt
                instruction.name = "or"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x26:
                # xor
                instruction.type = IT.GenericInt
                instruction.name = "xor"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x27:
                # nor
                instruction.type = IT.GenericInt
                instruction.name = "nor"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x28:
                # mfsa
                instruction.type = IT.GenericInt
                instruction.name = "mfsa"
                instruction.dest = (opcode >> 11) & 0x1F
            case 0x29:
                # mfsa
                instruction.type = IT.GenericInt
                instruction.name = "mtsa"
                instruction.dest = (opcode >> 11) & 0x1F
            case 0x2A:
                # slt
                instruction.type = IT.GenericInt
                instruction.name = "slt"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x2B:
                # sltu
                instruction.type = IT.GenericInt
                instruction.name = "sltu"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x2C:
                # dadd
                instruction.type = IT.GenericInt
                instruction.name = "dadd"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x2D:
                # daddu
                instruction.type = IT.GenericInt
                instruction.name = "daddu"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x2E:
                # dsub
                instruction.type = IT.GenericInt
                instruction.name = "dsub"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x2F:
                # dsubu
                instruction.type = IT.GenericInt
                instruction.name = "dsubu"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.source2 = (opcode >> 21) & 0x1F
            case 0x34:
                # teq
                instruction.type = IT.GenericInt
                instruction.name = "teq"
                instruction.dest = (opcode >> 16) & 0x1F
                instruction.source1 = (opcode >> 21) & 0x1F
            case 0x38:
                # dsll
                instruction.type = IT.GenericInt
                instruction.name = "dsll"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x3A:
                # dsrl
                instruction.type = IT.GenericInt
                instruction.name = "dsrl"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x3B:
                # dsra
                instruction.type = IT.GenericInt
                instruction.name = "dsra"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x3C:
                # dsll32
                instruction.type = IT.GenericInt
                instruction.name = "dsll32"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x3E:
                # dsrl32
                instruction.type = IT.GenericInt
                instruction.name = "dsrl32"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
            case 0x3F:
                # dsra32
                instruction.type = IT.GenericInt
                instruction.name = "dsra32"
                instruction.dest = (opcode >> 11) & 0x1F
                instruction.source1 = (opcode >> 16) & 0x1F
                instruction.operand = (opcode >> 6) & 0x1F
        return instruction

    @staticmethod
    def decode(data: bytes, addr: int) -> Instruction:
        opcode = int.from_bytes(data, "little")
        op = opcode >> 26
        instruction = EmotionEngine.Instruction()

        match op:
            case 0x00:
                return EmotionEngine._decode_special(opcode, addr)
            case _:
                return instruction

    def get_instruction_info(self, data: bytes, addr: int):
        result = InstructionInfo()
        result.length = 4
        return result
    
    def get_instruction_text(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = self.decode(data[0:4], addr)
        IT = EmotionEngine.InstructionType
        tokens = []

        if instruction.type == IT.UNDEFINED:
            return None

        match instruction.type:
            case IT.GenericInt:
                tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, instruction.name))
                if instruction.dest is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, " "))
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

        return tokens, 4