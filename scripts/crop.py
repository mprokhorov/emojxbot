import io
import math
from itertools import product

from PIL import Image


def split_static_image(image):
    w, h = image.size
    d = 100
    if w % 100 != 0 or h % 100 != 0:
        new_w = math.ceil(w / 100.) * 100
        new_h = math.ceil(h / 100.) * 100
        img = Image.new('RGBA', (new_w, new_h), (255, 0, 0, 0))
        back_im = img.copy()
        back_im.paste(image, ((new_w - w) // 2, (new_h - h) // 2))
        image = back_im
        w = new_w
        h = new_h
    grid = product(range(0, h, d), range(0, w, d))
    tiles = []
    for i, j in grid:
        result = image.crop((j, i, j + d, i + d))
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        buf.seek(0)
        tiles.append(buf.getvalue())
    return tiles
