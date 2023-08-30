"""
# Notion To Obsidian Converter

Notion has hashes at the end of folders/files. This script removes those hashes and
renames all relevant file links.

It's named `notion2obsidian` because I originally wrote this script to convert my
files from Notion to, obviously, Obsidian.
"""
import os
import argparse
from pathlib import Path
import re
from urllib.parse import unquote

LINK_RE = re.compile(r"\]\((.+?)\)")
CONVERTED_FILES = {}


def should_skip_file(file: str):
    base_name, extension = os.path.splitext(file)
    return extension not in {".md", ".csv"}


def convert(match):
    if len(match.group(1)) >= 4 and match.group(1)[:4] == "http":
        return match.group(0)
    link = unquote(match.group(1))
    for file in CONVERTED_FILES:
        link = link.replace(file, CONVERTED_FILES[file])
    output = "](" + link.replace(" ", "%20") + ")"
    print(match.group(0), "->", output)
    return output


def convert_links(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if should_skip_file(name):
                continue
            original_path = os.path.join(root, name)
            print(original_path)
            contents = Path(original_path).read_text()
            Path(original_path).write_text(LINK_RE.sub(convert, contents))
            print("Rewrote links in", original_path)
        for name in dirs:
            convert_links(os.path.join(root, name))


def remove_last_word(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files + dirs:
            if name in files and should_skip_file(name):
                continue
            original_path = os.path.join(root, name)
            base_name, extension = os.path.splitext(name)

            new_name = (
                # Remove the last "word"
                " ".join(base_name.split()[:-1])
                + extension
            )
            new_path = os.path.join(root, new_name)
            os.rename(original_path, new_path)
            CONVERTED_FILES[name] = new_name
            print(f"Renamed {original_path!r} to {new_path!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove the pesky hashes in Notion exports"
    )
    parser.add_argument(
        "folder_path", help="Path to the folder containing your Notion export"
    )
    args = parser.parse_args()

    remove_last_word(args.folder_path)
    convert_links(args.folder_path)
