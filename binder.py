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
from vnnv.convert import vnnv_flashcards_to_apy
from vnnv.utilities import call, cd, pdflatex, apy_add_from_file, render_rmarkdown


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

    def collect_notes_with_preambles(self) -> List:
        """
        @todo: Docstring for note_generator
        """
        return [
            note for note in [
                Note(self, note_path)
                for note_path in list(self.path.glob('*md'))
            ] if note.preamble is not None
        ]
        # console.print(list(self.path.glob('*.md')))

    def search_notes(self, tags=None, dates=None, **opts) -> List[str]:
        """
        @todo: Docstring for search_notes
        """
        # console.print(self.collect_notes_with_preambles())
        # console.print(tags)
        # notes = self.collect_notes_with_preambles()
        # console.print(notes)
        if tags is None and dates is None:
            console.print('No valid query was given to search notes with!',
                          style='warning')
            raise SystemExit
        if tags is not None:
            notes = [
                tagged_note for tagged_note in [
                    note for note in self.collect_notes_with_preambles()
                    if 'tags' in note.preamble.keys()
                ] if set([tag.lower() for tag in tags]).issubset(
                    set(tagged_note.preamble['tags']))
            ]
            # notes = [
            #     note for note in [
            #         tagged_note
            #         for tagged_note in self.collect_notes_with_preambles()
            #         if 'tags' in tagged_note.keys()
            #     ] if set([tag.lower()
            #               for tag in tags]).issubset(set(note['tags']))
            # ]
        # # console.print(notes)
        return notes

    def preamble_to_note(self, preambles) -> List:
        """
        @todo: Docstring for preamble_to_note
        """
        notes = [
            Note(
                self,
                self.preamble_date_to_string(preamble['date']) +
                preamble['title']) for preamble in preambles
        ]
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
                note.preamble['date'][key] for key in
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

    def tabularize(self, notes, **opts) -> None:
        """
        @todo: Docstring for tabularize
        """
        notes = self.sort_by_date(notes)
        # console.print(notes)
        table_title = 'notes '
        if opts['tags'] is not None:
            table_title += 'tagged with: ' + ', '.join(opts['tags'])
        if opts['dates'] is not None:
            table_title += opts['dates']
        table = Table(title=table_title)
        table.add_column('tags', width=60)
        table.add_column('date')
        table.add_column('bib')
        table.add_column('title')
        # console.print(table_title)
        # console.print(table_title, style='info')
        row = {}
        for note in notes:
            if 'bib' not in note.preamble.keys():
                row['bib'] = 'None'
            else:
                match = re.match(r'@.*\{(.*),', note.preamble['bib'])
                row['bib'] = match.group(1)
                row['title'] = note.preamble['title']
            row['tags'] = note.preamble['tags']
            table.add_row(', '.join(row['tags']), note.render_date_dict(),
                          row['bib'], note.preamble['title'])
        console.clear()
        console.print(table)
        # Prompt.ask("Continue?", choices=['y', 'n'])

    def read_in_markup(self, notes, latex=None, rmarkdown=None, sort=None, **opts) -> None:
        """
        @todo: Docstring for read
        """
        # if opts['-l']:
        #     pdflatex(lines)

        if sort is not None:
            notes = self.sort_by_tag(notes)
        else:
            notes = self.sort_by_date(notes)

        lines_and_links = [(note.read_lines(), note.preamble['links']) for note in notes]

        if latex:
            console.print(
                'vnnv read -l =', latex, ':',
                'Converting the lines of all queried notes to latex')
            lines = markdown_to_latex(lines_and_links)
            # console.print(lines)
            pdflatex(lines)

            # latex_build_dir = Path(
            #     os.path.expandvars(cfg['latex']['build_dir']))
        if rmarkdown:
            console.print(
                'vnnv read -r =', rmarkdown, ':',
                'Rendering the lines of all queried notes to rmarkdown pdf')
            lines = [''.join(note) for note, links in lines_and_links]
            lines = ''.join(lines)
            render_rmarkdown(lines)
        else:
            console.print(
                Panel.fit(
                    'Give a valid option for output format! For example: vnnv read -l ...',
                    style='error'))
            raise SystemExit
        return lines

    def collect_flashcards(self, notes, **opts) -> List[str]:
        """
        @todo: Docstring for collect_flashcards
        """

        flash_card_dicts = []
        parsed_cards = [
            note.parse_vnnv_anki_codeblocks()
            for note in notes
        ]
        for card in parsed_cards:
            if isinstance(card, list):
                flash_card_dicts += card
            else:
                flash_card_dicts += [card]

        # if len(flash_card_dicts) != 0:
        #     self.modified = True

        return flash_card_dicts

    def give_notes_to_apy(self, flashcards) -> None:
        """
        @todo: Docstring for give_cards_to_apy
        """
        lines = vnnv_flashcards_to_apy(flashcards)
        apy_add_from_file(lines)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.modified:
            console.print('remember to save changes and sync to github')
            with cd(self.path):
                call(['git', 'add', '.'])
                call(['git', 'add', '-u'])
                call(['git', 'commit'])

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
    # console.print(my_binder.collect_notes_with_preambles())
    # print(my_binder.note_generator())
    my_binder.tabularize(['MollerStruth'])
