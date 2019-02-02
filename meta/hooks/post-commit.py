import os
import subprocess
import sys

"""
A very basic attempt to keep the 72x72/ directory up to date, without just rebuilding it all the time.
Not intended to be bulletproof, should just cover day-to-day building
"""

try:
    with open(".commit", 'r') as commit_changes:
        file_list = commit_changes.readlines()
except FileNotFoundError:
    # if there is no .commit file, we early out
    sys.exit(0)

inkscape_executable = "C:/Program Files/Inkscape/inkscape.exe"


def to_character(filename):
    # split the extension and directory from filename
    # ie. "svg/1f991.svg" -> "1f991" 🦑
    return os.path.splitext(os.path.basename(filename))[0]


for file_entry in file_list:
    # format of lines is 'XY filename'
    # X is status of the index
    index_status = file_entry[0]
    filename = file_entry[3:]

    # approach:
    # work through images changes, listing them as needing fixes
    # work through svgs, updating said fixes
    # make fixes
    to_build = set()  # images we need to build
    to_remove = set()  # images we need to remove

    if filename.endswith(".png") and filename.startswith("72x72/"):
        if index_status in ["D", "M"]:
            # image deleted or modified, need to rebuild it
            to_build.add(to_character(filename))
        elif index_status == "A":
            # we don't really want manually added ones, remove
            to_remove.add(to_character(filename))
        elif index_status == "R":
            # renamed image, need to rebuild both
            new_name, old_name = filename.split('\00')
            to_build.add(to_character(old_name))
            to_build.add(to_character(new_name))

    elif filename.endswith(".svg") and filename.startswith("svg/"):
        if index_status in ["M", "A"]:
            # modified or added get images built
            to_build.add(to_character(filename))
            pass
        elif index_status == "R":
            new_name, old_name = filename.split('\00')
            # file renamed. remove old, rebuild new
            to_build.add(to_character(new_name))
            to_remove.add(to_character(old_name))
        elif index_status == "D":
            # file deleted, remove image
            to_remove.add(to_character(filename))


for character in to_remove:
    print("Removing {}.png".format(character))
    os.remove("./72x72/{}.png".format(character))

for character in to_build:
    print("Exporting", character)
    in_path = "./svg/{}.svg".format(character)
    out_path = "./72x72/{}.png".format(character)
    subprocess.call([inkscape_executable, in_path,
                     '--export-png={}'.format(out_path)])

changed_characters = to_remove.union(to_build)
# if we actually made any changes
if changed_characters:
    print(len(changed_characters), "character images changed")
    for character in changed_characters:
        out_path = "./72x72/{}.png".format(character)
        subprocess.call(["git", "add", out_path])
    # commit our changes as an amendment
    subprocess.call(["git", "commit", "-amend" "--no-verify"])
