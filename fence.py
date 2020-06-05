import re
import neovim_plugins.markdown_parser.fence_latex as latex
import neovim_plugins.markdown_parser.fence_python as fence_python


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
        self.fencenames = ['LaTeX', 'python', 'anki_cloze']
        # Probably will move this
        #
        # self.currently_writing_types = [
        #     '<++Writing LaTeX++>', '<++Writing anki-cloze flashcard++>',
        #     '<++Writing python++>'
        # ]

    def testfunction(self, *args):
        self.nvim.command(':echo "hello"')

    def is_link(self):
        """
        Checks if the current line matches the given link regex
        """
        LINKREGEX = r'!?\[(.+)\]\((https?:\/\/)?([a-zA-Z0-9_\-\/\:\.]+?(\.\w+)?)([\"\w+\d+\s]+)?(#\s*[a-zA-Z0-9_\.\s\'\"]+)?\)'
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
                return url
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
            self.nvim.command('let b:message="Starting the link class"')
            self.nvim.command('echo b:message')
        elif self.return_fences():
            fences = self.return_fences()
            fencetypes = {
                'LaTeX': latex.FenceLatex(),
                'python': fence_python.EnterPythonFence(self.nvim, fences),
                'anki-cloze': latex.FenceAnki()
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
