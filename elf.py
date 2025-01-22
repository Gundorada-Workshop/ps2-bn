from enum import Enum, IntEnum
from typing import Optional

from binaryninja import BinaryView, log_info

# https://en.wikipedia.org/wiki/Executable_and_Linkable_Format

ELF_MAGIC_ID = b'\x7fELF'

class EndianType(IntEnum):
    Undefined = 0x0,
    Little    = 0x1
    Big       = 0x2

class FormatType(IntEnum):
    Undefined = 0x0
    Format32  = 0x1
    Format64  = 0x2

# 32 bit only
class ProgramHeaderOffsets(IntEnum):
    Type            = 0x00
    Offset          = 0x04
    VirtualAddress  = 0x08
    PhysicalAddress = 0x0C
    FileSize        = 0x10
    MemorySize      = 0x14
    Flags           = 0x18
    Alignment       = 0x1C

# 32 bit only
class HeaderOffsets(IntEnum):
    Magic                    = 0x00
    Class                    = 0x04
    Data                     = 0x05
    Version                  = 0x06
    Abi                      = 0x07
    AbiVersion               = 0x08
    Type                     = 0x10
    Machine                  = 0x12
    Version2                 = 0x14
    Entry                    = 0x18
    ProgramHeaderOffset      = 0x1C
    SectionHeaderOffset      = 0x20
    MachineFlags             = 0x24
    HeaderSize               = 0x28
    ProgramHeaderSize        = 0x2A
    ProgramHeaderCount       = 0x2C
    SectionHeaderSize        = 0x2E
    SectionHeaderCount       = 0x30
    SectionHeaderStringIndex = 0x32

class AbiType(IntEnum):
    SystemV = 0x00
    HPUX    = 0x01
    NetBSD  = 0x02
    Linux   = 0x03
    GNUHurd = 0x04
    Solaris = 0x06
    AIX     = 0x07
    IRIX    = 0x08
    FreeBSD = 0x09
    OpenVMS = 0x0D
    NonStop = 0x0E
    AROS    = 0x0F
    Fenix   = 0x10
    Nuxi    = 0x11
    OpenVOS = 0x12

class MachineType(IntEnum):
    Undefined = 0x00
    Bellmac32 = 0x01
    SPARC     = 0x02
    i386      = 0x03
    M68k      = 0x04
    M88k      = 0x05
    iMCU      = 0x06
    i860      = 0x07
    MIPS      = 0x08
    System370 = 0x09
    RS3000    = 0x0A
    PARisc    = 0x0F
    i960      = 0x13
    PowerPC   = 0x14
    PowerPC64 = 0x15
    S390      = 0x16
    V800      = 0x24
    FR20      = 0x25
    RH32      = 0x26
    Arm       = 0x28
    SuperH    = 0x2A
    SPARC9    = 0x2B
    TriCore   = 0x2C
    Argonaut  = 0x2D
    IA64      = 0x32
    MIPSX     = 0x33
    ColdFire  = 0x34
    Cell      = 0x38

class SegmentType(IntEnum):
    Null               = 0x00
    Loadable           = 0x01
    Dynamic            = 0x02
    Interpreter        = 0x03
    Note               = 0x04
    ProgramHeader      = 0x06
    ThreadLocalStorage = 0x07

class SegmentFlags(IntEnum):
    Executable = 1 << 0
    Writeable  = 1 << 1
    Readable   = 1 << 2

class SectionType(IntEnum):
    Null                     = 0x00
    ProgramBits              = 0x01
    SymbolTable              = 0x02
    StringTable              = 0x03
    RelocationWithAddends    = 0x04
    SymbolHashTable          = 0x05
    DynamicLinking           = 0x06
    Notes                    = 0x07
    Bss                      = 0x08
    Relocation               = 0x09
    DynamicLinkerSymbolTable = 0x0B
    InitArray                = 0x0E
    DeinitArray              = 0x0F
    PreinitArray             = 0x10
    Group                    = 0x11
    ExtendedSectionIndices   = 0x12
    TypeCound                = 0x13

