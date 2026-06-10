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
    print("PLTE Chunk Information:")
    print("-" * 44)
    print(f"  {'Field':<22} {'Value'}")
    print("-" * 44)
    print(f"  {'Number of entries':<22} {len(palette)}")
    print("-" * 44)
    print(f"  {'No.':<6} {'R':<8} {'G':<8} {'B'}")
    print("-" * 44)
    limit = min(5, len(palette))
    for i in range(limit):
        r, g, b = palette[i]
        print(f"  {i+1:<6} {r:<8} {g:<8} {b}")
    if len(palette) > limit:
        print(f"  ... and {len(palette) - limit} more entries.")
    print("-" * 44)