import os
import math
from src.rsa_math import rsa_encrypt_number, rsa_decrypt_number
from src.padding import get_block_size, add_padding, remove_padding

def cbc_encrypt(data: bytes, public_key: tuple, iv: bytes = None) -> tuple[bytes, bytes]:
    """ Encrypts data using RSA in CBC mode """
    e, n = public_key
    block_size, chunk_size = get_block_size(n)

    padded_data = add_padding(data, chunk_size)

    if iv is None:
        iv = os.urandom(chunk_size)

    encrypted_data = bytearray()
    previous_block = iv

    for i in range(0, len(padded_data), chunk_size):
        chunk = padded_data[i:i + chunk_size]

        xor_chunk = bytes(a ^ b for a, b in zip(chunk, previous_block))

        m = int.from_bytes(xor_chunk, 'big')

        c = rsa_encrypt_number(m, public_key)

        encrypted_block = c.to_bytes(block_size, 'big')
        encrypted_data.extend(encrypted_block)

        previous_block = encrypted_block

    return bytes(encrypted_data), iv

def cbc_decrypt(data: bytes, private_key: tuple, iv: bytes) -> bytes:
    """ Decrypts data using RSA in CBC mode """
    d, n = private_key
    block_size, chunk_size = get_block_size(n)

    decrypted_data = bytearray()
    previous_block = iv

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]

        c = int.from_bytes(block, 'big')

        m = rsa_decrypt_number(c, private_key)

        decrypted_block = m.to_bytes(chunk_size, 'big')

        original_chunk = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))

        decrypted_data.extend(original_chunk)

        previous_block = block

    return remove_padding(bytes(decrypted_data))