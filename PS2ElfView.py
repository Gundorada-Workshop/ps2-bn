import struct

from binaryninja import BinaryView, Architecture, log_info
from binaryninja.enums import SegmentFlag

from .ElfLoader import HeaderOffsets, FileHeader, EndianType

ELF_MAGIC_ID   = b'\x7fELF'
R9000_MAGIC_ID = 0x00920000

class PS2ExecutableView(BinaryView):
    name      = "PS2 ELF"
    long_name = "PlayStation 2 Executable"

    @classmethod
    def is_valid_for_data(self, data: BinaryView) -> bool:
        magic  = data.read(0x0, 4)
        endian = int.from_bytes(data.read(0x5, 1),  'little')
        flags  = int.from_bytes(data.read(0x24, 4), 'little')

        log_info(magic)
        log_info(endian)
        log_info(flags)

        if magic != ELF_MAGIC_ID:
            return False
        
        if EndianType(endian) != EndianType.Little:
            return False
        
        if flags & R9000_MAGIC_ID != R9000_MAGIC_ID:
            return False
    
        return True
    
    def __init__(self, data: BinaryView):
        BinaryView.__init__(self, parent_view = data, file_metadata = data.file)

        self.arch     = Architecture["EmotionEngine"]
        self.platform = Architecture["EmotionEngine"].standalone_platform
        self.data     = data

        magic  = data.read(0x0, 4)
        format = data.read(0x4, 1)
        endian = data.read(0x5, 1)

        log_info(magic)
        log_info(format)
        log_info(endian)

    def init(self) -> bool:
        self.add_auto_segment(0x00100000, 0xd0fa0, 0x001000, 0xd0fa0, SegmentFlag.SegmentReadable|SegmentFlag.SegmentExecutable)
        self.add_entry_point(0x100008)

        return True
    
    def perform_is_executable(self) -> bool:
        return True
    
    def perform_get_entry_point(self):
        return 0
    
    def perform_get_address_size(self):
        return 4
