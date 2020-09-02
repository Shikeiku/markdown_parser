import os
import re
import shutil
import subprocess
from tempfile import NamedTemporaryFile
from typing import List, Dict
from pathlib import Path

from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

from vnnv.note import Note
from vnnv.config import cfg, console
from vnnv.convert import markdown_to_latex
from vnnv.utilities import call, cd


class Binder:
    """
    @todo: docstring for binder
    """
    def __init__(self, path=None, check=None, **kwargs):
        """@todo: Docstring for init method.

        /path=None/ @todo
        /**cfg/ @todo

        """

        self.modified = False
        self._init_load_binder(path, check)

    def _init_load_binder(self, path, check) -> None:
        """
        @todo: Docstring for _init_load_binder
        """
        if check == None:
            if path == None:
                console.print(
                    Panel.fit('No notes directory was given!', style='error'))

            path_path = Path(os.path.expandvars(path))
            # console.print('Path to notes directory is [bold]', path_path, style='info')
            if not (path_path / 'index.md').exists():
                console.print(
                    Panel.fit('An invalid notes directory was given!',
                              style='error'))

        self.path = path_path

    def collect_preambles(self) -> List:
        """
        @todo: Docstring for note_generator
        """
        return [
            Note(self, note_path).parse_preamble()
            for note_path in list(self.path.glob('*.md'))
            if Note(self, note_path).parse_preamble() is not None
        ]
        # console.print(list(self.path.glob('*.md')))

    def search_notes(self, tags, dates=None) -> List[str]:
        """
        @todo: Docstring for search_notes
        """
        # console.print(self.collect_preambles())
        # console.print(tags)
        # notes = self.collect_preambles()
        # console.print(notes)
        if tags is None and dates is None:
            console.print('No valid query was given to search notes with!',
                          style='warning')
            return
        if tags is not None:
            notes = [
                note for note in [
                    tagged_note for tagged_note in self.collect_preambles()
                    if 'tags' in tagged_note.keys()
                ] if set([tag.lower()
                          for tag in tags]).issubset(set(note['tags']))
            ]
        # console.print(notes)
        return notes

    def sort_by_tag(self, notes: List) -> List:
        """
        @todo: Docstring for sort_by_tag
        """
        pass

    def sort_by_date(self, notes: List) -> List:
        """
        @todo: Docstring for sort_by_date
        """
        def date_key(note):
            return [
                note['date'][key] for key in
                ['second', 'minute', 'hour', 'day', 'month', 'year'][::-1]
            ]

        notes = sorted(notes, key=date_key)
        return notes

    def preamble_date_to_string(self, preamble_date) -> str:
        """
        @todo: Docstring for preamble_date_to_string
        """
        return preamble_date['year'] + preamble_date['month'] + preamble_date[
            'day'] + '-' + preamble_date['hour'] + 'h' + preamble_date[
                'minute'] + 'm' + preamble_date['second'] + 's_'

    def render_date_dict(self, date_dict):
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
        rendered_date = date_dict['day'] + ' ' + numeric_to_name.get(
            date_dict['month']) + ' ' + date_dict['year']
        return rendered_date

    def tabularize(self, TAGS=None, DATES=None, SORT=None, **opts) -> None:
        """
        @todo: Docstring for tabularize
        """
        notes = self.search_notes(TAGS, DATES)
        notes = self.sort_by_date(notes)
        # console.print(notes)
        table_title = 'notes '
        if TAGS is not None:
            table_title += 'tagged with: ' + ', '.join(TAGS)
        if DATES is not None:
            table_title += DATES
        table = Table(title=table_title)
        table.add_column('tags', width=60)
        table.add_column('date')
        table.add_column('bib')
        table.add_column('title')
        # console.print(table_title)
        # console.print(table_title, style='info')
        for note in notes:
            if 'bib' not in note.keys():
                note['bib'] = 'None'
            else:
                match = re.match(r'@.*\{(.*),', note['bib'])
                note['bib'] = match.group(1)
            table.add_row(', '.join(note['tags']),
                          self.render_date_dict(note['date']), note['bib'],
                          note['title'])
        console.clear()
        console.print(table)
        # Prompt.ask("Continue?", choices=['y', 'n'])

    def read(self, TAGS=None, DATES=None, SORT=None, **opts) -> None:
        """
        @todo: Docstring for read
        """

        notes = self.search_notes(TAGS, DATES)
        if SORT is not None:
            notes = self.sort_by_tag(notes)
        else:
            notes = self.sort_by_date(notes)

        notes_lines = [
            Note(
                self,
                self.preamble_date_to_string(preamble['date']) +
                preamble['title']).read_lines() for preamble in notes
        ]

        if opts['-l']:
            console.print(
                'vnnv read -l =', opts['-l'], ':',
                'Converting the lines of all queried notes to latex')
            lines = ''.join(markdown_to_latex(notes_lines))
            console.print(lines)
            latex_build_dir = Path(
                os.path.expandvars(cfg['latex']['build_dir']))
        else:
            console.print(
                Panel.fit(
                    'Give a valid option for output format! For example: vnnv read -l ...',
                    style='error'))
        return lines

    def collect_flashcards(self, TAGS=None, **opts) -> List[str]:
        """
        @todo: Docstring for collect_flashcards
        """
        if TAGS is not None:
            notes = self.search_notes(TAGS)

        flash_card_dicts = [
            Note(
                self,
                self.preamble_date_to_string(preamble['date']) +
                preamble['title']).parse_vnnv_anki_codeblocks()
            for preamble in notes
        ]

        if len(flash_card_dicts) == 0:
            self.modified = True

        return flash_card_dicts

        # console.print(lines)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.modified:
            console.print('remember to save changes and sync to github')

    def add_note(self, *args, **kwargs):
        return

    def delete_note(self, *args, **kwargs):
        return


# print(my_binder.base)
# width, height = shutil.get_terminal_size()
# print(width, height)
if __name__ == '__main__':
    my_binder = Binder(**cfg)
    # console.print(my_binder.note_list())
    # console.print(my_binder.collect_preambles())
    # print(my_binder.note_generator())
    my_binder.tabularize(['MollerStruth'])
