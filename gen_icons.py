"""Generate ATHLETICS app icons (volt lightning bolt on obsidian) as raw PNGs — no dependencies."""
import struct, zlib

def png_bytes(w, h, rows):
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    raw = b''.join(b'\x00' + b''.join(bytes(p) for p in row) for row in rows)
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9))
            + chunk(b'IEND', b''))

BOLT = [(0.575, 0.06), (0.22, 0.56), (0.455, 0.56), (0.395, 0.94), (0.80, 0.42), (0.525, 0.42)]

def inside(x, y, poly):
    n = len(poly); j = n - 1; c = False
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c

def make(size, name):
    bg, fg = (11, 11, 12), (204, 255, 0)
    ss = 3 if size <= 192 else 2
    rows = []
    for py in range(size):
        row = []
        for px in range(size):
            hits = 0
            for sy in range(ss):
                for sx in range(ss):
                    x = (px + (sx + .5) / ss) / size
                    y = (py + (sy + .5) / ss) / size
                    if inside(x, y, BOLT):
                        hits += 1
            a = hits / (ss * ss)
            row.append(tuple(int(bg[i] + (fg[i] - bg[i]) * a) for i in range(3)))
        rows.append(row)
    with open(name, 'wb') as f:
        f.write(png_bytes(size, size, rows))
    print('wrote', name)

for s, n in [(180, 'icon-180.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    make(s, n)
