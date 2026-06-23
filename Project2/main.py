"""
E-media — projekt 2 : RSA encryption of PNG multimedia files.

Sub-commands
------------
  genkey   <key.json> [--bits N]
  encrypt  <in.png> <out.png> --key <key.json> [--mode ECB|CBC]
  decrypt  <in.png> <out.png> --key <key.json>
  demo     <in.png> [--bits N] [--outdir DIR]      full end-to-end showcase
  selftest                                         quick byte-level ECB/CBC check
"""

import argparse
import os

from src.rsa_math import (
    generate_keypair, rsa_encrypt_number, rsa_decrypt_number,
)
from src.keystore import save_keys, load_keys
from src.png_crypto import encrypt_png, decrypt_png
from src.image_cipher import MODE_ECB, MODE_CBC
from src.compression_test import run_compression_comparison
from src.library_compare import (
    run_library_comparison, encrypt_png_with_library,
    encrypt_pixels_padded_library,
)
from src.png_pixels import PngImage
from src.ecb import ecb_encrypt, ecb_decrypt
from src.cbc import cbc_encrypt, cbc_decrypt

def _read(path):
    with open(path, "rb") as f:
        return f.read()

def _write(path, data):
    with open(path, "wb") as f:
        f.write(data)

def _pixel_delta(png_a: bytes, png_b: bytes):
    pa = PngImage(png_a).get_pixel_data()
    pb = PngImage(png_b).get_pixel_data()
    delta = bytes(abs(x - y) for x, y in zip(pa, pb))
    return delta, (max(delta) if delta else 0)

def _save_delta_png(template_png: bytes, delta_pixels: bytes, path: str):
    tpl = PngImage(template_png    """ Decrypts a single integer (bit block) """)
    tpl.chunks = [c for c in tpl.chunks if c["type"] != "rsAe"]
    _write(path, tpl.rebuild_with_pixels(delta_pixels))

def cmd_genkey(args):
    pub, priv = generate_keypair(key_size=args.bits)
    save_keys(args.keyfile, pub, priv)
    print(f"Saved {args.bits}-bit key pair to {args.keyfile}")

def cmd_encrypt(args):
    pub, _ = load_keys(args.key)
    mode = MODE_CBC if args.mode.upper() == "CBC" else MODE_ECB
    out = encrypt_png(_read(args.infile), pub, mode=mode)
    _write(args.outfile, out)
    print(f"Encrypted ({mode}) -> {args.outfile}")

def cmd_decrypt(args):
    _, priv = load_keys(args.key)
    out = decrypt_png(_read(args.infile), priv)
    _write(args.outfile, out)
    print(f"Decrypted -> {args.outfile}")

def cmd_selftest(args):
    print("=== BYTE-LEVEL ECB/CBC SELF-TEST ===")
    pub, priv = generate_keypair(key_size=256)
    data = b"To jest tajna wiadomosc testowa dla naszego RSA!"

    enc = ecb_encrypt(data, pub)
    ok_ecb = ecb_decrypt(enc, priv) == data
    print(f"ECB round-trip ok? {ok_ecb}")

    enc, iv = cbc_encrypt(data, pub)
    ok_cbc = cbc_decrypt(enc, priv, iv) == data
    print(f"CBC round-trip ok? {ok_cbc}")

