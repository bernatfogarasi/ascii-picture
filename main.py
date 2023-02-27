import math
import os
import time

from PIL import Image


def convert_image_to_ascii(image, character_set, invert):
    pixels = image.load()
    width, height = image.size
    character_pixels = []
    for row in range(height):
        character_pixels.append([])
        for column in range(width):
            pixel = pixels[column, row]
            luminance = calculate_perceived_luminance(pixel, invert)
            character = get_character_by_luminance(luminance, character_set)
            character_pixels[-1].append(character)
    return character_pixels


def calculate_perceived_luminance(pixel, invert):
    r, g, b = pixel
    # https://www.w3.org/TR/AERT/#color-contrast
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    if invert:
        luminance = 255 - luminance
    return luminance


def get_character_by_luminance(luminance, character_set):
    return character_set[math.ceil(luminance / 255 * len(character_set)) - 1]


def write_character_pixels(file_name, character_pixels):
    with open(file_name, "w") as file:
        file.write("\n".join("".join(row) for row in character_pixels))


def resize_image(image, resolution, vertical_scale):
    width, height = image.size
    image = image.resize([width, int(height * vertical_scale)])
    width, height = image.size
    scale = resolution / max(width, height)
    image = image.resize([int(width * scale), int(height * scale)])
    return image


def open_image(image_source):
    return Image.open(image_source).convert("RGB")


def main():
    CHARACTER_SETS = [
        # https://stackoverflow.com/a/67780964
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.",
        # https://stackoverflow.com/a/30098597
        "WKli:,. ",
        "WXx=*°'",
        "WXI=,.",
        "W6O/=-. ",
    ]
    IMAGE_SOURCE = "mona_lisa.jpg"
    RESOLUTION = 100  # maximum number of characters in a row or column
    CHARACTER_SET_INDEX = 3  # see sets above
    INVERT = True  # if true, than lighter parts are displayed denser
    VERTICAL_SCALE = 0.4  # adjust to font-family and line-spacing

    print("Processing...")
    image = resize_image(open_image(IMAGE_SOURCE), RESOLUTION, VERTICAL_SCALE)
    character_set = CHARACTER_SETS[CHARACTER_SET_INDEX]
    character_pixels = convert_image_to_ascii(image, character_set, INVERT)
    file_name = f"{os.path.splitext(IMAGE_SOURCE)[0]}_{round(time.time())}.txt"
    write_character_pixels(file_name, character_pixels)
    print("Created ascii image in", file_name)


if __name__ == "__main__":
    main()
