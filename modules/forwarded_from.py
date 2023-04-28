import math

from PIL import Image


def resize_forwarded_from(res_path, save_as):
    target_w = 320
    target_h = 60

    fs = []
    for i in range(136):
        fs.append(Image.open(f"modules/frames/frame_{str(i).zfill(3)}_delay-0.04s.png"))
    vadim = Image.open(res_path)
    w, h = vadim.size
    vadimRGB = vadim.convert("RGB")
    r, g, b = vadimRGB.getpixel((0, h / 2))
    flag = True
    if w < target_w or h < target_h:
        width_M = target_w / w
        height_M = target_h / h
        if width_M >= height_M:
            new_vadim = vadim.resize((math.ceil(w * height_M), 60))
        else:
            new_vadim = vadim.resize((320, math.ceil(h * width_M)))
            flag = False
    else:
        return None
    # todo
    new_frames = []
    for frame_ in fs:
        img = Image.new("RGB", (320, 240), (r, g, b))
        img.paste(frame_, (0, 0))
        if flag:
            img.paste(new_vadim, ((320 - math.ceil(w * height_M)) // 2, 180))
        else:
            img.paste(new_vadim, (0, 180 + (60 - math.ceil(h * width_M)) // 2))
        new_frames.append(img)
    new_frames[0].save(save_as, save_all=True, duration=40, loop=0, append_images=new_frames[1:])
