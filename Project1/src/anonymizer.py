from src.chunks import ChunkInfo

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

CRITICAL_CHUNKS = {"IHDR", "PLTE", "IDAT", "IEND", "tRNS"}

def anonymize_png(image_bytes: bytes, chunks: list[ChunkInfo]) -> tuple[bytes, list[ChunkInfo]]:
    kept: list[ChunkInfo] = []
    removed: list[ChunkInfo] = []
    for chunk in chunks:
        (kept if chunk["type"] in CRITICAL_CHUNKS else removed).append(chunk)

    result = PNG_SIGNATURE
    for chunk in kept:
        start, length = chunk["start_index"], chunk["length"]
        result += image_bytes[start : start + 12 + length]

    return result, removed

def print_anonymization_report(removed: list[ChunkInfo]) -> None:
    print("Anonymization Report:")
    print("-" * 44)
    if not removed:
        print("  No ancillary chunks found — file is already clean.")
    else:
        print(f"  {'Chunk type':<22} {'Size (bytes)'}")
        print("-" * 44)
        for chunk in removed:
            print(f"  {chunk['type']:<22} {chunk['length']}")
    print("-" * 44)

def save_anonymized_png(data: bytes, original_path: str) -> str:
    output_path = original_path.replace('.png', '_anonymized.png')
    with open(output_path, 'wb') as f:
        f.write(data)
    return output_path
