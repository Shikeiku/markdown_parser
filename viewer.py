from pathlib import Path
import sys
import re
import subprocess as sub


class LaTeX_viewer():
    """
    Reads the markdown file and latexifies it
    """
    def __init__(self, nvim):
        self.nvim = nvim
        self.scratch = Path(
            '/Users/mike/.data/nvim/scratch_files/LaTeX/latex_view/view.tex')
        self.fencenames = ['LaTeX', 'python', 'anki-cloze', 'anki-img']
        self.current_list = {'value': 0}
        self.regex_dict = {
            'chapter': r'^#\s(?P<name>.*)',
            'section': r'^##\s(?P<name>.*)',
            # 'subsection': r'^###\s(?P<name>.*)',
            'subsubsection': r'^###\s(?P<name>.*)',
            'paragraph': r'^####\s(?P<name>.*)',
            'subparagraph': r'^#####\s(?P<name>.*)',
            'code': r'(?P<name>^```.*)',
            'hide': r'(?P<name>^([lL][iI][nN][kK])|^([tT][aA][gG][sS]))',
            'inline_link': r'^\!\[(?P<name>.*?)\]\((?P<path>.*?)\)',
            'hyper_link': r'^\[(?P<name>.*?)\]\((?P<path>.*?)\)',
            'list': r'^((?P<star>\*[\s]{1,3})|(?P<number>^(\d\.)[\s]{1,3}))(?P<name>.*)'
        }
        self.function_dict = {
            'chapter': self.latexSections,
            'section': self.latexSections,
            'subsection': self.latexSections,
            'subsubsection': self.latexSections,
            'paragraph': self.latexSections,
            'subparagraph': self.latexSections,
            'code': self.codeBlock,
            'hide': self.deleteLine,
            'inline_link': self.inlineLink,
            'hyper_link': self.hyperLink,
            'list': self.listBlock
        }
        self.code_dict = {
            'LaTeX': {
                'begin': '',
                'end': ''
            },
            'python': {
                'begin': '\\begin{listings}\n',
                'end': '\\end{listings}\n'
            },
            'anki-cloze': {
                'begin': '\\begin{comment}\n',
                'end': '\\end{comment}\n'
            },
            'anki-img': {
                'begin': '\\begin{comment}\n',
                'end': '\\end{comment}\n'
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

    def listBlock(self, line):
        line_dict = line[1].groupdict()
        if self.current_list['value'] == 0:
            if line_dict['star']:
                line = '\\begin{itemize}\n' + '\\item ' + line_dict['name']
                self.current_list = {'value': 1, 'type': 'itemize'}
            elif line_dict['number']:
                line = '\\begin{enumerate}\n' + '\\item ' + line_dict['name']
                self.current_list = {'value': 1, 'type': 'enumerate'}
        else:
            line = '\\item ' + line_dict['name']
        return line

    def deleteLine(self, line):
        line = ''
        return line

    def lineNotDefined(self, line):
        if self.current_list['value'] == 1:
            LIST_END_REGEX = r'^(\W)|^(?![\s\S]|^(\n))'
            match = re.search(LIST_END_REGEX, line.strip())
            if match:
                line = '\n\\end{'+self.current_list['type']+'}\n' + line
                self.current_list['value'] = 0
        return line

    def latexSections(self, named_target):
        line = '\\' + named_target[0] + '{' + named_target[1].group(
            'name') + '}\n'
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

    def inlineLink(self, line):
        link_dict = line[1].groupdict()
        # line = link_dict['path']
        PDF_REGEX = r'.*\.pdf$'
        match = re.search(PDF_REGEX, link_dict['path'])
        if match:
            line = '\n\\includepdf[scale=0.92, pages=-, pagecommand=\subsection{' + link_dict[
                'name'] + '}, offset=0 -2cm]{' + link_dict['path'].replace(
                    '\ ', ' ') + '}\n'
            # line = '\n\\includepdf[scale=0.8, pages=-, pagecommand={ }, offset=0 -3cm]{' + link_dict['path'].replace( '\ ', ' ') + '}\n'
        else:
            line = '\n\\begin{figure}[h!]\n\centering\n' + '\\fbox{\\includegraphics[width=\\textwidth, height=0.3\\textheight, keepaspectratio]{' + link_dict[
                'path'].replace('\ ', ' ') + '}}\n' + '\\caption{' + link_dict[
                    'name'] + '}\n' + '\\end{figure}\n'
        return line

    def hyperLink(self, line):
        # link_dict = line[1].groupdict()
        # line = '\href{file://' + link_dict['path'] + '}{' + link_dict[
        #     'name'] + '}\n'
        line = ''
        return line
    
    def typeset(self, line):
        BOLD_REGEX = r'\*\*([\w+\s]*?)\*\*'
        ITALIC_REGEX = r'\*([\w+\s]*?)\*'
        UNDERLINE_REGEX = r'\_([\w+\s]*?)\_'
        line = re.sub(BOLD_REGEX, r'\\textbf{\1}', line)
        line = re.sub(ITALIC_REGEX, r'\\textit{\1}', line)
        line = re.sub(UNDERLINE_REGEX, r'\\underline{\1}', line)
        return line

    def view_latex(self, options='current'):
        """
        Scans over the current file and uses the methods in the class to
        convert the markdown to a latex file
        """
        if options == 'current':
            lines = self.nvim.current.buffer[:]

        elif 'getTaggedFiles' in options.keys():
            print('found the tags flow')
            files = options['getTaggedFiles']
            print('these are the files in the viewer function,', files)
            lines = []
            for file_name in files:
                path = '/Users/mike/Documents/markdown_notes/' + file_name
                with open(path) as p:
                    lines += p.readlines()
            # print(lines)
            # raise SystemExit

        for i in range(len(lines)):
            target = self.latexRegexDictionary(lines[i])
            function, named_target = self.latexFunctionDictionary(target)
            lines[i] = function(named_target)
            lines[i] = self.typeset(lines[i])

            # if self.code_block(lines[i]):
            #     lines[i], code_block = self.code_block(lines[i])

        if options == 'current':
            self.scratch = Path(
            '/Users/mike/.data/nvim/scratch_files/LaTeX/scratch.tex')

        with open(self.scratch, 'w') as s:
            for line in lines:
                if options != 'current':
                    s.write(line)
                else:
                    s.write(line + '\n')


usage_string = "not implemented yet @todo"
manual_string = "not implemented yet @todo"


def showUsage():
    print(usage_string)


def orderChapters(tagged_dict):
    CHAPTER_REGEX = r'chapter(?P<chapter>[\d]*)'
    # print(tagged_dict)
    # tagged_files_dict = tagged_dict['getTaggedFiles']
    ordered_file_list = []
    chapters = []
    for note_file, tags in tagged_dict.items():
        # print(tags)
        for tag in tags:
            chapter = re.search(CHAPTER_REGEX, tag)
            if chapter:
                chapter = chapter.groupdict()['chapter']
                chapter = int(chapter)
                if chapters != []:
                    for i in range(len(chapters)):
                        if chapters[i] < chapter:
                            insert = i
                    chapters.insert(insert + 1, chapter)
                    ordered_file_list.insert(insert + 1, note_file)
                else:
                    chapters.append(chapter)
                    ordered_file_list.append(note_file)
        # print(chapters)
        # print(ordered_file_list)
    return ordered_file_list


def getTaggedFiles(tag_opt):
    # print(tag_opt)
    TAGS_FILE = Path('/Users/mike/Documents/markdown_notes/tags')
    TAG_REGEX = r'{(?P<tags>.*)}'
    FILE_REGEX = r'(?P<file>[^\/\s]*.md)'
    RETURN_DICT = {}
    with open(str(TAGS_FILE)) as t:
        lines = t.readlines()
        for line in lines:
            tag_match = re.search(TAG_REGEX, line)
            file_match = re.search(FILE_REGEX, line)
            if tag_match and file_match:
                tags = tag_match.groupdict()['tags']
                tags = tags.replace(' ', '').split(',')
                tagged_file = file_match.groupdict()['file']
                # print(tags)
                # print(tagged_file)
                for tag in tag_opt:
                    if tag in tags:
                        RETURN_DICT[tagged_file] = tags
    RETURN_DICT = orderChapters(RETURN_DICT)
    return RETURN_DICT


def getOptions(args_list):
    """
    Parsers the options, and catches the return value of the function that
    processes the option flag. 

    For example, the -t flag calls the getTaggedFiles function, which returns
    eventually an ordered list of files that are used to build the latex
    document.
    """
    FLAG_REGEX = r"-(?P<option>h?t?)|(--help)"
    OPTION_DICT = {'h': showUsage, 't': getTaggedFiles}
    RETURN_DICT = {}
    while args_list:
        args_list = args_list[::-1]
        # print(args_list)
        arg = args_list.pop()
        match = re.search(FLAG_REGEX, arg)
        if match:
            print('\nfound an option flag in the arguments,\n')
            groups = match.groupdict()
            for opt in groups['option']:
                # print(opt)
                function = OPTION_DICT.get(opt)
                if opt == 't':
                    print('Using the -t option,\n')
                    tag_opt = []
                    # print(args_list)
                    for arg in args_list:
                        # print(arg)
                        match = re.search(FLAG_REGEX, arg)
                        if not match:
                            tag_opt.append(arg)
                    RETURN_DICT[function.__name__] = function(tag_opt)
                    print(
                        f'Giving the tags {"".join(tag_opt)} to {function.__name__}\n'
                    )
    print(f'Caught the following from the option functions: \n{RETURN_DICT}\n')
    return RETURN_DICT


if __name__ == "__main__":
    # print(f"Name of the script      : {sys.argv[0]=}")
    # print(f"Arguments of the script : {sys.argv[1:]=}")
    try:
        args = sys.argv[1:]
    except IndexError:
        raise SystemExit(usage_string)

    viewer = LaTeX_viewer('non-nvim')
    option_dict = getOptions(args)
    viewer.view_latex(options=option_dict)

    sub.run([
        'bash',
        '/Users/mike/Documents/code/python/my_modules/neovim_plugins/markdown_parser/pdflatex.sh'
    ])
    sub.run([
        'open', '-a', 'Skim',
        '/Users/mike/.data/nvim/scratch_files/LaTeX/latex_view/latex_wrapper.pdf'
    ])
