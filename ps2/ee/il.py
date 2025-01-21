from .registers import registers as gpr
from ..instruction import Instruction

def nop(instruction: Instruction, addr: int, il):
    il.append(il.nop())

def sll(instruction: Instruction, addr: int, il):
    val = il.shift_left(4, il.reg(4, instruction.reg2), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.reg1, val))

def jr(instruction: Instruction, addr: int, il):
    if instruction.reg1 == instruction.arch.link_register:
        il.append(il.ret(0))
    else:
        il.append(il.unimplemented())
