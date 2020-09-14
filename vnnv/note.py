import re
import os
import readchar
import subprocess
import shutil

from rich.markdown import Markdown
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.prompt import Confirm, Prompt

from pathlib import Path, PosixPath
from typing import ClassVar, List, Dict, AnyStr

from vnnv.config import console
from vnnv.convert import vnnv_flashcards_to_apy, markdown_to_latex
from vnnv.utilities import choose, apy_add_from_file, editor, call, cd, jupyter_wrapper, pdflatex
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
            preamble_str += 'tags = {' + ', '.join(
                preamble_dict['tags']) + '}\n'
        if 'links' in preamble_dict_keys:
            preamble_str += 'links = {\n' + '\n'.join(
                preamble_dict['links']
            ) + '\n}\n'  # Not sure if there should be one more whitespace here
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

    def markdown_print(self,
                       outline=False,
                       preamble=False,
                       level=None,
                       max_outline=None) -> None:
        """
        @todo: Docstring for markdown_print
        """
        lines = self.read_lines()
        if preamble:
            preamble_str = [self.preamble_dict_to_str()]
            lines = preamble_str + lines
        max_outline = 0
        if outline:
            repr_str = ''
            for line in lines:
                match = re.match(r'(#+) .+', line)
                if match:
                    if level is not None:
                        if level >= len(match.group(1)):
                            repr_str += match.group(0) + '\n'
                        if len(match.group(1)) >= max_outline:
                            max_outline = len(match.group(1))
            lines = repr_str + '\n'

        md = Markdown(''.join(lines), justify="left")
        console.print(Align(md, "center", width=80))
        return max_outline

    def parse_vnnv_anki_codeblocks(self) -> List[str]:
        """
        @todo: Docstring for parse_vnnv_anki_codeblocks
        """
        lines = self.read_lines()
        print(lines)
        parsed_cards = []
        vnnv_anki = False
        for line in lines:
            match = re.match(r'<vnnvanki>', line)
            if match:
                vnnv_anki = True
                field = 'Text'
                flashcard = {'fields': {}}
                flashcard['fields'][field] = ''
                console.print(Panel.fit('Found a flashcard!', style='succes'))
                continue

            match = re.match(r'</vnnvanki>', line)
            if match:
                if vnnv_anki:
                    vnnv_anki = False
                    # console.print(
                    #     Panel.fit(
                    #         'Found the end of the flashcard! Adding collected fields to the list of flashcards',
                    #         style='succes'))
                    preamble = self.preamble
                    flashcard['tags'] = preamble['tags']
                    if 'deck' in self.preamble.keys():
                        flashcard['deck'] = preamble['deck']
                    else:
                        flashcard['deck'] = 'inbox anki-cloze'
                    parsed_cards += [flashcard]
                    continue

            match = re.match(r'<Text/context>\s*', line)
            if match:
                if vnnv_anki:
                    field = 'context'
                    flashcard['fields'][field] = ''
                continue
            
            match = re.match(r'\!\[[^]]*?\]\(([^\)]*?)\)', line)
            if match:
                if vnnv_anki:
                    anki_media_dir = Path('/Users/mikevink/Library/Application Support/Anki2/User 1/collection.media')
                    image_url = Path(match.group(1))
                    if not anki_media_dir.exists():
                        console.print('Anki media collection invalid!')
                        raise SystemExit
                    elif not image_url.exists():
                        console.print(image_url)
                        console.print('The image url is invalid, check if escaping spaces helps')
                        image_url = Path(str(image_url).replace(' ', '\\ '))
                        if image_url.exists():
                            console.print('Space escaped path does exist!', style='succes')
                            pass
                        else:
                            raise SystemExit
                    shutil.copy(image_url, anki_media_dir / image_url.name)


            if vnnv_anki:
                flashcard['fields'][field] += line
        return parsed_cards

    def convert_inline_to_ref(self, lines, links, regex) -> List:
        console.print('Preamble before self.convert_inline_to_ref',
                      self.preamble)
        # console.print(self.preamble['links'], style='succes')
        new_links = False
        for text, url in links:
            if 'links' in self.preamble.keys():
                if self.preamble['links'][0] == '':
                    del self.preamble['links'][0]
            else:
                console.print(
                    Panel.fit('Preamble does not have a link section!',
                              style='error'))
                raise SystemExit

            link_in_text = text + ': ' + url
            if link_in_text.strip() not in self.preamble['links']:
                console.print('adding new links to preamble')
                self.preamble['links'] += [link_in_text]
                new_links = True
        console.print('New preamble links after adding links:\n\n',
                      self.preamble['links'])
        if new_links:
            with open(self.n, 'r+') as n:
                lines = n.read()
                n.seek(0)
                lines = self.update_preamble(lines)
                lines = re.sub(regex, r'\1', lines)
                n.write(lines)
        # print(lines)

    def update_preamble(self, lines):
        preamble_str = self.preamble_dict_to_str()
        PREAMBLE_REGEX = r'~~~\{\.preamble.*\}[\s\S]+?~~~'
        match = re.match(PREAMBLE_REGEX, lines)
        if match:
            # console.print('Found the preamble:\n\n', match.group(0))
            print('Self.update_preamble will update the preamble to:\n\n',
                  preamble_str)
            lines = re.sub(PREAMBLE_REGEX, preamble_str.strip(), lines)
            # print('After updating the preamble the lines look like:\n\n', lines)
            # print(self.preamble)
            # console.print(lines)
        return lines

    def write_lines(self) -> None:
        """
        @todo: Docstring for update_lines
        """
        # preamble = self.preamble_dict_to_str()
        # lines = preamble + self.lines
        # console.print(lines)
        # with open(self.n, 'w') as n:
        #     pass
        # self.b.modified = True
        pass
        

    def read_lines(self) -> List:
        """
        @todo: Docstring for read_lines
        """
        # console.print('deleting the preamble lines from lines of', self.n)
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
        str_lines = ''.join(lines)
        IMAGE_LINK_REGEX = r'(?<![\\])\!\[([^\]]+?)\]\(([^\)]+?)\)'
        images = re.findall(IMAGE_LINK_REGEX, str_lines)
        self.preamble['images'] = images
        # console.print('This note has these images', self.preamble['images'])
        INLINE_NON_IMAGE_LINK_REGEX = r'(?<![\!|\\])(\[[^\(\]]+?\])\(([\s\S]+?)\)'
        links = re.findall(INLINE_NON_IMAGE_LINK_REGEX, str_lines)
        # console.print('the links that were found and given to convert_inline_to_ref:', links)
        begin_time = os.path.getmtime(self.n)
        if links != []:
            self.convert_inline_to_ref(str_lines, links,
                                       INLINE_NON_IMAGE_LINK_REGEX)
            end_time = os.path.getmtime(self.n)
            if end_time != begin_time:
                console.print('The file was modified because links were reorganised to the preamble')
                Prompt.ask("Press enter to continue")
                self.b.modified = True
        self.lines = lines
        return lines

    def edit(self) -> None:
        """
        @todo: Docstring for edit
        """
        begin_time = os.path.getmtime(self.n)
        retcode = editor(self.n)
        if retcode != 0:
            console.print(f'Editor returned with retcode {retcode}')
            Confirm.ask("did you see the retcode?")
        end_time = os.path.getmtime(self.n)
        if end_time != begin_time:
            self.b.modified = True
            console.print('The file was modified')
            Prompt.ask("Press enter to continue")

            # self.b.modified = True
        # console.print(retcode)

    def open_images(self) -> None:
        """
        @todo: Docstring for open_images
        """
        urls = []
        for name, url in self.preamble['images']:
            urls.append(url.replace(' ', ' '))
        # urls[0] = urls[0].lstrip('/Users/mikevink/')
        with cd('/Users/mikevink'):
            call(['open'] + urls)
        # for name, url in self.preamble['images']:
        #     call(['open', '-a', 'Preview', url])

    def convert(self, to=None):
        """
        @todo: Docstring for convert
        """
        # lines = ''.join(self.lines)
        if to == 'jupyter':
            # console.print('converting to jupyter')
            # Prompt.ask("Press enter to continue")
            jupyter_wrapper(self)
            Prompt.ask("If file was changed it will updated after pressing any key")
            # self.lines = ret_lines
            # self.write_lines()
        if to == 'latex':
            lines_and_links = [(self.lines, self.preamble['links'])]
            latex = markdown_to_latex(lines_and_links)
            pdflatex(latex)

    def delete(self) -> None:
        """
        @todo: Docstring for delete
        """
        self.n.unlink()

    def review(self, i=None, number_of_notes=None) -> None:
        """
        @todo: Docstring for review
        """
        actions = {
            'c': 'Continue',
            'e': 'Edit',
            'd': 'Delete',
            'f': 'Show images',
            'z': 'follow link mode',
            'o': 'Choose format and open',
            'a': 'Give flashcards in note to apy',
            '[': 'Decrease outline level',
            ']': 'Increase outline level',
            's': 'Save and stop',
            'x': 'Abort',
        }
        # console.print(self)
        # self.markdown_print(preamble=True)  # outline=True)
        # return True
        refresh = True
        print_outline = True
        print_preamble = False
        outline_level = 2
        max_outline = None
        while True:
            if refresh:
                console.clear()
                if i is None:
                    if len(', '.join(self.preamble['tags'])) >= len('Reviewing note'):
                        console.print(Panel.fit(', '.join(self.preamble['tags']), title="Reviewing note"), style='info')
                    else:
                        console.print("Reviewing note", style='info')
                elif number_of_notes is None:
                    if len(', '.join(self.preamble['tags'])) >= len(f'Reviewing note {i+1}'):
                        console.print(Panel.fit(', '.join(self.preamble['tags']), title=f"Reviewing note {i+1}"), style='info')
                    else:
                        console.print(f'Reviewing note {i+1}', style='info')
                else:
                    if len(', '.join(self.preamble['tags'])) >= len(f'Reviewing note {i+1} of {number_of_notes}'):
                        console.print(Panel.fit(', '.join(self.preamble['tags']), title=f"Reviewing note {i+1} of {number_of_notes}"), style='info')
                    else:
                        console.print(f'Reviewing note {i+1} of {number_of_notes}',
                                      style='info')

                # column = 0
                # for x, y in actions.items():
                #     menu = '[green]' + x + '[/green]: ' + y
                #     if column < 3:
                #         console.print(f'{menu:28s}')
                #     else:
                #         console.print(menu)
                #     column = (column + 1) % 4

                menu = []
                for x, y in actions.items():
                    item = ['[green]' + x + '[/green]: ' + y]
                    menu += item
                # console.print(menu)
                columns = Columns(menu,
                                  equal=True,
                                  expand=True,
                                  column_first=True)

                # console.print('max outline:', max_outline, 'current:', outline_level)
                console.print(columns)

                max_outline = self.markdown_print(outline=print_outline,
                                                  preamble=print_preamble,
                                                  level=outline_level,
                                                  max_outline=max_outline)
                if not print_outline:
                    Prompt.ask('Press enter to stop reading in terminal.')
                    print_outline = True
                    continue

            else:
                refresh = True

            choice = readchar.readchar()
            action = actions.get(choice)
            if action == 'Continue':
                return True

            if action == 'Edit':
                self.edit()
                continue
            
            if action == 'Delete':
                choice = Confirm.ask("Are you sure you want to delete the file?")
                if choice:
                    self.delete()
                    return True
                if not choice:
                    continue
            
            if action == 'Show images':
                console.print(self.preamble['images'])
                self.open_images()
                # Prompt.ask("Pres enter to continue")

            if action == 'Choose format and open':
                choice = choose(['Rmd', 'jupyter', 'latex', 'terminal'])
                if choice == 'latex':
                    self.convert(to='latex')
                    continue
                if choice == 'jupyter':
                    self.convert(to='jupyter')
                    continue
                if choice == 'Rmd':
                    self.convert(to='Rmd')
                if choice == 'terminal':
                    print_outline = False

            if action == 'Give flashcards in note to apy':
                flashcards = self.parse_vnnv_anki_codeblocks()
                lines = vnnv_flashcards_to_apy(flashcards)
                apy_add_from_file(lines)
                Prompt.ask("Press enter to continue")

            if action == 'Increase outline level':
                if outline_level + 1 > max_outline:
                    console.print('Max outline level reached!',
                                  style='warning')
                    Prompt.ask("Pres enter to continue")
                    continue
                else:
                    outline_level += 1
                    continue

            if action == 'Decrease outline level':
                if outline_level - 1 < 1:
                    console.print('Minimum outline level reached!',
                                  style='warning')
                    Prompt.ask("Pres enter to continue")
                    continue
                else:
                    outline_level -= 1
                    continue

            if action == 'Save and stop':
                return False


if __name__ == '__main__':
    # my_note = Note(Binder, '/Users/mikevink/Documents/markdown_notes/20200608-10h48m50s_2008_Steiner.md')
    pass
