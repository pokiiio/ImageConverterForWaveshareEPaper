import sys
import colorsys
import epd2in7b
from PIL import Image, ImageOps

E_PAPER_WIDTH = 264
E_PAPER_HEIGHT = 176


def create_resized_image():
    image = Image.open(sys.argv[1])

    if image.size[0] < image.size[1]:
        image = image.rotate(90, expand=True)

    image.thumbnail((E_PAPER_HEIGHT, E_PAPER_HEIGHT), Image.LANCZOS)
    image = image.crop((0, (image.size[1] - E_PAPER_WIDTH) / 2, E_PAPER_HEIGHT,
                        (image.size[1] - E_PAPER_WIDTH) / 2 + E_PAPER_WIDTH))

    image = image.rotate(270, expand=True)
    return image


def create_black_and_red_image(image):
    image = image.convert("RGB")
    black_image = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))
    red_image = Image.new(
        "RGB", (E_PAPER_WIDTH, E_PAPER_HEIGHT), (255, 255, 255))

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b = image.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)

            if (h > 0.85 or h < 0.05) and s > 0.1:
                red_image.putpixel((x, y), (r, g, b))
                black_image.putpixel((x, y), (255, 255, 255))
            else:
                red_image.putpixel((x, y), (255, 255, 255))
                black_image.putpixel((x, y), (r, g, b))

    return black_image, red_image


def show_image(black_image, red_image):
    epd = epd2in13b.EPD()
    epd.init()

    frame_black = epd.get_frame_buffer(black_image)
    frame_red = epd.get_frame_buffer(red_image)
    epd.display_frame(frame_black, frame_red)


if __name__ == '__main__':
    black_image, red_image = create_black_and_red_image(create_resized_image())
    show_image(black_image, red_image)
