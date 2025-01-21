from __future__ import annotations
from enum import Enum, auto, unique
from typing import Optional, Callable, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Arch import EmotionEngine

@unique
class InstructionType(Enum):
    UNDEFINED = auto()
    GenericInt = auto()
    Branch = auto()
    LoadStore = auto()

class Instruction:
    type: InstructionType
    name: Optional[str]
    branch_dest: Optional[int]
    reg1: Optional[int]
    reg2: Optional[int]
    reg3: Optional[int]
    operand: Optional[str]
    il_func: Optional[Callable]
    arch: Optional[Type[EmotionEngine]]

    def __init__(self):
        self.type = InstructionType.UNDEFINED
        self.name = None
        self.branch_dest = None
        self.reg1 = None
        self.reg2 = None
        self.reg3 = None
        self.operand = None
        self.il_func = None
        self.arch = None
