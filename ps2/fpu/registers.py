from binaryninja.architecture import RegisterName
from typing import List, Tuple

ACC_REGISTER = RegisterName("$acc")

# name, size
registers: List[Tuple[RegisterName, int]] = [
    (RegisterName("$f0"), 4),   # 0
    (RegisterName("$f1"), 4),   # 0
    (RegisterName("$f2"), 4),   # 0
    (RegisterName("$f3"), 4),   # 0
    (RegisterName("$f4"), 4),   # 0
    (RegisterName("$f5"), 4),   # 0
    (RegisterName("$f6"), 4),   # 0
    (RegisterName("$f7"), 4),   # 0
    (RegisterName("$f8"), 4),   # 0
    (RegisterName("$f9"), 4),   # 0
    (RegisterName("$f10"), 4),  # 0
    (RegisterName("$f11"), 4),  # 0
    (RegisterName("$f12"), 4),  # 0
    (RegisterName("$f13"), 4),  # 0
    (RegisterName("$f14"), 4),  # 0
    (RegisterName("$f15"), 4),  # 0
    (RegisterName("$f16"), 4),  # 0
    (RegisterName("$f17"), 4),  # 0
    (RegisterName("$f18"), 4),  # 0
    (RegisterName("$f19"), 4),  # 0
    (RegisterName("$f20"), 4),  # 0
    (RegisterName("$f21"), 4),  # 0
    (RegisterName("$f22"), 4),  # 0
    (RegisterName("$f23"), 4),  # 0
    (RegisterName("$f24"), 4),  # 0
    (RegisterName("$f25"), 4),  # 0
    (RegisterName("$f26"), 4),  # 0
    (RegisterName("$f27"), 4),  # 0
    (RegisterName("$f28"), 4),  # 0
    (RegisterName("$f29"), 4),  # 0
    (RegisterName("$f30"), 4),  # 0
    (RegisterName("$f31"), 4),  # 0
    (ACC_REGISTER, 4),
]

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid FPU register index {index}")

    return registers[index][0]

# name, size
# TODO
c_registers: List[Tuple[RegisterName, int]] = [
    (RegisterName(f"$FPUCR{i}"), 4) for i in range(0, 32)
]
c_registers[31] = (RegisterName("FCSR"), 4)

CONDITION_REG = RegisterName("COP1_CONDITION")

c_registers.append((CONDITION_REG, 4))

def get_c_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise ValueError(f"Invalid FPU Control register index {index}")

    return registers[index][0]