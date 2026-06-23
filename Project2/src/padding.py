import os
import math

def get_block_size(n: int):
    block_size = math.ceil(n.bit_length() / 8)

    chunk_size = block_size - 1
    return block_size, chunk_size

def add_padding(data: bytes, chunk_size: int) -> bytes:
    padding_length = chunk_size - len(data) % chunk_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def remove_padding(data: bytes) -> bytes:
    padding_length = data[-1]
    return data[:-padding_length]