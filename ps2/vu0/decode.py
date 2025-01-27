from ..instruction import Instruction, InstructionType
from .registers import (
    get_f_name,
    get_i_name,
    Q_REGISTER,
    ACC_REGISTER,
    I_REGISTER,
    R_REGISTER,
    CMSAR0_REGISTER
)

component_bits: list[str] = [
    'x',
    'y',
    'z',
    'w',
]

# precomputed lookup table
# bit 1: w
# bit 2: z
# bit 3: y
# bit 4: z
field_bits_to_string = [
    'invalid',
    'w',
    'z',
    'zw',
    'y',
    'yw',
    'yz',
    'yxw',
    'x',
    'xw',
    'xz',
    'xzw',
    'xy',
    'xyw',
    'xyz',
    'xyzw'
]

def decode_component_bits(bits: int):
    return field_bits_to_string[bits]

def decode_single_component_name(id: int):
    return component_bits[id & 0x03]

def decode_destination_register_index(opcode: int) -> int:
    return (opcode >> 6) & 0x1F

def decode_source_register_index(opcode: int) -> int:
    return (opcode >> 11) & 0x1F

def decode_temp_register_index(opcode: int) -> int:
    return (opcode >> 16) & 0x1F

def decode_destination_component_bits(opcode: int) -> int:
    return (opcode >> 21) & 0x0F

def decode_broadcast_component_id(opcode: int) -> int:
    return (opcode >> 0)  & 0x03

def decode_source_component_id(opcode: int) -> int:
    return (opcode >> 21) & 0x03

def decode_temp_component_id(opcode: int) -> int:
    return (opcode >> 23) & 0x03

def decode_immediate_value(opcode: int) -> int:
    return (opcode >> 5) & 0x1F

def decode_destination_register_name_float(opcode: int) -> int:
    return get_f_name(decode_destination_register_index(opcode))

def decode_destination_register_name_int(opcode: int) -> int:
    return get_i_name(decode_destination_register_index(opcode))

def decode_source_register_name_float(opcode: int) -> int:
    return get_f_name(decode_source_register_index(opcode))

def decode_source_register_name_int(opcode: int) -> int:
    return get_i_name(decode_source_register_index(opcode))

def decode_temp_register_name_float(opcode: int) -> int:
    return get_f_name(decode_temp_register_index(opcode))

def decode_temp_register_name_int(opcode: int) -> int:
    return get_i_name(decode_temp_register_index(opcode))

