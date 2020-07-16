import re


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
        self.writing_placeholder = '<++Writing python++>'

    def currently_writing(self):
        """
        Shows that the scratch file has not been returned to the markdown file
        yet.
        """
        start, end = self.fences['upper']['row'], self.fences['lower']['row']
        del self.buf[start - 1:end]
        self.buf[start - 1] = self.writing_placeholder

    def scratch_write(self):
        """
        Gets the content of the block from lines and writes it to the
        scratchfile
        """
        start, end = self.fences['upper']['row'], self.fences['lower']['row']
        contents = self.lines[start:end - 1]
        with open(self.scratch, 'w') as scratch:
            for line in contents:
                line = re.sub(r'^( #)', r'#', line)
                scratch.write(line + '\n')
        return 'wrote to scratch'

    def open_buffers(self):
        # md_buffer = self.nvim.current.buffer

        self.nvim.command(':w')
        self.nvim.command(':e ' + self.scratch)

        # self.nvim.command('let b:message="' + str(self.buf) + '"')
        # self.nvim.command('echo b:message')

    def enter(self):
        self.currently_writing()
        self.scratch_write()
        self.open_buffers()