def cmd_demo(args):
    src = args.infile
    outdir = args.outdir or os.path.dirname(os.path.abspath(src))
    os.makedirs(outdir, exist_ok=True)

    print(f"Input image : {src}")
    print(f"Output dir  : {outdir}\n")

    pub, priv = generate_keypair(key_size=args.bits)
    keyfile = os.path.join(outdir, "demo_key.json")
    save_keys(keyfile, pub, priv)

    original = _read(src)
    orig_pixels = PngImage(original).get_pixel_data()

    encrypted = {}
    decrypted = {}
    for mode in (MODE_ECB, MODE_CBC):
        enc_path = os.path.join(outdir, f"encrypted_{mode.lower()}.png")
        dec_path = os.path.join(outdir, f"decrypted_{mode.lower()}.png")

        enc = encrypt_png(original, pub, mode=mode)
        _write(enc_path, enc)
        encrypted[mode] = enc

        dec = decrypt_png(enc, priv)
        _write(dec_path, dec)
        decrypted[mode] = dec

        same = orig_pixels == PngImage(dec).get_pixel_data()
        print(f"[{mode}] encrypted -> {os.path.basename(enc_path)}, "
              f"decrypted -> {os.path.basename(dec_path)}, "
              f"pixels lossless? {same}")

    print("\nOpen encrypted_ecb.png vs encrypted_cbc.png:")
    print("  ECB keeps equal blocks equal -> object outline stays visible.")
    print("  CBC chains blocks -> output looks like uniform noise.")

    d_dec, max_dec = _pixel_delta(decrypted[MODE_ECB], decrypted[MODE_CBC])
    _save_delta_png(original, d_dec,
                    os.path.join(outdir, "delta_decrypted_ecb_vs_cbc.png"))
    print(f"\n[delta] decrypted ECB vs decrypted CBC : max |diff| = {max_dec} "
          f"({'identical -> both recover the original' if max_dec == 0 else 'MISMATCH!'})")

    lib_enc = encrypt_png_with_library(original, pub, priv, mode="ECB")
    _write(os.path.join(outdir, "encrypted_ecb_library.png"), lib_enc)
    d_lib, max_lib = _pixel_delta(encrypted[MODE_ECB], lib_enc)
    _save_delta_png(original, d_lib,
                    os.path.join(outdir, "delta_ours_vs_library_ecb.png"))
    print("\n[library, raw primitive m^e mod n] same key pair:")
    print(f"  ours      -> encrypted_ecb.png")
    print(f"  library   -> encrypted_ecb_library.png")
    print(f"  delta     -> delta_ours_vs_library_ecb.png : max |diff| = {max_lib} "
          f"({'byte-identical -> our RSA == reference RSA' if max_lib == 0 else 'differ'})")

    orig_len = len(orig_pixels)
    pad_stream = encrypt_pixels_padded_library(orig_pixels, pub, priv,
                                               scheme="pkcs1_v1_5")
    pad_pixels = pad_stream[:orig_len].ljust(orig_len, b"\x00")
    _save_delta_png(original, pad_pixels,
                    os.path.join(outdir, "encrypted_ecb_library_padded.png"))

    our_ecb_pixels = PngImage(encrypted[MODE_ECB]).get_pixel_data()
    d_pad = bytes(abs(x - y) for x, y in zip(our_ecb_pixels, pad_pixels))
    max_pad = max(d_pad)
    differing = sum(1 for v in d_pad if v) / len(d_pad) * 100
    _save_delta_png(original, d_pad,
                    os.path.join(outdir, "delta_ours_vs_library_padded.png"))
    print("\n[library, PKCS#1 v1.5 padding] same key pair:")
    print(f"  library   -> encrypted_ecb_library_padded.png  "
          f"(expanded: {len(pad_stream)} B vs {orig_len} B pixels)")
    print(f"  delta     -> delta_ours_vs_library_padded.png : max |diff| = {max_pad}, "
          f"{differing:.1f}% of pixels differ")
    print("  -> padding randomises every block, so the result shares NOTHING with")
    print("     our textbook RSA (and re-running it changes again).")

    print()
    print(run_compression_comparison(original, pub))
    print()
    print(run_library_comparison(pub, priv))

def build_parser():
    p = argparse.ArgumentParser(description="RSA encryption of PNG files.")
    sub = p.add_subparsers(dest="command", required=True)

    g = sub.add_parser("genkey", help="generate and save an RSA key pair")
    g.add_argument("keyfile")
    g.add_argument("--bits", type=int, default=512)
    g.set_defaults(func=cmd_genkey)

    e = sub.add_parser("encrypt", help="encrypt a PNG's pixel data")
    e.add_argument("infile"); e.add_argument("outfile")
    e.add_argument("--key", required=True)
    e.add_argument("--mode", default="ECB", choices=["ECB", "CBC", "ecb", "cbc"])
    e.set_defaults(func=cmd_encrypt)

    d = sub.add_parser("decrypt", help="decrypt a PNG encrypted by us")
    d.add_argument("infile"); d.add_argument("outfile")
    d.add_argument("--key", required=True)
    d.set_defaults(func=cmd_decrypt)

    dm = sub.add_parser("demo", help="full end-to-end demonstration")
    dm.add_argument("infile")
    dm.add_argument("--bits", type=int, default=512)
    dm.add_argument("--outdir", default=None)
    dm.set_defaults(func=cmd_demo)

    st = sub.add_parser("selftest", help="quick byte-level ECB/CBC check")
    st.set_defaults(func=cmd_selftest)

    return p

def main():
    args = build_parser().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
