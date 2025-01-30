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
from .ps2.vu0.decode import component_bits_to_string, component_id_to_string
from .ps2.cop0.registers import registers as COP0Registers
from .ps2.cop0.registers import c_registers as COP0CRegisters
from .ps2.intrinsics import PS2Intrinsic
from binaryninja import lowlevelil, IntrinsicInfo, Type
from binaryninja.architecture import Architecture
from binaryninja.callingconvention import CallingConvention
from binaryninja.enums import InstructionTextTokenType, BranchType
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.lowlevelil import LowLevelILConst, LowLevelILInstruction, LowLevelILLabel, LowLevelILOperation, \
    LowLevelILSetReg, LowLevelILIf, LowLevelILCall, LowLevelILReg, LLIL_TEMP

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
    max_instr_length = 12 # 8 is needed for branches, but up to 12 can be consumed for li.s construct
    WANT_PSEUDO_OP = True

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
                        result.add_branch(BranchType.UnresolvedBranch)
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

        # cop2 vaddx
        if instruction.broadcast_component is not None:
            name += component_id_to_string(instruction.broadcast_component)

        # cop2 vaddx.xyz
        if instruction.destination_components is not None:
            name += f".{component_bits_to_string(instruction.destination_components)}"

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

        if EmotionEngine.WANT_PSEUDO_OP:
            # Converts instruction properties to that of a psuedo-operation
            # e.g. beq zero, zero -> b or addiu v0, zero, 1 -> li v0, 1
            instruction, length = convert_to_pseudo(data, addr)
        else:
            length = 4
            instruction = decode(data[0:4], addr)

        IT = InstructionType
        tokens = []

        if instruction.type == IT.UNDEFINED:
            return None
        
        # Instruction name + spaces
        name = self._get_instruction_name(instruction)
        pad = 20 # Spaces will be padded to a *multiple* of this length
        spaces = " " * ((pad - len(name)) % pad + 1)
        tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, name))
        tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, spaces))

        match instruction.type:
            case IT.GenericInt:
                if instruction.reg1 is not None:
                    register_name = instruction.reg1

                    # note: no cop2 instruction with both source0 and dest components
                    # no broadcast components should land here
                    if instruction.source0_component is not None:
                        register_name += component_id_to_string(instruction.source0_component)
                    elif instruction.destination_components is not None:
                        register_name += component_bits_to_string(instruction.destination_components)

                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, register_name))

                if instruction.reg2 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))

                    register_name = instruction.reg2

                    # note: no cop2 instruction with both source1 and dest components
                    # it's possible to have the broadcast component on reg2 ie vclip
                    if instruction.broadcast_component is not None and instruction.reg3 is None:
                        register_name += component_id_to_string(instruction.broadcast_component)
                    elif instruction.source1_component is not None:
                        register_name += component_id_to_string(instruction.source1_component)
                    elif instruction.destination_components is not None:
                        register_name += component_bits_to_string(instruction.destination_components)


                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, register_name))
                if instruction.reg3 is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))

                    register_name = instruction.reg3

                    if instruction.broadcast_component is not None:
                        register_name += component_id_to_string(instruction.broadcast_component)
                    elif instruction.destination_components is not None:
                        register_name += component_bits_to_string(instruction.destination_components)

                    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, register_name))
                if instruction.operand is not None:
                    tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, EmotionEngine.operand_separator))
                    if isinstance(instruction.operand, float):
                        tokens.append(InstructionTextToken(InstructionTextTokenType.FloatingPointToken, f"{instruction.operand}f"))
                    else:
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

        return tokens, length
    
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
                done = LowLevelILLabel()
                il.append(il.if_expr(cond, t, f))
                il.mark_label(t)
                il.set_current_address(addr + 4)
                if instruction2.il_func is not None:
                    instruction2.il_func(instruction2, addr + 4, il)
                il.jump(instruction1.branch_dest)
                il.goto(done)
                il.mark_label(f)
                il.jump(addr + 8)
                il.mark_label(done)
            else:
                # Normal branch
                # https://github.com/Vector35/binaryninja-api/blob/dev/arch/mips/arch_mips.cpp#L543
                # Do what the regular MIPS architecture does and use a temp register
                # to store the value of any potentially clobbered registers. This will
                # generate more correct IL in the case of something like:
                # beqz v0, label
                # li v0, 1

                # Add a nop we can replace to store the value set in the delay slot
                il.set_current_address(addr + 4)
                nop = il.nop()
                il.append(nop)

                instruction2 = decode(data[4:8], addr + 4)
                if instruction2.il_func is not None:
                    instruction2.il_func(instruction2, addr + 4, il)
                
                instr_index = il.get_expr_count()
                clobbered = None
                if instr_index != 0:
                    # FIXME: Like the regular arch, we're assuming here that the last
                    # instruction is what clobbers the register, when it might not be
                    # or there may be multiple instructions which do so.
                    delayed = il.get_expr(instr_index - 1)
                    if isinstance(delayed, LowLevelILSetReg) and \
                        delayed.address == addr + 4:
                        clobbered = delayed.dest
            
                il.set_current_address(addr)
                instruction1.il_func(instruction1, addr, il)

                if clobbered is not None:
                    lifted = None
                    for i in range(instr_index, il.get_expr_count()):
                        # Try and find our if_expr expression
                        expr = il.get_expr(i)
                        if isinstance(expr, (LowLevelILIf, LowLevelILCall)) and \
                            expr.address == addr:
                            lifted = expr
                            break
                    if lifted is not None:
                        replace = False
                        temp = LLIL_TEMP(1)

                        # Replace any if conditions with a check against the clobbered register
                        # to instead use a temp register, which will be set later.
                        def traversal_cb(expr: LowLevelILInstruction) -> None:
                            if isinstance(expr, LowLevelILReg) and expr.src == clobbered:
                                return expr

                        for expr in lifted.traverse(traversal_cb):
                            replace = True
                            il.replace_expr(expr, il.reg(expr.size, temp))

                        if replace:
                            # Replace the NOP we created at the beginning with an assigment
                            # to the temp register from the clobbered register.
                            il.set_current_address(addr + 4)
                            il.replace_expr(nop, il.set_reg(delayed.size, temp, il.reg(delayed.size, delayed.dest)))
                            il.set_current_address(addr)
        else:
            instruction1.il_func(instruction1, addr, il)
        
        return length
