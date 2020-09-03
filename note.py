import re
import os

from rich.markdown import Markdown
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
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
        self._init_parse_preamble()

    def _init_note(self, note):
        # console.print(str(note))
        if not isinstance(note, PosixPath):
            # console.print('Note path given is not PosixPath!', style='warning')
            note = Path(note)
            if not note.exists():
                console.print(
                    f'After converting to posixpath it was invalid! Trying to prepend {self.b.path}',
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

    def _init_parse_preamble(self) -> Dict:
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

            match = re.search(r'deck = \{(.*)\}', preamble_string)
            if match:
                preamble['deck'] = match.group(1).strip()
            # preamble = preamble_string

        # console.print(preamble)
        # return preamble
        self.preamble = preamble

    def __repr__(self) -> str:
        """
        @todo: Docstring for __repr__
        """
        lines = self.read_lines()
        repr_str = ''
        for line in lines:
            match = re.match(r'#+ .+', line)
            if match:
                repr_str += match.group(0) + '\n'
        return repr_str + '\n'

    def preamble_dict_to_str(self) -> str:
        """
        @todo: Docstring for preamble_dict_to_str
        """
        preamble_dict = self.preamble
        preamble_dict_keys = preamble_dict.keys()

        preamble_str = ''
        preamble_str += '~~~{.preamble}\n'
        if 'bib' in preamble_dict_keys:
            preamble_str += preamble_dict['bib'] + '\n'
        if 'tags' in preamble_dict_keys:
            preamble_str += 'tags = {' + ''.join(preamble_dict['tags']) + '}\n'
        if 'links' in preamble_dict_keys:
            preamble_str += 'links = {\n' + ''.join(
                preamble_dict['links']) + '\n}\n'
        if 'deck' in preamble_dict_keys:
            preamble_str += 'deck = {' + preamble_dict['deck'] + '}\n'
        preamble_str += '~~~\n'
        return preamble_str

    def render_date_dict(self):
        numeric_to_name = {
            '01': 'Jan',
            '02': 'Feb',
            '03': 'Mar',
            '04': 'Apr',
            '05': 'May',
            '06': 'Jun',
            '07': 'Jul',
            '08': 'Aug',
            '09': 'Sep',
            '10': 'Oct',
            '11': 'Nov',
            '12': 'Dec'
        }
        rendered_date = self.preamble['date'][
            'day'] + ' ' + numeric_to_name.get(
                self.preamble['date']
                ['month']) + ' ' + self.preamble['date']['year']
        return rendered_date

    def markdown_print(self, outline=False, preamble=False) -> None:
        """
        @todo: Docstring for markdown_print
        """
        lines = self.read_lines()
        if preamble:
            preamble_str = [self.preamble_dict_to_str()]
            lines = preamble_str + lines
        if outline:
            repr_str = ''
            for line in lines:
                match = re.match(r'#+ .+', line)
                if match:
                    repr_str += match.group(0) + '\n'
            lines = repr_str + '\n'

        md = Markdown(''.join(lines), justify="left")
        console.print(Align(md, "center", width=80))

    def parse_vnnv_anki_codeblocks(self) -> List[str]:
        """
        @todo: Docstring for parse_vnnv_anki_codeblocks
        """
        lines = self.read_lines()
        # console.print(lines)
        parsed_cards = []
        vnnv_anki = False
        for line in lines:
            match = re.match(r'~~~\{\.vnnv_anki\}', line)
            if match:
                vnnv_anki = True
                field = 'Text'
                flashcard = {'fields': {}}
                flashcard['fields'][field] = ''
                console.print(Panel.fit('Found a flashcard!', style='succes'))
                continue

            match = re.match(r'~~~$', line)
            if match:
                if vnnv_anki:
                    vnnv_anki = False
                    # console.print(
                    #     Panel.fit(
                    #         'Found the end of the flashcard! Adding collected fields to the list of flashcards',
                    #         style='succes'))
                    preamble = self.preamble
                    flashcard['tags'] = preamble['tags']
                    flashcard['deck'] = preamble['deck']
                    parsed_cards += [flashcard]
                    continue

            match = re.match(r'<Text/context>\s*', line)
            if match:
                field = 'context'
                flashcard['fields'][field] = ''
                continue

            if vnnv_anki:
                flashcard['fields'][field] += line
        return parsed_cards

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

    def review(self, i=None, number_of_notes=None) -> None:
        """
        @todo: Docstring for review
        """
        actions = {
            'c': 'Continue',
            'e': 'Edit',
            'o': 'Organise links',
            'f': 'Show images',
            'l': 'Read in latex',
            'm': 'Toggle full text',
            'p': 'Toggle print preamble',
            'a': 'Give tags to apy review',
            'z': 'follow link mode',
            's': 'Save and stop',
            'j': 'Open note in jupyter notebook',
            'r': 'Read in Rmarkdown',
            'x': 'Abort',
        }
        # console.print(self)
        self.markdown_print(preamble=True)  # outline=True)
        # return True
        refresh = True
        print_outline = True
        print_preamble = False
        while True:
            if refresh:
                console.clear()
                if i is None:
                    console.print('Reviewing note', style='info')
                elif number_of_notes is None:
                    console.print(f'Reviewing note {i+1}', style='info')
                else:
                    console.print(f'Reviewing note {i+1} of {number_of_notes}',
                                  style='info')

                column = 0
                for x, y in actions.items():
                    menu = '[green]' + x + '[/green]: ' + y
                    if column < 3:
                        console.print(f'{menu:28s}')
                    else:
                        console.print(menu)
                    column = (column + 1) % 4

                console.print('\n')

                self.markdown_print(outline=print_outline,
                                    preamble=print_preamble)
            else:
                refresh = True
            return False


if __name__ == '__main__':
    # my_note = Note(Binder, '/Users/mikevink/Documents/markdown_notes/20200608-10h48m50s_2008_Steiner.md')
    pass
