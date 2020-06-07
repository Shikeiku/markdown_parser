import re
from datetime import datetime
from pathlib import Path


def newnote(nvim):
    """
    Makes a new note
    """
    nvim.command(':let b:note_name=input("New markdown_note:")')
    input_note_name = nvim.eval('b:note_name')
    now = datetime.now()

    dt_string = now.strftime("%Y%m%d-%Hh%Mm%Ss_")
    note_name = dt_string + input_note_name + '.md'
    note_name = re.sub(' ', '_', note_name)
    path = '~/Documents/markdown_notes/' + note_name
    if input_note_name != '':
        nvim.command(':e ' + path)
        nvim.command(':cd ~/Documents/markdown_notes')
    else:
        nvim.command(':echo "file name was empty, could not make a new note"')
