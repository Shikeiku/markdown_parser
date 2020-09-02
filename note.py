import re
from rich.panel import Panel
from pathlib import Path, PosixPath
from typing import ClassVar, List, Dict, AnyStr

from vnnv.config import console
# from vnnv.binder import Binder


class Note:
    """
    @todo: Docstring for Note
    """
    def __init__(self, binder: ClassVar, note):
        """@todo: to be defined."""
        self.b = binder
        self._init_note(note)

    def _init_note(self, note):
        # console.print(str(note))
        if not isinstance(note, PosixPath):
            # console.print('Note path given is not PosixPath!', style='warning')
            note = Path(note)
            if not note.exists():
                console.print(
                    'After converting to posixpath it was invalid! Trying to add b.path',
                    style='warning')
                note = self.b.path / note
                if not note.exists():
                    console.print('The note does not exist!', style='error')
                else:
                    self.n = note
            else:
                self.n = note
            return
        else:
            # console.print('Testing the posixpath')
            if not note.exists():
                console.print('The path is not valid!', style='warning')
            else:
                self.n = note

            # note = Path(note)
            # if not note.exists():
            #     console.print(Panel.fit('Error invalid note path!'), style='error')
            # else:
            #     self.n = note

    def parse_preamble(self) -> None:
        """
        @todo: Docstring for _init_preamble
        """
        with open(self.n, 'r') as n:
            first = n.readline()
            # preamble = first
            match = re.match(r'~~~\{\.preamble.*\}', first)
            if not match:
                preamble = None
            else:
                preamble = True
                preamble_string = ''
                while True:
                    line = n.readline()
                    match = re.match(r'\s*~~~\s*', line)
                    if match:
                        break
                    preamble_string += line
        if preamble:
            preamble = {}
            # '20200818-13h20m40s_Moller_Struth_chapter_2'

            match = re.search(r'\d{8}\-\d{2}h\d{2}m\d{2}s\_(.*)',
                              str(self.n.name))
            if match:
                preamble['title'] = match.group(1)

            match = re.search(
                r'(\d{4})(\d{2})(\d{2})\-(\d{2})h(\d{2})m(\d{2})s\_.*',
                str(self.n.name))
            if match:
                preamble['date'] = {
                    'year': match.group(1),
                    'month': match.group(2),
                    'day': match.group(3),
                    'hour': match.group(4),
                    'minute': match.group(5),
                    'second': match.group(6)
                }
            # console.print(preamble_string)

            # console.print(preamble_string, style='info')
            # console.print(Panel.fit(preamble_string, style='succes'))
            match = re.search(r'@.*?\{[\s\S]*?\n\}', preamble_string)
            if match:
                preamble['bib'] = match.group(0)
                # console.print(Panel.fit(preamble['bib'], style='warning'))
                # console.print(preamble_string, style='info')
                # console.print(preamble)

            # console.print(preamble_string)
            match = re.search(r'tags = \{([\s\S]*?)\}', preamble_string)
            if match:
                # preamble['tags'] = match.group(0)
                # console.print(Panel.fit(preamble['tags'], style='succes'))
                # console.print(preamble_string, style='info')
                # console.print(preamble, style='info')
                preamble['tags'] = [
                    tag.strip().lower() for tag in match.group(1).split(',')
                ]

            match = re.search(r'links = \{([\s\S]*?)\}', preamble_string)
            if match:
                # preamble['links'] = match.group(1)
                preamble['links'] = [
                    link for link in match.group(1).strip().split('\n')
                ]
            # preamble = preamble_string

        # console.print(preamble)
        return preamble

    def parse_vnnv_anki_codeblocks(self, args) -> List[str]:
        """
        @todo: Docstring for parse_vnnv_anki_codeblocks
        """
        

    def read_lines(self) -> List:
        """
        @todo: Docstring for read_lines
        """
        console.print('deleting the preamble lines from lines of', self.n)
        with open(self.n, 'r') as n:
            lines = n.readlines()
        i = 0
        # console.print(lines)
        while True:
            match = re.match(r'~~~$', lines[i])
            if match:
                del lines[i]
                # print(lines[i])
                break
            else:
                # print(lines[i])
                del lines[i]
            # i += 1
        # print(lines)
        return lines


if __name__ == '__main__':
    # my_note = Note(Binder, '/Users/mikevink/Documents/markdown_notes/20200608-10h48m50s_2008_Steiner.md')
    pass
