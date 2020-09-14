import re
from neovim_plugins.mvn.link import Link_handler
# import neovim_plugins.markdown_parser.fence_latex as fence_latex
# import neovim_plugins.markdown_parser.fence_python as fence_python
# import neovim_plugins.markdown_parser.link as fence_link


class Fence():
    """
    The class that finds fences in your markdown file, and calls other
    classes that handle actions based on types of fences

    - Get line information of current buffer
    - Get row index
    - Check if there is a link on current line
    - If there is a link use link handler class
    - If there is no link then find fences
    - Scan for fences and store in dict
    - Determine fence type and call actions for fence type
    """
    def __init__(self, nvim):
        self.nvim = nvim
        self.buf = self.nvim.current.buffer
        self.lines = self.nvim.current.buffer[:]
        self.row = self.nvim.current.window.cursor[0]
        self.up = self.lines[self.row - 2::-1]
        self.down = self.lines[self.row:]
        self.fencenames = ['LaTeX', 'python', 'anki-cloze']
        # Probably will move this
        #
        # self.currently_writing_types = [
        #     '<++Writing LaTeX++>', '<++Writing anki-cloze flashcard++>',
        #     '<++Writing python++>'
        # ]

    def is_link(self):
        """
        Checks if the current line matches the given link regex
        """
        LINKREGEX = r'!?\[(.+)\]\((https?:\/\/)?([a-zA-Z0-9_\s\\\/\?\=\-\:\.]+?(\.[a-z]+)?)(\"[\w+\d+\s]*?\")?(#\s*[a-zA-Z0-9_\.\s\'\"]+)?\)'
        line = self.lines[self.row - 1]
        line = str(line).strip()
        link = re.search(LINKREGEX, line)
        if link:
            url = link.group(3)
            if link.group(2):
                http = link.group(2)
                link_info = {'http': http, 'link': url}
                return link_info
            else:
                suffix = link.group(4)
                link_info = {'link': url, 'suffix': suffix}
                return link_info
        else:
            return None

    def search_fence(self, direction):
        """
        Scans a file in the given direction, and if there is a line where the
        FENCEREGEX matches, the search stops and the fence name and row are
        returned
        """
        FENCEREGEX = '(?P<prefix>^```(?P<name>' + '|'.join(
            self.fencenames) + ')?)'
        steps = 1
        for i in range(len(direction)):
            fence = re.search(FENCEREGEX, direction[i])
            if fence:
                break
            steps += 1
        if fence:
            name = fence.group('name')
            prefix = fence.group('prefix')
            return prefix, name, steps
        else:
            return '', '', ''
        # self.nvim.command('echo "Found a fence fence!"')
        # self.nvim.command('let b:fence1=' + str(fence[1]))
        # self.nvim.command('echo b:fences1')

    def return_fences(self):
        fences = {}
        prefix, name, steps = self.search_fence(self.up)
        if name in self.fencenames:
            upper = {'fence': name, 'row': self.row - steps}
            fences['upper'] = upper
            #         self.nvim.command('let b:fence0="' + name + '"')
            #         self.nvim.command('echo b:fence0')
            prefix, name, steps = self.search_fence(self.down)
            if prefix and not name:
                lower = {'fence': prefix, 'row': self.row + steps}
                fences['lower'] = lower
            else:
                pass
        else:
            pass
        return fences

    def enterfence(self):
        """
        High-level function, defines the logic that happens when the :EnterFence
        is called.
        """
        # self.nvim.command('let b:row=' + str(self.down))
        # self.nvim.command('echo b:row')
        # fences = self.return_fences()
        if self.is_link():
            link = self.is_link()
            link_handler = Link_handler(self.nvim, link)

            link_handler.open_link()

        elif self.return_fences():
            fences = self.return_fences()
            fencetypes = {
                'LaTeX': fence_latex.FenceLatex(self.nvim, fences),
                'python': fence_python.EnterPythonFence(self.nvim, fences),
                'anki-cloze': fence_latex.FenceAnki(self.nvim, fences)
            }
            self.nvim.command('let b:message="' + str(fences) + '"')
            self.nvim.command('echo b:message')
            if fences['upper']['fence'] in fencetypes.keys():
                fencetypes[fences['upper']['fence']].enter()

            # self.nvim.command('let b:fences=' + str(fences))
            # self.nvim.command('echo b:fences')
            # self.nvim.command('let b:link=' + str(fences))
            # self.nvim.command('echo b:link')

        return ()

    def closefence(self, mdbuffer, fences):
        """
        Closes the fence and updates the markdown file.
        """
        contents = ['```' + fences['upper']['fence']]
        contents = contents + self.nvim.current.buffer[:]
        contents.append(fences['lower']['fence'])

        for i in range(len(contents)):
            contents[i] = re.sub(r'^#', r' #', contents[i])

        self.nvim.command(':wincmd o')
        self.nvim.current.buffer = self.nvim.buffers[mdbuffer]

        row = fences['upper']['row']
        self.nvim.current.buffer[row:row] = contents
        del self.nvim.current.buffer[row - 1]
        # contents = b[:]

        # b[row:row] = contents
        # self.nvim.command('let b:fences=' + str(type(fences)) + '')
        # self.nvim.command('echo b:fences')


class FenceLatex(Fence):
    """
    Issues the commands for opening a latex markdown block.

    - Write the block contents to the scratch.tex file
    - Open the scratch.tex file in the current buffer
    - Start vimtex autocompile
    """
    def __init__(self, fences, nvim=''):
        Fence.__init__(self, nvim)
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
        del self.buf[start - 1:end - 1]
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

        self.nvim.command(':w')
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


class FenceAnki(Fence):
    """
    Inherits things from fencelatex
    - Writes the anki block contents to the scratch_anki.tex file.
    - Opens vimtex autcompile
    """
    def __init__(self, fences, nvim=''):
        Fence.__init__(self, nvim)
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

        self.nvim.command(':w')
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


# from neovim_plugins.markdown_parser.fence import Fence
class EnterPythonFence():
    """
    Sequence of actions after pressing enter on a python block in markdown.

    - Write lines to the scratch.py file
    - Change the buffer to the scratchfile
    - Toggle repl
    """
    def __init__(self, fences, nvim=''):
        Fence.__init__(self, nvim)
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
