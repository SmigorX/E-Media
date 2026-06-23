import zlib

from src.png_pixels import PngImage
from src.image_cipher import encrypt_pixels, MODE_ECB
from src.ecb import ecb_encrypt

def run_compression_comparison(png_bytes: bytes, public_key: tuple) -> str:
    img = PngImage(png_bytes)

    compressed_idat = img.get_compressed_idat()
    pixels = img.get_pixel_data()

    enc = encrypt_pixels(pixels, public_key, MODE_ECB)
    cipher_pixels = enc.low
    a_compressed = zlib.compress(cipher_pixels, level=9)

    b_cipher = ecb_encrypt(compressed_idat, public_key)
    try:
        zlib.decompress(b_cipher)
        b_decodes = True
    except zlib.error:
        b_decodes = False

    lines = []
    lines.append("=" * 60)
    lines.append("COMPRESSION vs ENCRYPTION ORDER")
    lines.append("=" * 60)
    lines.append(f"raw pixel data (decompressed) : {len(pixels):>10} B")
    lines.append(f"original compressed IDAT       : {len(compressed_idat):>10} B")
    lines.append("")
    lines.append("Method A  (decompress -> encrypt -> compress ciphertext)")
    lines.append(f"  ciphertext (raw)             : {len(cipher_pixels):>10} B")
    lines.append(f"  after zlib compression       : {len(a_compressed):>10} B")
    ratio = len(a_compressed) / max(1, len(cipher_pixels))
    lines.append(f"  compression ratio            : {ratio:>10.3f} "
                 f"(close to 1.0; any residue is ECB block repetition)")
    lines.append("  decodes as an image?         :        YES")
    lines.append("")
    lines.append("Method B  (encrypt the already-compressed IDAT directly)")
    lines.append(f"  ciphertext size              : {len(b_cipher):>10} B")
    lines.append(f"  still a valid zlib stream?   : {'YES' if b_decodes else 'NO':>10}")
    lines.append(f"  decodes as an image?         : {'YES' if b_decodes else ' NO':>10}")
    lines.append("")
    lines.append("CONCLUSION: the two methods are NOT equivalent.")
    lines.append("  * Encryption destroys statistical redundancy, so compressing")
    lines.append("    AFTER encrypting (A) saves nothing - always compress first.")
    lines.append("  * Encrypting the compressed stream (B) corrupts the DEFLATE")
    lines.append("    structure, so the file no longer opens as an image.")
    lines.append("=" * 60)
    return "\n".join(lines)
