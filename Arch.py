from __future__ import annotations
from typing import Optional
from .ps2.decode import convert_to_pseudo, decode
from .ps2.instruction import Instruction, InstructionType
from .ps2.ee.il import get_branch_cond_expr
from .ps2.ee.registers import registers as EERegisters
from .ps2.ee.registers import HI_REG, LO_REG, PC_REG, SA_REG, RA_REG, SP_REG, ZERO_REG
from .ps2.ee.registers import CALLER_SAVED_REGS as EE_CALLER_SAVED_REGS
from .ps2.ee.registers import CALLEE_SAVED_REGS as EE_CALLEE_SAVED_REGS
from .ps2.ee.registers import INT_ARG_REGS, INT_RETURN_REG, HIGH_INT_RETURN_REG, GLOBAL_POINTER_REG
from .ps2.fpu.registers import registers as FPURegisters
from .ps2.fpu.registers import c_registers as FPUCRegisters
from .ps2.fpu.registers import CALLER_SAVED_REGS as FPU_CALLER_SAVED_REGS
from .ps2.fpu.registers import CALLEE_SAVED_REGS as FPU_CALLEE_SAVED_REGS
from .ps2.fpu.registers import FLOAT_ARG_REGS, FLOAT_RETURN_REG
from .ps2.vu0.registers import i_registers as VU0IRegisters
from .ps2.vu0.registers import f_registers as VU0FRegisters
from .ps2.vu0.registers import c_registers as VU0CRegisters
from .ps2.cop0.registers import registers as COP0Registers
from .ps2.cop0.registers import c_registers as COP0CRegisters
from .ps2.intrinsics import PS2Intrinsic
from binaryninja import lowlevelil, IntrinsicInfo, Type
from binaryninja.architecture import Architecture
from binaryninja.callingconvention import CallingConvention
from binaryninja.enums import InstructionTextTokenType, BranchType
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.lowlevelil import LowLevelILConst, LowLevelILInstruction, LowLevelILLabel

