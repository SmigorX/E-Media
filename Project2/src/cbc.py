import os
import math
from src.rsa_math import rsa_encrypt_number, rsa_decrypt_number
from src.padding import get_block_size, add_padding, remove_padding

def cbc_encrypt(data: bytes, public_key: tuple, iv: bytes = None) -> tuple[bytes, bytes]:
    """ Encrypts data using RSA in CBC mode """
    e, n = public_key
    block_size, chunk_size = get_block_size(n)
    
    # Add padding to the data
    padded_data = add_padding(data, chunk_size)
    
    # Generate a random IV if not provided
    if iv is None:
        iv = os.urandom(chunk_size)
    
    encrypted_data = bytearray()
    previous_block = iv
    
    # Process each chunk of data
    for i in range(0, len(padded_data), chunk_size):
        chunk = padded_data[i:i + chunk_size]

        # XOR the current chunk with the previous block (or IV for the first block)
        xor_chunk = bytes(a ^ b for a, b in zip(chunk, previous_block))

        # Convert the XORed chunk to an integer
        m = int.from_bytes(xor_chunk, 'big')

        # Encrypt the integer using RSA
        c = rsa_encrypt_number(m, public_key)

        # Convert the encrypted integer back to bytes and append it to the result
        encrypted_block = c.to_bytes(block_size, 'big')
        encrypted_data.extend(encrypted_block)

        # Update the previous block to be the current encrypted block
        previous_block = encrypted_block
    
    return bytes(encrypted_data), iv

def cbc_decrypt(data: bytes, private_key: tuple, iv: bytes) -> bytes:
    """ Decrypts data using RSA in CBC mode """
    d, n = private_key
    block_size, chunk_size = get_block_size(n)
    
    decrypted_data = bytearray()
    previous_block = iv
    
    # Process each block of encrypted data
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]

        # Convert the block to an integer
        c = int.from_bytes(block, 'big')

        # Decrypt the integer using RSA
        m = rsa_decrypt_number(c, private_key)

        # Convert the decrypted integer back to bytes
        decrypted_block = m.to_bytes(chunk_size, 'big')

        # XOR the decrypted block with the previous block (or IV for the first block)
        original_chunk = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))

        # Append the original chunk to the result
        decrypted_data.extend(original_chunk)

        # Update the previous block to be the current encrypted block
        previous_block = block
    
    # Remove padding from the decrypted data
    return remove_padding(bytes(decrypted_data))