from binaryninja.architecture import RegisterName
from typing import List, Tuple

ZERO_REG = RegisterName("$zero")
SP_REG = RegisterName("$sp")
RA_REG = RegisterName("$ra")
HI_REG = RegisterName("$hi")
LO_REG = RegisterName("$lo")
PC_REG = RegisterName("$pc")
SA_REG = RegisterName("$sa")

# name, size
registers: List[Tuple[RegisterName, int]] = [
    (ZERO_REG, 16),    # 0
    (RegisterName("$at"), 16),      # 1
    (RegisterName("$v0"), 16),      # 2
    (RegisterName("$v1"), 16),      # 3
    (RegisterName("$a0"), 16),      # 4
    (RegisterName("$a1"), 16),      # 5
    (RegisterName("$a2"), 16),      # 6
    (RegisterName("$a3"), 16),      # 7
    (RegisterName("$t0"), 16),      # 8
    (RegisterName("$t1"), 16),      # 9
    (RegisterName("$t2"), 16),      # 10
    (RegisterName("$t3"), 16),      # 11
    (RegisterName("$t4"), 16),      # 12
    (RegisterName("$t5"), 16),      # 13
    (RegisterName("$t6"), 16),      # 14
    (RegisterName("$t7"), 16),      # 15
    (RegisterName("$s0"), 16),      # 16
    (RegisterName("$s1"), 16),      # 17
    (RegisterName("$s2"), 16),      # 18
    (RegisterName("$s3"), 16),      # 19
    (RegisterName("$s4"), 16),      # 20
    (RegisterName("$s5"), 16),      # 21
    (RegisterName("$s6"), 16),      # 22
    (RegisterName("$s7"), 16),      # 23
    (RegisterName("$t8"), 16),      # 24
    (RegisterName("$t9"), 16),      # 25
    (RegisterName("$k0"), 16),      # 26
    (RegisterName("$k1"), 16),      # 27
    (RegisterName("$gp"), 16),      # 28
    (SP_REG, 16),      # 29
    (RegisterName("$fp"), 16),      # 30
    (RA_REG, 16),      # 31
    (LO_REG, 16),                   # special
    (HI_REG, 16),                   # special
    (PC_REG, 4),                    # special
    (SA_REG, 8),                    # special
]

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        return ValueError(f"Invalid register index {index}")

    return registers[index][0]
