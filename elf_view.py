import struct

from binaryninja import BinaryView, Architecture, log_info
from binaryninja.enums import SegmentFlag

from .elf import (
    EndianType,
    SegmentFlags,
    read_elf_header,
    read_program_header
)

TX79_FLAG = 0x00920000

def elf_program_segment_flags_to_binary_ninja_flag(flags: SegmentFlags):
    out = 0
    
    if flags & SegmentFlags.Executable:
        out |= SegmentFlag.SegmentExecutable

    if flags & SegmentFlags.Readable:
        out |= SegmentFlag.SegmentReadable

    if flags & SegmentFlags.Writeable:
        out |= SegmentFlag.SegmentWritable

    return out

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

        self.arch     = Architecture["EmotionEngine"]
        self.platform = Architecture["EmotionEngine"].standalone_platform
        self.data     = data

    def init(self) -> bool:
        header   = read_elf_header(self.data)

        self.add_entry_point(header.entry_point)

        offset = header.program_header_offset

        for i in range(header.program_header_count):
            log_info(f"Reading segment {i} at {hex(offset)}")

            program_header = read_program_header(self.data, offset)
            log_info(vars(program_header))

            virtual_address = program_header.virtual_address
            memory_size     = program_header.memory_size
            data_offset     = program_header.offset
            length          = program_header.file_size

            flags = elf_program_segment_flags_to_binary_ninja_flag(program_header.flags)

            self.add_auto_segment(virtual_address, memory_size, data_offset, length, flags)

            offset += header.program_header_size

        return True
    
    def perform_is_executable(self) -> bool:
        return True
    
    def perform_get_entry_point(self):
        return 0
    
    def perform_get_address_size(self):
        return 4
