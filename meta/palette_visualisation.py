import json
from PIL import Image, ImageColor
from math import floor, ceil, sqrt


with open("palette.json", "r") as palette:
    colors = json.load(palette)

with open("files_by_color.json", "r") as files_by_color_input:
    files_by_color = json.load(files_by_color_input)


colors.sort()
cutoff = 10  # colors must appear in this many emoji (removes a lot of flag specific colors)
colors = [color for color in colors if len(files_by_color[color]) >= cutoff]

num_colors = len(colors)
width = floor(sqrt(num_colors))
height = ceil(num_colors/float(width))

palette_image = Image.new("RGB", (width, height))

color_data = [ImageColor.getrgb(color) for color in colors]
palette_image.putdata(color_data)

image_scale = 100
palette_image = palette_image.resize((width * image_scale, height * image_scale), Image.NEAREST)
palette_image.show()
