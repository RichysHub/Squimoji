from lxml import etree
import subprocess
import tempfile
import os
import sys

template_path = "./tweet_template.svg"
svg_directory = "../../svg/"
out_directory = os.path.dirname(sys.argv[0]) + "/"
inkscape_executable = "C:/Program Files/Inkscape/inkscape.exe"

# SVG namespace
SVGNS = u"http://www.w3.org/2000/svg"


def create_tweet_image(character_name, background_color_override=None, text_color_override=None):

    in_svg_path = os.path.join(svg_directory, character_name + ".svg")

    with open(in_svg_path, "r") as in_svg:
        character_data = in_svg.read()

    character = etree.fromstring(character_data)
    template = etree.parse(template_path)

    # obtain the container element
    emoji_container = template.find(".//{%s}g[@id='emoji_container']" % SVGNS)
    # insert our emoji into the container
    emoji_container.extend(list(character))

    if background_color_override is not None:
        background = template.find(".//{%s}rect[@id='background']" % SVGNS)
        background.attrib["fill"] = background_color_override

    if text_color_override is not None:
        text_container = template.find(".//{%s}g[@id='text_container']" % SVGNS)
        text_container.attrib["fill"] = text_color_override

    temp_svg = tempfile.NamedTemporaryFile(delete=False)
    template.write(temp_svg)
    temp_svg.close()

    out_path = os.path.join(out_directory, character_name + "_tweet.png")

    subprocess.call([inkscape_executable, temp_svg.name,
                     '--export-png={}'.format(out_path)])

    # os.unlink(temp_svg.name)

emojis = ["1f0cf"]
# don't forget #s
colors = ["#9266CC"]
text_colors = [None]
for emoji, color, text_color in zip(emojis, colors, text_colors):
    create_tweet_image(emoji, color, text_color)
