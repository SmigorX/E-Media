import os
import math

def get_block_size(n: int):
    # We calculate the block size in bytes based on the modulus n
    block_size = math.ceil(n.bit_length() / 8)

    chunk_size = block_size - 1
    return block_size, chunk_size

def add_padding(data: bytes, chunk_size: int) -> bytes:
    # We add padding to the data to ensure that it fits into the chunk size.
    padding_length = chunk_size - len(data) % chunk_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def remove_padding(data: bytes) -> bytes:
    # We remove the padding from the data after decryption.
    padding_length = data[-1]
    return data[:-padding_length]