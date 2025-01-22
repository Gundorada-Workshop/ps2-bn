import struct

from binaryninja import BinaryView, Architecture, log_info
from binaryninja.enums import SegmentFlag

from .elf import HeaderOffsets, FileHeader, EndianType, read_elf_header

TX79_FLAG = 0x00920000

class PS2ExecutableView(BinaryView):
    name      = "PS2 ELF"
    long_name = "PlayStation 2 Executable"

    @classmethod
    def is_valid_for_data(self, data: BinaryView) -> bool:
        header = read_elf_header(data)

        # not an elf
        if header is None:
            return False
        
        # ps2 is le so we don't care about be elfs
        if header.endian != EndianType.Little:
            return False
        
        # platform specific flags
        # in this case Toshiba hides the EE check here
        if header.flags & TX79_FLAG != TX79_FLAG:
            return False
    
        return True
    
    def __init__(self, data: BinaryView):
        BinaryView.__init__(self, parent_view = data, file_metadata = data.file)

        print("init")

        self.arch     = Architecture["EmotionEngine"]
        self.platform = Architecture["EmotionEngine"].standalone_platform
        self.data     = data
        self.header   = read_elf_header(data)

    def init(self) -> bool:
        self.add_auto_segment(0x00100000, 0xd0fa0, 0x001000, 0xd0fa0, SegmentFlag.SegmentReadable|SegmentFlag.SegmentExecutable)
        self.add_entry_point(self.header.entry_point)

        return True
    
    def perform_is_executable(self) -> bool:
        return True
    
    def perform_get_entry_point(self):
        return 0
    
    def perform_get_address_size(self):
        return 4
