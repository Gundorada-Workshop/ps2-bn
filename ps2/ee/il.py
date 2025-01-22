from .registers import registers as gpr
from .registers import ZERO_REG
from ..instruction import Instruction

def addiu(instruction: Instruction, addr: int, il):
    value = None
    if instruction.reg2 == ZERO_REG:
        # li
        value = il.const(4, instruction.operand)
    else:
        # addiu
        value = il.add(4, il.reg(4, instruction.reg2), il.const(4, instruction.operand))

    il.append(il.set_reg(4, instruction.reg1, value))

def jr(instruction: Instruction, addr: int, il):
    il.append(
        il.jump(
            il.reg(4, instruction.reg1)
        )
    )

def nop(instruction: Instruction, addr: int, il):
    il.append(il.nop())

def sll(instruction: Instruction, addr: int, il):
    val = il.shift_left(4, il.reg(4, instruction.reg2), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.reg1, val))
