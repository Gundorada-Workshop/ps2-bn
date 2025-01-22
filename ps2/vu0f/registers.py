from binaryninja.architecture import RegisterName
from typing import List, Tuple

# name, size
registers: List[Tuple[RegisterName, int]] = [
    (RegisterName("$vf0"), 4),   # 0
    (RegisterName("$vf1"), 4),   # 0
    (RegisterName("$vf2"), 4),   # 0
    (RegisterName("$vf3"), 4),   # 0
    (RegisterName("$vf4"), 4),   # 0
    (RegisterName("$vf5"), 4),   # 0
    (RegisterName("$vf6"), 4),   # 0
    (RegisterName("$vf7"), 4),   # 0
    (RegisterName("$vf8"), 4),   # 0
    (RegisterName("$vf9"), 4),   # 0
    (RegisterName("$vf10"), 4),  # 0
    (RegisterName("$vf11"), 4),  # 0
    (RegisterName("$vf12"), 4),  # 0
    (RegisterName("$vf13"), 4),  # 0
    (RegisterName("$vf14"), 4),  # 0
    (RegisterName("$vf15"), 4),  # 0
    (RegisterName("$vf16"), 4),  # 0
    (RegisterName("$vf17"), 4),  # 0
    (RegisterName("$vf18"), 4),  # 0
    (RegisterName("$vf19"), 4),  # 0
    (RegisterName("$vf20"), 4),  # 0
    (RegisterName("$vf21"), 4),  # 0
    (RegisterName("$vf22"), 4),  # 0
    (RegisterName("$vf23"), 4),  # 0
    (RegisterName("$vf24"), 4),  # 0
    (RegisterName("$vf25"), 4),  # 0
    (RegisterName("$vf26"), 4),  # 0
    (RegisterName("$vf27"), 4),  # 0
    (RegisterName("$vf28"), 4),  # 0
    (RegisterName("$vf29"), 4),  # 0
    (RegisterName("$vf30"), 4),  # 0
    (RegisterName("$vf31"), 4),  # 0
]

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid VU0F register index {index}")

    return registers[index][0]

# name, size
# TODO
c_registers: List[Tuple[RegisterName, int]] = [
    (RegisterName(f"$vcr{i}"), 4) for i in range(0, 32)
]

CONDITION_REG = RegisterName("COP2_CONDITION")

c_registers.append((CONDITION_REG, 4))

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid VU0 Control register index {index}")

    return registers[index][0]