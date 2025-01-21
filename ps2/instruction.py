from __future__ import annotations
from enum import Enum, auto, unique
from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Arch import EmotionEngine

@unique
class InstructionType(Enum):
    UNDEFINED = auto()
    GenericInt = auto()
    Branch = auto()

class Instruction:
    type: InstructionType
    name: Optional[str]
    dest: Optional[int]
    source1: Optional[int]
    source2: Optional[int]
    operand: Optional[str]
    il_func: Optional[Callable]
    arch: Optional[EmotionEngine]

    def __init__(self):
        self.type = InstructionType.UNDEFINED
        self.name = None
        self.dest = None
        self.source1 = None
        self.source2 = None
        self.operand = None
        self.il_func = None
        self.arch = None
