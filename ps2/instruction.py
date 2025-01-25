from __future__ import annotations
from enum import Enum, auto, unique
from typing import Optional, Callable, Type, TYPE_CHECKING
from binaryninja.architecture import RegisterName

if TYPE_CHECKING:
    from ..Arch import EmotionEngine

@unique
class InstructionType(Enum):
    UNDEFINED = auto()
    GenericInt = auto()
    Branch = auto()
    LoadStore = auto()

class Instruction:
    __slots__ = [
        "type", "name", "branch_dest", "reg1", "reg2", "reg3", "operand", "il_func",
        "arch", "cop_branch_type", "is_likely",
    ]

    type: InstructionType
    name: Optional[str]
    branch_dest: Optional[int]
    reg1: Optional[RegisterName]
    reg2: Optional[RegisterName]
    reg3: Optional[RegisterName]
    operand: Optional[str]
    il_func: Optional[Callable]
    arch: Optional[Type[EmotionEngine]]
    cop_branch_type: Optional[bool]
    """
    Determines if a COP branch (bc1 or bc2) branches on true or false condition
    """
    is_likely: bool
    """
    If branch instruction, is it likely
    """

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
        self.cop_branch_type = None
        self.is_likely = False
