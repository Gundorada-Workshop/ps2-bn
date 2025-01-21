from enum import Enum, auto, unique
from typing import Optional, Callable

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

    def __init__(self):
        self.type = InstructionType.UNDEFINED
        self.name = None
        self.dest = None
        self.source1 = None
        self.source2 = None
        self.operand = None
        self.il_func = None
