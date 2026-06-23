import os
import math
from src.rsa_math import rsa_encrypt_number, rsa_decrypt_number
from src.padding import get_block_size, add_padding, remove_padding

def ecb_encrypt(data: bytes, public_key: tuple) -> bytes:
    """ Encrypts data using RSA in ECB mode """
    e, n = public_key
    block_size, chunk_size = get_block_size(n)

    padded_data = add_padding(data, chunk_size)

    encrypted_data = bytearray()

    for i in range(0, len(padded_data), chunk_size):
        chunk = padded_data[i:i + chunk_size]

        m = int.from_bytes(chunk, 'big')

        c = rsa_encrypt_number(m, public_key)

        encrypted_data.extend(c.to_bytes(block_size, 'big'))

    return bytes(encrypted_data)

def ecb_decrypt(encrypted_data: bytes, private_key: tuple) -> bytes:
    """ Decrypts data using RSA in ECB mode """
    d, n = private_key
    block_size, chunk_size = get_block_size(n)

    decrypted_data = bytearray()

    for i in range(0, len(encrypted_data), block_size):
        block = encrypted_data[i:i + block_size]

        c = int.from_bytes(block, 'big')

        m = rsa_decrypt_number(c, private_key)

        decrypted_data.extend(m.to_bytes(chunk_size, 'big'))

    return remove_padding(bytes(decrypted_data))