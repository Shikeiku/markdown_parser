# from neovim_plugins.markdown_parser.fence import Fence
class EnterPythonFence():
    """
    Sequence of actions after pressing enter on a python block in markdown.

    - Write lines to the scratch.py file
    - Change the buffer to the scratchfile
    - Toggle repl
    """
    def __init__(self, nvim, fences):
        self.nvim = nvim
        self.buf = self.nvim.current.buffer
        self.lines = self.nvim.current.buffer[:]
        self.fences = fences
        self.scratch = '/Users/mike/.data/nvim/scratch_files/scratch.py'

    def scratch_write(self):
        """
        Gets the content of the block from lines and writes it to the
        scratchfile
        """
        start, end = self.fences['upper']['row'], self.fences['lower']['row']
        contents = self.lines[start:end - 1]
        with open(self.scratch, 'w') as scratch:
            for line in contents:
                scratch.write(line + '\n')
        return 'wrote to scratch'

    def enter(self):
        self.scratch_write()
        self.nvim.command('let b:message="' + str() + '"')
        self.nvim.command('echo b:message')
