from vnnv.console import console

def console_attributes():
    """
    @todo Docstring for richConsoleAttributes
    """
    size = (console.size.height, console.size.width)
    encoding = console.encoding
    is_terminal = console.is_terminal
    color_sys = console.color_system
    console.print(locals())

if __name__ == "__main__":
    console_attributes()
