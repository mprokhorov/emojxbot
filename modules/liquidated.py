from PIL import Image

def resize_and_overlay(text_path, image_path, result_path):
    # Open the images
    text_image = Image.open(text_path).convert("RGBA")
    image = Image.open(image_path).convert("RGBA")

    # Get the dimensions of the image
    image_width, image_height = image.size

    # Resize the text image to match the shortest side of the image
    new_size = min(image_width, image_height)
    text_image = text_image.resize((new_size, new_size))

    # Calculate the position to center the text image
    x_offset = (image_width - new_size) // 2
    y_offset = (image_height - new_size) // 2

    # Create a new image with the same size as the background image
    result_image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))

    # Paste the background image onto the result image
    result_image.paste(image, (0, 0))

    # Paste the resized text image onto the result image
    result_image.paste(text_image, (x_offset, y_offset), text_image)

    # Save the result image
    result_image.save(result_path)