class SectionAttributeFlags(IntEnum):
    Write           = 1 << 0
    Alloc           = 1 << 1
    Executable      = 1 << 2
    Merge           = 1 << 4
    Strings         = 1 << 5
    InfoLink        = 1 << 6
    LinkOrder       = 1 << 7
    OsNonConforming = 1 << 8
    Group           = 1 << 9
    ThreadLocalData = 1 << 10

class ProgramHeader:
    type: SegmentType
    flags: SegmentFlags
    offset: int
    virtual_address: int
    physical_address: int
    file_size: int
    memory_size: int
    alignment: int

class SectionHeader:
    name: str
    type: SectionType
    flags: SectionAttributeFlags
    address: int
    offset: int
    size: int
    link: int
    info: int
    alignment: int
    fixed_entry_size: int

class FileHeader:
    magic: str
    format: FormatType
    endian: EndianType
    abi: AbiType
    arch: MachineType
    entry_point: int
    program_header_offset: int
    section_header_offset: int
    flags: int
    program_header_size: int
    program_header_count: int
    section_header_size: int
    section_header_count: int
    section_header_name_index: int

def read_elf_header(data: BinaryView) -> Optional[FileHeader]:
    header = FileHeader()

    header.magic = data.read(HeaderOffsets.Magic, 4)

    if header.magic != ELF_MAGIC_ID:
        return None

    bits = data.read(HeaderOffsets.Class, 1)
    header.format = int.from_bytes(bits, 'little')

    # dont support reading elf64
    if header.format != FormatType.Format32:
        return None

    endian = data.read(HeaderOffsets.Data, 1)
    flags  = data.read(HeaderOffsets.MachineFlags, 4)
    abi    = data.read(HeaderOffsets.Abi, 1)
    arch   = data.read(HeaderOffsets.Machine, 2)
    entry  = data.read(HeaderOffsets.Entry, 4)

    program_header_offset = data.read(HeaderOffsets.ProgramHeaderOffset, 4)
    program_header_count  = data.read(HeaderOffsets.ProgramHeaderCount, 2)
    program_header_size   = data.read(HeaderOffsets.ProgramHeaderSize, 2)

    header.endian      = int.from_bytes(endian, 'little')
    header.abi         = int.from_bytes(abi,    'little')
    header.arch        = int.from_bytes(arch,   'little')
    header.entry_point = int.from_bytes(entry,  'little')

    header.program_header_offset = int.from_bytes(program_header_offset, 'little')
    header.program_header_count  = int.from_bytes(program_header_count, 'little')
    header.program_header_size   = int.from_bytes(program_header_size, 'little')

    header.flags  = int.from_bytes(flags, 'little')

    return header

def read_program_header(data: BinaryView, start: int) -> Optional[ProgramHeader]:
    header_type      = data.read(start + ProgramHeaderOffsets.Type, 4)
    offset           = data.read(start + ProgramHeaderOffsets.Offset, 4)
    virtual_address  = data.read(start + ProgramHeaderOffsets.VirtualAddress, 4)
    physical_address = data.read(start + ProgramHeaderOffsets.PhysicalAddress, 4)
    file_size        = data.read(start + ProgramHeaderOffsets.FileSize, 4)
    memory_size      = data.read(start + ProgramHeaderOffsets.MemorySize, 4)
    flags            = data.read(start + ProgramHeaderOffsets.Flags, 4)
    alignment        = data.read(start + ProgramHeaderOffsets.Alignment, 4)

    program_header = ProgramHeader()

    program_header.type             = int.from_bytes(header_type, 'little')
    program_header.offset           = int.from_bytes(offset, 'little')
    program_header.virtual_address  = int.from_bytes(virtual_address, 'little')
    program_header.physical_address = int.from_bytes(physical_address, 'little')
    program_header.file_size        = int.from_bytes(file_size, 'little')
    program_header.memory_size      = int.from_bytes(memory_size, 'little')
    program_header.flags            = int.from_bytes(flags, 'little')
    program_header.alignment        = int.from_bytes(alignment, 'little')

    return program_header