import os
import colorama
import sys
import json

from requests import get
from colr import color

reset = colorama.Style.RESET_ALL

# load config file: located in ~/.config/ll/config.json
config_file = os.path.expanduser("~/.config/ll/config.json")
if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        f.write(json.dumps(get("https://raw.githubusercontent.com/HACKERqq420/ll/main/.config/ll/config.json"), indent=4))
        f.close()
    print("Config file created. Please run again.")
else:
    with open(config_file, "r") as f:
        config = json.load(f)

chars = config["chars"]
colors = config["colors"]
style = config["style"]

# hex to rgb func
def hex2rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

for hex in colors.items():
    colors[hex[0]] = hex2rgb(hex[1])

if len(sys.argv) > 1:
    dir = os.path.expanduser(sys.argv[1])
else:
    dir = os.getcwd()

files = []
bytes = []

for file in os.listdir(dir):
    if config["showHidden"]:
        if file.startswith("."):
            continue
    if not config["showOver30chars"]:
        if len(file) > 30:
            continue
    files.append(file)

def get_bytes(file):
    name = os.path.join(dir, file)
    size = str(os.path.getsize(name))
    return size

def info(file):
    name = file
    ext = os.path.splitext(name)[1].strip(".")
    formatted_file = ""
    if os.path.isdir(name):
        text = f'{chars["dir"]} {name}{reset}'
        formatted_file = f'{color(text=text, style=style, fore=colors["dir"])}'
    elif ext in chars.keys():
        text = f'{chars[ext]} {name}{reset}'
        formatted_file = f'{color(text=text, style=style, fore=colors[ext])}'
    else:
        text = f'{chars["other"]} {name}{reset}'
        formatted_file = f'{color(text=text, style=style, fore=colors["other"])}'
    return formatted_file

# get longest in list
def get_longest(lst):
    longest = 0
    for item in lst:
        if len(item) > longest:
            longest = len(item)
    return longest

for file in files:
    bytes.append(str(get_bytes(file)))

padding = get_longest(bytes)

print()

for i in range(0, len(files)):
    bytes_of_files = color(fore=colors["bytes"], text=str(bytes[i]))
    print(" "*3 + bytes_of_files + " "*(padding - len(bytes[i]) + 3) + info(files[i]) + reset)

print()
