from .ee import il as ee_func
from .ee.registers import ZERO_REG
from .ee.registers import get_name as ee_get_name
from .fpu.registers import get_name as fpu_get_name
from .vu0.registers import get_f_name as vu0f_get_name
from .cop0.registers import get_name as cop0_get_name
from .fpu.registers import get_c_name as fpu_get_c_name
from .vu0.registers import get_c_name as vu0f_get_c_name
from .vu0.decode import decode_cop2_special
from .cop0.registers import get_c_name as cop0_get_c_name
from .instruction import Instruction, InstructionType

def sign_extend_16_bit(i: int):
    if i >= 0x8000:
        i -= 0x10000
    return i

def get_branch_dest(opcode: int, addr: int) -> int:
    offset = sign_extend_16_bit(opcode & 0xFFFF) << 2
    offset += addr
    offset += 4 # for branch delay slot
    return offset

def decode_regimm(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 16) & 0x1F

    match op:
        case 0x00:
            # bltz
            instruction.type = IT.Branch
            instruction.name = "bltz"
            instruction.il_func = ee_func.bltz
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x01:
            # bgez
            instruction.type = IT.Branch
            instruction.name = "bgez"
            instruction.il_func = ee_func.bgez
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x02:
            # bltzl
            instruction.type = IT.Branch
            instruction.name = "bltzl"
            instruction.il_func = ee_func.bltzl
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x03:
            # bgezl
            instruction.type = IT.Branch
            instruction.name = "bgezl"
            instruction.il_func = ee_func.bgezl
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x10:
            # bltzal
            instruction.type = IT.Branch
            instruction.name = "bltzal"
            instruction.il_func = ee_func.bltzal
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x11:
            # bgezal
            instruction.type = IT.Branch
            instruction.name = "bgezal"
            instruction.il_func = ee_func.bgezal
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x12:
            # bltzall
            instruction.type = IT.Branch
            instruction.name = "bltzall"
            instruction.il_func = ee_func.bltzall
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x13:
            # bgezall
            instruction.type = IT.Branch
            instruction.name = "bgezall"
            instruction.il_func = ee_func.bgezall
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x18:
            # mtsab
            instruction.type = IT.GenericInt
            instruction.name = "mtsab"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x19:
            # mtsah
            instruction.type = IT.GenericInt
            instruction.name = "mtsah"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)

    return instruction

