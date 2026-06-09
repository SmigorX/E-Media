def read_all_chunks(image_bytes: bytes) -> list[dict]:
    cursor = 8  # Skip the PNG signature
    chunks = []

    while cursor < len(image_bytes):

        chunk_length = int.from_bytes(image_bytes[cursor:cursor+4], "big")
        chunk_type = image_bytes[cursor+4:cursor+8].decode("ascii")

        chunks.append({
            "type": chunk_type,
            "length": chunk_length,
            "start_index": cursor,
        })
        # 4 bytes - length, 4 bytes - type, chunk_length bytes - data, 4 bytes - CRC
        cursor += 12 + chunk_length

        if chunk_type == "IEND":
            break

    return chunks

def print_all_chunks(chunks: list[dict]) -> None:
    print("\nAll chunks in the PNG file:")
    print("-" * 50)
    print(f"{'No.':<4} {'Type':<6} {'Length':<17} {'Start Index':<15}")
    print("-" * 50)
    for i, chunk in enumerate(chunks):
        print(f"  {i+1:<4} {chunk['type']:<6} {chunk['length']:<17} {chunk['start_index']:<15}")
    print("-" * 50)