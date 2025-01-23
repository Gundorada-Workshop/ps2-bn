from binaryninja.architecture import RegisterName, RegisterInfo
from typing import Dict, List

i_register_names = [RegisterName(f"$vi{i}") for i in range(16)]
i_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 2) for name in i_register_names
}

Q_REGISTER = RegisterName("Q")
i_registers[Q_REGISTER] = RegisterInfo(Q_REGISTER, 2)

def get_i_name(index: int) -> RegisterName:
    if not 0 <= index < 16:
        raise IndexError(f"Invalid VU0I register index {index}")

    return i_register_names[index]

f_register_names = [RegisterName(f"$vf{i}") for i in range(32)]
f_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 16) for name in f_register_names
}

_components = ["x", "y", "z", "w"]

def get_f_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid VU0F register index {index}")

    return f_register_names[index]

def get_subregister_name(index: int, component: int):
    if not 0 <= index < 32:
        raise IndexError(f"Invalid VU0F register index {index}")
    
    return RegisterName(f"{get_f_name(index)}{_components[component]}")

for i in range(len(f_registers)):
    for component in range(0, 4):
        name = get_subregister_name(i, component)
        f_registers[name] = RegisterInfo(get_f_name(i), 4, i * 4)

# TODO
c_register_names = [RegisterName(f"$vcr{i}") for i in range(32)]
c_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 2) for name in c_register_names
}

CONDITION_REG = RegisterName("COP2_CONDITION")

c_registers[CONDITION_REG] = RegisterInfo(CONDITION_REG, 4)

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid VU0 Control register index {index}")

    return c_register_names[index]
