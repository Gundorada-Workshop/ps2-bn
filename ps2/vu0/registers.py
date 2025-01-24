from binaryninja.architecture import RegisterName, RegisterInfo
from typing import Dict, List

i_register_names = [RegisterName(f"$vi{i}") for i in range(16)]
i_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 2) for name in i_register_names
}

# rng reg
R_REGISTER = RegisterName("$vir")
i_registers[R_REGISTER] = RegisterInfo(R_REGISTER, 3) # actually 23-bit

# EFU results
P_REGISTER = RegisterName("$vip")
i_registers[P_REGISTER] = RegisterInfo(P_REGISTER, 4)

def get_i_name(index: int) -> RegisterName:
    if not 0 <= index < 16:
        raise IndexError(f"Invalid VU0I register index {index}")

    return i_register_names[index]

f_register_names = [RegisterName(f"$vf{i}") for i in range(32)]
f_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 16) for name in f_register_names
}

# result of div/sqrt etc
Q_REGISTER = RegisterName("$vfq")
f_registers[Q_REGISTER] = RegisterInfo(Q_REGISTER, 2)

# accumulator
ACC_REGISTER = RegisterName("$vfacc")
f_registers[ACC_REGISTER] = RegisterInfo(ACC_REGISTER, 16)

# immediate value reg
I_REGISTER = RegisterName("$vfi")
f_registers[I_REGISTER] = RegisterInfo(I_REGISTER, 4)

_components = ["x", "y", "z", "w"]

def get_f_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid VU0F register index {index}")

    return f_register_names[index]

# TODO
c_register_names = [RegisterName(f"$vcr{i}") for i in range(32)]
c_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in c_register_names
}

CONDITION_REG = RegisterName("COP2_CONDITION")

c_registers[CONDITION_REG] = RegisterInfo(CONDITION_REG, 4)

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid VU0 Control register index {index}")

    return c_register_names[index]
