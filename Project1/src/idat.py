IDAT_NAME: bytes = b'IDAT'

def read_IDAT_chunks(idat_chunks_list: list[dict]) -> dict[str, int]:
    idat_info: dict[str, int] = {
        "Count": len(idat_chunks_list),
        "Total_Size": sum(chunk["length"] for chunk in idat_chunks_list)
    }
    return idat_info

def print_IDAT_info(idat_info: dict[str, int]) -> None:
    print("\nIDAT Chunk Information:")
    print(f"  Number of IDAT chunks: {idat_info['Count']}")
    print(f"  Total size of IDAT data: {idat_info['Total_Size']} bytes")