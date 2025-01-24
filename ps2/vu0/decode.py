from ..instruction import Instruction, InstructionType
from .registers import get_f_name, get_i_name, Q_REGISTER, ACC_REGISTER, I_REGISTER, CMSAR0_REGISTER

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
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)

        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubbc
            # VF[fd].comp = VF[fs].comp - VF[ft].bcomp
            instruction.name = "vsub"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddbc
            # VF[fd].comp = ACC.comp + (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmadd"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubbc
            # VF[fd].comp = ACC.comp - (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmsub"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x10 | 0x11 | 0x12 | 0x13:
            # vmaxbc
            # VF[fd].comp = max(VF[fs].comp, VF[ft].bcomp)
            instruction.name = "vmax"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x14 | 0x15 | 0x16 | 0x17:
            # vminibc
            # VF[fd].comp = min(VF[fs].comp, VF[ft].bcomp)
            instruction.name = "vmini"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulbc
            # VF[fd].comp = VF[fs].comp + VF[ft].bcomp
            instruction.name = "vmulbc"
            bcomp = (opcode >> 0)  & 0x03
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x1C:
            # vmulq
            # VF[fd].comp = VF[fs].comp * Q
            instruction.name = "vmulq"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x1D:
            # vmaxi
            # VF[fd].comp = max(VF[fs].comp, I)
            instruction.name = "vmaxi"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x1E:
            # vmuli
            # VF[fd].comp = VF[fs].comp * I
            instruction.name = "vmuli"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x1F:
            # vminii
            # VF[fd].comp = min(VF[fs].comp, I)
            instruction.name = "vminii"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x20:
            # vaddq
            # VF[fd].comp = VF[fs].comp + Q
            instruction.name = "vaddq"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x21:
            # vmaddq
            # VF[fd].comp = ACC + (VF[fs].comp * Q)
            instruction.name = "vmaddq"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x22:
            # vaddi
            # VF[fd].comp = VF[fs].comp + I
            instruction.name = "vaddi"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x23:
            # vmaddi
            # VF[fd].comp = ACC.comp + (VF[fs].comp * I)
            instruction.name = "vmaddi"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x24:
            # vsubq
            # VF[fd].comp = VF[fs].comp - Q
            instruction.name = "vsubq"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x25:
            # vmsubq
            # VF[fd].comp = ACC.comp - (VF[fs].comp * Q)
            instruction.name = "vmsubq"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x26:
            # vsubi
            # VF[fd].comp = VF[fs.comp] - I
            instruction.name = "vsubi"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x27:
            # vmsubi
            # VF[fd] = ACC.comp - (VF[fs].comp * I)
            instruction.name = "vmsubi"
            fd   = (opcode >> 6)  & 0x1F
            fs   = (opcode >> 11) & 0x1F
            comp = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x28:
            # vadd
            # VF[fd].comp = VF[fs].comp + VF[ft].comp
            instruction.name = "vadd"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x29:
            # vmadd
            # VF[vd].comp = ACC.comp + (VF[fs] * VF[ft])
            instruction.name = "vmadd"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2A:
            # vmul
            # VF[fd].comp = VF[fs].comp * VF[ft].comp
            instruction.name = "vmul"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2B:
            # vmax
            # VF[fd].comp = max(VF[fs].comp, VF[ft].comp)
            instruction.name = "vmax"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2C:
            # vsub
            # VF[fd].comp = VF[fs].comp - VF[ft].comp
            instruction.name = "vsub"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2D:
            # vmsub
            # VF[fd].comp = ACC.comp - (VF[fs].comp * VF[vt].comp)
            instruction.name = "vmsub"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2E:
            # vopmsub
            # VF[fd].xyz = ACC.xyz - VF[fs].xyz * VF[ft].xyz
            instruction.name = "vopmsub"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F # hardcoded to xyz

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x2F:
            # vmini
            # VF[fd].comp = min(VF[fs], VF[ft])
            instruction.name = "vmini"
            fd    = (opcode >> 6)  & 0x1F
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = get_f_name(fd)
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x30:
            # viadd
            # VI[id] = VI[is] + VI[it]
            instruction.name = "viadd"
            id    = (opcode >> 6)  & 0x1F
            _is   = (opcode >> 11) & 0x1F
            it    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F # hardcoded to none

            instruction.reg1 = get_i_name(id)
            instruction.reg2 = get_i_name(_is)
            instruction.reg3 = get_i_name(it)
        case 0x31:
            # visub
            # VI[id] = VI[is] - VI[it]
            instruction.name = "visub"
            id    = (opcode >> 6)  & 0x1F
            _is   = (opcode >> 11) & 0x1F
            it    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F # hardcoded to none

            instruction.reg1 = get_i_name(id)
            instruction.reg2 = get_i_name(_is)
            instruction.reg3 = get_i_name(it)
        case 0x32:
            # viaddi
            #
            instruction.name = "viaddi"
        case 0x34:
            # viand
            # VI[id] = VI[is] & VI[it]
            instruction.name = "viand"
            id    = (opcode >> 6)  & 0x1F
            _is   = (opcode >> 11) & 0x1F
            it    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F # hardcoded to none

            instruction.reg1 = get_i_name(id)
            instruction.reg2 = get_i_name(_is)
            instruction.reg3 = get_i_name(it)
        case 0x35:
            # vior
            # VI[id] = VI[is] | VI[it]
            instruction.name = "vior"
            id    = (opcode >> 6)  & 0x1F
            _is   = (opcode >> 11) & 0x1F
            it    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F # hardcoded to none

            instruction.reg1 = get_i_name(id)
            instruction.reg2 = get_i_name(_is)
            instruction.reg3 = get_i_name(it)
        case 0x38:
            # vcallms
            # call addr
            instruction.name = "vcallms"
            imm = (opcode >> 6) & 0x7FFF
            instruction.operand = imm
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
            bcomp = (opcode >> 0)  & 0x03
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x04 | 0x05 | 0x06 | 0x07:
            # vsubabc
            # ACC.comp = VF[fs].comp - VF[ft].bcomp
            instruction.name = "vsuba"
            bcomp = (opcode >> 0)  & 0x03
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x08 | 0x09 | 0x0A | 0x0B:
            # vmaddabc
            # ACC.comp = ACC.comp + (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmadda"
            bcomp = (opcode >> 0)  & 0x03
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x0C | 0x0D | 0x0E | 0x0F:
            # vmsubabc
            # ACC.comp = ACC.comp - (VF[fs].comp * VF[ft].bcomp)
            instruction.name = "vmsuba"
            bcomp = (opcode >> 0)  & 0x03
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x10:
            # vitof0
            #
            instruction.name = "vitof0"
        case 0x11:
            # vitof4
            #
            instruction.name = "vitof4"
        case 0x12:
            # vitof12
            #
            instruction.name = "vitof12"
        case 0x13:
            # vitof15
            #
            instruction.name = "vitof15"
        case 0x14:
            # vftoi0
            #
            instruction.name = "vftoi0"
        case 0x15:
            # vftoi4
            #
            instruction.name = "vftoi4"
        case 0x16:
            # vftoi12
            instruction.name = "vftoi12"
        case 0x17:
            # vftoi15
            instruction.name = "vftoi15"
        case 0x18 | 0x19 | 0x1A | 0x1B:
            # vmulabc
            # ACC.comp = VF[fs].comp * VF[ft].bcomp
            instruction.name = "vmula"
            bcomp = (opcode >> 0)  & 0x03
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x1C:
            # vmulaq
            #
            instruction.name = "vmulaq"
        case 0x1D:
            # vabs
            #
            instruction.name = "vabs"
        case 0x1E:
            # vmulai
            #
            instruction.name = "vmulai"
        case 0x1F:
            # vclip
            #
            instruction.name = "vclip"
        case 0x20:
            # vaddaq
            # ACC.comp = VF[fs].comp + Q
            instruction.name = "vaddaq"
            fs    = (opcode >> 11) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = Q_REGISTER
        case 0x21:
            # vmaddaq
            #
            instruction.name = "vmaddaq"
        case 0x22:
            # vaddai
            # ACC.comp = VF[fs].comp + I
            instruction.name = "vaddai"
            fs    = (opcode >> 11) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = I_REGISTER
        case 0x23:
            # vmaddai
            #
            instruction.name = "vmaddai"
        case 0x25:
            # vmsubaq
            #
            instruction.name = "vmsubaq"
        case 0x26:
            # vsubai
            #
            instruction.name = "vsubai"
        case 0x27:
            # vmsubai
            #
            instruction.name = "vmsubai"
        case 0x28:
            # vadda ACC.comp = VF[fs].comp + VF[ft].comp
            instruction.name = "vadda"
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            comp  = (opcode >> 21) & 0x1F

            instruction.reg1 = ACC_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x29:
            # vmadda
            #
            instruction.name = "vmadda"
        case 0x2A:
            # vmula
            #
            instruction.name = "vmula"
        case 0x2C:
            # vsuba
            #
            instruction.name = "vsuba"
        case 0x2D:
            # vmsuba
            #
            instruction.name = "vmsuba"
        case 0x2E:
            # vopmula
            #
            instruction.name = "vopmula"
        case 0x2F:
            # vnop
            #
            instruction.name = "vnop"
        case 0x30:
            # vmove
            #
            instruction.name = "vmove"
        case 0x31:
            # vmr32
            #
            instruction.name = "vmr32"
        case 0x34:
            # vlqi
            #
            instruction.name = "vlqi"
        case 0x35:
            # vsqi
            #
            instruction.name = "vsqi"
        case 0x36:
            # vlqd
            #
            instruction.name = "vlqd"
        case 0x37:
            # vsqd
            #
            instruction.name = "vsqd"
        case 0x38:
            # vdiv
            # Q = VF[fs].fsf / VF[ft].ftf
            instruction.name = "vdiv"
            fs    = (opcode >> 11) & 0x1F
            ft    = (opcode >> 16) & 0x1F
            fsf   = (opcode >> 21) & 0x03
            ftf   = (opcode >> 23) & 0x03

            instruction.reg1 = Q_REGISTER
            instruction.reg2 = get_f_name(fs)
            instruction.reg3 = get_f_name(ft)
        case 0x39:
            # vsrqt
            # Q = sqrt(VF[ft].ftf)
            instruction.name = "vsqrt"
            ft    = (opcode >> 16) & 0x1F
            ftf   = (opcode >> 23) & 0x03

            instruction.reg1 = Q_REGISTER
            instruction.reg2 = get_f_name(ft)
        case 0x3A:
            # vrsqrt
            #
            instruction.name = "vrsqrt"
        case 0x3B:
            # vwaitq
            #
            instruction.name = "vwaitq"
        case 0x3C:
            # vmtir
            #
            instruction.name = "vmtir"
        case 0x3D:
            # vmfir
            #
            instruction.name = "vmfir"
        case 0x3E:
            # vilwr
            #
            instruction.name = "vilwr"
        case 0x3F:
            # viswr
            #
            instruction.name = "viswr"
        case 0x40:
            # vrnext
            #
            instruction.name = "vrnext"
        case 0x41:
            # vrget
            #
            instruction.name = "vrget"
        case 0x42:
            instruction.name = "vrinit"
        case 0x43:
            # vrxor
            #
            instruction.name = "vrxor"

    return instruction