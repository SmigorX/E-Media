import os

from src.rsa_math import rsa_encrypt_number, rsa_decrypt_number
from src.padding import get_block_size, add_padding, remove_padding

MODE_ECB = "ECB"
MODE_CBC = "CBC"

class EncryptedPixels:
    def __init__(self, low, overflow, mode, iv, pad, chunk_size, block_size):
        self.low = low
        self.overflow = overflow
        self.mode = mode
        self.iv = iv
        self.pad = pad
        self.chunk_size = chunk_size
        self.block_size = block_size

def encrypt_pixels(pixels: bytes, public_key: tuple, mode: str = MODE_ECB,
                   iv: bytes = None, encrypt_fn=None) -> EncryptedPixels:
    encrypt_fn = encrypt_fn or rsa_encrypt_number
    e, n = public_key
    block_size, chunk_size = get_block_size(n)

    padded = add_padding(pixels, chunk_size)
    pad = len(padded) - len(pixels)

    if mode == MODE_CBC:
        iv = iv if iv is not None else os.urandom(chunk_size)
    else:
        iv = b""

    low = bytearray()
    overflow = bytearray()
    prev = iv

    high_unit = 1 << (8 * chunk_size)

    for i in range(0, len(padded), chunk_size):
        chunk = padded[i:i + chunk_size]

        if mode == MODE_CBC:
            chunk = bytes(a ^ b for a, b in zip(chunk, prev))

        m = int.from_bytes(chunk, "big")
        c = encrypt_fn(m, public_key)

        low_bytes = (c % high_unit).to_bytes(chunk_size, "big")
        high_byte = c // high_unit

        low += low_bytes
        overflow.append(high_byte)

        if mode == MODE_CBC:
            prev = low_bytes

    return EncryptedPixels(bytes(low), bytes(overflow), mode, iv,
                           pad, chunk_size, block_size)

def decrypt_pixels(low: bytes, overflow: bytes, private_key: tuple, mode: str,
                   iv: bytes, pad: int, chunk_size: int) -> bytes:
    high_unit = 1 << (8 * chunk_size)
    out = bytearray()
    prev = iv

    num_blocks = len(low) // chunk_size
    for b in range(num_blocks):
        low_bytes = low[b * chunk_size:(b + 1) * chunk_size]
        c = overflow[b] * high_unit + int.from_bytes(low_bytes, "big")
        m = rsa_decrypt_number(c, private_key)
        chunk = m.to_bytes(chunk_size, "big")

        if mode == MODE_CBC:
            chunk = bytes(a ^ b for a, b in zip(chunk, prev))
            prev = low_bytes

        out += chunk

    return remove_padding_with_len(bytes(out), pad)

def remove_padding_with_len(data: bytes, pad: int) -> bytes:
    return data[:-pad] if pad else data
