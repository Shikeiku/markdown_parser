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

    def section(self, line):
        """
        Is called in the main function to transform lines with headers to
        latex chapters or sections
        """
        CHAPTER_REGEX = r'^#\s(?P<name>.*)'
        SECTION_REGEX = r'^##\s(?P<name>.*)'
        SUBSECTION_REGEX = r'^###\s(?P<name>.*)'
        SUBSUBSECTION_REGEX = r'^####\s(?P<name>.*)'
        PARAGRAPH_REGEX = r'^#####\s(?P<name>.*)'
        SUBPARAGRAPH_REGEX = r'^######\s(?P<name>.*)'

        chapter = re.search(CHAPTER_REGEX, line)
        section = re.search(SECTION_REGEX, line)
        subsection = re.search(SUBSECTION_REGEX, line)
        subsubsection = re.search(SUBSUBSECTION_REGEX, line)
        paragraph = re.search(PARAGRAPH_REGEX, line)
        subparagraph = re.search(SUBPARAGRAPH_REGEX, line)

        if chapter:
            line = r'\chapter{' + chapter.group('name') + '}'
        elif section:
            line = r'\section{' + section.group('name') + '}'
        elif subsection:
            line = r'\subsection{' + subsection.group('name') + '}'
        elif subsubsection:
            line = r'\subsubsection{' + subsubsection.group('name') + '}'
        elif paragraph:
            line = r'\paragraph{' + paragraph.group('name') + '}'
        elif subparagraph:
            line = r'\subparagraph{' + subparagraph.group('name') + '}'

        return line

    def code_block(self, line, current_block=None):
        """
        Transforms the lines containing fences of code blocks to latex listings
        things or deletes the fences if the fences are latex
        """
        CODE_BLOCK_REGEX = r'(?P<prefix>^```(?P<name>' + '|'.join(
            self.fencenames) + ')?)'

        # if :
        # else:
        #     return None

    def input_handler(self, relative_link):
        """
        Opens the markdown file in the link, and writes the contents of the
        file as part of the whole document.
        """

    def file_link(self, link):
        """
        Puts the path in the markdown file in a \href{...}
        """

    def citation(self, unknown):
        """
        Need to figure out how to write down a citation in markdown files

        probably could write \citealp
        """

    def image(self, link):
        """
        Link to an image should probably become a template where the absolute
        path to the image is substituted in
        """

    def write_contents(self, lines):
        """
        Takes the list that was build up with all other functions and writes 
        it to the scratch file
        """

    def view_latex(self):
        """
        Scans over the current file and uses the methods in the class to
        convert the markdown to a latex file
        """
        lines = self.nvim.current.buffer[:]
        for i in range(len(lines)):
            if self.section(lines[i]):
                lines[i] = self.section(lines[i])
            if self.code_block(lines[i]):
                lines[i], code_block = self.code_block(lines[i])

        with open(self.scratch, 'w') as s:
            for line in lines:
                s.write(line + '\n')
