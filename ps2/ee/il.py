from .registers import registers as gpr
from .registers import ZERO_REG
from ..instruction import Instruction
from ..intrinsics import PS2Intrinsic
from binaryninja.architecture import Architecture
from binaryninja.lowlevelil import LowLevelILFunction, LowLevelILLabel, LowLevelILInstruction, ExpressionIndex, LowLevelILConst

def add(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 4)

def addi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 4)

def _addiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    if instruction.reg2 == ZERO_REG:
        # li
        value = il.const(size, instruction.operand)
    else:
        # addiu
        value = il.add(size, il.reg(size, instruction.reg2), il.const(size, instruction.operand))

    il.append(il.set_reg(size, instruction.reg1, value))

def addiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 4)

def _addu(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    r1, r2, r3 = instruction.reg1, instruction.reg2, instruction.reg3
    if r2 == ZERO_REG and r3 == ZERO_REG:
        # move
        value = il.const(size, 0)
    if r2 == ZERO_REG:
        # move
        value = il.reg(size, r3)
    elif r3 == ZERO_REG:
        # move
        value = il.reg(size, r2)
    else:
        # addu
        value = il.add(size, il.reg(size, r2), il.reg(size, r3))
    
    il.append(il.set_reg(size, r1, value))

def addu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 4)

def _unconditional_branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(
        il.jump(
            il.const(4, instruction.branch_dest)
        )
    )

def _unconditional_failed_branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.nop())

def _branch(instruction: Instruction, addr: int, il: 'LowLevelILFunction', cond: ExpressionIndex) -> None:
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
        il.append(il.jump(t_dest))
        il.append(il.goto(done))
    if f_indirect:
        il.mark_label(f)
        il.append(il.jump(f_dest))
    il.mark_label(done)

def beq(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    r1 = instruction.reg1
    r2 = instruction.reg2
    val1 = il.reg(4, instruction.reg1)
    val2 = il.reg(4, instruction.reg2)

    if r1 == ZERO_REG and r2 == ZERO_REG:
        return _unconditional_branch(instruction, addr, il)
    elif r1 == ZERO_REG:
        val1 = il.const(4, 0)
    elif r2 == ZERO_REG:
        val2 = il.const(4, 0)

    cond = il.compare_equal(4, val1, val2)
    _branch(instruction, addr, il, cond)

def bne(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    r1 = instruction.reg1
    r2 = instruction.reg2
    val1 = il.reg(4, instruction.reg1)
    val2 = il.reg(4, instruction.reg2)

    if r1 == ZERO_REG and r2 == ZERO_REG:
        return _unconditional_failed_branch(instruction, addr, il)
    elif r1 == ZERO_REG:
        val1 = il.const(4, 0)
    elif r2 == ZERO_REG:
        val2 = il.const(4, 0)

    cond = il.compare_not_equal(4, val1, val2)
    _branch(instruction, addr, il, cond)

def dadd(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 8)

def daddi(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 8)

def daddiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 8)

def daddu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 8)

def di(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.DI, []))

def ei(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.EI, []))

def jr(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(
        il.jump(
            il.reg(4, instruction.reg1)
        )
    )

def _load(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int, sign_extend: bool) -> None:
    value = il.load(size, il.add(4, il.reg(4, instruction.reg2), il.const(4, instruction.operand)))
    if sign_extend:
        value = il.sign_extend(8, value)

    # lb, lh, lw, ld write first 64-bits of register; lq writes all 128-bits
    reg_size = max(8, size)
    il.append(il.set_reg(reg_size, instruction.reg1, value))

lb  = lambda instruction, addr, il: _load(instruction, addr, il, 1, sign_extend=True)
lbu = lambda instruction, addr, il: _load(instruction, addr, il, 1, sign_extend=False)
ld  = lambda instruction, addr, il: _load(instruction, addr, il, 8, sign_extend=False)
lh  = lambda instruction, addr, il: _load(instruction, addr, il, 2, sign_extend=True)
lhu = lambda instruction, addr, il: _load(instruction, addr, il, 2, sign_extend=False)
lq  = lambda instruction, addr, il: _load(instruction, addr, il, 16, sign_extend=False)
lw  = lambda instruction, addr, il: _load(instruction, addr, il, 4, sign_extend=True)
lwu = lambda instruction, addr, il: _load(instruction, addr, il, 4, sign_extend=False)

def lui(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand << 16)
    il.append(il.set_reg(4, instruction.reg1, val))

def nop(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.nop())

def sll(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.shift_left(4, il.reg(4, instruction.reg2), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.reg1, val))

def slt(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.reg(4, instruction.reg3)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_signed_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def slti(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_signed_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def sltiu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_unsigned_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def sltu(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    val = il.reg(4, instruction.reg3)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_unsigned_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def _store(instruction: Instruction, addr: int, il: 'LowLevelILFunction', size: int) -> None:
    value = None
    if instruction.reg1 == ZERO_REG:
        value = il.const(size, 0)
    else:
        value = il.reg(size, instruction.reg1)
    addr = il.add(4, il.reg(4, instruction.reg2), il.const(4, instruction.operand))
    
    il.append(il.store(size, addr, value))

sb  = lambda instruction, addr, il: _store(instruction, addr, il, 1)
sd  = lambda instruction, addr, il: _store(instruction, addr, il, 8)
sh  = lambda instruction, addr, il: _store(instruction, addr, il, 2)
sq  = lambda instruction, addr, il: _store(instruction, addr, il, 16)
sw  = lambda instruction, addr, il: _store(instruction, addr, il, 4)

def syscall(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    il.append(il.system_call())
