from rich.console import Console, OverflowMethod

console = Console(width=100, record=True)


def console_attributes():
    """
    @todo Docstring for richConsoleAttributes
    """
    size = (console.size.height, console.size.width)
    encoding = console.encoding
    is_terminal = console.is_terminal
    color_sys = console.color_system
    console.print(locals())


def logging_and_printing():
    """
    @todo Docstring for myFunction
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
    @todo Docstring for overflow
    """
    overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(string, overflow=overflow, style="bold blue")
        console.print()


def rich_input(string="What is [b]your[/b] [bold red]name[/]? :smiley: "):
    """
    @todo Docstring for rich_input
    """
    console.input(string)


if __name__ == "__main__":
    console.print("\nprinting console_attributes")
    console_attributes()
    console.print("\nprinting logging and printing")
    logging_and_printing()
    console.print("\nprinting justify_or_align")
    justify_or_align()
    console.print("\noverflow:")
    overflow()
    console.print("\nrich_input")
    rich_input()
    # text = console.export_text(clear=True)


