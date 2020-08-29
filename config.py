import os
import json
from rich.console import Console
from rich.theme import Theme


config_file = os.environ.get("VNNV_CONFIG", "$HOME/.dotfiles/vnnv/config.json")

with open(os.path.expandvars(config_file)) as c:
    cfg = json.load(c)

console = Console(theme=Theme(cfg["style"]), width=200)

