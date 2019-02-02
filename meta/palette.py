import os
import re
import json

from collections import defaultdict


# simple encoder that renders sets as lists
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


# point to svg folder of Twemoji's version 2 assets
source_dir_string = "../../Twemoji/2/svg/"
source_dir = os.fsencode(source_dir_string)

color_regex = "#[\da-fA-f]+"

found_colors = set()
files_by_color = defaultdict(set)
colors_by_file = defaultdict(set)

for file in os.listdir(source_dir):
    filename = os.fsdecode(file)
    if filename.endswith(".svg"):
        with open(os.path.join(source_dir_string, filename), "r") as svg:
            data = svg.read()
            colors = re.findall(color_regex, data)
            for color in colors:
                found_colors.add(color)
                colors_by_file[filename].add(color)
                files_by_color[color].add(filename)

print(len(found_colors), "colors found in", len(colors_by_file), "files")

max_files = max(len(v) for v in files_by_color.values())
max_colors = max(len(v) for v in colors_by_file.values())

most_popular_colors = [k for k, v in files_by_color.items() if len(v) == max_files]
most_colorful_files = [k for k, v in colors_by_file.items() if len(v) == max_colors]

print(most_popular_colors, "is the most popular color, appearing in", max_files, "files")
print(most_colorful_files, "is the most colorful file, using", max_colors, "colors")

with open("./palette.json", "w") as palette:
    json.dump(found_colors, palette, sort_keys=True, indent=4, cls=SetEncoder)

with open("./colors_by_file.json", "w") as colors_by_file_output:
    json.dump(colors_by_file, colors_by_file_output, sort_keys=True, indent=4, cls=SetEncoder)

with open("./files_by_color.json", "w") as files_by_color_output:
    json.dump(files_by_color, files_by_color_output, sort_keys=True, indent=4, cls=SetEncoder)