def decode_cop2_special(opcode: int, addr: int) -> Instruction:
    instruction = Instruction()
    IT = InstructionType

    op = opcode & 0x3F

    instruction.type = IT.GenericInt

    match op:
        case 0x00 | 0x01 | 0x02 | 0x03:
            # vaddbc
            # VF[fd].comp = VF[fs].comp + VF[ft].bcomp
            instruction.name = "vadd"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)

        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubbc
            # VF[fd].comp = VF[fs].comp - VF[ft].bcomp
            instruction.name = "vsub"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddbc
            # VF[fd].comp = ACC.comp + (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmadd"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubbc
            # VF[fd].comp = ACC.comp - (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmsub"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x10 | 0x11 | 0x12 | 0x13:
            # vmaxbc
            # VF[fd].comp = max(VF[fs].comp, VF[ft].bcomp)
            instruction.name = "vmax"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x14 | 0x15 | 0x16 | 0x17:
            # vminibc
            # VF[fd].comp = min(VF[fs].comp, VF[ft].bcomp)
            instruction.name = "vmini"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulbc
            # VF[fd].comp = VF[fs].comp + VF[ft].bcomp
            instruction.name = "vmul"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x1C:
            # vmulq
            # VF[fd].comp = VF[fs].comp * Q
            instruction.name = "vmulq"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x1D:
            # vmaxi
            # VF[fd].comp = max(VF[fs].comp, I)
            instruction.name = "vmaxi"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x1E:
            # vmuli
            # VF[fd].comp = VF[fs].comp * I
            instruction.name = "vmuli"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x1F:
            # vminii
            # VF[fd].comp = min(VF[fs].comp, I)
            instruction.name = "vminii"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x20:
            # vaddq
            # VF[fd].comp = VF[fs].comp + Q
            instruction.name = "vaddq"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x21:
            # vmaddq
            # VF[fd].comp = ACC + (VF[fs].comp * Q)
            instruction.name = "vmaddq"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x22:
            # vaddi
            # VF[fd].comp = VF[fs].comp + I
            instruction.name = "vaddi"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x23:
            # vmaddi
            # VF[fd].comp = ACC.comp + (VF[fs].comp * I)
            instruction.name = "vmaddi"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x24:
            # vsubq
            # VF[fd].comp = VF[fs].comp - Q
            instruction.name = "vsubq"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x25:
            # vmsubq
            # VF[fd].comp = ACC.comp - (VF[fs].comp * Q)
            instruction.name = "vmsubq"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x26:
            # vsubi
            # VF[fd].comp = VF[fs.comp] - I
            instruction.name = "vsubi"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x27:
            # vmsubi
            # VF[fd] = ACC.comp - (VF[fs].comp * I)
            instruction.name = "vmsubi"
            comp = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x28:
            # vadd
            # VF[fd].comp = VF[fs].comp + VF[ft].comp
            instruction.name = "vadd"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x29:
            # vmadd
            # VF[vd].comp = ACC.comp + (VF[fs] * VF[ft])
            instruction.name = "vmadd"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2A:
            # vmul
            # VF[fd].comp = VF[fs].comp * VF[ft].comp
            instruction.name = "vmul"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2B:
            # vmax
            # VF[fd].comp = max(VF[fs].comp, VF[ft].comp)
            instruction.name = "vmax"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2C:
            # vsub
            # VF[fd].comp = VF[fs].comp - VF[ft].comp
            instruction.name = "vsub"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2D:
            # vmsub
            # VF[fd].comp = ACC.comp - (VF[fs].comp * VF[vt].comp)
            instruction.name = "vmsub"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2E:
            # vopmsub
            # VF[fd].xyz = ACC.xyz - VF[fs].xyz * VF[ft].xyz
            instruction.name = "vopmsub"
            comp  = decode_destination_component_bits(opcode) # hardcoded to xyz

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2F:
            # vmini
            # VF[fd].comp = min(VF[fs].comp, VF[ft].comp)
            instruction.name = "vmini"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_destination_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x30:
            # viadd
            # VI[id] = VI[is] + VI[it]
            instruction.name = "viadd"

            instruction.reg1 = decode_destination_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x31:
            # visub
            # VI[id] = VI[is] - VI[it]
            instruction.name = "visub"

            instruction.reg1 = decode_destination_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
            instruction.reg3 = decode_temp_register_name_int(opcode)
        case 0x32:
            # viaddi
            # VI[it] = VI[is] + immm
            instruction.name = "viaddi"

            instruction.operand = decode_immediate_value(opcode)

            instruction.reg1 = decode_temp_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x34:
            # viand
            # VI[id] = VI[is] & VI[it]
            instruction.name = "viand"

            instruction.reg1 = decode_destination_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
            instruction.reg3 = decode_temp_register_name_int(opcode)
        case 0x35:
            # vior
            # VI[id] = VI[is] | VI[it]
            instruction.name = "vior"

            instruction.reg1 = decode_destination_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
            instruction.reg3 = decode_temp_register_name_int(opcode)
        case 0x38:
            # vcallms
            # call addr
            instruction.name = "vcallms"
            instruction.operand = (opcode >> 6) & 0x7FFF
        case 0x39:
            # vcallmsr
            # call CMSAR0
            instruction.name = "vcallmsr"
            instruction.reg1 = CMSAR0_REGISTER
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
            # ACC.comp = VF[fs].comp + VF[ft].bcomp
            instruction.name = "vadda"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubabc
            # ACC.comp = VF[fs].comp - VF[ft].bcomp
            instruction.name = "vsuba"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddabc
            # ACC.comp = ACC.comp + (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmadda"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubabc
            # ACC.comp = ACC.comp - (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmsuba"
            bcomp = decode_broadcast_component_id(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x10:
            # vitof0
            # VF[ft] = ToF32FromFixedPoint0(VF[fs])
            instruction.name = "vitof0"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x11:
            # vitof4
            # VF[ft] = ToF32FromFixedPoint4(VF[fs])
            instruction.name = "vitof4"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x12:
            # vitof12
            # VF[ft] = ToF32FromFixedPoint12(VF[fs])
            instruction.name = "vitof12"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x13:
            # vitof15
            # VF[ft] = ToF32FromFixedPoint15(VF[fs])
            instruction.name = "vitof15"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x14:
            # vftoi0
            # VF[ft] = ToFixedPoint0FromF32(VF[fs])
            instruction.name = "vftoi0"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x15:
            # vftoi4
            # VF[ft] = ToFixedPoint4FromF32(VF[fs])
            instruction.name = "vftoi4"
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x16:
            # vftoi12
            # VF[ft] = ToFixedPoint12FromF32(VF[fs])
            instruction.name = "vftoi12"
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x17:
            # vftoi15
            # VF[ft] = ToFixedPoint15FromF32(VF[fs])
            instruction.name = "vftoi15"
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulabc
            # ACC.comp = VF[fs].comp * VF[ft].bcomp
            instruction.name = "vmula"
            bcomp = decode_broadcast_component_id(opcode)
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x1C:
            # vmulaq
            # ACC.comp = VF[fs].comp * Q
            instruction.name = "vmulaq"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x1D:
            # vabs
            # VF[ft].comp = abs(VF[fs].comp)
            instruction.name = "vabs"
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x1E:
            # vmulai
            # ACC.comp = VF[fs].comp * I
            instruction.name = "vmulai"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x1F:
            # vclip
            # CF = clip(VF[fs].xyz, VF[ft].w)
            instruction.name = "vclip"
            bcomp = decode_broadcast_component_id(opcode) # harcoded to w
            ft    = decode_temp_register_index(opcode)
            comp  = decode_destination_component_bits(opcode) # hardcoded to xyz

            instruction.broadcast_component    = decode_single_component_name(bcomp)
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_source_register_name_float(opcode)
            instruction.reg2 = decode_temp_register_name_float(opcode)
        case 0x20:
            # vaddaq
            # ACC.comp = VF[fs].comp + Q
            instruction.name = "vaddaq"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x21:
            # vmaddaq
            # ACC.comp = ACC.comp + (VF[fs].comp * Q)
            instruction.name = "vmaddaq"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x22:
            # vaddai
            # ACC.comp = VF[fs].comp + I
            instruction.name = "vaddai"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x23:
            # vmaddai
            # ACC.comp = ACC.comp + (VF[fs].comp * I)
            instruction.name = "vmaddai"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x25:
            # vmsubaq
            # ACC.comp = ACC.comp - (VF[fs].comp * Q)
            instruction.name = "vmsubaq"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = Q_REGISTER
        case 0x26:
            # vsubai
            # ACC.comp = VF[fs].comp - I
            instruction.name = "vsubai"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x27:
            # vmsubai
            # ACC.comp = ACC.comp - (VF[fs].comp * I)
            instruction.name = "vmsubai"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = I_REGISTER
        case 0x28:
            # vadda ACC.comp = VF[fs].comp + VF[ft].comp
            instruction.name = "vadda"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x29:
            # vmadda
            # ACC.comp = ACC.comp + (VF[fs].comp * VF[ft].comp)
            instruction.name = "vmadda"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2A:
            # vmula
            # ACC.comp = VF[fs].comp * VF[ft].comp
            instruction.name = "vmula"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2C:
            # vsuba
            # ACC.comp = VF[fs].comp - VF[ft].comp
            instruction.name = "vsuba"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2D:
            # vmsuba
            # ACC.comp = ACC.comp - (VF[fs].comp * VF[ft].comp)
            instruction.name = "vmsuba"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2E:
            # vopmula
            # ACC.xyz = VF[fs].xyz * VF[ft].xyz
            instruction.name = "vopmula"
            comp  = decode_destination_component_bits(opcode)

            # hardcoded to xyz
            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x2F:
            # vnop
            instruction.name = "vnop"
        case 0x30:
            # vmove
            # VF[ft].comp = VF[fs].comp
            instruction.name = "vmove"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x31:
            # vmr32
            # VF[ft].comp = rotate_right(VF[ft])
            instruction.name = "vmr32"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x34:
            # vlqi
            # VF[ft].comp = read(VI[is]).comp
            # VF[ft]++
            instruction.name = "vlqi"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x35:
            # vsqi
            # write(VI[it], VF[fs].comp)
            # VI[it]++
            instruction.name = "vsqi"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_source_register_name_float(opcode)
            instruction.reg2 = decode_temp_register_name_int(opcode)
        case 0x36:
            # vlqd
            # VF[ft] = read(VI[is]--)
            instruction.name = "vlqd"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x37:
            # vsqd
            # write(VI[it]--, VF[fs].comp)
            instruction.name = "vsqd"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_source_register_name_float(opcode)
            instruction.reg2 = decode_temp_register_name_int(opcode)
        case 0x38:
            # vdiv
            # Q = VF[fs].fsf / VF[ft].ftf
            instruction.name = "vdiv"
            fsf   = decode_source_component_id(opcode)
            ftf   = decode_temp_component_id(opcode)

            instruction.source0_component = decode_single_component_name(fsf)
            instruction.source1_component = decode_single_component_name(ftf)

            instruction.reg1 = Q_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x39:
            # vsrqt
            # Q = sqrt(VF[ft].ftf)
            instruction.name = "vsqrt"
            ftf   = decode_temp_component_id(opcode)

            instruction.source1_component = decode_single_component_name(ftf)

            instruction.reg1 = Q_REGISTER
            instruction.reg2 = decode_temp_register_name_float(opcode)
        case 0x3A:
            # vrsqrt
            # Q = VF[fs].fsf / sqrt(VF[ft].ftf)
            instruction.name = "vrsqrt"
            fsf   = decode_source_component_id(opcode)
            ftf   = decode_temp_component_id(opcode)

            instruction.source0_component = decode_single_component_name(fsf)
            instruction.source1_component = decode_single_component_name(ftf)

            instruction.reg1 = Q_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
            instruction.reg3 = decode_temp_register_name_float(opcode)
        case 0x3B:
            # vwaitq
            instruction.name = "vwaitq"
        case 0x3C:
            # vmtir
            # VI[it] = trunc16(VF[fs].fsf)
            instruction.name = "vmtir"
            fsf   = decode_source_component_id(opcode)

            instruction.source0_component = decode_single_component_name(fsf)

            instruction.reg1 = decode_temp_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x3D:
            # vmfir
            # VF[ft].comp = VI[is]
            instruction.name = "vmfir"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x3E:
            # vilwr
            # VI[it].comp = read(VI[is]).comp
            instruction.name = "vilwr"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x3F:
            # viswr
            # write(VI[is], read(VI[it]).comp)
            instruction.name = "viswr"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_int(opcode)
            instruction.reg2 = decode_source_register_name_int(opcode)
        case 0x40:
            # vrnext
            # VF[ft].comp = rand(R)
            instruction.name = "vrnext"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = R_REGISTER
        case 0x41:
            # vrget
            # VF[ft].comp = R
            instruction.name = "vrget"
            comp  = decode_destination_component_bits(opcode)

            instruction.destination_components = decode_component_bits(comp)

            instruction.reg1 = decode_temp_register_name_float(opcode)
            instruction.reg2 = R_REGISTER
        case 0x42:
            # vrinit
            # R = VF[fs].fsf
            instruction.name = "vrinit"
            fsf   = decode_source_component_id(opcode)

            instruction.source0_component = decode_single_component_name(fsf)

            instruction.reg1 = R_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)
        case 0x43:
            # vrxor
            # R = VF[fs].fsf ^ R
            instruction.name = "vrxor"
            fsf   = decode_source_component_id(opcode)

            instruction.source0_component = decode_single_component_name(fsf)

            instruction.reg1 = R_REGISTER
            instruction.reg2 = decode_source_register_name_float(opcode)

    return instruction