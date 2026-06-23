from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5

from src.rsa_math import rsa_encrypt_number, rsa_decrypt_number
from src.png_crypto import encrypt_png

def make_library_primitive(public_key: tuple, private_key: tuple):
    """Return an `(m, public_key) -> c` callable backed by pycryptodome's raw RSA."""
    e, n = public_key
    d, _ = private_key
    lib_key = RSA.construct((n, e, d))
    return lambda m, _pk: lib_key._encrypt(m)

def encrypt_png_with_library(png_bytes: bytes, public_key: tuple,
                             private_key: tuple, mode: str = "ECB") -> bytes:
    fn = make_library_primitive(public_key, private_key)
    return encrypt_png(png_bytes, public_key, mode=mode, encrypt_fn=fn)

def encrypt_pixels_padded_library(pixels: bytes, public_key: tuple,
                                  private_key: tuple,
                                  scheme: str = "pkcs1_v1_5") -> bytes:
    e, n = public_key
    d, _ = private_key
    lib_key = RSA.construct((n, e, d))
    block_size = (n.bit_length() + 7) // 8

    if scheme == "oaep":
        cipher = PKCS1_OAEP.new(lib_key)
        overhead = 2 * 20 + 2
    else:
        cipher = PKCS1_v1_5.new(lib_key)
        overhead = 11

    msg_size = block_size - overhead
    if msg_size < 1:
        raise ValueError("Key too small for this padding scheme; use --bits 1024.")

    out = bytearray()
    for i in range(0, len(pixels), msg_size):
        out += cipher.encrypt(pixels[i:i + msg_size])
    return bytes(out)

def run_library_comparison(public_key: tuple, private_key: tuple) -> str:
    e, n = public_key
    d, _ = private_key

    lib_key = RSA.construct((n, e, d))

    lines = []
    lines.append("=" * 60)
    lines.append("COMPARISON WITH A READY-MADE RSA LIBRARY (pycryptodome)")
    lines.append("=" * 60)
    lines.append(f"shared modulus n bit-length : {n.bit_length()}")
    lines.append("")

    m = 0x4D6564696120524141
    if m >= n:
        m = m % n
    ours = rsa_encrypt_number(m, public_key)
    theirs = lib_key._encrypt(m)
    lines.append("1) Raw textbook primitive  c = m^e mod n")
    lines.append(f"   our    c = {hex(ours)[:42]}...")
    lines.append(f"   library c = {hex(theirs)[:42]}...")
    lines.append(f"   identical?                 : {ours == theirs}")
    lines.append(f"   our decrypt recovers m?    : {rsa_decrypt_number(ours, private_key) == m}")
    lines.append("")

    lines.append("2) Production scheme  PKCS#1 OAEP (same key pair)")
    cipher = PKCS1_OAEP.new(lib_key)
    msg = b"Media RAA"
    c1 = cipher.encrypt(msg)
    c2 = cipher.encrypt(msg)
    lines.append(f"   OAEP(msg) run #1 : {c1.hex()[:40]}...")
    lines.append(f"   OAEP(msg) run #2 : {c2.hex()[:40]}...")
    lines.append(f"   two runs identical?        : {c1 == c2}  "
                 f"(False -> randomised, unlike textbook RSA)")
    recovered = cipher.decrypt(c2)
    lines.append(f"   OAEP decrypt recovers msg? : {recovered == msg}")
    lines.append("")
    lines.append("WHY THE DIFFERENCE:")
    lines.append("  Our ECB/CBC modes use *textbook* RSA: deterministic, so equal")
    lines.append("  blocks -> equal ciphertext (the ECB pattern). Real libraries add")
    lines.append("  randomised padding (OAEP), making encryption non-deterministic and")
    lines.append("  semantically secure - no visible structure survives.")
    lines.append("=" * 60)
    return "\n".join(lines)
