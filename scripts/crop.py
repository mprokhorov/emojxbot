import io

from itertools import product


def split_static_image(image):
    w, h = image.size
    d = 100
    grid = product(range(0, h, d), range(0, w, d))
    tiles = []
    for i, j in grid:
        result = image.crop((j, i, j + d, i + d))
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        buf.seek(0)
        tiles.append(buf.getvalue())
    return tiles


# def split_multi_frame_image(image, name, ext):
#     w, h = image.size
#     d = 100
#     grid = product(range(0, h, 100), range(0, w, 100))
#
#     def crop_image(original_img, left, top, right, bottom):
#         frames = []
#         for frame_ in ImageSequence.Iterator(original_img):
#             frames.append(frame_.crop((left, top, right, bottom)))
#         return frames
#
#     for i, j in grid:
#         result = crop_image(image, j, i, j + d, i + d)
#         result[0].save(f'{name}{i}_{j}.{ext}', save_all=True, append_images=result[1:], optimize=False, loop=0)