def decode_cop(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 21) & 0x1F
    cop_id = ((opcode >> 26) & 0x3)

    if cop_id == 2 and op >= 0x10:
        return decode_cop2_special(opcode, addr)
    
    match (op | (cop_id * 0x100)):
        case 0x000:
            # mfc0
            instruction.type = IT.GenericInt
            instruction.name = "mfc0"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = cop0_get_name((opcode >> 11) & 0x1F)
        case 0x100:
            # mfc1
            instruction.type = IT.GenericInt
            instruction.name = "mfc1"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x004:
            # mtc0
            instruction.type = IT.GenericInt
            instruction.name = "mtc0"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = cop0_get_name((opcode >> 11) & 0x1F)
        case 0x104:
            # mtc1
            instruction.type = IT.GenericInt
            instruction.name = "mtc1"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x010:
            op2 = opcode & 0x3F
            match op2:
                case 0x1:
                    # tlbr
                    instruction.type = IT.GenericInt
                    instruction.name = "tlbr"
                case 0x2:
                    # tlbwi
                    instruction.type = IT.GenericInt
                    instruction.name = "tlbwi"
                case 0x18:
                    # eret
                    instruction.type = IT.Branch
                    instruction.name = "eret"
                case 0x38:
                    # ei
                    instruction.type = IT.GenericInt
                    instruction.name = "ei"
                    instruction.il_func = ee_func.ei
                case 0x39:
                    # di
                    instruction.type = IT.GenericInt
                    instruction.name = "di"
                    instruction.il_func = ee_func.di
        case 0x102:
            # cfc1
            instruction.type = IT.GenericInt
            instruction.name = "cfc1"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_c_name((opcode >> 11) & 0x1F)
        case 0x202:
            # cfc2
            instruction.type = IT.GenericInt
            instruction.name = "cfc2"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_c_name((opcode >> 11) & 0x1F)
        case 0x106:
            # ctc1
            instruction.type = IT.GenericInt
            instruction.name = "ctc1"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = fpu_get_c_name((opcode >> 11) & 0x1F)
        case 0x206:
            # ctc2
            instruction.type = IT.GenericInt
            instruction.name = "ctc2"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_c_name((opcode >> 11) & 0x1F)
        case 0x008:
            # bc0
            instruction.type = IT.Branch
            instruction.name = "bc0"
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.cop_branch_type = bool((opcode >> 16) & 1)
            instruction.is_likely = bool((opcode >> 17) & 1)
        case 0x108:
            # bc1
            instruction.type = IT.Branch
            instruction.name = "bc1"
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.cop_branch_type = bool((opcode >> 16) & 1)
            instruction.is_likely = bool((opcode >> 17) & 1)
        case 0x208:
            # bc2
            instruction.type = IT.Branch
            instruction.name = "bc2"
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.cop_branch_type = bool((opcode >> 16) & 1)
            instruction.is_likely = bool((opcode >> 17) & 1)
        case 0x110:
            # FPU functions
            return decode_cop_s(opcode, addr)
        case 0x114:
            # cvt.s.w
            instruction.type = IT.GenericInt
            instruction.name = "cvt.s.w"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x201:
            # qmfc2
            instruction.type = IT.GenericInt
            instruction.name = "qmfc2"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_name((opcode >> 11) & 0x1F)
        case 0x205:
            # qmtc2
            instruction.type = IT.GenericInt
            instruction.name = "qmtc2"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = vu0f_get_name((opcode >> 11) & 0x1F)

    return instruction

