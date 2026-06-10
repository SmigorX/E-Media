IEND_LENGTH: bytes = b'\x00\x00\x00\x00'
IEND_NAME: bytes = b'IEND'

def read_IEND_chunk(image_bytes: bytes, start_index: int) -> bool:
    chunk_length = image_bytes[start_index:start_index+4]
    chunk_name = image_bytes[start_index+4:start_index+8]

    if chunk_length != IEND_LENGTH:
        raise ValueError("IEND chunk length is not 0.")
    
    if chunk_name != IEND_NAME:
        raise ValueError("The chunk is not IEND.")
    
    return True

def print_IEND_info(is_valid: bool) -> None:
    print("IEND Chunk Information:")
    print("-" * 44)
    print(f"  {'Status':<22} {'valid' if is_valid else 'INVALID'}")
    print("-" * 44)