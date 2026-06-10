IDAT_NAME: bytes = b'IDAT'

def read_IDAT_chunks(idat_chunks_list: list[dict]) -> dict[str, int]:
    idat_info: dict[str, int] = {
        "Count": len(idat_chunks_list),
        "Total_Size": sum(chunk["length"] for chunk in idat_chunks_list)
    }
    return idat_info

def print_IDAT_info(idat_info: dict[str, int]) -> None:
    print("IDAT Chunk Information:")
    print("-" * 44)
    print(f"  {'Field':<22} {'Value'}")
    print("-" * 44)
    print(f"  {'Number of chunks':<22} {idat_info['Count']}")
    print(f"  {'Total size':<22} {idat_info['Total_Size']} bytes")
    print("-" * 44)