def decode_cop_s(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = opcode & 0x3F

    match op:
        case 0x0:
            # add.s
            instruction.type = IT.GenericInt
            instruction.name = "add.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1:
            # sub.s
            instruction.type = IT.GenericInt
            instruction.name = "sub.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x2:
            # mul.s
            instruction.type = IT.GenericInt
            instruction.name = "mul.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x3:
            # div.s
            instruction.type = IT.GenericInt
            instruction.name = "div.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x4:
            # sqrt.s
            instruction.type = IT.GenericInt
            instruction.name = "sqrt.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x5:
            # abs.s
            instruction.type = IT.GenericInt
            instruction.name = "abs.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x6:
            # mov.s
            instruction.type = IT.GenericInt
            instruction.name = "mov.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x7:
            # neg.s
            instruction.type = IT.GenericInt
            instruction.name = "neg.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x16:
            # rsqrt.s
            instruction.type = IT.GenericInt
            instruction.name = "rsqrt.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x18:
            # adda.s
            instruction.type = IT.GenericInt
            instruction.name = "adda.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x19:
            # suba.s
            instruction.type = IT.GenericInt
            instruction.name = "suba.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1A:
            # mula.s
            instruction.type = IT.GenericInt
            instruction.name = "mula.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1C:
            # madd.s
            instruction.type = IT.GenericInt
            instruction.name = "madd.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1D:
            # msub.s
            instruction.type = IT.GenericInt
            instruction.name = "msub.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1E:
            # madda.s
            instruction.type = IT.GenericInt
            instruction.name = "madda.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x1F:
            # msuba.s
            instruction.type = IT.GenericInt
            instruction.name = "msuba.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x24:
            # cvt.w.s
            instruction.type = IT.GenericInt
            instruction.name = "cvt.w.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
        case 0x28:
            # max.s
            instruction.type = IT.GenericInt
            instruction.name = "max.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x29:
            # min.s
            instruction.type = IT.GenericInt
            instruction.name = "min.s"
            instruction.reg1 = fpu_get_name((opcode >> 6) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg3 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x30:
            # c.f.s
            instruction.type = IT.GenericInt
            instruction.name = "c.f.s"
        case 0x32:
            # c.eq.s
            instruction.type = IT.GenericInt
            instruction.name = "c.eq.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x34:
            # c.lt.s
            instruction.type = IT.GenericInt
            instruction.name = "c.lt.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)
        case 0x36:
            # c.eq.s
            instruction.type = IT.GenericInt
            instruction.name = "c.le.s"
            instruction.reg1 = fpu_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = fpu_get_name((opcode >> 16) & 0x1F)

    return instruction

def decode_special(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType

    op = opcode & 0x3F
    match op:
        case 0x00:
            # sll
            instruction.type = IT.GenericInt

            dest = ee_get_name((opcode >> 11) & 0x1F)
            if dest == ZERO_REG:
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
            instruction.il_func = ee_func.srl
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x03:
            # sra
            instruction.type = IT.GenericInt
            instruction.name = "sra"
            instruction.il_func = ee_func.sra
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
            instruction.type = IT.Branch
            instruction.name = "syscall"
            instruction.il_func = ee_func.syscall
        case 0x0D:
            # break
            instruction.type = IT.GenericInt
            instruction.name = "break"
            instruction.il_func = ee_func.break_ee
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
            instruction.il_func = ee_func.add
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x21:
            # addu
            instruction.type = IT.GenericInt
            instruction.name = "addu"
            instruction.il_func = ee_func.addu
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
            instruction.il_func = ee_func.ee_and
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x25:
            # or
            instruction.type = IT.GenericInt
            instruction.name = "or"
            instruction.il_func = ee_func.ee_or
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x26:
            # xor
            instruction.type = IT.GenericInt
            instruction.name = "xor"
            instruction.il_func = ee_func.ee_xor
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x27:
            # nor
            instruction.type = IT.GenericInt
            instruction.name = "nor"
            instruction.il_func = ee_func.ee_nor
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
            instruction.il_func = ee_func.slt
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x2B:
            # sltu
            instruction.type = IT.GenericInt
            instruction.name = "sltu"
            instruction.il_func = ee_func.sltu
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x2C:
            # dadd
            instruction.type = IT.GenericInt
            instruction.name = "dadd"
            instruction.il_func = ee_func.dadd
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x2D:
            # daddu
            instruction.type = IT.GenericInt
            instruction.name = "daddu"
            instruction.il_func = ee_func.daddu
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
            instruction.il_func = ee_func.dsll
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3A:
            # dsrl
            instruction.type = IT.GenericInt
            instruction.name = "dsrl"
            instruction.il_func = ee_func.dsrl
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3B:
            # dsra
            instruction.type = IT.GenericInt
            instruction.name = "dsra"
            instruction.il_func = ee_func.dsra
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3C:
            # dsll32
            instruction.type = IT.GenericInt
            instruction.name = "dsll32"
            instruction.il_func = ee_func.dsll32
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3E:
            # dsrl32
            instruction.type = IT.GenericInt
            instruction.name = "dsrl32"
            instruction.il_func = ee_func.dsrl32
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
        case 0x3F:
            # dsra32
            instruction.type = IT.GenericInt
            instruction.name = "dsra32"
            instruction.il_func = ee_func.dsra32
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = (opcode >> 6) & 0x1F
    return instruction

def decode_mmi(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = opcode & 0x3F

    match op:
        case 0x00:
            # madd
            instruction.type = IT.GenericInt
            instruction.name = "madd"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x01:
            # maddu
            instruction.type = IT.GenericInt
            instruction.name = "maddu"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x04:
            # plzcw
            instruction.type = IT.GenericInt
            instruction.name = "plzcw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x08:
            return decode_mmi0(opcode, addr)
        case 0x09:
            return decode_mmi2(opcode, addr)
        case 0x10:
            # mfhi1
            instruction.type = IT.GenericInt
            instruction.name = "mfhi1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x11:
            # mthi1
            instruction.type = IT.GenericInt
            instruction.name = "mthi1"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # mflo1
            instruction.type = IT.GenericInt
            instruction.name = "mflo1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x13:
            # mtlo1
            instruction.type = IT.GenericInt
            instruction.name = "mtlo1"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x18:
            # mult1
            instruction.type = IT.GenericInt
            instruction.name = "mult1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x19:
            # multu1
            instruction.type = IT.GenericInt
            instruction.name = "multu1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # div1
            instruction.type = IT.GenericInt
            instruction.name = "div1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1B:
            # divu1
            instruction.type = IT.GenericInt
            instruction.name = "divu1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x20:
            # madd1
            instruction.type = IT.GenericInt
            instruction.name = "madd1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x21:
            # maddu1
            instruction.type = IT.GenericInt
            instruction.name = "maddu1"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x28:
            return decode_mmi1(opcode, addr)
        case 0x29:
            return decode_mmi3(opcode, addr)
        case 0x30:
            return decode_pmfhlfmt(opcode, addr)
        case 0x31:
            # pmthllw
            instruction.type = IT.GenericInt
            instruction.name = "pmthllw"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F) 
        case 0x34:
            # psllh
            instruction.type = IT.GenericInt
            instruction.name = "psllh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        case 0x36:
            # psrlh
            instruction.type = IT.GenericInt
            instruction.name = "psrlh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        case 0x37:
            # psrah
            instruction.type = IT.GenericInt
            instruction.name = "psrah"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        case 0x3C:
            # psllw
            instruction.type = IT.GenericInt
            instruction.name = "psllw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        case 0x3E:
            # psrlw
            instruction.type = IT.GenericInt
            instruction.name = "psrlw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        case 0x3F:
            # psraw
            instruction.type = IT.GenericInt
            instruction.name = "psraw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F) 
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F) 
        
    return instruction

def decode_mmi0(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 6) & 0x1F

    match op:
        case 0x00:
            # paddw
            instruction.type = IT.GenericInt
            instruction.name = "paddw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x01:
            # psubw
            instruction.type = IT.GenericInt
            instruction.name = "psubw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x02:
            # pcgtw
            instruction.type = IT.GenericInt
            instruction.name = "pcgtw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x03:
            # pmaxw
            instruction.type = IT.GenericInt
            instruction.name = "pmaxw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x04:
            # paddh
            instruction.type = IT.GenericInt
            instruction.name = "paddh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x05:
            # psubh
            instruction.type = IT.GenericInt
            instruction.name = "psubh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x06:
            # pcgth
            instruction.type = IT.GenericInt
            instruction.name = "pcgth"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x07:
            # pmaxh
            instruction.type = IT.GenericInt
            instruction.name = "pmaxh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x08:
            # paddb
            instruction.type = IT.GenericInt
            instruction.name = "paddb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x09:
            # psubb
            instruction.type = IT.GenericInt
            instruction.name = "psubb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x0A:
            # pcgtb
            instruction.type = IT.GenericInt
            instruction.name = "pcgtb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x10:
            # paddsw
            instruction.type = IT.GenericInt
            instruction.name = "paddsw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x11:
            # psubsw
            instruction.type = IT.GenericInt
            instruction.name = "psubsw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # pextlw
            instruction.type = IT.GenericInt
            instruction.name = "pextlw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x13:
            # ppacw
            instruction.type = IT.GenericInt
            instruction.name = "ppacw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x14:
            # paddsh
            instruction.type = IT.GenericInt
            instruction.name = "paddsh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x15:
            # psubsh
            instruction.type = IT.GenericInt
            instruction.name = "psubsh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x16:
            # pextlh
            instruction.type = IT.GenericInt
            instruction.name = "pextlh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x17:
            # ppach
            instruction.type = IT.GenericInt
            instruction.name = "ppach"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x18:
            # paddsb
            instruction.type = IT.GenericInt
            instruction.name = "paddsb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x19:
            # psubsb
            instruction.type = IT.GenericInt
            instruction.name = "psubsb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # pextlb
            instruction.type = IT.GenericInt
            instruction.name = "pextlb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1B:
            # ppacb
            instruction.type = IT.GenericInt
            instruction.name = "ppacb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1E:
            # pext5
            instruction.type = IT.GenericInt
            instruction.name = "pext5"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1F:
            # ppac5
            instruction.type = IT.GenericInt
            instruction.name = "ppac5"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)

    return instruction

def decode_mmi1(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 6) & 0x1F

    match op:
        case 0x01:
            # pabsw
            instruction.type = IT.GenericInt
            instruction.name = "pabsw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x02:
            # pceqw
            instruction.type = IT.GenericInt
            instruction.name = "pceqw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x03:
            # pminw
            instruction.type = IT.GenericInt
            instruction.name = "pminw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x04:
            # padsbh
            instruction.type = IT.GenericInt
            instruction.name = "padsbh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x05:
            # pabsh
            instruction.type = IT.GenericInt
            instruction.name = "pabsh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x06:
            # pceqh
            instruction.type = IT.GenericInt
            instruction.name = "pceqh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x07:
            # pminh
            instruction.type = IT.GenericInt
            instruction.name = "pminh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x0A:
            # pceqb
            instruction.type = IT.GenericInt
            instruction.name = "pceqb"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x10:
            # padduw
            instruction.type = IT.GenericInt
            instruction.name = "padduw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x11:
            # psubuw
            instruction.type = IT.GenericInt
            instruction.name = "psubuw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # pextuw
            instruction.type = IT.GenericInt
            instruction.name = "pextuw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x14:
            # padduh
            instruction.type = IT.GenericInt
            instruction.name = "padduh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x15:
            # psubuh
            instruction.type = IT.GenericInt
            instruction.name = "psubuh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x16:
            # pextuh
            instruction.type = IT.GenericInt
            instruction.name = "pextuh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x18:
            # paddub
            instruction.type = IT.GenericInt
            instruction.name = "paddub"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x19:
            # psubub
            instruction.type = IT.GenericInt
            instruction.name = "psubub"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # pextub
            instruction.type = IT.GenericInt
            instruction.name = "pextub"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1B:
            # qfsrv
            instruction.type = IT.GenericInt
            instruction.name = "qfsrv"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)

    return instruction

