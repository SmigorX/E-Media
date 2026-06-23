import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}

class PngImage:
    """Parsed PNG: the ordered list of chunks plus IHDR geometry."""

    def __init__(self, raw: bytes):
        if raw[:8] != PNG_SIGNATURE:
            raise ValueError("Not a PNG file (bad signature).")
        self.signature = raw[:8]
        self.chunks = _split_chunks(raw)

        ihdr = self._chunk_data("IHDR")
        self.width = int.from_bytes(ihdr[0:4], "big")
        self.height = int.from_bytes(ihdr[4:8], "big")
        self.bit_depth = ihdr[8]
        self.color_type = ihdr[9]
        self.interlace = ihdr[12]
        if self.interlace != 0:
            raise ValueError("Interlaced PNGs (Adam7) are not supported.")

        channels = _CHANNELS[self.color_type]
        bits_per_pixel = self.bit_depth * channels
        self.bpp = max(1, bits_per_pixel // 8)
        self.stride = (self.width * bits_per_pixel + 7) // 8

    def _chunk_data(self, ctype: str) -> bytes:
        for c in self.chunks:
            if c["type"] == ctype:
                return c["data"]
        raise ValueError(f"Missing {ctype} chunk.")

    def get_compressed_idat(self) -> bytes:
        return b"".join(c["data"] for c in self.chunks if c["type"] == "IDAT")

    def get_pixel_data(self) -> bytes:
        decompressed = zlib.decompress(self.get_compressed_idat())
        return _defilter(decompressed, self.height, self.stride, self.bpp)

    def rebuild_with_pixels(self, pixel_data: bytes, extra_chunks=None) -> bytes:
        filtered = _refilter_none(pixel_data, self.height, self.stride)
        new_idat = zlib.compress(filtered, level=9)

        out = bytearray(self.signature)
        wrote_idat = False
        for c in self.chunks:
            if c["type"] == "IDAT":
                if not wrote_idat:
                    out += _make_chunk("IDAT", new_idat)
                    wrote_idat = True
                continue
            if c["type"] == "IEND"::
                for etype, edata in (extra_chunks or []):
                    out += _make_chunk(etype, edata)
            out += _make_chunk(c["type"], c["data"])
        return bytes(out)

    def get_ancillary(self, ctype: str):
        for c in self.chunks:
            if c["type"] == ctype:
                return c["data"]
        return None

def _split_chunks(raw: bytes) -> list:
    chunks = []
    cursor = 8
    while cursor < len(raw):
        length = int.from_bytes(raw[cursor:cursor + 4], "big")
        ctype = raw[cursor + 4:cursor + 8].decode("ascii")
        data = raw[cursor + 8:cursor + 8 + length]
        chunks.append({"type": ctype, "data": data})
        cursor += 12 + length
        if ctype == "IEND":
            break
    return chunks

def _make_chunk(ctype: str, data: bytes) -> bytes:
    type_bytes = ctype.encode("ascii")
    crc = zlib.crc32(type_bytes + data) & 0xFFFFFFFF
    return (
        len(data).to_bytes(4, "big")
        + type_bytes
        + data
        + crc.to_bytes(4, "big")
    )

def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c

def _defilter(data: bytes, height: int, stride: int, bpp: int) -> bytes:
    out = bytearray()
    prev = bytearray(stride)
    pos = 0
    for _ in range(height):
        ftype = data[pos]
        pos += 1
        line = bytearray(data[pos:pos + stride])
        pos += stride
        if ftype == 0:
            pass
        elif ftype == 1:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + a) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                c = prev[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + _paeth(a, prev[i], c)) & 0xFF
        else:
            raise ValueError(f"Unknown PNG filter type {ftype}.")
        out += line
        prev = line
    return bytes(out)

def _refilter_none(pixel_data: bytes, height: int, stride: int) -> bytes:
    out = bytearray()
    for r in range(height):
        out.append(0)
        out += pixel_data[r * stride:(r + 1) * stride]
    return bytes(out)
