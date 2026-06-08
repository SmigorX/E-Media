"""
Wg specyfikacji po magicznych bajtach mamy:
- długość następnego chanka, dla IHDR zawsze 13 bajtów
- typ chunka, dla IHDR zawsze "IHDR"
- dane chunka IHDR
"""

IHDR_LENGTH: bytes = b'\x00\x00\x00\x0D'

IHDR_NAME: bytes = b'IHDR'

IHDR_CHUNK_BYTES_MAP: dict[str, int] = {
    "Width": 4,
    "Height": 4,
    "Bit_Depth": 1,
    "Color_Type": 1,
    "Compression_Method": 1,
    "Filter_Method": 1,
    "Interlace_Method": 1
}


def read_IHDR_chunk(image_bytes: bytes) -> dict[str, bytes]:
    ihdr_info: dict[str, bytes] = {}
    image_bytes = image_bytes[8:]

    if image_bytes[:4] != IHDR_LENGTH:
        raise ValueError("The first chunk is not IHDR or has an incorrect length.")
    
    if image_bytes[4:8] != IHDR_NAME:
        raise ValueError("The first chunk is not IHDR.")
    
    ihdr_data = image_bytes[8:21]
    
    for key, value in IHDR_CHUNK_BYTES_MAP.items():
        ihdr_info[key] = ihdr_data[:value]
        ihdr_data = ihdr_data[value:]

    return ihdr_info


COLOR_TYPES = {0: "grayscale", 2: "RGB", 3: "palette",
               4: "grayscale+alpha", 6: "RGBA"}
INTERLACE = {0: "none", 1: "Adam7"}

def print_IHDR_info(ihdr_info: dict[str, bytes]) -> None:
    values = {k: int.from_bytes(v, "big") for k, v in ihdr_info.items()}
    print("IHDR Chunk Information:")
    print(f"  Dimensions:    {values['Width']} x {values['Height']} px")
    print(f"  Bit depth:     {values['Bit_Depth']}")
    print(f"  Color type:    {values['Color_Type']} ({COLOR_TYPES.get(values['Color_Type'], 'unknown')})")
    print(f"  Compression:   {values['Compression_Method']}")
    print(f"  Filter:        {values['Filter_Method']}")
    print(f"  Interlace:     {values['Interlace_Method']} ({INTERLACE.get(values['Interlace_Method'], 'unknown')})")
