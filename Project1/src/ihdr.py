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


def print_IHDR_info(ihdr_info: dict[str, bytes]) -> None:
    print("IHDR Chunk Information:")
    for key, value in ihdr_info.items():
        print(f"{key}: {int.from_bytes(value, 'big')}")
