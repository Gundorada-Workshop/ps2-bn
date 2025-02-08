from ..instruction import Instruction
from binaryninja.lowlevelil import LowLevelILFunction

def cvt_s_w(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.int_to_float(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def cvt_w_s(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_to_int(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)
