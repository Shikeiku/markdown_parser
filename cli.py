#!/Users/mikevink/.dotfiles/virtualenvs/vnnv/bin/python3
"""Usage: vnnv [-h]
       vnnv add [-h]
       vnnv list [-h]  (-t TAGS ... | -f FILES ... | -d DATES ...) [ -s KEY ]
       vnnv read [-hrlw] (-t TAGS ... | -f FILES ... | -d DATES ...)
       vnnv anki [-h] ( -t TAGS ... )
       vnnv review [-h] ( -t TAGS ... )

options:
-h --help   show this, use after command to show specific help

commands:
list        list notes based on tags or something else
read        read notes in latex or in html
anki        add flashcards in notes to anki
review       interactively select notes and review them one by one
"""
from docopt import docopt
from typing import List, Dict

from rich.panel import Panel

from vnnv.binder import Binder
from vnnv.config import console, cfg

opts = docopt(__doc__, help=False)
opts = dict((k.lower(), v) for k, v in opts.items())

# console.print(dict(opts))
# console.print(cfg)


def infoNotes() -> None:
    """
    @todo Docstring for infoNotes

    #c# @todo

    """
    console.print(infoNotes.__doc__)


def listNotes(**opts) -> None:
    """Usage: vnnv list [-h] [ -s KEY ] (-t TAGS ... | -f FILES ... | -d DATES ...)

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
        opts['dates'] = None
    if not opts['-t']:
        opts['tags'] = None
    if not opts['-s']:
        opts['key'] = None
    # console.print(opts)
    # console.print(list)
    # console.print(TAGS)
    with Binder(**cfg) as b:
        notes = b.search_notes(**opts)
        b.tabularize(notes, **opts)


def readNotes(**opts) -> None:
    """vnnv read [-hrlw] [ -s KEY ] (-t TAGS ... | -f FILES ... | -d DATES ...)

    options:
    -h --help       show this help string of vnnv list
    -t TAGS ...     specify the tags to use as a query for notes to list. Tags
                    should be words or numbers sepparated by any number of
                    spaces.
    -d DATES ...    @todo: Implement query by a range of dates
    -f FILES ...    @todo: Implement opening with filename queries
    -s KEY ...      @todo: Implement a sort key that is based on tags. For
                    example a note with tags chapter1 is sorted before a note with tags
                    chapter2.

    """
    if opts['--help']:
        console.print(readNotes.__doc__)
    if not opts['-d']:
        opts['dates'] = None
    if not opts['-t']:
        opts['tags'] = None
    if not opts['-s']:
        opts['key'] = None
    if opts['-l']:
        opts['latex'] = True
    if opts['-r']:
        opts['rmarkdown'] = True
    console.print(opts)
    with Binder(**cfg) as b:
        notes = b.search_notes(**opts)
        if len(notes) == 0:
            console.print(
                Panel.fit("No notes could be found with the query!",
                          style='error'))
        b.read_in_markup(notes, **opts)


def anki(**opts) -> None:
    """vnnv anki [-h] ( -t TAGS ... )

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
    For example: Book chapter 1 exercise 1
    ~~~

    The <question> and <answer> tags are to give some extra html styling to
    your card within the anki fields. The {{c1::.*}} pattern is the cloze
    deletion that will be hidden on the front of your card.

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
    if not opts['tags']:
        opts['tags'] = None
    # console.print(opts)

    with Binder(**cfg) as b:
        notes = b.search_notes(**opts)
        if len(notes) == 0:
            console.print(
                Panel.fit('No notes were found with the query!',
                          style='error'))
        flashcards = b.collect_flashcards(notes, **opts)
        if flashcards is None:
            console.print(
                Panel.fit('No flashcards found inside the queried notes!',
                          style='error'))
            return
        elif len(flashcards) == 0:
            console.print(
                Panel.fit('No flashcards found inside the queried notes!',
                          style='error'))
            return
        b.give_notes_to_apy(flashcards)
        # console.print(flashcards)
        # console.print(lines)
        if not opts['-t']:
            console.print(
                Panel.fit(
                    '@todo: Currently only adding flashcards by tags is supported!',
                    style='error'))


def review(**opts):
    """vnnv review [-h] ( -t TAGS ... )

    options:
    -h --help       show this help string of vnnv list
    -t TAGS ...     specify the tags to use as a query for notes to list. Tags
                    should be words or numbers sepparated by any number of
                    spaces.
    -d DATES ...    @todo: Implement query by a range of dates
    -f FILES ...    @todo: implement files query
    -s KEY ...      @todo: Implement a sort key that is based on tags. For
                    example a note with tags chapter1 is sorted before a note with tags
                    chapter2.

    """
    if opts['--help']:
        console.print(anki.__doc__)
    if not opts['tags']:
        opts['tags'] = None
    with Binder(**cfg) as b:
        notes = b.search_notes(**opts)
        notes = b.sort_by_date(notes)
        if len(notes) == 0:
            console.print(
                Panel.fit('No notes were found with the query!',
                          style='error'))
        number_of_notes = len(notes)
        for i, note in enumerate(notes):
            if not note.review(i, number_of_notes):
                break


if opts['list']:
    listNotes(**opts)
elif opts['read']:
    readNotes(**opts)
elif opts['anki']:
    anki(**opts)
elif opts['review']:
    review(**opts)
elif not opts['--help']:
    infoNotes()
else:
    print(__doc__)

# if options['--help']:
#     print(__doc__)
# if __name__ == '__main__':
# print(console.size)
# print(__doc__)
