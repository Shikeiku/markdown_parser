from rich import print
from rich.panel import Panel
from vnnv.config import config
print(Panel("Hello, [red]World!"))

print(Panel.fit("Hello, [red]World!"))

print(Panel("Hello, [red]World!", title="Welcome"))

console.print(Panel.fit('helll', style='succes'))
