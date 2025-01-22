from .registers import registers as gpr
from .registers import ZERO_REG
from ..instruction import Instruction
from ..intrinsics import Intrinsic
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
    il.append(il.nop())
    # Broken in Python?
    #il.append(il.intrinsic([], Intrinsic.DI, []))

def ei(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.nop())
    # Broken in Python?
    #il.append(il.intrinsic([], Intrinsic.EI, []))

def jr(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(
        il.jump(
            il.reg(4, instruction.reg1)
        )
    )

def lui(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.const(4, instruction.operand << 16)
    il.append(il.set_reg(4, instruction.reg1, val))

def nop(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.nop())

def sll(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    val = il.shift_left(4, il.reg(4, instruction.reg2), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.reg1, val))

def syscall(instruction: Instruction, addr: int, il: 'lowlevelil.LowLevelILFunction') -> None:
    il.append(il.system_call())
