from ..instruction import Instruction
from .registers import CONDITION_FLAG
from ..ee.il import _branch
from binaryninja.lowlevelil import LowLevelILFunction, LowLevelILLabel

def fpu_abs(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_abs(4, il.reg(4, instruction.reg2))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

def add(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    expr = il.float_add(4, il.reg(4, instruction.reg2), il.reg(4, instruction.reg3))
    expr = il.set_reg(4, instruction.reg1, expr)
    il.append(expr)

bc1 = _branch

def c_s(instruction: Instruction, addr: int, il: 'LowLevelILFunction') -> None:
    cond = get_compare_cond_expr(instruction, addr, il)
    t = LowLevelILLabel()
    f = LowLevelILLabel()
    done = LowLevelILLabel()

    il.append(il.if_expr(cond, t, f))
    il.mark_label(t)
    il.append(il.set_flag(CONDITION_FLAG, il.const(3, 1)))
    il.append(il.goto(done))
    il.mark_label(f)
    il.append(il.set_flag(CONDITION_FLAG, il.const(3, 0)))
    il.mark_label(done)

c_f_s = c_s
c_eq_s = c_s
c_le_s = c_s
c_lt_s = c_s

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

def get_compare_cond_expr(instruction: Instruction, addr: int, il: LowLevelILFunction) -> None:
    match instruction.name:
        case "c.eq.s":
            return il.float_compare_equal(4, il.reg(4, instruction.reg1), il.reg(4, instruction.reg2))
        case "c.f.s":
            return il.const(1, 0)
        case "c.le.s":
            return il.float_compare_less_equal(4, il.reg(4, instruction.reg1), il.reg(4, instruction.reg2))
        case "c.lt.s":
            return il.float_compare_less_than(4, il.reg(4, instruction.reg1), il.reg(4, instruction.reg2))
        case _:
            raise ValueError(f"Unknown float compare instruction {instruction.name}")
