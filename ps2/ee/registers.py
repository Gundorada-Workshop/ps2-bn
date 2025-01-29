from binaryninja.architecture import RegisterInfo, RegisterName
from typing import Dict, List, Tuple

ZERO_REG = RegisterName("$zero")
AT_REG = RegisterName("$at")
V0_REG = RegisterName("$v0")
V1_REG = RegisterName("$v1")
A0_REG = RegisterName("$a0")
A1_REG = RegisterName("$a1")
A2_REG = RegisterName("$a2")
A3_REG = RegisterName("$a3")
T0_REG = RegisterName("$t0")
T1_REG = RegisterName("$t1")
T2_REG = RegisterName("$t2")
T3_REG = RegisterName("$t3")
T4_REG = RegisterName("$t4")
T5_REG = RegisterName("$t5")
T6_REG = RegisterName("$t6")
T7_REG = RegisterName("$t7")
S0_REG = RegisterName("$s0")
S1_REG = RegisterName("$s1")
S2_REG = RegisterName("$s2")
S3_REG = RegisterName("$s3")
S4_REG = RegisterName("$s4")
S5_REG = RegisterName("$s5")
S6_REG = RegisterName("$s6")
S7_REG = RegisterName("$s7")
T8_REG = RegisterName("$t8")
T9_REG = RegisterName("$t9")
K0_REG = RegisterName("$k0")
K1_REG = RegisterName("$k1")
GP_REG = RegisterName("$gp")
SP_REG = RegisterName("$sp")
FP_REG = RegisterName("$fp")
RA_REG = RegisterName("$ra")
LO_REG = RegisterName("$lo")
HI_REG = RegisterName("$hi")
PC_REG = RegisterName("$pc")
SA_REG = RegisterName("$sa")

# Calling convention stuff
GLOBAL_POINTER_REG = GP_REG
# FIXME: Using entire 128-bit registers for return regs is incorrect,
# but BN doesn't currently support using partial registers for return regs
#_RET_LO = RegisterName("$v0_lo")
#_RET_LO_INFO = RegisterInfo(V0_REG, 4, 0)
INT_RETURN_REG = V0_REG
#_RET_HI = RegisterName("$v1_lo")
#_RET_HI_INFO = RegisterInfo(V1_REG, 4, 0)
HIGH_INT_RETURN_REG = V1_REG
INT_ARG_REGS = [A0_REG, A1_REG, A2_REG, A3_REG, T0_REG, T1_REG]
CALLER_SAVED_REGS = [
    AT_REG, V0_REG, V1_REG, A0_REG, A1_REG, A2_REG, A3_REG,
    T0_REG, T1_REG, T2_REG, T3_REG, T4_REG, T5_REG, T6_REG,
    T7_REG, T8_REG, T9_REG, RA_REG,
]
CALLEE_SAVED_REGS = [
    S0_REG, S1_REG, S2_REG, S3_REG, S4_REG, S5_REG, S6_REG,
    S7_REG, K0_REG, K1_REG, GP_REG, SP_REG, FP_REG,
]

# name, size
register_params: List[Tuple[RegisterName, int]] = [
    (ZERO_REG, 16),    # 0
    (AT_REG, 16),      # 1
    (V0_REG, 16),      # 2
    (V1_REG, 16),      # 3
    (A0_REG, 16),      # 4
    (A1_REG, 16),      # 5
    (A2_REG, 16),      # 6
    (A3_REG, 16),      # 7
    (T0_REG, 16),      # 8
    (T1_REG, 16),      # 9
    (T2_REG, 16),      # 10
    (T3_REG, 16),      # 11
    (T4_REG, 16),      # 12
    (T5_REG, 16),      # 13
    (T6_REG, 16),      # 14
    (T7_REG, 16),      # 15
    (S0_REG, 16),      # 16
    (S1_REG, 16),      # 17
    (S2_REG, 16),      # 18
    (S3_REG, 16),      # 19
    (S4_REG, 16),      # 20
    (S5_REG, 16),      # 21
    (S6_REG, 16),      # 22
    (S7_REG, 16),      # 23
    (T8_REG, 16),      # 24
    (T9_REG, 16),      # 25
    (K0_REG, 16),      # 26
    (K1_REG, 16),      # 27
    (GP_REG, 16),      # 28
    (SP_REG, 16),      # 29
    (FP_REG, 16),      # 30
    (RA_REG, 16),      # 31
    (LO_REG, 16),                   # special
    (HI_REG, 16),                   # special
    (PC_REG, 4),                    # special
    (SA_REG, 8),                    # special
]
registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, size) for name, size in register_params
}
#registers[_RET_LO] = _RET_LO_INFO
#registers[_RET_HI] = _RET_HI_INFO 

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid EE GPR register index {index}")

    return register_params[index][0]