def decode_mmi2(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 6) & 0x1F

    match op:
        case 0x00:
            # pmaddw
            instruction.type = IT.GenericInt
            instruction.name = "pmaddw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x02:
            # psllvw
            instruction.type = IT.GenericInt
            instruction.name = "psllvw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x03:
            # psrlvw
            instruction.type = IT.GenericInt
            instruction.name = "psrlvw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x04:
            # pmsubw
            instruction.type = IT.GenericInt
            instruction.name = "pmsubw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x08:
            # pmfhi
            instruction.type = IT.GenericInt
            instruction.name = "pmfhi"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x09:
            # pmflo
            instruction.type = IT.GenericInt
            instruction.name = "pmflo"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x0A:
            # pinth
            instruction.type = IT.GenericInt
            instruction.name = "pinth"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xC:
            # pmultw
            instruction.type = IT.GenericInt
            instruction.name = "pmultw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xD:
            # pdivw
            instruction.type = IT.GenericInt
            instruction.name = "pdivw"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xE:
            # pcpyld
            instruction.type = IT.GenericInt
            instruction.name = "pcpyld"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x10:
            # pmaddh
            instruction.type = IT.GenericInt
            instruction.name = "pmaddh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x11:
            # phmadh
            instruction.type = IT.GenericInt
            instruction.name = "phmadh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # pand
            instruction.type = IT.GenericInt
            instruction.name = "pand"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x13:
            # pxor
            instruction.type = IT.GenericInt
            instruction.name = "pxor"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x14:
            # pmsubh
            instruction.type = IT.GenericInt
            instruction.name = "pmsubh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x15:
            # phmsbh
            instruction.type = IT.GenericInt
            instruction.name = "phmsbh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # pexeh
            instruction.type = IT.GenericInt
            instruction.name = "pexeh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1B:
            # prevh
            instruction.type = IT.GenericInt
            instruction.name = "prevh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1C:
            # pmulth
            instruction.type = IT.GenericInt
            instruction.name = "pmulth"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1D:
            # pext5
            instruction.type = IT.GenericInt
            instruction.name = "pdivbw"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1E:
            # pexew
            instruction.type = IT.GenericInt
            instruction.name = "pexew"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1F:
            # prot3w
            instruction.type = IT.GenericInt
            instruction.name = "prot3w"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)

    return instruction

