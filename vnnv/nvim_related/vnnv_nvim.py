import pynvim
from pathlib import Path

from vnnv.binder import Binder
# -- How to add a comment
# pynvim.plugin.command(name, nargs=0, complete=None, range=None, count=None, bang=False, register=False, sync=False, allow_nested=False, eval=None)

# --- How to add an autocommand
# pynvim.plugin.autocmd(name, pattern='*', sync=False, allow_nested=False, eval=None)[source]


@pynvim.plugin
class VnnvNeovimPortal():
    """
    Here the functions and command (mainly commands) for my few markdown
    functions are stored.

    Auto-Commands:
    - EnterFence, when pressing enter in markdown files this command should
      occur.
    - CloseFence, closes the buffer and returns to the buffer where the
      EnterFence was called.

    Editor-Commands:
    - Flashcards, prepares the anki cards for import into Anki
    - NewNote, make a new note with the datetime str in front

    Function:
    - Markdowntags, takes the output of an fzf search against the tags in the
      markdown notes
    - Markdownlinks, thakes the output of a fzf search in hte documents folder
    - Markdownnotes
    """
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('vnnvFzF')
    def MarkdownLinkTags(self, *args):
        if 'link_tag' in args:
            pass
        elif 'open' in args:
            pass
        else:
            pass
        my_fzf = fzf.Markdown_fzf(self.nvim)
        my_fzf.fzf_tag_linker(lines)
