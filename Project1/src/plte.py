PLTE_NAME: bytes = b'PLTE'

def read_PLTE_chunks(image_bytes: bytes, start_index: int, length: int) -> list[tuple[int, int, int]]:
    chunk_name = image_bytes[start_index+4:start_index+8]
    if chunk_name != PLTE_NAME:
        raise ValueError("The chunk is not PLTE.")
    
    plte_data = image_bytes[start_index+8:start_index+8+length]

    if len(plte_data) % 3 != 0:
        raise ValueError("PLTE chunk data length is not a multiple of 3.")
    
    palette: list[tuple[int, int, int]] = []
    for i in range(0, len(plte_data), 3):
        r = plte_data[i]
        g = plte_data[i+1]
        b = plte_data[i+2]
        palette.append((r, g, b))

    return palette

def print_PLTE_info(palette: list[tuple[int, int, int]]) -> None:
    print("\nPLTE Chunk Information:")
    print(f"  Number of palette entries: {len(palette)}")
    
    limit = min(5, len(palette))
    for i in range(limit):
        print(f"  Entry {i+1}: R={palette[i][0]}, G={palette[i][1]}, B={palette[i][2]}")

    if len(palette) > limit:
        print(f"  ... and {len(palette) - limit} more entries.")