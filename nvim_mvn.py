import pynvim
from pathlib import Path

import neovim_plugins.mvn.fence as fence
import neovim_plugins.mvn.anki as anki
import neovim_plugins.mvn.fzf as fzf
import neovim_plugins.mvn.viewer as viewer
import neovim_plugins.mvn.new_note as new_note
import neovim_plugins.mvn.link as link

# -- How to add a comment
# pynvim.plugin.command(name, nargs=0, complete=None, range=None, count=None, bang=False, register=False, sync=False, allow_nested=False, eval=None)

# --- How to add an autocommand
# pynvim.plugin.autocmd(name, pattern='*', sync=False, allow_nested=False, eval=None)[source]


@pynvim.plugin
class MarkdownNeovimPortal():
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

    @pynvim.command('EnterFence')
    def enterfence(self):
        b = self.nvim.current.buffer
        self.nvim.command('let g:mdfence="' + str(b.number) + '"')
        instance = fence.Fence(self.nvim)
        fences = instance.return_fences()
        self.nvim.command('let g:fences=' + str(fences) + '')
        instance.enterfence()

    @pynvim.command('CloseFence')
    def closefence(self):
        b = self.nvim.eval('g:mdfence')
        b = int(b)
        i = self.nvim.eval('g:fences')
        instance = fence.Fence(self.nvim)
        instance.closefence(b, i)

    @pynvim.command('FlashCards')
    def flashcards(self):
        cards = anki.BatchCards(self.nvim)
        cards.write_flashcards()

    @pynvim.command('NewNote')
    def new_note(self):
        """
        Make a new note in the markdown_notes folder with a dt_string in front
        """
        new_note.newnote(self.nvim)

    @pynvim.command('LaTeXview')
    def latex_view(self):
        """
        Opens the current file and all linked files in latex mode.
        """
        LaTeX_view = viewer.LaTeX_viewer(self.nvim)
        LaTeX_view.view_latex()

    @pynvim.function('Markdowntags')
    def tag_sink_portal(self, lines):
        my_fzf = fzf.Markdown_fzf(self.nvim)
        my_fzf.markdown_tag_sink(lines)

    @pynvim.function('Markdownnotes')
    def note_sink_portal(self, lines):
        my_fzf = fzf.Markdown_fzf(self.nvim)
        my_fzf.markdown_note_sink(lines)

    @pynvim.function('MarkdownLinkTags')
    def MarkdownLinkTags(self, lines):
        my_fzf = fzf.Markdown_fzf(self.nvim)
        my_fzf.fzf_tag_linker(lines)
