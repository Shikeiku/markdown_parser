from typing import ClassVar, List, Dict, AnyStr
from pathlib import Path

from vnnv.binder import Binder
from vnnv.config import console, panel

class Note:
    """
    @todo: Docstring for Note
    """
    def __init__(self, binder: ClassVar, note: str):
        """@todo: to be defined."""
        self.b = binder
        self._init_preamble()

    def _init_preamble(self) -> None:
        """
        @todo: Docstring for _init_preamble
        """

        

if __name__ == '__main__':
    pass
