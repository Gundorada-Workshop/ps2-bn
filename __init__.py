from .Arch import EmotionEngine, PS2CdeclCall
from .elf_view import PS2ExecutableView
from binaryninja.architecture import Architecture

EmotionEngine.register()
PS2ExecutableView.register()

EE = Architecture[EmotionEngine.name]
cdecl = PS2CdeclCall(EE, "__cdecl")
EE.register_calling_convention(cdecl)
EE.cdecl_calling_convention = EE.default_calling_convention = cdecl
