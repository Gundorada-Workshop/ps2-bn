from typing import List, Tuple
from binaryninja.architecture import RegisterName

# name, size
# TODO
registers: List[Tuple[RegisterName, int]] = [
    (RegisterName(f"$COPZ{i}"), 4) for i in range(0, 32)
]

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid COP0 register index {index}")

    return registers[index][0]

# name, size
# TODO
c_registers: List[Tuple[RegisterName, int]] = [
    (RegisterName(f"$COPZCR{i}"), 4) for i in range(0, 32)
]

CONDITION_REG = RegisterName("COP0_CONDITION")

c_registers.append((CONDITION_REG, 4))

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid COP0 Control register index {index}")

    return registers[index][0]