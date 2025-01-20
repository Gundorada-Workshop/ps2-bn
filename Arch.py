from binaryninja.architecture import Architecture
from binaryninja.function import RegisterInfo, InstructionInfo, InstructionTextToken
from binaryninja.enums import InstructionTextTokenType, BranchType

class EmotionEngine(Architecture):
    name             = "EmotionEngine"
    address_size     = 4
    default_int_size = 4
    instr_alignment  = 1

    regs = {
        'zero': RegisterInfo('zero', 16),
        'at':   RegisterInfo('at', 16),
        'v0':   RegisterInfo('v0', 16),
        'v1':   RegisterInfo('v1', 16),
        'a0':   RegisterInfo('a0', 16),
        'a1':   RegisterInfo('a1', 16),
        'a2':   RegisterInfo('a2', 16),
        'a3':   RegisterInfo('a3', 16),
        't0':   RegisterInfo('t0', 16),
        't1':   RegisterInfo('t1', 16),
        't2':   RegisterInfo('t2', 16),
        't3':   RegisterInfo('t3', 16),
        't4':   RegisterInfo('t4', 16),
        't5':   RegisterInfo('t5', 16),
        't6':   RegisterInfo('t6', 16),
        't7':   RegisterInfo('t7', 16),
        's0':   RegisterInfo('s0', 16),
        's1':   RegisterInfo('s1', 16),
        's2':   RegisterInfo('s2', 16),
        's3':   RegisterInfo('s3', 16),
        's4':   RegisterInfo('s4', 16),
        's5':   RegisterInfo('s5', 16),
        's6':   RegisterInfo('s6', 16),
        's7':   RegisterInfo('s7', 16),
        't8':   RegisterInfo('t8', 16),
        't9':   RegisterInfo('t9', 16),
        'k0':   RegisterInfo('k0', 16),
        'k1':   RegisterInfo('k1', 16),
        'gp':   RegisterInfo('gp', 16),
        'sp':   RegisterInfo('sp', 16),
        'fp':   RegisterInfo('fp', 16),
        'ra':   RegisterInfo('ra', 16),
    }

    stack_pointer = 'sp'
    link_register = 'ra'

    def get_instruction_info(self, data, addr):
        result = InstructionInfo()
        result.lenth = 1
        return result
    
    def get_instruction_text(self, data, addr):
        tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "Hello")]
        return tokens, 1