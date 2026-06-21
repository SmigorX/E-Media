# src/rsa_math.py

import math
import random
import sympy  # prime numbers generator and utilities

def generate_keypair(key_size=512):
    """
    Generating a pair of RSA keys: (public_key, private_key)
    key_size specifies the total size of the key in bits (e.g., 512, 1024, 2048).
    """
    print(f"Generating {key_size}-bit RSA keys. This may take a moment...")
    
    # 1. Generate two large prime numbers p and q
    # Search for numbers in the range that will give us the desired size in bits
    min_key_value = 2 ** (key_size // 2 - 1)
    max_key_value = 2 ** (key_size // 2)
    
    p = sympy.randprime(min_key_value, max_key_value)
    q = sympy.randprime(min_key_value, max_key_value)
    
    # Check if p and q are the same, chances are low but we want to ensure they are different for security reasons
    while p == q:
        q = sympy.randprime(min_key_value, max_key_value)

    # 2. Calculate the modulus n
    n = p * q

    # 3. Calculate Euler's totient function (phi), which determines the number of integers relatively prime to n
    phi = (p - 1) * (q - 1)

    # 4. Choose the public key 'e' (encryption exponent)
    # In cryptographic practice, the number 65537 is most commonly chosen,
    # its binary representation is (10000000000000001), 
    # which makes it efficient for computation and is also a prime number.
    e = 65537
    
    # Check if 'e' and 'phi' are relatively prime (their Greatest Common Divisor is 1)
    if math.gcd(e, phi) != 1:
        # If not, we randomly choose another 'e' until we find one that works
        while True:
            e = random.randrange(2, phi)
            if math.gcd(e, phi) == 1:
                break

    # 5. Calculate the private key 'd' (decryption exponent)
    # 'd' is the so-called modular multiplicative inverse of 'e' modulo 'phi'.
    # We can calculate it instantly using Python's built-in pow function with three arguments, which computes the modular inverse efficiently.
    d = pow(e, -1, phi)

    print("Keys generated successfully!")

    
    # Return two tuples: Public Key (e, n) and Private Key (d, n)
    return ((e, n), (d, n))

def rsa_encrypt_number(m: int, public_key: tuple) -> int:
    """ Encrypts a single integer (bit block) """
    e, n = public_key
    # Encryption formula: c = m^e (mod n)
    return pow(m, e, n)

def rsa_decrypt_number(c: int, private_key: tuple) -> int:
    """ Decrypts a single integer (bit block) """
    d, n = private_key
    # Decryption formula: m = c^d (mod n)
    return pow(c, d, n)