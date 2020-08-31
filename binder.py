import os
import re
import shutil
from typing import List, Dict
from pathlib import Path

from rich.panel import Panel
from rich.table import Table

from vnnv.note import Note
from vnnv.config import cfg, console


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

    def preambles_to_list(self) -> List:
        """
        @todo: Docstring for note_generator
        """
        return [
            Note(self, note_path).preamble
            for note_path in list(self.path.glob('*.md'))
            if Note(self, note_path).preamble is not None
        ]
        # console.print(list(self.path.glob('*.md')))

    def tabularize_notes(self, query) -> None:
        """
        @todo: Docstring for tabularize_notes
        """
        table_title = 'notes for query: ' + query.split()
        table = Table(title=table_title)
        pass

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.modified:
            print('remember to save changes and sync to github')

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
    console.print(my_binder.preambles_to_list())
    # print(my_binder.note_generator())
