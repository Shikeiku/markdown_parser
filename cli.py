#!/Users/mikevink/.dotfiles/virtualenvs/vnnv/bin/python3
"""Usage: vnnv [-h]
       vnnv list [-st TAGS ...]
       vnnv read [-lt TAGS ...]
       vnnv anki [-t TAGS ...]
       vnnv i-mode [-t TAGS ...]

vnnv        if called without arguments prints some info on notes
-h --help   show this
list        list notes based on tags, default: marked
list -t     specify
read -l     comp
"""
from docopt import docopt
from typing import List, Dict

from vnnv.console import console
from vnnv.config import cfg

opts = docopt(__doc__, help=False)

# console.print(dict(opts))
# console.print(cfg)

def infoNotes() -> None:
    """
    @todo Docstring for infoNotes

    #c# @todo

    """
    console.print(infoNotes.__doc__)


def listNotes(**opts) -> None:
    """
    @todo Docstring for listNotes

    #**opts# @todo

    """
    console.print(listNotes.__doc__)


def readNotes(**opts) -> None:
    """
    @todo Docstring for readNotes

    #**opts# @todo

    """
    console.print(readNotes.__doc__)


def anki(**opts) -> None:
    """
    @todo Docstring for anki

    #**opts# @todo

    """
    console.print(anki.__doc__)


def i_mode(**opts) -> None:
    """
    @todo Docstring for i_mode

    #**opts# @todo

    """
    console.print(i_mode.__doc__)


if opts['list']:
    listNotes(**opts)
elif opts['read']:
    readNotes(**opts)
elif opts['anki']:
    anki(**opts)
elif not opts['--help']:
    infoNotes()
else:
    print(__doc__)

# if options['--help']:
#     print(__doc__)
# if __name__ == '__main__':
# print(console.size)
# print(__doc__)
