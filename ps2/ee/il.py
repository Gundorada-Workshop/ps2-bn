from .registers import registers as gpr
from .registers import ZERO_REG, LO_REG, HI_REG, LO1_REG, HI1_REG, SP_REG
from ..fpu.registers import CONDITION_FLAG as FPU_CONDITION_FLAG
from ..instruction import Instruction
from ..intrinsics import PS2Intrinsic
from binaryninja.architecture import Architecture
from binaryninja.lowlevelil import LowLevelILFunction, LowLevelILLabel, LowLevelILInstruction, ExpressionIndex, LowLevelILConst

def add(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _add(instruction, addr, il, 4)

def addi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addi(instruction, addr, il, 4)

def _addi(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    if instruction.reg2 == ZERO_REG:
        # li
        value = il.const(size, instruction.operand)
    else:
        # addiu
        value = il.add(size, il.reg(size, instruction.reg2), il.const(size, instruction.operand))

    if size < 8:
        if instruction.reg1 != SP_REG: # HACK to prevent function prologue/epilogue junk in IL
            value = il.sign_extend(8, value)
            size = 8
        else:
            size = 4

    il.append(il.set_reg(size, instruction.reg1, value))

def addiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addi(instruction, addr, il, 4)

def _add(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    r1, r2, r3 = instruction.reg1, instruction.reg2, instruction.reg3
    if r2 == ZERO_REG and r3 == ZERO_REG:
        # move
        value = il.const(size, 0)
    elif r2 == ZERO_REG:
        # move
        value = il.reg(size, r3)
    elif r3 == ZERO_REG:
        # move
        value = il.reg(size, r2)
    else:
        # addu
        value = il.add(size, il.reg(size, r2), il.reg(size, r3))
    
    if size < 8:
        value = il.sign_extend(8, value)

    il.append(il.set_reg(8, r1, value))

def addu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _add(instruction, addr, il, 4)

def ee_and(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    sreg1 = il.reg(8, instruction.reg2)
    sreg2 = il.reg(8, instruction.reg3)

    expr = il.and_expr(8, sreg1, sreg2)
    if instruction.reg2 == ZERO_REG or instruction.reg3 == ZERO_REG:
        expr = il.const(8, 0)
        
    il.append(il.set_reg(8, instruction.reg1, expr))

def andi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg = il.reg(8, instruction.reg2)
    imm = il.const(8, instruction.operand)

    expr = il.and_expr(8, sreg, imm)
    if instruction.reg2 == ZERO_REG:
        expr = il.const(8, 0)
        
    il.append(il.set_reg(8, instruction.reg1, expr))

def _unconditional_branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(
        il.jump(
            il.const(4, instruction.branch_dest)
        )
    )

def _unconditional_failed_branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.nop())

def _branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction', true_jump_fn = None) -> None:
    if true_jump_fn is None:
        true_jump_fn = il.jump

    cond = get_branch_cond_expr(instruction, addr, il)

    # Adapted from NES example, gotta figure out what indirect is used for later on
    t = None
    f = None
    t_dest = il.const(4, instruction.branch_dest)
    f_dest = il.const(4, addr + 8)
    t_indirect = False
    f_indirect = False
    instr1 = LowLevelILInstruction.create(il, t_dest)
    instr2 = LowLevelILInstruction.create(il, f_dest)
    if isinstance(instr1, LowLevelILConst):
        t = il.get_label_for_address(Architecture[instruction.arch.name], instr1.constant)
    if t is None:
        t_indirect = True
        t = LowLevelILLabel()
    if isinstance(instr2, LowLevelILConst):
        f = il.get_label_for_address(Architecture[instruction.arch.name], instr2.constant)
    if f is None:
        f_indirect = True
        f = LowLevelILLabel()

    done = LowLevelILLabel()
    il.append(il.if_expr(cond, t, f))
    if t_indirect:
        il.mark_label(t)
        il.append(true_jump_fn(t_dest))
        il.append(il.goto(done))
    if f_indirect:
        il.mark_label(f)
        il.append(il.jump(f_dest))
    il.mark_label(done)

def break_ee(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.breakpoint())

def beq(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    r1 = instruction.reg1
    r2 = instruction.reg2

    if r1 == ZERO_REG and r2 == ZERO_REG:
        return _unconditional_branch(instruction, addr, il)

    _branch(instruction, addr, il)

beql = beq
bgez = _branch
bgezl = bgez
def bgezal(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    _branch(instruction, addr, il, true_jump_fn=il.call)
bgezall = bgezal
bgtz = _branch
bgtzl = bgtz
blez = _branch
blezl = blez
bltz = _branch
bltzl = bltz
def bltzal(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    _branch(instruction, addr, il, true_jump_fn=il.call)
bltzall = bltzal


def bne(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    r1 = instruction.reg1
    r2 = instruction.reg2

    if r1 == ZERO_REG and r2 == ZERO_REG:
        return _unconditional_failed_branch(instruction, addr, il)
    
    _branch(instruction, addr, il, get_branch_cond_expr(instruction, addr, il))

def bnel(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    bne(instruction, addr, il)

def dadd(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _add(instruction, addr, il, 8)

def daddi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addi(instruction, addr, il, 8)

def daddiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addi(instruction, addr, il, 8)

def daddu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _add(instruction, addr, il, 8)

def di(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.DI, []))

def div(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg1)
    sreg2 = il.reg(4, instruction.reg2)

    div_expr = il.sign_extend(8, il.div_unsigned(4, sreg1, sreg2))
    mod_expr = il.sign_extend(8, il.mod_unsigned(4, sreg1, sreg2))
        
    il.append(il.set_reg(8, LO_REG, div_expr))
    il.append(il.set_reg(8, HI_REG, mod_expr))

def div1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg1)
    sreg2 = il.reg(4, instruction.reg2)

    div_expr = il.sign_extend(8, il.div_unsigned(4, sreg1, sreg2))
    mod_expr = il.sign_extend(8, il.mod_unsigned(4, sreg1, sreg2))
    
    il.append(il.set_reg(8, LO1_REG, div_expr))
    il.append(il.set_reg(8, HI1_REG, mod_expr))

def divu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg1)
    sreg2 = il.reg(4, instruction.reg2)

    div_expr = il.sign_extend(8, il.div_unsigned(4, sreg1, sreg2))
    mod_expr = il.sign_extend(8, il.mod_unsigned(4, sreg1, sreg2))
        
    il.append(il.set_reg(8, LO_REG, div_expr))
    il.append(il.set_reg(8, HI_REG, mod_expr))

def divu1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg1)
    sreg2 = il.reg(4, instruction.reg2)

    div_expr = il.sign_extend(8, il.div_unsigned(4, sreg1, sreg2))
    mod_expr = il.sign_extend(8, il.mod_unsigned(4, sreg1, sreg2))
        
    il.append(il.set_reg(8, LO1_REG, div_expr))
    il.append(il.set_reg(8, HI1_REG, mod_expr))

def dsll(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sll(instruction, addr, il, 8, il.const(1, instruction.operand))

def dsll32(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sll(instruction, addr, il, 8, il.const(1, instruction.operand + 32))

def dsllv(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sllv(instruction, addr, il, 8)

def dsra(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sra(instruction, addr, il, 8, il.const(1, instruction.operand))

def dsra32(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sra(instruction, addr, il, 8, il.const(1, instruction.operand + 32))

def dsrav(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srav(instruction, addr, il, 8)

def dsrl(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srl(instruction, addr, il, 8, il.const(1, instruction.operand))

def dsrl32(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srl(instruction, addr, il, 8, il.const(1, instruction.operand + 32))

def dsrlv(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srlv(instruction, addr, il, 8)

def dsub(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    _sub(instruction, addr, il, 8)

dsubu = dsub

def ei(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.EI, []))

def j(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _unconditional_branch(instruction, addr, il)

def jal(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(
        il.call(
            il.const(
                4, instruction.branch_dest
            )
        )
    )

def jalr(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.call(il.reg(4, instruction.reg1)))

def jr(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    if instruction.reg1 == instruction.arch.link_register:
        # Assume this is a function return
        expr = il.ret
    else:
        expr = il.jump
    
    il.append(expr(il.reg(4, instruction.reg1)))

def _load(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int, sign_extend: bool) -> None:
    value = il.load(size, il.add(4, il.reg(4, instruction.reg2), il.const(4, instruction.operand)))
    if size < 8:
        if sign_extend:
            value = il.sign_extend(8, value)
        else:
            value = il.zero_extend(8, value)

    # lb, lh, lw, ld write first 64-bits of register; lq writes all 128-bits
    reg_size = max(8, size)
    il.append(il.set_reg(reg_size, instruction.reg1, value))

lb   = lambda instruction, addr, il: _load(instruction, addr, il, 1, sign_extend=True)
lbu  = lambda instruction, addr, il: _load(instruction, addr, il, 1, sign_extend=False)
ld   = lambda instruction, addr, il: _load(instruction, addr, il, 8, sign_extend=False)
lh   = lambda instruction, addr, il: _load(instruction, addr, il, 2, sign_extend=True)
lhu  = lambda instruction, addr, il: _load(instruction, addr, il, 2, sign_extend=False)
lq   = lambda instruction, addr, il: _load(instruction, addr, il, 16, sign_extend=False)
lqc2 = lambda instruction, addr, il: _load(instruction, addr, il, 16, sign_extend=False)
lw   = lambda instruction, addr, il: _load(instruction, addr, il, 4, sign_extend=True)
lwu  = lambda instruction, addr, il: _load(instruction, addr, il, 4, sign_extend=False)
lwc1 = lambda instruction, addr, il: _load(instruction, addr, il, 4, sign_extend=True)

def lui(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand << 16)
    val = il.sign_extend(8, val)
    il.append(il.set_reg(8, instruction.reg1, val))

def _mfc(instruction: Instruction, addr: int, il: 'LowLevelILFunction', cop_id: int) -> None:
    size = 16 if cop_id == 2 else 4

    val = il.reg(size, instruction.reg2)
    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(max(size, 8), instruction.reg1, val))

def mfc0(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mfc(instruction, addr, il, 0)

def mfc1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mfc(instruction, addr, il, 1)

def mfhi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, instruction.reg1, il.reg(8, HI_REG)))

def mfhi1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, instruction.reg1, il.reg(8, HI1_REG)))

def mflo(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, instruction.reg1, il.reg(8, LO_REG)))

def mflo1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, instruction.reg1, il.reg(8, LO1_REG)))

def _cond_move(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    cond = get_move_cond_expr(instruction, addr, il)
    t = LowLevelILLabel()
    f = LowLevelILLabel()

    il.append(il.if_expr(cond, t, f))
    il.mark_label(t)
    il.append(il.set_reg(8, instruction.reg1, il.reg(8, instruction.reg2)))
    il.mark_label(f)

movn = _cond_move
movz = _cond_move

def _mtc(instruction: Instruction, addr: int, il: 'LowLevelILFunction', cop_id: int) -> None:
    size = 16 if cop_id == 2 else 4
    il.append(il.set_reg(size, instruction.reg2, il.reg(size, instruction.reg1)))

def mtc0(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mtc(instruction, addr, il, 0)

def mtc1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mtc(instruction, addr, il, 1)

def mthi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, HI_REG, il.reg(8, instruction.reg1)))

def mthi1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, HI1_REG, il.reg(8, instruction.reg1)))

def mtlo(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, LO_REG, il.reg(8, instruction.reg1)))

def mtlo1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.set_reg(8, LO1_REG, il.reg(8, instruction.reg1)))

def mult(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg2)
    sreg2 = il.reg(4, instruction.reg3)

    # prod[0..63] = GPR1[0..31] * GPR2[0..31]
    # rd[0..63] = sign_extend(8, prod[0..31])
    # lo[0..63] = sign_extend(8, prod[0..31])
    # hi[0..63] = sign_extend(8, prod[32..63])
    mult_expr = il.mult_double_prec_signed(4, sreg1, sreg2)
    lo_expr = mult_expr
    hi_expr = il.arith_shift_right(8, mult_expr, il.const(1, 32))

    il.append(il.set_reg(8, LO1_REG, lo_expr))
    il.append(il.set_reg(8, LO1_REG, il.sign_extend(8, il.reg(4, LO1_REG))))
    il.append(il.set_reg(8, HI1_REG, hi_expr))
    if instruction.reg1 != ZERO_REG:
        il.append(il.set_reg(8, instruction.reg1, lo_expr)) # R5900 also allows for a destination register for this opcode
        il.append(il.set_reg(8, instruction.reg1, il.sign_extend(8, il.reg(4, instruction.reg1))))

def mult1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg2)
    sreg2 = il.reg(4, instruction.reg3)

    mult_expr = il.mult_double_prec_signed(4, sreg1, sreg2)
    lo_expr = mult_expr
    hi_expr = il.arith_shift_right(8, mult_expr, il.const(1, 32))

    il.append(il.set_reg(8, LO1_REG, lo_expr))
    il.append(il.set_reg(8, LO1_REG, il.sign_extend(8, il.reg(4, LO1_REG))))
    il.append(il.set_reg(8, HI1_REG, hi_expr))
    if instruction.reg1 != ZERO_REG:
        il.append(il.set_reg(8, instruction.reg1, lo_expr)) # R5900 also allows for a destination register for this opcode
        il.append(il.set_reg(8, instruction.reg1, il.sign_extend(8, il.reg(4, instruction.reg1))))

def multu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg2)
    sreg2 = il.reg(4, instruction.reg3)

    mult_expr = il.mult_double_prec_unsigned(4, sreg1, sreg2)
    lo_expr = mult_expr
    hi_expr = il.arith_shift_right(8, mult_expr, il.const(1, 32))

    il.append(il.set_reg(8, LO_REG, lo_expr))
    il.append(il.set_reg(8, LO_REG, il.sign_extend(8, il.reg(4, LO_REG))))
    il.append(il.set_reg(8, HI_REG, hi_expr))
    if instruction.reg1 != ZERO_REG:
        il.append(il.set_reg(8, instruction.reg1, lo_expr)) # R5900 also allows for a destination register for this opcode
        il.append(il.set_reg(8, instruction.reg1, il.sign_extend(8, il.reg(4, instruction.reg1))))

def multu1(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg1 = il.reg(4, instruction.reg2)
    sreg2 = il.reg(4, instruction.reg3)

    mult_expr = il.mult_double_prec_unsigned(4, sreg1, sreg2)
    lo_expr = mult_expr
    hi_expr = il.arith_shift_right(8, mult_expr, il.const(1, 32))

    il.append(il.set_reg(8, LO1_REG, lo_expr))
    il.append(il.set_reg(8, LO1_REG, il.sign_extend(8, il.reg(4, LO1_REG))))
    il.append(il.set_reg(8, HI1_REG, hi_expr))
    if instruction.reg1 != ZERO_REG:
        il.append(il.set_reg(8, instruction.reg1, lo_expr)) # R5900 also allows for a destination register for this opcode
        il.append(il.set_reg(8, instruction.reg1, il.sign_extend(8, il.reg(4, instruction.reg1))))

def nop(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.nop())

def ee_nor(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    sr1 = instruction.reg2
    sr2 = instruction.reg3
    sreg1 = il.reg(8, sr1)
    sreg2 = il.reg(8, sr2)
    not_sreg1 = il.not_expr(8, sreg1)
    not_sreg2 = il.not_expr(8, sreg2)

    expr = il.or_expr(8, not_sreg1, not_sreg2)
    if sr1 == ZERO_REG and sr2 == ZERO_REG:
        expr = il.const(8, 0xFFFFFFFF_FFFFFFFF)
    elif sr1 == ZERO_REG:
        expr = not_sreg2
    elif sr2 == ZERO_REG:
        expr = not_sreg1

    il.append(il.set_reg(8, instruction.reg1, expr))

def ee_or(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    sr1 = instruction.reg2
    sr2 = instruction.reg3
    sreg1 = il.reg(8, sr1)
    sreg2 = il.reg(8, sr2)

    expr = il.or_expr(8, sreg1, sreg2)
    if sr1 == ZERO_REG and sr2 == ZERO_REG:
        expr = il.const(8, 0)
    elif sr1 == ZERO_REG:
        expr = sreg2
    elif sr2 == ZERO_REG:
        expr = sreg1

    il.append(il.set_reg(8, instruction.reg1, expr))

def ori(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg = il.reg(8, instruction.reg2)
    imm = il.const(8, instruction.operand)

    expr = il.or_expr(8, sreg, imm)
    if instruction.reg2 == ZERO_REG:
        expr = imm

    il.append(il.set_reg(8, instruction.reg1, expr))

def qmfc2(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mfc(instruction, addr, il, 2)

def qmtc2(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _mtc(instruction, addr, il, 2)

def _sll(instruction: Instruction, addr: int, il: LowLevelILFunction, size: int, shift: ExpressionIndex) -> None:
    val = il.shift_left(size, il.reg(size, instruction.reg2), shift)

    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(size, instruction.reg1, val))

def sll(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sll(instruction, addr, il, 4, il.const(1, instruction.operand))

def _sllv(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    # NOTE: Technically this should read 5 bits (for sllv) or 6 bits (for dsllv) from rs but it's probably fine
    val = il.shift_left(size, il.reg(size, instruction.reg2), il.reg(1, instruction.reg3))

    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(size, instruction.reg1, val))

def sllv(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sllv(instruction, addr, il, 4)

def slt(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.reg(8, instruction.reg3)
    source = il.reg(8, instruction.reg2)
    expr = il.compare_signed_less_than(8, source, val)

    il.append(il.set_reg(8, instruction.reg1, expr))

def slti(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(8, instruction.operand)
    source = il.reg(8, instruction.reg2)
    expr = il.compare_signed_less_than(8, source, val)

    il.append(il.set_reg(8, instruction.reg1, expr))

def sltiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(8, instruction.operand)
    source = il.reg(8, instruction.reg2)
    expr = il.compare_unsigned_less_than(8, source, val)

    il.append(il.set_reg(8, instruction.reg1, expr))

def sltu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.reg(8, instruction.reg3)
    source = il.reg(8, instruction.reg2)
    expr = il.compare_unsigned_less_than(8, source, val)

    il.append(il.set_reg(8, instruction.reg1, expr))

def _sra(instruction: Instruction, addr: int, il: LowLevelILFunction, size: int, shift: ExpressionIndex) -> None:
    val = il.arith_shift_right(size, il.reg(size, instruction.reg2), shift)

    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(8, instruction.reg1, val))

def sra(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _sra(instruction, addr, il, 4, il.const(1, instruction.operand))

def _srav(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    # NOTE: Technically this should read 5 bits (for sllv) or 6 bits (for dsllv) from rs but it's probably fine
    val = il.arith_shift_right(size, il.reg(size, instruction.reg2), il.reg(1, instruction.reg3))

    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(8, instruction.reg1, val))

def srav(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srav(instruction, addr, il, 4)

def _srl(instruction: Instruction, addr: int, il: LowLevelILFunction, size: int, shift: ExpressionIndex) -> None:
    val = il.logical_shift_right(size, il.reg(size, instruction.reg2), shift)
    il.append(il.set_reg(size, instruction.reg1, val))

def srl(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srl(instruction, addr, il, 4, il.const(1, instruction.operand))

def _srlv(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    # NOTE: Technically this should read 5 bits (for sllv) or 6 bits (for dsllv) from rs but it's probably fine
    val = il.logical_shift_right(size, il.reg(size, instruction.reg2), il.reg(1, instruction.reg3))

    if size < 8:
        val = il.sign_extend(8, val)

    il.append(il.set_reg(8, instruction.reg1, val))

def srlv(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _srlv(instruction, addr, il, 4)

def _store(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    if instruction.reg1 == ZERO_REG:
        value = il.const(size, 0)
    else:
        value = il.reg(size, instruction.reg1)
    addr = il.add(4, il.reg(4, instruction.reg2), il.const(4, instruction.operand))
    
    il.append(il.store(size, addr, value))

sb   = lambda instruction, addr, il: _store(instruction, addr, il, 1)
sd   = lambda instruction, addr, il: _store(instruction, addr, il, 8)
sh   = lambda instruction, addr, il: _store(instruction, addr, il, 2)
sq   = lambda instruction, addr, il: _store(instruction, addr, il, 16)
sqc2 = lambda instruction, addr, il: _store(instruction, addr, il, 16)
sw   = lambda instruction, addr, il: _store(instruction, addr, il, 4)
swc1 = lambda instruction, addr, il: _store(instruction, addr, il, 4)

def _sub(instruction: Instruction, addr: int, il: LowLevelILFunction, size: int) -> None:
    value = None
    r1, r2, r3 = instruction.reg1, instruction.reg2, instruction.reg3
    if r2 == ZERO_REG and r3 == ZERO_REG:
        # move zero for some reason
        value = il.const(size, 0)
    elif r2 == ZERO_REG:
        # negate
        value = il.neg_expr(size, il.reg(size, r3))
    elif r3 == ZERO_REG:
        # move (why?)
        value = il.reg(size, r2)
    else:
        # subu
        value = il.sub(size, il.reg(size, r2), il.reg(size, r3))

    if size < 8:
        value = il.sign_extend(8, value)
    
    il.append(il.set_reg(8, r1, value))

def sub(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    _sub(instruction, addr, il, 4)

subu = sub

def syscall(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.system_call())

def ee_xor(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sr1 = instruction.reg2
    sr2 = instruction.reg3
    sreg1 = il.reg(8, sr1)
    sreg2 = il.reg(8, sr2)

    expr = il.xor_expr(8, sreg1, sreg2)
    if sr1 == sr2:
        expr = il.const(8, 0)
    elif sr1 == ZERO_REG:
        expr = sreg2
    elif sr2 == ZERO_REG:
        expr = sreg1

    il.append(il.set_reg(8, instruction.reg1, expr))

def xori(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    sreg = il.reg(8, instruction.reg2)
    imm = il.const(8, instruction.operand)

    expr = il.xor_expr(8, sreg, imm)
    if instruction.reg2 == ZERO_REG:
        expr = imm

    il.append(il.set_reg(8, instruction.reg1, expr))

def get_move_cond_expr(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> ExpressionIndex:
    # For movz, movn
    r3 = instruction.reg3

    if r3 == ZERO_REG:
        test = il.const(8, 0)
    else:
        test = il.reg(8, r3)

    match instruction.name:
        case "movn":
            return il.compare_not_equal(8, test, il.const(8, 0))
        case "movz":
            return il.compare_equal(8, test, il.const(8, 0))
        case _:
            raise ValueError(f"Unexpected conditional move operation {instruction.name}")

def get_branch_cond_expr(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> ExpressionIndex:
    # Returns the comparison for a branch (ignoring unconditional branches)

    r1 = instruction.reg1
    r2 = instruction.reg2
    
    val1 = None
    if r1 is not None:
        if r1 == ZERO_REG:
            val1 = il.const(8, 0)
        else:
            val1 = il.reg(8, instruction.reg1)

    val2 = None
    if r2 is not None:
        if r2 == ZERO_REG:
            val2 = il.const(8, 0)
        else:
            val2 = il.reg(8, instruction.reg2)

    match instruction.name:
        case "bc0":
            return il.unimplemented()
        case "bc1":
            return il.compare_equal(3, il.flag(FPU_CONDITION_FLAG), il.const(3, instruction.cop_branch_type))
        case "bc2":
            return il.unimplemented()
        case "beq" | "beql":
            return il.compare_equal(8, val1, val2)
        case "bgez" | "bgezl" | "bgezal" | "bgezall":
            return il.compare_signed_greater_equal(8, val1, il.const(8, 0))
        case "bgtz" | "bgtzl":
            return il.compare_signed_greater_than(8, val1, il.const(8, 0))
        case "blez" | "blezl":
            return il.compare_signed_less_equal(8, val1, il.const(8, 0))
        case "bltz" | "bltzl" | "bltzal" | "bltzall":
            return il.compare_signed_less_than(8, val1, il.const(8, 0))
        case "bne" | "bnel":
            return il.compare_not_equal(8, val1, val2)
        case _:
            raise ValueError(f"Unexpected branch operation {instruction.name}")
