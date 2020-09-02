#!/Users/mikevink/.dotfiles/virtualenvs/vnnv/bin/python3
"""Usage: vnnv [-h]
       vnnv list [-h] [ -t TAGS ... ] [ -d DATES ... ] [ -s KEY ]
       vnnv read [-hlw] [ -t TAGS ... ] [ -d DATES ... ] [ -s KEY ]
       vnnv anki [-h] [ -t TAGS ... ] [ -d DATES ... ] [ -s KEY ]

options:
-h --help   show this, use after command to show specific help

commands:
list        list notes based on tags or something else
read        read notes in latex or in html
anki        add flashcards in notes to anki
imode       interactively select notes and review them one by one
"""
from docopt import docopt
from typing import List, Dict

from rich.panel import Panel

from vnnv.binder import Binder
from vnnv.config import console, cfg
from vnnv.utilities import apy_add_from_file
from vnnv.utilities import pdflatex

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
    """Usage: vnnv list [-h] [ -t TAGS ... ] [ -d DATES ... ] [ -s KEY ]

    options:
    -h --help       show this help string of vnnv list
    -t TAGS ...     specify the tags to use as a query for notes to list. Tags
                    should be words or numbers sepparated by any number of
                    spaces.
    -d DATES ...    @todo: Implement query by a range of dates
    -s KEY ...      @todo: Implement a sort key that is based on tags. For
                    example a note with tags chapter1 is sorted before a note with tags
                    chapter2.

    """
    if opts['--help']:
        console.print(listNotes.__doc__)
        return
    # console.print(listNotes.__code__.co_varnames)
    if not opts['-d']:
        opts['DATES'] = None
    if not opts['-t']:
        opts['TAGS'] = None
    if not opts['-s']:
        opts['KEY'] = None
    # console.print(opts)
    # console.print(list)
    # console.print(TAGS)
    with Binder(**cfg) as b:
        b.tabularize(**opts)


def readNotes(**opts) -> None:
    """
    @todo Docstring for readNotes

    #**opts# @todo

    """
    if opts['--help']:
        console.print(readNotes.__doc__)
    if not opts['-d']:
        opts['DATES'] = None
    if not opts['-t']:
        opts['TAGS'] = None
    if not opts['-s']:
        opts['KEY'] = None
    console.print(opts)
    with Binder(**cfg) as b:
        lines = b.read(**opts)
        if opts['-l']:
            pdflatex(lines)


def anki(**opts) -> None:
    """vnnv anki [-h] [ -t TAGS ... ]

    Reads the markdown notes based on the query option. The flashcard has to be
    in the following syntax:

    ~~~{.vnnv-anki}
    <question>
    My question
    </question>

    {{c1::
    <answer>My answer</answer>

    Some other lines.
    }}

    ## context
    Book chapter 1 exercise 1
    ~~~

    options:
    -h --help       show this help string of vnnv list
    -t TAGS ...     specify the tags to use as a query for notes to list. Tags
                    should be words or numbers sepparated by any number of
                    spaces.
    -d DATES ...    @todo: Implement query by a range of dates
    -s KEY ...      @todo: Implement a sort key that is based on tags. For
                    example a note with tags chapter1 is sorted before a note with tags
                    chapter2.

    """
    if opts['--help']:
        console.print(anki.__doc__)
    if not opts['-t']:
        opts['TAGS'] = None
    console.print(opts)

    with Binder(**cfg) as b:
        if opts['-t']:
            flashcards = b.collect_flashcards(**opts)
            if len(flashcards) == 0:
                console.print(Panel.fit('No flashcards found!', style='error'))
                return
            apy_add_from_file(flashcards)
        else:
            console.print(
                Panel.fit(
                    '@todo: Currently only adding flashcards by tags is supported!',
                    style='error'))


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
