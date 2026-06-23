
import math
import random
import sympy

def generate_keypair(key_size=512):
    print(f"Generating {key_size}-bit RSA keys. This may take a moment...")

    min_key_value = 2 ** (key_size // 2 - 1)
    max_key_value = 2 ** (key_size // 2)

    p = sympy.randprime(min_key_value, max_key_value)
    q = sympy.randprime(min_key_value, max_key_value)

    while p == q:
        q = sympy.randprime(min_key_value, max_key_value)

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537

    if math.gcd(e, phi) != 1:
        while True:
            e = random.randrange(2, phi)
            if math.gcd(e, phi) == 1:
                break

    d = pow(e, -1, phi)

    print("Keys generated successfully!")

    return ((e, n), (d, n))

def rsa_encrypt_number(m: int, public_key: tuple) -> int:
    e, n = public_key
    return pow(m, e, n)

def rsa_decrypt_number(c: int, private_key: tuple) -> int:
    d, n = private_key
    return pow(c, d, n)