class PS2CdeclCall(CallingConvention):
    caller_saved_regs = EE_CALLER_SAVED_REGS + FPU_CALLER_SAVED_REGS
    callee_saved_regs = EE_CALLEE_SAVED_REGS + FPU_CALLEE_SAVED_REGS
    int_arg_regs = INT_ARG_REGS
    float_arg_regs = FLOAT_ARG_REGS
    int_return_reg = INT_RETURN_REG
    high_int_return_reg = HIGH_INT_RETURN_REG
    float_return_reg = FLOAT_RETURN_REG
    global_pointer_reg = GLOBAL_POINTER_REG

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 4
    max_instr_length = 8 # Branch + Branch delay slot

    regs = EERegisters | COP0Registers | COP0CRegisters | FPURegisters | FPUCRegisters | VU0IRegisters | VU0FRegisters | VU0CRegisters
    intrinsics = {
        PS2Intrinsic.DI: IntrinsicInfo([],  []),
        PS2Intrinsic.EI: IntrinsicInfo([],  []),
    }

    stack_pointer = SP_REG
    link_register = RA_REG
    operand_separator = ', '

    def get_instruction_info(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = decode(data[0:4], addr)
        IT = InstructionType

        result = InstructionInfo()
        result.length = 4

        if instruction.type == IT.Branch:
            name = instruction.name
            if instruction.name == "beq" and instruction.reg1 == ZERO_REG and instruction.reg2 == ZERO_REG:
                # Fix behavior of beq zero, zero in graph view
                name = "b"

            result.branch_delay = 1
            match name:
                case "jr":
                    if instruction.reg1 == EmotionEngine.link_register:
                        result.add_branch(BranchType.FunctionReturn)
                    else:
                        result.add_branch(BranchType.IndirectBranch)
                case "jal":
                    result.add_branch(BranchType.CallDestination, instruction.branch_dest)
                case "jalr":
                    result.add_branch(BranchType.CallDestination)
                case "b" | "j":
                    result.add_branch(BranchType.UnconditionalBranch, instruction.branch_dest)
                case "syscall":
                    result.add_branch(BranchType.SystemCall)
                    result.branch_delay = 0
                case "eret":
                    result.add_branch(BranchType.FunctionReturn)
                    result.branch_delay = 0
                case _:
                    if instruction.branch_dest is None:
                        raise RuntimeError(f"Invalid branch dest for {instruction.name}")
                    result.add_branch(BranchType.TrueBranch, instruction.branch_dest)
                    result.add_branch(BranchType.FalseBranch, addr + 8)

        return result
    
    def _get_instruction_name(self, instruction: Instruction) -> str:
        name = instruction.name

        if instruction.broadcast_component is not None:
            name += instruction.broadcast_component

        if instruction.destination_components is not None:
            name += f".{instruction.destination_components}"

        if instruction.type == InstructionType.Branch:
            if instruction.cop_branch_type is not None:
                # Coprocessor branches
                if instruction.cop_branch_type:
                    name += "t"
                else:
                    name += "f"
                
                if instruction.is_likely:
                    name += "l"
        
        return name
    
    def get_instruction_text(self, data: bytes, addr: int):
        if len(data) < 4:
            return None

        instruction = decode(data[0:4], addr)

        # Converts instruction properties to that of a psuedo-operation
        # e.g. beq zero, zero -> b or addiu v0, zero, 1 -> li v0, 1
        convert_to_pseudo(instruction)

        IT = InstructionType
        tokens = []

        if instruction.type == IT.UNDEFINED:
            return None
        
        # Instruction name + spaces
        name = self._get_instruction_name(instruction)
        pad = 7 # Spaces will be padded to a *multiple* of this length
        spaces = " " * ((pad - len(name)) % pad + 1)
        tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, name))
        tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, spaces))

        match instruction.type:
            case IT.GenericInt:
                if instruction.reg1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg1))
                if instruction.reg2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg2))
                if instruction.reg3 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg3))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    str_func = hex if abs(instruction.operand) >= 10 else str
                    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str_func(instruction.operand)))
            case IT.Branch:


                if instruction.reg1 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg1))
                if instruction.reg2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg2))
                if instruction.branch_dest is not None:
                    if instruction.reg1 is not None:
                        tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(instruction.branch_dest)))
            case IT.LoadStore:
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg1))
                tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                str_func = hex if abs(instruction.operand) >= 10 else str
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, str_func(instruction.operand)))
                tokens.append(InstructionTextToken(InstructionTextTokenType.BeginMemoryOperandToken, "("))
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, instruction.reg2))
                tokens.append(InstructionTextToken(InstructionTextTokenType.EndMemoryOperandToken, ")"))

        if len(tokens) == 2:
            # Remove spaces from instruction only text
            del tokens[1]

        return tokens, 4
    
    def get_instruction_low_level_il(self, data: bytes, addr: int, il: 'lowlevelil.LowLevelILFunction') -> Optional[int]:
        if len(data) < 4:
            return None
        
        length = 4

        instruction1 = decode(data[0:4], addr)        
        instruction1.arch = EmotionEngine
        if instruction1.il_func is None:
            il.append(il.unimplemented())
            return 4
        
        # Handle branches
        if len(data) >= 8 and \
            instruction1.type == InstructionType.Branch and \
            instruction1.name not in ["eret", "syscall"]:
            instruction2 = decode(data[4:8], addr + 4)
            instruction2.arch = EmotionEngine
            length += 4

            if instruction1.is_likely:
                # Likely branches
                # Only do the branch delay slot if the branch condition is true
                cond = get_branch_cond_expr(instruction1, addr, il)

                t = LowLevelILLabel()
                f = LowLevelILLabel()
                il.append(il.if_expr(cond, t, f))
                il.mark_label(t)
                if instruction2.il_func is not None:
                    instruction2.il_func(instruction2, addr + 4, il)
                il.mark_label(f)
            else:
                # Normal branch
                instruction2 = decode(data[4:8], addr + 4)
                if instruction2.il_func is not None:
                    instruction2.il_func(instruction2, addr + 4, il)
        
        instruction1.il_func(instruction1, addr, il)
        return length
