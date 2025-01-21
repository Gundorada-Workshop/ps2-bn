import struct
from enum import Enum

# https://en.wikipedia.org/wiki/Executable_and_Linkable_Format

class EndianType(Enum):
    Undefined = 0x0,
    Little    = 0x1
    Big       = 0x2

class FormatType(Enum):
    Undefined = 0x0
    Format32  = 0x1
    Format64  = 0x2

class HeaderOffsets(Enum):
    Magic       = 0x00
    Class       = 0x04
    Data        = 0x05
    Version     = 0x06
    Abi         = 0x07
    AbiVersion  = 0x08
    Type        = 0x10
    Machine     = 0x12
    Version2    = 0x14
    Entry       = 0x18

class AbiType(Enum):
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

class MachineType(Enum):
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

class SegmentType(Enum):
    Null               = 0x00
    Loadable           = 0x01
    Dynamic            = 0x02
    Interpreter        = 0x03
    Note               = 0x04
    ProgramHeader      = 0x06
    ThreadLocalStorage = 0x07

class SegmentFlags(Enum):
    Executable = 0x1
    Writeable  = 0x2
    Readable   = 0x3

class SectionType(Enum):
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

class SectionAttributeFlags(Enum):
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
    type: int
    flags: int
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
    