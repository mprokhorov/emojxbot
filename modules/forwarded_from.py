import math

from PIL import Image


def resize_and_overlay(res_path, save_as):
    target_w = 320
    target_h = 60
    source_gif_frames = []
    for i in range(136):
        source_gif_frames.append(Image.open(f'modules/frames/frame_{str(i).zfill(3)}_delay-0.04s.png'))
    lower_image = Image.open(res_path)
    w, h = lower_image.size
    lower_image_RGB = lower_image.convert('RGB')
    r, g, b = lower_image_RGB.getpixel((0, h // 2))
    flag = True
    if w < target_w or h < target_h:
        width_M = target_w / w
        height_M = target_h / h
        if width_M >= height_M:
            new_vadim = lower_image.resize((math.ceil(w * height_M), 60))
        else:
            new_vadim = lower_image.resize((320, math.ceil(h * width_M)))
            flag = False
    else:
        lower_image = lower_image.resize((lower_image.width // 2, lower_image.height // 2))
        width_M = target_w / w
        height_M = target_h / h
        if width_M >= height_M:
            new_vadim = lower_image.resize((math.ceil(w * height_M), 60))
        else:
            new_vadim = lower_image.resize((320, math.ceil(h * width_M)))
            flag = False
    output_gif_frames = []
    for output_gif_frame in source_gif_frames:
        img = Image.new('RGB', (320, 240), (r, g, b))
        img.paste(output_gif_frame, (0, 0))
        if flag:
            img.paste(new_vadim, ((320 - math.ceil(w * height_M)) // 2, 180))
        else:
            img.paste(new_vadim, (0, 180 + (60 - math.ceil(h * width_M)) // 2))
        output_gif_frames.append(img)
    output_gif_frames[0].save(save_as, save_all=True, duration=40, loop=0, append_images=output_gif_frames[1:])
