from typing import Dict, Tuple
from ..ee.registers import END_INDEX

START_INDEX = END_INDEX

# Index, (name, size)
registers: Dict[int, Tuple[str, int]] = {
    0: ("$zero", 16),
    1: ("$at", 16),
    2: ("$v0", 16),
    3: ("$v1", 16),
    4: ("$a0", 16),
    5: ("$a1", 16),
    6: ("$a2", 16),
    7: ("$a3", 16),
    8: ("$t0", 16),
    9: ("$t1", 16),
    10: ("$t2", 16),
    11: ("$t3", 16),
    12: ("$t4", 16),
    13: ("$t5", 16),
    14: ("$t6", 16),
    15: ("$t7", 16),
    16: ("$s0", 16),
    17: ("$s1", 16),
    18: ("$s2", 16),
    19: ("$s3", 16),
    20: ("$s4", 16),
    21: ("$s5", 16),
    22: ("$s6", 16),
    23: ("$s7", 16),
    24: ("$t8", 16),
    25: ("$t9", 16),
    26: ("$k0", 16),
    27: ("$k1", 16),
    28: ("$gp", 16),
    29: ("$sp", 16),
    30: ("$fp", 16),
    31: ("$ra", 16),
    32: ("$lo", 16), # Special
    33: ("$hi", 16), # Special
    34: ("$pc", 4),  # Special
    35: ("$sa", 8),  # Special
}
END_INDEX = START_INDEX + len(registers)

def convert_index(index: int) -> int:
    # Converts an operator index (as would appear in an opcode) to the architecture register index
    return START_INDEX + index
