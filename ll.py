import os
import colorama
import sys
import json

from colr import color
# from tabulate import tabulate

default_config = {
    "showHidden": True,
    "showOver30chars": False,
    "showIcons": True,
    "showColors": True,
    "style": "normal",
    "colors": {
        "py": "#4B8BBE",
        "js": "#FFCE00",
        "go": "#00B8D4",
        "rb": "#FF0000",
        "cs": "#569CD6",
        "java": "#F5871F",
        "php": "#4F5D95",
        "html": "#E44D26",
        "css": "#1572B6",
        "sql": "#E7C547",
        "sh": "#B82E2E",
        "pl": "#0067A5",
        "coffee": "#6F4E37",
        "c": "#555555",
        "cpp": "#C34E00",
        "ps1": "#00A1FF",
        "bat": "#A6E22E",
        "xml": "#7F9FB6",
        "json": "#F8C300",
        "vim": "#199F4B",
        "other": "#666666"
    },
    "chars": {
        "py": "\ue235",
        "js": "\ue718",
        "go": "\ue626",
        "rb": "\ue739",
        "cs": "\uf81a",
        "java": "\ue738",
        "php": "\ue73d",
        "html": "\ue736",
        "css": "\ue749",
        "sql": "\ue7c4",
        "sh": "",
        "pl": "\ue769",
        "coffee": "\ue751",
        "c": "\ue61e",
        "cpp": "\ue61d",
        "ps1": "\uf489",
        "bat": "",
        "xml": "\uf72d",
        "json": "\ue60b",
        "vim": "\ue62b",
        "dir": "\uf114",
        "zip": "\uf410",
        "other": "\uf15c"
    }
}

reset = colorama.Style.RESET_ALL

# load config file: located in ~/.config/ll/config.json
config_file = os.path.expanduser("~/.config/ll/config.json")
if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        f.write(json.dumps(default_config, indent=4))
        f.close()
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

for file in os.listdir(dir):
    if config["showHidden"]:
        if file.startswith("."):
            continue
    if config["showOver30chars"]:
        if len(file) > 30:
            continue
    else:
        files.append(file)

def add_bytes(files):
    formatted_ffiles = []
    for i in range(0, len(files)):
        name = os.path.join(dir, files[i])
        name_without_dir = files[i]
        size = colorama.Fore.LIGHTBLUE_EX + str(os.path.getsize(name)) + colorama.Fore.RESET
        if not len(name_without_dir) > 30:
            formatted_ffiles.append([size, name_without_dir])
    return formatted_ffiles

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

ffiles = add_bytes(files)
formatted_files = []

for i in range(0, len(ffiles)):
    formatted_files.append(info(ffiles[i][1]))
    print(" "*2+formatted_files[i])

print()

# print()
# print("\n".join(formatted_files))
# print()

# table = tabulate(formatted_files, tablefmt="plain")
# print("\n"+table+"\n")
