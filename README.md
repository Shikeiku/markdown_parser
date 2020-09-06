# vnnv - versatile notes in neovim

Under construction! Worked on it for only two weeks so far. Current aim is just
personal use, which is making organised notes, flashcards, and R/python
notebooks with one tool.

## The command line interface

Vnnv works by configuring one directory as your binder. In this directory you
store all you markdown files that have a vnnv specific preamble code block on
top that stores information about the file. A file in this directory with the
preamble can be found by vnnv and is called a note.

Here is the current docopt for the tool, it is still under construction!
```
Usage: vnnv [-h]
       vnnv add [-h]
       vnnv list [-h]  (-t TAGS ... )
       vnnv read [-hrl] (-t TAGS ..)
       vnnv anki [-h] ( -t TAGS ... )
       vnnv review [-h] ( -t TAGS ... )

options:
-h --help   show this, use after command to show specific help

commands:
add         not implemented yet
list        list notes based on tags or something else
read        read notes in latex or in html
anki        add flashcards in notes to anki
review      interactively select notes and review them one by one

```

## vnnv [commands]
### vnnv add

Currently not yet working, need to make a template and method in the binder
class to add a new note.

### vnnv list

Prints a pretty table of your notes, currently shows tags, date, bibfile, and
title of your note in different columns.
```
Usage: vnnv list [-h] [ -s KEY ] (-t TAGS ... | -f FILES ... | -d DATES ...)

    options:
    -h --help       show this help string of vnnv list
    -t TAGS ...     specify the tags to use as a query for notes to list. Tags
                    should be words or numbers sepparated by any number of
                    spaces.
    -d DATES ...    @todo: Implement query by a range of dates
    -s KEY ...      @todo: Implement a sort key that is based on tags. For
                    example a note with tags chapter1 is sorted before a note with tags
                    chapter2.
```

Screenshot after using `vnnv list -t [ TAGS ... ]`:
![Screenshot vnnv list](./media/screenshot_vnnv_list.png)
