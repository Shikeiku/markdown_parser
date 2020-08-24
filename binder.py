import os
import re
import shutil
from pathlib import Path
from rich import print


class Binder():
    """
    Docstring for Binder
    """
    def __init__(self, base=None, **kwargs):
        """@todo: to be defined.

        :kwargs: @todo

        """

        self.modified = False

        self._init_load_filenames(base)

        # self.filenames_to_title = {
        #     f['name']: f['title']
        #     for f in filenames.keys()
        # }

    def _init_load_filenames(self, base):
        """
        @todo Docstring for load_filenames
        """

        basepath = Path(base)
        filenames = list(basepath.glob('*.md'))
        return filenames

    def filename_to_date_and_title(self, filenames)
        file_date_title = {
            f: {
                'date': f"{}",
                'title': f
            }
            for f in filenames
        }
        print(file_date_title)

        return file_date_title

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.modified:
            print('remember to save changes and sync to github')
    
    def add_note(self, *args, **kwargs):
        return

    def delete_note(self, *args, **kwargs):
        return

    def list_notes(self, *args, **kwargs):
        return



cfg = {'base': '/Users/mike/Documents/markdown_notes'}

my_binder = Binder(**cfg)
# print(my_binder.base)
width, height = shutil.get_terminal_size()
print(width, height)
