import json
import re
import subprocess
import sys

inkscape_executable = "C:/Program Files/Inkscape/inkscape.exe"

print("Checking staged files for color compliance")

try:
    # Get files in staging area:
    commit_text = subprocess.check_output(["git", "status", "--porcelain", "-uno", "-z"],
                                          stderr=subprocess.STDOUT).decode("utf-8")
except subprocess.CalledProcessError:
    print("Error calling git status in pre-commit hook")
    sys.exit(12)

# making note of the commit changes, for processing in the post-commit
with open(".commit", 'w') as commit_changes:
    commit_changes.write(commit_text)

with open("../palette.json", "r") as palette:
    valid_colors = set(json.load(palette))

with open("files_by_color.json", "r") as files_by_color_input:
    files_by_color = json.load(files_by_color_input)

color_regex = "#[\da-fA-f]+"

scarcity_cuttoff = 10


def validate_colors(svg_filename):
    acceptable_colors = True
    with open(svg_filename, "r") as svg:
        data = svg.read()
        colors = re.findall(color_regex, data)
        for color in colors:
            if color not in valid_colors:
                print("Invalid color", color, "present in", svg_filename)
                acceptable_colors = False
            else:
                number_occurances = len(files_by_color[color])
                if number_occurances <= scarcity_cuttoff:
                    print("Color", color, "present in", svg_filename, "appears in only", number_occurances, "emoji.")
                    acceptable_colors = False

    return acceptable_colors


file_list = commit_text.splitlines()
validations = []
# Check all files:
for file_entry in file_list:
    # format of lines is 'XY filename'
    # X is status of the index
    index_status = file_entry[0]
    filename = file_entry[3:]
    # only interested in svgs
    if filename.endswith(".svg") and filename.startswith("svg/"):
        if index_status not in ['R', 'D', 'C']:  # Renames, copies and deletes don't need checking
            validations.append(validate_colors(filename))
    elif filename.endswith(".png") and filename.startswith("72x72/"):
        print('Changed rendered image "{}". This change subject to be overridden by post-commit.'.format(filename))


if all(validations):
    # Everything seams to be okay:
    print("No unexpected colors found.")
    sys.exit(0)
else:
    print("Commit aborted, fix colors and recommit.")
    sys.exit(1)
