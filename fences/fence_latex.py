class FenceLatex():
    """
    Issues the commands for opening a latex markdown block.

    - Write the block contents to the scratch.tex file
    - Open the scratch.tex file in the current buffer
    - Start vimtex autocompile
    """
    def __init__(self, nvim, fences):
        self.nvim = nvim
        self.fences = fences
        self.buf = self.nvim.current.buffer
        self.lines = self.nvim.current.buffer[:]
        self.scratch = '/Users/mike/.data/nvim/scratch_files/LaTeX/scratch.tex'
        self.writing_placeholder = '<++Writing LaTeX++>'

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
                scratch.write(line + '\n')
        return 'wrote to scratch'

    def open_buffers(self):
        # md_buffer = self.nvim.current.buffer

        self.nvim.command(':e! ' + self.scratch)

        # Maybe later I can change this to not hard coded, using the window and
        # buffers lists in the nvim class
        self.nvim.command(':normal ,ll')

        # self.nvim.command('let b:message="' + str(self.buf) + '"')
        # self.nvim.command('echo b:message')

    def enter(self):
        self.currently_writing()
        self.scratch_write()
        self.open_buffers()


class FenceAnki():
    """
    Inherits things from fencelatex
    - Writes the anki block contents to the scratch_anki.tex file.
    - Opens vimtex autcompile
    """
    def __init__(self, nvim, fences):
        self.nvim = nvim
        self.fences = fences
        self.buf = self.nvim.current.buffer
        self.lines = self.nvim.current.buffer[:]
        self.divider = '<++divide cloze/prompt++>'
        self.scratch = '/Users/mike/.data/nvim/scratch_files/LaTeX/scratch.tex'
        self.writing_placeholder = '<++Writing Flashcard++>'

    def currently_writing(self):
        """
        Shows that the scratch file has not been returned to the markdown file
        yet.
        """
        start, end = self.fences['upper']['row'], self.fences['lower']['row']
        del self.buf[start - 1:end - 1]
        self.buf[start - 1] = self.writing_placeholder

    def scratch_write(self):
        """
        Gets the content of the block from lines and writes it to the
        scratchfile
        """
        start, end = self.fences['upper']['row'], self.fences['lower']['row']
        contents = self.lines[start:end - 1]
        if '<++divide cloze/prompt++>' not in contents:
            contents.append('<++divide cloze/prompt++>')
        with open(self.scratch, 'w') as scratch:
            for line in contents:
                scratch.write(line + '\n')
        return 'wrote to scratch'

    def open_buffers(self):
        # md_buffer = self.nvim.current.buffer

        self.nvim.command(':e ' + self.scratch)

        # Maybe later I can change this to not hard coded, using the window and
        # buffers lists in the nvim class
        # self.nvim.command(':normal ,ll')

        # self.nvim.command('let b:message="' + str(self.buf) + '"')
        # self.nvim.command('echo b:message')

    def enter(self):
        self.currently_writing()
        self.scratch_write()
        self.open_buffers()
