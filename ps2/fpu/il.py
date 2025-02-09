from ..instruction import Instruction
from binaryninja.lowlevelil import LowLevelILFunction

def fpu_abs(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_abs(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def add(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_add(4, il.reg(4, instruction.reg2), il.reg(4, instruction.reg3))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def cvt_s_w(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.int_to_float(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def cvt_w_s(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_to_int(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def div(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_div(4, il.reg(4, instruction.reg2), il.reg(4, instruction.reg3))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def mov(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.set_reg(4, instruction.reg1, il.reg(4, instruction.reg2))
    il.append(expr)

def mul(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_mult(4, il.reg(4, instruction.reg2), il.reg(4, instruction.reg3))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def neg(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_neg(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def rsqrt(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_sqrt(4, il.reg(4, instruction.reg3))
    expr = il.float_div(4, il.reg(4, instruction.reg2), expr)
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def sqrt(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_sqrt(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def sub(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_sub(4, il.reg(4, instruction.reg2), il.reg(4, instruction.reg3))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

