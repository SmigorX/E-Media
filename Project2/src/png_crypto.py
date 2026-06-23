from src.png_pixels import PngImage
from src.image_cipher import (
    encrypt_pixels, decrypt_pixels, MODE_ECB, MODE_CBC,
)

ANCILLARY_TYPE = "rsAe"
_MAGIC = b"RSAX"
_MODE_CODE = {MODE_ECB: 0, MODE_CBC: 1}
_MODE_NAME = {0: MODE_ECB, 1: MODE_CBC}

def _pack_meta(enc, orig_len: int, tail: bytes) -> bytes:
    out = bytearray(_MAGIC)
    out.append(1)
    out.append(_MODE_CODE[enc.mode])
    out += enc.chunk_size.to_bytes(4, "big")
    out += enc.block_size.to_bytes(4, "big")
    out += orig_len.to_bytes(8, "big")
    out += enc.pad.to_bytes(4, "big")
    num_blocks = len(enc.overflow)
    out += num_blocks.to_bytes(8, "big")
    out += len(enc.iv).to_bytes(4, "big") + enc.iv
    out += len(tail).to_bytes(4, "big") + tail
    out += enc.overflow
    return bytes(out)

def _unpack_meta(data: bytes) -> dict:
    if data[:4] != _MAGIC:
        raise ValueError("rsAe chunk has a bad magic; file not encrypted by us.")
    p = 5
    mode = _MODE_NAME[data[p]]; p += 1
    chunk_size = int.from_bytes(data[p:p + 4], "big"); p += 4
    block_size = int.from_bytes(data[p:p + 4], "big"); p += 4
    orig_len = int.from_bytes(data[p:p + 8], "big"); p += 8
    pad = int.from_bytes(data[p:p + 4], "big"); p += 4
    num_blocks = int.from_bytes(data[p:p + 8], "big"); p += 8
    iv_len = int.from_bytes(data[p:p + 4], "big"); p += 4
    iv = data[p:p + iv_len]; p += iv_len
    tail_len = int.from_bytes(data[p:p + 4], "big"); p += 4
    tail = data[p:p + tail_len]; p += tail_len
    overflow = data[p:p + num_blocks]
    return {
        "mode": mode, "chunk_size": chunk_size, "block_size": block_size,
        "orig_len": orig_len, "pad": pad, "iv": iv, "tail": tail,
        "overflow": overflow,
    }

def encrypt_png(png_bytes: bytes, public_key: tuple, mode: str = MODE_ECB,
                iv: bytes = None, encrypt_fn=None) -> bytes:
    img = PngImage(png_bytes)
    pixels = img.get_pixel_data()
    orig_len = len(pixels)

    enc = encrypt_pixels(pixels, public_key, mode, iv, encrypt_fn=encrypt_fn)

    image_pixels = enc.low[:orig_len]
    tail = enc.low[orig_len:]

    meta = _pack_meta(enc, orig_len, tail)
    return img.rebuild_with_pixels(image_pixels,
                                   extra_chunks=[(ANCILLARY_TYPE, meta)])

def decrypt_png(png_bytes: bytes, private_key: tuple) -> bytes:
    img = PngImage(png_bytes)
    raw_meta = img.get_ancillary(ANCILLARY_TYPE)
    if raw_meta is None:
        raise ValueError("No rsAe chunk found - is this an encrypted PNG?")
    m = _unpack_meta(raw_meta)

    image_pixels = img.get_pixel_data()
    low = image_pixels + m["tail"]

    pixels = decrypt_pixels(
        low, m["overflow"], private_key, m["mode"], m["iv"],
        m["pad"], m["chunk_size"],
    )
    img.chunks = [c for c in img.chunks if c["type"] != ANCILLARY_TYPE]
    return img.rebuild_with_pixels(pixels, extra_chunks=None)
