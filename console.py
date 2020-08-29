from rich.console import Console
from rich.theme import Theme

from vnnv.config import cfg

# print(cfg["style"])

console = Console(theme=Theme(cfg["style"]), width=200)
# console.print(console)
