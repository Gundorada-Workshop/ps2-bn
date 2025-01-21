from .ee import il as ee_func
from .ee.registers import get_name as ee_get_name
from .ee.registers import ZERO_REG
from .fpu.registers import get_name as fpu_get_name
from .vu0f.registers import get_name as vu0f_get_name
from .instruction import Instruction, InstructionType

def sign_extend_16_bit(i: int):
    if i >= 0x8000:
        i -= 0x10000
    return i

@staticmethod
def _decode_special(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType

    op = opcode & 0x3F
    match op:
        case 0x00:
            # sll
            instruction.type = IT.GenericInt

            dest = ee_get_name((opcode >> 11) & 0x1F)
            if dest == 0:
                # nop
                instruction.name = "nop"
                instruction.il_func = ee_func.nop
            else:   
                instruction.name = "sll"
                instruction.il_func = ee_func.sll
                instruction.reg1 = dest
                instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
                instruction.operand = (opcode >> 6) & 0x1F
        case 0x02:
            # srl
            instruction.type = IT.GenericInt
            instruction.name = "srl"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x03:
            # sra
            instruction.type = IT.GenericInt
            instruction.name = "sra"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x04:
            # sllv
            instruction.type = IT.GenericInt
            instruction.name = "sllv"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x06:
            # srlv
            instruction.type = IT.GenericInt
            instruction.name = "srlv"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x07:
            # srav
            instruction.type = IT.GenericInt
            instruction.name = "srav"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x08:
            # jr
            instruction.type = IT.Branch
            instruction.name = "jr"
            instruction.il_func = ee_func.jr
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x09:
            # jalr
            instruction.type = IT.Branch
            instruction.name = "jalr"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x0A:
            # movz
            instruction.type = IT.GenericInt
            instruction.name = "movz"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x0B:
            # movn
            instruction.type = IT.GenericInt
            instruction.name = "movn"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
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
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x11:
            # mthi
            instruction.type = IT.GenericInt
            instruction.name = "mthi"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # mflo
            instruction.type = IT.GenericInt
            instruction.name = "mflo"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x13:
            # mtlo
            instruction.type = IT.GenericInt
            instruction.name = "mtlo"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x14:
            # dsllv
            instruction.type = IT.GenericInt
            instruction.name = "dsllv"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x16:
            # dsrlv
            instruction.type = IT.GenericInt
            instruction.name = "dsrlv"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x17:
            # dsrav
            instruction.type = IT.GenericInt
            instruction.name = "dsrav"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x18:
            # mult
            instruction.type = IT.GenericInt
            instruction.name = "mult"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x19:
            # multu
            instruction.type = IT.GenericInt
            instruction.name = "multu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # div
            instruction.type = IT.GenericInt
            instruction.name = "div"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1B:
            # divu
            instruction.type = IT.GenericInt
            instruction.name = "divu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x20:
            # add
            instruction.type = IT.GenericInt
            instruction.name = "add"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x21:
            # addu
            instruction.type = IT.GenericInt
            instruction.name = "addu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x22:
            # sub
            instruction.type = IT.GenericInt
            instruction.name = "sub"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x23:
            # subu
            instruction.type = IT.GenericInt
            instruction.name = "subu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x24:
            # and
            instruction.type = IT.GenericInt
            instruction.name = "and"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x25:
            # or
            instruction.type = IT.GenericInt
            instruction.name = "or"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x26:
            # xor
            instruction.type = IT.GenericInt
            instruction.name = "xor"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x27:
            # nor
            instruction.type = IT.GenericInt
            instruction.name = "nor"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x28:
            # mfsa
            instruction.type = IT.GenericInt
            instruction.name = "mfsa"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x29:
            # mfsa
            instruction.type = IT.GenericInt
            instruction.name = "mtsa"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x2A:
            # slt
            instruction.type = IT.GenericInt
            instruction.name = "slt"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2B:
            # sltu
            instruction.type = IT.GenericInt
            instruction.name = "sltu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2C:
            # dadd
            instruction.type = IT.GenericInt
            instruction.name = "dadd"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2D:
            # daddu
            instruction.type = IT.GenericInt
            instruction.name = "daddu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2E:
            # dsub
            instruction.type = IT.GenericInt
            instruction.name = "dsub"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2F:
            # dsubu
            instruction.type = IT.GenericInt
            instruction.name = "dsubu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x34:
            # teq
            instruction.type = IT.GenericInt
            instruction.name = "teq"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x38:
            # dsll
            instruction.type = IT.GenericInt
            instruction.name = "dsll"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3A:
            # dsrl
            instruction.type = IT.GenericInt
            instruction.name = "dsrl"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3B:
            # dsra
            instruction.type = IT.GenericInt
            instruction.name = "dsra"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3C:
            # dsll32
            instruction.type = IT.GenericInt
            instruction.name = "dsll32"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3E:
            # dsrl32
            instruction.type = IT.GenericInt
            instruction.name = "dsrl32"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3F:
            # dsra32
            instruction.type = IT.GenericInt
            instruction.name = "dsra32"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
    return instruction

@staticmethod
def decode(data: bytes, addr: int) -> Instruction:
    opcode = int.from_bytes(data, "little")
    op = opcode >> 26
    instruction = Instruction()
    IT = InstructionType

    match op:
        case 0x00:
            return _decode_special(opcode, addr)
        case 0x01:
            # TODO
            # regimm
            pass
        case 0x02:
            # j
            instruction.type = IT.Branch
            instruction.name = "j"
            offset = (opcode & 0x3FFFFFF) << 2
            offset += (addr + 4) & 0xF0000000
            instruction.branch_dest = offset
        case 0x03:
            # jal
            instruction.type = IT.Branch
            instruction.name = "jal"
            offset = (opcode & 0x3FFFFFF) << 2
            offset += (addr + 4) & 0xF0000000
            instruction.branch_dest = offset
        case 0x04:
            # beq
            instruction.type = IT.Branch
            instruction.name = "beq"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset

            # psuedo-ops
            if ee_get_name(instruction.reg1) == ZERO_REG and \
                ee_get_name(instruction.reg2) == ZERO_REG:
                instruction.name = "b"
            elif ee_get_name(instruction.reg2) == ZERO_REG:
                instruction.name = "beqz"
            elif ee_get_name(instruction.reg1) == ZERO_REG:
                # swap registers so $zero is last for easier handling later
                instruction.name = "beqz"
                instruction.reg1, instruction.reg2 = instruction.reg2, instruction.reg1
        case 0x05:
            # bne
            instruction.type = IT.Branch
            instruction.name = "bne"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset

            # psuedo-ops
            if ee_get_name(instruction.reg2) == ZERO_REG:
                instruction.name = "bnez"
            elif ee_get_name(instruction.reg1) == ZERO_REG:
                # swap registers so $zero is last for easier handling later
                instruction.name = "bnez"
                instruction.reg1, instruction.reg2 = instruction.reg2, instruction.reg1
        case 0x06:
            # blez
            instruction.type = IT.Branch
            instruction.name = "blez"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset
        case 0x07:
            # bgtz
            instruction.type = IT.Branch
            instruction.name = "bgtz"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset
        case 0x08:
            # addi
            instruction.type = IT.GenericInt
            instruction.name = "addi"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x09:
            # addiu
            instruction.type = IT.GenericInt
            instruction.name = "addiu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x0A:
            # slti
            instruction.type = IT.GenericInt
            instruction.name = "slti"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x0B:
            # sltiu
            instruction.type = IT.GenericInt
            instruction.name = "sltiu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            operand = opcode & 0xFFFF
            if operand >= 0x8000:
                # sltiu allows you to compare any number below 0x0-0x7FFF or
                # 0xFFFF8000-0xFFFFFFFF
                # thanks MIPS very cool
                operand = 0x1_0000_0000 - operand
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x0C:
            # andi
            instruction.type = IT.GenericInt
            instruction.name = "andi"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0D:
            # ori
            instruction.type = IT.GenericInt
            instruction.name = "ori"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0E:
            # xori
            instruction.type = IT.GenericInt
            instruction.name = "xori"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0F:
            # lui
            instruction.type = IT.GenericInt
            instruction.name = "lui"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x10 | 0x11 | 0x12 | 0x13:
            # cop instructions
            # TODO
            pass
        case 0x14:
            # beql
            instruction.type = IT.Branch
            instruction.name = "beql"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset

            # psuedo-ops
            if ee_get_name(instruction.reg2) == ZERO_REG:
                instruction.name = "beqzl"
            elif ee_get_name(instruction.reg1) == ZERO_REG:
                # swap registers so $zero is last for easier handling later
                instruction.name = "beqzl"
                instruction.reg1, instruction.reg2 = instruction.reg2, instruction.reg1
        case 0x15:
            # bnel
            instruction.type = IT.Branch
            instruction.name = "bnel"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset

            # psuedo-ops
            if ee_get_name(instruction.reg2) == ZERO_REG:
                instruction.name = "bnezl"
            elif ee_get_name(instruction.reg1) == ZERO_REG:
                # swap registers so $zero is last for easier handling later
                instruction.name = "bnezl"
                instruction.reg1, instruction.reg2 = instruction.reg2, instruction.reg1
        case 0x16:
            # blezl
            instruction.type = IT.Branch
            instruction.name = "blezl"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset
        case 0x17:
            # bgtzl
            instruction.type = IT.Branch
            instruction.name = "bgtzl"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
            instruction.branch_dest = offset
        case 0x18:
            # daddi
            instruction.type = IT.GenericInt
            instruction.name = "daddi"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x19:
            # daddiu
            instruction.type = IT.GenericInt
            instruction.name = "daddiu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x1A:
            # ldl
            instruction.type = IT.LoadStore
            instruction.name = "ldl"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x1B:
            # ldr
            instruction.type = IT.LoadStore
            instruction.name = "ldr"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x1C:
            # mmi
            # TODO
            pass
        case 0x1E:
            # lq
            instruction.type = IT.LoadStore
            instruction.name = "lq"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x1F:
            # sq
            instruction.type = IT.LoadStore
            instruction.name = "sq"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x20:
            # lb
            instruction.type = IT.LoadStore
            instruction.name = "lb"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x21:
            # lh
            instruction.type = IT.LoadStore
            instruction.name = "sq"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x22:
            # lwl
            instruction.type = IT.LoadStore
            instruction.name = "lwl"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x23:
            # lw
            instruction.type = IT.LoadStore
            instruction.name = "lw"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x24:
            # lbu
            instruction.type = IT.LoadStore
            instruction.name = "lbu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x25:
            # lhu
            instruction.type = IT.LoadStore
            instruction.name = "lhu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x26:
            # lwr
            instruction.type = IT.LoadStore
            instruction.name = "lwr"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x27:
            # lwu
            instruction.type = IT.LoadStore
            instruction.name = "lwu"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x28:
            # sb
            instruction.type = IT.LoadStore
            instruction.name = "sb"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x29:
            # sh
            instruction.type = IT.LoadStore
            instruction.name = "sh"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2A:
            # swl
            instruction.type = IT.LoadStore
            instruction.name = "swl"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2B:
            # sw
            instruction.type = IT.LoadStore
            instruction.name = "sw"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2C:
            # sdl
            instruction.type = IT.LoadStore
            instruction.name = "sdl"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2D:
            # sdr
            instruction.type = IT.LoadStore
            instruction.name = "sdr"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2E:
            # swr
            instruction.type = IT.LoadStore
            instruction.name = "swr"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x2F:
            # cache
            instruction.type = IT.GenericInt
            instruction.name = "cache"
            instruction.il_func = ee_func.nop
        case 0x31:
            # lwc1
            instruction.type = IT.LoadStore
            instruction.name = "lwc1"
            instruction.reg1 = fpu_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x33:
            # prefetch
            instruction.type = IT.GenericInt
            instruction.name = "prefetch"
            instruction.il_func = ee_func.nop
        case 0x36:
            # lqc2
            instruction.type = IT.LoadStore
            instruction.name = "lqc2"
            instruction.reg1 = vu0f_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x37:
            # ld
            instruction.type = IT.LoadStore
            instruction.name = "ld"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x39:
            # swc1
            instruction.type = IT.LoadStore
            instruction.name = "swc1"
            instruction.reg1 = fpu_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x3E:
            # sqc2
            instruction.type = IT.LoadStore
            instruction.name = "sqc2"
            instruction.reg1 = vu0f_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x3F:
            # sd
            instruction.type = IT.LoadStore
            instruction.name = "sd"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case _:
            return instruction