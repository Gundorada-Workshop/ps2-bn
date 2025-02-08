from typing import Dict, List, Tuple
from binaryninja.architecture import RegisterInfo, RegisterName

INDEX_REGISTER = RegisterName("$Index")
RANDOM_REGISTER = RegisterName("$Random")
ENTRYLO0_REGISTER = RegisterName("$EntryLo0")
ENTRYLO1_REGISTER = RegisterName("$EntryLo1")
CONTEXT_REGISTER = RegisterName("$Context")
PAGEMASK_REGISTER = RegisterName("$PageMask")
WIRED_REGISTER = RegisterName("$Wired")
BADVADDR_REGISTER = RegisterName("$BadVAddr")
COUNT_REGISTER = RegisterName("$Count")
ENTRYHI_REGISTER = RegisterName("$EntryHi")
COMPARE_REGISTER = RegisterName("$Compare")
STATUS_REGISTER = RegisterName("$Status")
CAUSE_REGISTER = RegisterName("$Cause")
EPC_REGISTER = RegisterName("$EPC")
PRID_REGISTER = RegisterName("$PRid")
CONFIG_REGISTER = RegisterName("$Config")
BADPADDR_REGISTER = RegisterName("$BadPAddr")
DEBUG_REGISTER = RegisterName("$Debug")
PERF_REGISTER = RegisterName("$Perf")
TAGLO_REGISTER = RegisterName("$TagLo")
TAGHI_REGISTER = RegisterName("$TagHi")
ERROREPC_REGISTER = RegisterName("$ErrorEPC")

register_names: List[RegisterName] = [
    INDEX_REGISTER,
    RANDOM_REGISTER,
    ENTRYLO0_REGISTER,
    ENTRYLO1_REGISTER,
    CONTEXT_REGISTER,
    WIRED_REGISTER,
    RegisterName("$COPZ7"),
    BADVADDR_REGISTER,
    COUNT_REGISTER,
    ENTRYHI_REGISTER,
    COMPARE_REGISTER,
    STATUS_REGISTER,
    CAUSE_REGISTER,
    EPC_REGISTER,
    PRID_REGISTER,
    CONFIG_REGISTER,
    RegisterName("$COPZ17"),
    RegisterName("$COPZ18"),
    RegisterName("$COPZ19"),
    RegisterName("$COPZ20"),
    RegisterName("$COPZ21"),
    RegisterName("$COPZ22"),
    BADPADDR_REGISTER,
    DEBUG_REGISTER,
    PERF_REGISTER,
    RegisterName("$COPZ26"),
    RegisterName("$COPZ27"),
    TAGLO_REGISTER,
    TAGHI_REGISTER,
    ERROREPC_REGISTER,
    RegisterName("$COPZ31"),
]
registers: Dict[RegisterName, RegisterInfo] = {
    name: RegisterInfo(name, 4) for name in register_names
}

def get_name(index: int) -> RegisterName:
    if not 0 <= index < 32:
        raise IndexError(f"Invalid COP0 register index {index}")

    return register_names[index]
