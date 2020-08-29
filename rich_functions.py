from typing import List, Literal
from rich.console import Console, OverflowMethod
from rich.theme import Theme

custom_theme = Theme({
    "info": "dim cyan",
    "succes": "green",
    "error": "bold red",
    "warning": "green",
    "danger": "bold red"
})

console.print(i)

console = Console(theme=custom_theme, width=100)  # , record=True)


def console_attributes() -> None:
    """
    Docstring for richConsoleAttributes
    """
    size = (console.size.height, console.size.width)
    encoding = console.encoding
    is_terminal = console.is_terminal
    color_sys = console.color_system
    console.print('%g' % (size[0]), locals())


def logging_and_printing() -> None:
    """
    Docstring for myFunction
    """
    hello = "hello, world"
    # console.print(hello)
    console.log(hello, log_locals=True)


def justify_or_align(style="bold white on blue", **kwargs):
    """
    You can also set the console attributes of course
    """
    console.print("Rich", style=style, justify="left")
    console.print("Rich", style=style, justify="center")
    console.print("Rich", style=style, justify="right")
    console.log(style, log_locals=True)


def overflow(console=Console(width=14),
             string="supercalifragilisticexpialidocious"):
    """
    Docstring for overflow
    """
    overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(string, overflow=overflow, style="bold blue")
        console.print()


def rich_input(string="What is [b]your[/b] [bold red]name[/]? :smiley: "):
    """
    Docstring for rich_input
    """
    console.input(string)


def colors():
    console.print("DANGER!", style="red on white")
    console.print("DANGER!", style="bold red on white")
    console.print("DANGER!", style="conceal")
    console.print("DANGER!", style="italic")
    console.print("DANGER!", style="reverse")
    console.print("DANGER!", style="strike")
    console.print("DANGER!", style="underline yellow on green")
    console.print("DANGER!", style="frame")
    console.print("DANGER!", style="encircle")
    console.print("DANGER!", style="overline")
    console.print("DANGER! [not bold]nevermind[/not bold]", style="bold")
    console.print("DANGER!")


def print_theme():
    console.print("This is information", style="info")
    console.print("Something terrible happened", style="danger")
    console.print("[warning]The pod bay doors are locked[/warning]")
    console.print("This is a succes! yay", style="succes")
    console.print("This is an eror", style="error")


if __name__ == "__main__":
    # console.print("\nprinting console_attributes")
    # console_attributes()
    # console.print("\nprinting logging and printing")
    # logging_and_printing()
    # console.print("\nprinting justify_or_align")
    # justify_or_align()
    # console.print("\noverflow:")
    # overflow()
    # console.print("\nrich_input")
    # rich_input()
    # text = console.export_text(clear=True)
    # console_attributes()

    # Styling functions
    colors()
    print_theme()
