from pathlib import Path
import re


class LaTeX_viewer():
    """
    Reads the markdown file and latexifies it
    """
    def __init__(self, nvim):
        self.nvim = nvim
        self.scratch = Path(
            '/Users/mike/.data/nvim/scratch_files/LaTeX/scratch.tex')
        self.fencenames = ['LaTeX', 'python', 'anki-cloze']
        self.regex_dict = {
            'chapter': r'^#\s(?P<name>.*)',
            'section': r'^##\s(?P<name>.*)',
            'subsection': r'^###\s(?P<name>.*)',
            'subsubsection': r'^####\s(?P<name>.*)',
            'paragraph': r'^#####\s(?P<name>.*)',
            'subparagraph': r'^######\s(?P<name>.*)',
            'code': r'(?P<name>^```.*)'
        }
        self.function_dict = {
            'chapter': self.latexSections,
            'section': self.latexSections,
            'subsection': self.latexSections,
            'subsubsection': self.latexSections,
            'paragraph': self.latexSections,
            'subparagraph': self.latexSections,
            'code': self.codeBlock
        }
        self.code_dict = {
            'LaTeX': {
                'begin': '\n',
                'end': '\n'
            },
            'python': {
                'begin': '\\begin{listings}',
                'end': '\\end{listings}'
            }
        }

    def latexRegexDictionary(self, line):
        """
        Is called in the main function to transform lines with headers to
        latex chapters or sections
        """
        for name, regex in self.regex_dict.items():
            target = re.search(regex, line)
            if target:
                named_target = [name, target]
                rv = named_target
                break
            else:
                rv = line
        return rv

    def latexFunctionDictionary(self, named_target):
        if isinstance(named_target, list):
            func = self.function_dict.get(named_target[0], self.lineNotDefined)
            return func, named_target
        else:
            return self.lineNotDefined, named_target

    def lineNotDefined(self, line):
        return line

    def latexSections(self, named_target):
        line = '\\' + named_target[0] + '{' + named_target[1].group(
            'name') + '}'
        return line
        # print('hello')

    def codeBlock(self, line):
        """
        Transforms the lines containing fences of code blocks to latex listings
        things or deletes the fences if the fences are latex
        """
        global current_code
        line = line[1].group('name')
        code_regex = r'(?P<prefix>^```(?P<name>' + '|'.join(
            self.fencenames) + '))'
        code_match = re.search(code_regex, line)
        if code_match:
            current_code = code_match.group('name')
            line = self.code_dict[code_match.group('name')]['begin']
        elif current_code in self.code_dict:
            line = self.code_dict[current_code]['end']
            current_code = ''
        return line

    def view_latex(self, files='current'):
        """
        Scans over the current file and uses the methods in the class to
        convert the markdown to a latex file
        """
        if files == 'current':
            lines = self.nvim.current.buffer[:]

        for i in range(len(lines)):
            target = self.latexRegexDictionary(lines[i])
            function, named_target = self.latexFunctionDictionary(target)
            lines[i] = function(named_target)

            # if self.code_block(lines[i]):
            #     lines[i], code_block = self.code_block(lines[i])

        with open(self.scratch, 'w') as s:
            for line in lines:
                s.write(line + '\n')
