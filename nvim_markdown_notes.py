import pynvim
import neovim_plugins.markdown_parser.fence as fence
# import importlib
# importlib.reload(fence)

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
    - GoodByeFence, closes the buffer and returns to the buffer where the
      EnterFence was called.

    Editor-Commands:
    - AnkiCards, prepares the anki cards for import into Anki
    - NewNote, make a new note with the datetime str in front

    Function:
    - Tagsink, takes the output of an fzf search against the tags in the
      markdown notes
    - LinkSink, thakes the output of a fzf search in hte documents folder
    """
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('Testfunction', sync=True)
    def testfunction(self, args):
        self.fence.testfunction()

    @pynvim.command('EnterFence')
    def enterfence(self):
        self.fence = fence.Fence(self.nvim)
        self.fence.enterfence()

    @pynvim.function('Rtp', sync=True)
    def list(self):
        self.nvim.list_runtime_paths()
