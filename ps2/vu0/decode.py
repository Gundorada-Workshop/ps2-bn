from ..instruction import Instruction, InstructionType

def decode_cop2_special(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType

    op = opcode & 0x3F

    instruction.type = IT.GenericInt

    match op:
        case 0x00 | 0x01 | 0x02 | 0x03:
            # vaddbc
            instruction.name = "vadd"
        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubbc
            instruction.name = "vsub"
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddbc
            instruction.name = "vmadd"
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubbc
            instruction.name = "vmsub"
        case 0x10 | 0x11 | 0x12 | 0x13:
            # vmaxbc
            instruction.name = "vmax"
        case 0x14 | 0x15 | 0x16 | 0x17:
            # vminibc
            instruction.name = "vmini"
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulbc
            instruction.name = "vmulbc"
        case 0x1C:
            instruction.name = "vmulq"
        case 0x1D:
            instruction.name = "vmaxi"
        case 0x1E:
            instruction.name = "vmuli"
        case 0x1F:
            instruction.name = "vminii"
        case 0x20:
            instruction.name = "vaddq"
        case 0x21:
            instruction.name = "vmaddq"
        case 0x22:
            instruction.name = "vaddi"
        case 0x23:
            instruction.name = "vmaddi"
        case 0x24:
            instruction.name = "vsubq"
        case 0x25:
            instruction.name = "vmsubq"
        case 0x26:
            instruction.name = "vsubi"
        case 0x27:
            instruction.name = "vmsubi"
        case 0x28:
            instruction.name = "vadd"
        case 0x29:
            instruction.name = "vmadd"
        case 0x2A:
            instruction.name = "vmul"
        case 0x2B:
            instruction.name = "vmax"
        case 0x2C:
            instruction.name = "vsub"
        case 0x2D:
            instruction.name = "vmsub"
        case 0x2E:
            instruction.name = "vopmsub"
        case 0x2F:
            instruction.name = "vmini"
        case 0x30:
            instruction.name = "viadd"
        case 0x31:
            instruction.name = "visub"
        case 0x32:
            instruction.name = "viaddi"
        case 0x34:
            instruction.name = "viand"
        case 0x35:
            instruction.name = "vior"
        case 0x38:
            instruction.name = "vcallms"
        case 0x39:
            instruction.name = "vcallmsr"
        case 0x3C | 0x3D | 0x3E | 0x3F:
            return decode_cop2_special2(opcode, addr)

    return instruction

def decode_cop2_special2(opcode: int, addr: int) -> Instruction:
    op = opcode & 3 | (opcode >> 4) & 0x7C

    instruction = Instruction()
    IT = InstructionType

    instruction.type = IT.GenericInt

    match op:
        case 0x00 | 0x01 | 0x02 | 0x03:
            # vaddabc
            instruction.name = "vadda"
        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubabc
            instruction.name = "vsuba"
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddabc
            instruction.name = "vmadda"
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubabc
            instruction.name = "vmsuba"
        case 0x10:
            instruction.name = "vitof0"
        case 0x11:
            instruction.name = "vitof4"
        case 0x12:
            instruction.name = "vitof12"
        case 0x13:
            instruction.name = "vitof15"
        case 0x14:
            instruction.name = "vftoi0"
        case 0x15:
            instruction.name = "vftoi4"
        case 0x16:
            instruction.name = "vftoi12"
        case 0x17:
            instruction.name = "vftoi15"
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulabc
            instruction.name = "vmula"
        case 0x1C:
            instruction.name = "vmulaq"
        case 0x1D:
            instruction.name = "vabs"
        case 0x1E:
            instruction.name = "vmulai"
        case 0x1F:
            instruction.name = "vclip"
        case 0x20:
            instruction.name = "vaddaq"
        case 0x21:
            instruction.name = "vmaddaq"
        case 0x22:
            instruction.name = "vaddai"
        case 0x23:
            instruction.name = "vmaddai"
        case 0x25:
            instruction.name = "vmsubaq"
        case 0x26:
            instruction.name = "vsubai"
        case 0x27:
            instruction.name = "vmsubai"
        case 0x28:
            instruction.name = "vadda"
        case 0x29:
            instruction.name = "vmadda"
        case 0x2A:
            instruction.name = "vmula"
        case 0x2C:
            instruction.name = "vsuba"
        case 0x2D:
            instruction.name = "vmsuba"
        case 0x2E:
            instruction.name = "vopmula"
        case 0x2F:
            instruction.name = "vnop"
        case 0x30:
            instruction.name = "vmove"
        case 0x31:
            instruction.name = "vmr32"
        case 0x34:
            instruction.name = "vlqi"
        case 0x35:
            instruction.name = "vsqi"
        case 0x36:
            instruction.name = "vlqd"
        case 0x37:
            instruction.name = "vsqd"
        case 0x38:
            instruction.name = "vdiv"
        case 0x39:
            instruction.name = "vsqrt"
        case 0x3A:
            instruction.name = "vrsqrt"
        case 0x3B:
            instruction.name = "vwaitq"
        case 0x3C:
            instruction.name = "vmtir"
        case 0x3D:
            instruction.name = "vmfir"
        case 0x3E:
            instruction.name = "vilwr"
        case 0x3F:
            instruction.name = "viswr"
        case 0x40:
            instruction.name = "vrnext"
        case 0x41:
            instruction.name = "vrget"
        case 0x42:
            instruction.name = "vrinit"
        case 0x43:
            instruction.name = "vrxor"

    return instruction