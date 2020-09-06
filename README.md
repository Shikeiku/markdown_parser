# vnnv - versatile notes in neovim

Under construction! Worked on it for only two weeks so far. Current aim is just
personal use, which is making organised notes, flashcards, and R/python
notebooks with one tool.

## The command line interface

Vnnv works by configuring one directory as your binder. In this directory you
store all you markdown files that have a vnnv specific preamble code block on
top that stores information about the file. A file with this preamble can be
found by vnnv and is called a note.

Here is the current docopt for the tool, it is still under construction!
```shell
Usage: vnnv [-h]
       vnnv add [-h]
       vnnv list [-h]  (-t TAGS ... | -f FILES ... | -d DATES ...)
       vnnv read [-hrlw] (-t TAGS ... | -f FILES ... | -d DATES ...)
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
