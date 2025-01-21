from .registers import gpr
from ..instruction import Instruction

def nop(instruction: Instruction, il):
    il.append(il.nop())

def sll(instruction: Instruction, il):
    val = il.shift_left(4, il.reg(4, instruction.source1), il.const(1, instruction.operand))
    il.append(il.set_reg(4, instruction.dest, val))

def jr(instruction: Instruction, il):
    if gpr[instruction.dest] == "$ra":
        il.append(il.ret(0))
    else:
        il.append(il.unimplemented())