def decode_mmi3(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 6) & 0x1F

    match op:
        case 0x00:
            # pmadduw
            instruction.type = IT.GenericInt
            instruction.name = "pmadduw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x03:
            # psravw
            instruction.type = IT.GenericInt
            instruction.name = "psravw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x08:
            # pmthi
            instruction.type = IT.GenericInt
            instruction.name = "pmthi"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x09:
            # pmtlo
            instruction.type = IT.GenericInt
            instruction.name = "pmtlo"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x0A:
            # pinteh
            instruction.type = IT.GenericInt
            instruction.name = "pinteh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xC:
            # pmultuw
            instruction.type = IT.GenericInt
            instruction.name = "pmultuw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xD:
            # pdivuw
            instruction.type = IT.GenericInt
            instruction.name = "pdivuw"
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
        case 0xE:
            # pcpyud
            instruction.type = IT.GenericInt
            instruction.name = "pcpyud"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x12:
            # por
            instruction.type = IT.GenericInt
            instruction.name = "por"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x13:
            # pnor
            instruction.type = IT.GenericInt
            instruction.name = "pnor"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg3 = ee_get_name((opcode >> 21) & 0x1F)
        case 0x1A:
            # pexch
            instruction.type = IT.GenericInt
            instruction.name = "pexch"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1B:
            # pcpyh
            instruction.type = IT.GenericInt
            instruction.name = "pcpyh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
        case 0x1E:
            # pexcw
            instruction.type = IT.GenericInt
            instruction.name = "pexew"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)

    return instruction

