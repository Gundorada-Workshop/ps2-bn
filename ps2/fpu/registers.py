from binaryninja.architecture import RegisterName, RegisterInfo
from typing import Dict, List, Tuple

F0_REG = RegisterName("$f0")
FLOAT_RETURN_REG = F0_REG
FLOAT_ARG_REGS = [RegisterName(f"$f{i}") for i in range(12, 20)]
CALLER_SAVED_REGS = [F0_REG] + [RegisterName(f"$f{i}") for i in range(1, 12)] + FLOAT_ARG_REGS
CALLEE_SAVED_REGS = [RegisterName(f"$f{i}") for i in range(20, 32)]

register_names = [RegisterName(f"$f{i}") for i in range(32)]
registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in register_names
}

ACC_REGISTER = RegisterName("$acc")
registers[ACC_REGISTER] = RegisterInfo(ACC_REGISTER, 4)

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid FPU register index {index}")

    return register_names[index]

# name, size
# TODO
c_register_names = [f"$FPUCR{i}" for i in range(32)]
c_register_names[31] = RegisterName("FCSR")

c_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in c_register_names
}

CONDITION_REG = RegisterName("COP1_CONDITION")
c_registers[CONDITION_REG] = RegisterInfo(CONDITION_REG, 4)

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid FPU Control register index {index}")

    return c_register_names[index]
