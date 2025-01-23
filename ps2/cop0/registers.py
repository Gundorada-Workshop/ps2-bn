from typing import Dict, List, Tuple
from binaryninja.architecture import RegisterInfo, RegisterName

# name, size
# TODO
register_names: List[RegisterName] = [RegisterName(f"COPZ{i}") for i in range(32)]
registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in register_names
}

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid COP0 register index {index}")

    return register_names[index]

# name, size
# TODO
c_register_names: List[RegisterName] = [RegisterName(f"COPCRZ{i}") for i in range(32)]
c_registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in c_register_names
}

CONDITION_REG = RegisterName("COP0_CONDITION")
c_registers[CONDITION_REG] = RegisterInfo(CONDITION_REG, 4)

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid COP0 Control register index {index}")

    return c_register_names[index]
