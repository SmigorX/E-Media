import zlib
from typing import TypedDict

class ChunkInfo(TypedDict):
    type: str
    length: int
    start_index: int

def check_chunk_crc(image_bytes: bytes, chunk: ChunkInfo) -> bool:
    start = chunk["start_index"]
    length = chunk["length"]
    type_and_data = image_bytes[start + 4 : start + 8 + length]
    computed = zlib.crc32(type_and_data)
    stored = int.from_bytes(image_bytes[start + 8 + length : start + 8 + length + 4], "big")
    return computed == stored

def read_all_chunks(image_bytes: bytes) -> list[ChunkInfo]:
    cursor = 8
    chunks = []

    while cursor < len(image_bytes):

        chunk_length = int.from_bytes(image_bytes[cursor:cursor+4], "big")
        chunk_type = image_bytes[cursor+4:cursor+8].decode("ascii")

        chunks.append({
            "type": chunk_type,
            "length": chunk_length,
            "start_index": cursor,
        })
        cursor += 12 + chunk_length

        if chunk_type == "IEND":
            break

    return chunks

def print_all_chunks(chunks: list[ChunkInfo], image_bytes: bytes) -> None:
    print("\nAll chunks in the PNG file:")
    print("-" * 60)
    print(f"{'No.':<4} {'Type':<6} {'Length':<17} {'Start Index':<15} {'CRC':<6}")
    print("-" * 60)
    for i, chunk in enumerate(chunks):
        crc_ok = "OK" if check_chunk_crc(image_bytes, chunk) else "FAIL"
        print(f"  {i+1:<4} {chunk['type']:<6} {chunk['length']:<17} {chunk['start_index']:<15} {crc_ok:<6}")
    print("-" * 60)