from PIL import Image


def resize_and_overlay(text_path, image_path, result_path):
    text_image = Image.open(text_path).convert("RGBA")
    image = Image.open(image_path).convert("RGBA")
    image_width, image_height = image.size
    new_size = min(image_width, image_height)
    text_image = text_image.resize((new_size, new_size))
    x_offset = (image_width - new_size) // 2
    y_offset = (image_height - new_size) // 2
    result_image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    result_image.paste(image, (0, 0))
    result_image.paste(text_image, (x_offset, y_offset), text_image)
    result_image.save(result_path)
