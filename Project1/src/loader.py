def _read_image_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def _verify_png(image_bytes: bytes) -> bool:
    png_signature = b'\x89PNG\r\n\x1a\n'
    return image_bytes[:8] == png_signature

def load_png_image(image_path: str) -> bytes:
    image_bytes = _read_image_bytes(image_path)
    if not _verify_png(image_bytes):
        raise ValueError("The provided file is not a valid PNG image.")
    return image_bytes