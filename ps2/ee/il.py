from .registers import registers as gpr
from .registers import ZERO_REG
from ..instruction import Instruction
from ..intrinsics import PS2Intrinsic
from ...util import Functor
from binaryninja import lowlevelil

def add(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 4)

def addi(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 4)

def _addiu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction', size: int) -> None:
    value = None
    if instruction.reg2 == ZERO_REG:
        # li
        value = il.const(size, instruction.operand)
    else:
        # addiu
        value = il.add(size, il.reg(size, instruction.reg2), il.const(size, instruction.operand))

    il.append(il.set_reg(size, instruction.reg1, value))

def addiu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 4)

def _addu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction', size: int) -> None:
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

def addu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 4)

def dadd(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 8)

def daddi(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 8)

def daddiu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addiu(instruction, addr, il, 8)

def daddu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    _addu(instruction, addr, il, 8)

def di(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.DI, []))

def ei(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.intrinsic([], PS2Intrinsic.EI, []))

def jr(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(
        il.jump(
            il.reg(4, instruction.reg1)
        )
    )

def _load(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction', size: int, sign_extend: bool) -> None:
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

def lui(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand << 16)
    il.append(il.set_reg(4, instruction.reg1, val))

def nop(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.nop())

def sll(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.shift_left(4, il.reg(4, instruction.reg2), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.reg1, val))

def slt(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.reg(4, instruction.reg3)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_signed_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def slti(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_signed_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def sltiu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_unsigned_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def sltu(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.reg(4, instruction.reg3)
    source = il.reg(4, instruction.reg2)
    expr = il.compare_unsigned_less_than(4, source, val)

    il.append(il.set_reg(4, instruction.reg1, expr))

def _store(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction', size: int) -> None:
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

def syscall(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.system_call())