def decode_pmfhlfmt(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType
    op = (opcode >> 6) & 0x1F

    match op:
        case 0x00:
            # pmfhllw
            instruction.type = IT.GenericInt
            instruction.name = "pmfhllw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x01:
            # pmfhluw
            instruction.type = IT.GenericInt
            instruction.name = "pmfhluw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x02:
            # pmfhlslw
            instruction.type = IT.GenericInt
            instruction.name = "pmfhlslw"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x03:
            # pmfhllh
            instruction.type = IT.GenericInt
            instruction.name = "pmfhllh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)
        case 0x04:
            # pmfhlsh
            instruction.type = IT.GenericInt
            instruction.name = "pmfhlsh"
            instruction.reg1 = ee_get_name((opcode >> 11) & 0x1F)

    return instruction

def decode(data: bytes, addr: int) -> Instruction:
    opcode = int.from_bytes(data, "little")
    op = opcode >> 26
    instruction = Instruction()
    IT = InstructionType

    match op:
        case 0x00:
            return decode_special(opcode, addr)
        case 0x01:
            return decode_regimm(opcode, addr)
        case 0x02:
            # j
            instruction.type = IT.Branch
            instruction.name = "j"
            instruction.il_func = ee_func.j
            offset = (opcode & 0x3FFFFFF) << 2
            offset += (addr + 4) & 0xF0000000
            instruction.branch_dest = offset
        case 0x03:
            # jal
            instruction.type = IT.Branch
            instruction.name = "jal"
            instruction.il_func = ee_func.jal
            offset = (opcode & 0x3FFFFFF) << 2
            offset += (addr + 4) & 0xF0000000
            instruction.branch_dest = offset
        case 0x04:
            # beq
            instruction.type = IT.Branch
            instruction.name = "beq"
            instruction.il_func = ee_func.beq
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x05:
            # bne
            instruction.type = IT.Branch
            instruction.name = "bne"
            instruction.il_func = ee_func.bne
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x06:
            # blez
            instruction.type = IT.Branch
            instruction.name = "blez"
            instruction.il_func = ee_func.blez
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x07:
            # bgtz
            instruction.type = IT.Branch
            instruction.name = "bgtz"
            instruction.il_func = ee_func.bgtz
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
        case 0x08:
            # addi
            instruction.type = IT.GenericInt
            instruction.name = "addi"
            instruction.il_func = ee_func.addi
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x09:
            # addiu
            instruction.type = IT.GenericInt
            instruction.name = "addiu"
            instruction.il_func = ee_func.addiu
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x0A:
            # slti
            instruction.type = IT.GenericInt
            instruction.name = "slti"
            instruction.il_func = ee_func.slti
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x0B:
            # sltiu
            instruction.type = IT.GenericInt
            instruction.name = "sltiu"
            instruction.il_func = ee_func.sltiu
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
            instruction.il_func = ee_func.andi
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0D:
            # ori
            instruction.type = IT.GenericInt
            instruction.name = "ori"
            instruction.il_func = ee_func.ori
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0E:
            # xori
            instruction.type = IT.GenericInt
            instruction.name = "xori"
            instruction.il_func = ee_func.xori
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x0F:
            # lui
            instruction.type = IT.GenericInt
            instruction.name = "lui"
            instruction.il_func = ee_func.lui
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.operand = opcode & 0xFFFF
        case 0x10 | 0x11 | 0x12 | 0x13:
            # cop instructions
            return decode_cop(opcode, addr)
        case 0x14:
            # beql
            instruction.type = IT.Branch
            instruction.name = "beql"
            instruction.il_func = ee_func.beq
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x15:
            # bnel
            instruction.type = IT.Branch
            instruction.name = "bnel"
            instruction.il_func = ee_func.bne
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x16:
            # blezl
            instruction.type = IT.Branch
            instruction.name = "blezl"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x17:
            # bgtzl
            instruction.type = IT.Branch
            instruction.name = "bgtzl"
            instruction.reg1 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.branch_dest = get_branch_dest(opcode, addr)
            instruction.is_likely = True
        case 0x18:
            # daddi
            instruction.type = IT.GenericInt
            instruction.name = "daddi"
            instruction.il_func = ee_func.daddi
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x19:
            # daddiu
            instruction.type = IT.GenericInt
            instruction.name = "daddiu"
            instruction.il_func = ee_func.daddiu
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
            return decode_mmi(opcode, addr)
        case 0x1E:
            # lq
            instruction.type = IT.LoadStore
            instruction.name = "lq"
            instruction.il_func = ee_func.lq
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x1F:
            # sq
            instruction.type = IT.LoadStore
            instruction.name = "sq"
            instruction.il_func = ee_func.sq
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x20:
            # lb
            instruction.type = IT.LoadStore
            instruction.name = "lb"
            instruction.il_func = ee_func.lb
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x21:
            # lh
            instruction.type = IT.LoadStore
            instruction.name = "lh"
            instruction.il_func = ee_func.lh
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
            instruction.il_func = ee_func.lw
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x24:
            # lbu
            instruction.type = IT.LoadStore
            instruction.name = "lbu"
            instruction.il_func = ee_func.lbu
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x25:
            # lhu
            instruction.type = IT.LoadStore
            instruction.name = "lhu"
            instruction.il_func = ee_func.lhu
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
            instruction.il_func = ee_func.lwu
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x28:
            # sb
            instruction.type = IT.LoadStore
            instruction.name = "sb"
            instruction.il_func = ee_func.sb
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x29:
            # sh
            instruction.type = IT.LoadStore
            instruction.name = "sh"
            instruction.il_func = ee_func.sh
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
            instruction.il_func = ee_func.sw
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
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
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
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x37:
            # ld
            instruction.type = IT.LoadStore
            instruction.name = "ld"
            instruction.il_func = ee_func.ld
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x39:
            # swc1
            instruction.type = IT.LoadStore
            instruction.name = "swc1"
            instruction.reg1 = fpu_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x3E:
            # sqc2
            instruction.type = IT.LoadStore
            instruction.name = "sqc2"
            instruction.reg1 = vu0f_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        case 0x3F:
            # sd
            instruction.type = IT.LoadStore
            instruction.name = "sd"
            instruction.il_func = ee_func.sd
            instruction.reg1 = ee_get_name((opcode >> 16) & 0x1F)
            instruction.reg2 = ee_get_name((opcode >> 21) & 0x1F)
            instruction.operand = sign_extend_16_bit(opcode & 0xFFFF)
        
    return instruction

def convert_to_pseudo(instruction: Instruction) -> None:
    """
    Modifies an instruction for the text disasm step so that a psuedo operation can be displayed instead.
    """
    match instruction.name:
        case "addi" | "addiu":
            if instruction.reg2 == ZERO_REG:
                # li
                instruction.name = "li"
                instruction.reg2 = None
        case "add" | "addu":
            if instruction.reg2 == ZERO_REG:
                # move
                instruction.name = "move"
                instruction.reg2 = instruction.reg3
                instruction.reg3 = None
            elif instruction.reg3 == ZERO_REG:
                # move
                instruction.name = "move"
                instruction.reg3 = None
        case "beq":
            if instruction.reg1 == ZERO_REG and instruction.reg2 == ZERO_REG:
                # b
                instruction.name = "b"
                instruction.reg1 = None
                instruction.reg2 = None
            elif instruction.reg1 == ZERO_REG:
                # beqz
                instruction.name = "beqz"
                instruction.reg1 = instruction.reg2
                instruction.reg2 = None
            elif instruction.reg2 == ZERO_REG:
                # beqz
                instruction.name = "beqz"
                instruction.reg2 = None
        case "beql":
            if instruction.reg1 == ZERO_REG:
                # beqzl
                instruction.name = "beqzl"
                instruction.reg1 = instruction.reg2
                instruction.reg2 = None
            elif instruction.reg2 == ZERO_REG:
                # beqzl
                instruction.name = "beqzl"
                instruction.reg2 = None
        case "bne":
            if instruction.reg1 == ZERO_REG:
                # bnez
                instruction.name = "bnez"
                instruction.reg1 = instruction.reg2
                instruction.reg2 = None
            elif instruction.reg2 == ZERO_REG:
                # bnez
                instruction.name = "bnez"
                instruction.reg2 = None
        case "bnel":
            if instruction.reg1 == ZERO_REG:
                # bnezl
                instruction.name = "bnezl"
                instruction.reg1 = instruction.reg2
                instruction.reg2 = None
            elif instruction.reg2 == ZERO_REG:
                # bnezl
                instruction.name = "bnezl"
                instruction.reg2 = None
        case "daddi" | "daddiu":
            if instruction.reg2 == ZERO_REG:
                # dli
                instruction.name = "dli"
                instruction.reg2 = None
        case "dadd" | "daddu":
            if instruction.reg2 == ZERO_REG:
                # dmove
                instruction.name = "dmove"
                instruction.reg2 = instruction.reg3
                instruction.reg3 = None
            elif instruction.reg3 == ZERO_REG:
                # dmove
                instruction.name = "dmove"
                instruction.reg3 = None
        case "paddb" | "paddh" | "paddw" | "paddub" | "padduh" | "padduw":
            if instruction.reg2 == ZERO_REG:
                # qmove
                instruction.name = "qmove"
                instruction.reg2 = instruction.reg3
                instruction.reg3 = None
            elif instruction.reg3 == ZERO_REG:
                # qmove
                instruction.name = "qmove"
                instruction.reg3 = None
