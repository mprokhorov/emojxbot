import os
from math import floor, fabs
from PIL import Image, ImageSequence
from itertools import product


def split_static_image(image, name, ext):
    w, h = image.size
    d = 100
    grid = product(range(0, h, 100), range(0, w, 100))

    def crop_image(original_img, left, top, right, bottom):
        img_w, img_h = (original_img.size[0], original_img.size[1])
        return original_img.crop((left, top, right, bottom))

    for i, j in grid:
        result = crop_image(image, j, i, j + d, i + d)
        n_frames = getattr(img, 'n_frames', 1)
        result.save(f'{name}{i}_{j}.{ext}')


def split_multi_frame_image(image, name, ext):
    w, h = image.size
    d = 100
    grid = product(range(0, h, 100), range(0, w, 100))

    def crop_image(original_img, left, top, right, bottom):
        img_w, img_h = (original_img.size[0], original_img.size[1])
        frames = []
        for frame_ in ImageSequence.Iterator(original_img):
            frames.append(frame_.crop((left, top, right, bottom)))
        return frames

    for i, j in grid:
        result = crop_image(image, j, i, j + d, i + d)
        n_frames = getattr(img, 'n_frames', 1)
        result[0].save(f'{name}{i}_{j}.{ext}', save_all=True, append_images=result[1:], optimize=False, loop=0)


if __name__ == '__main__':
    img = Image.open('chicken.png')
    split_static_image(img, 'out/chicken_split', 'png')
