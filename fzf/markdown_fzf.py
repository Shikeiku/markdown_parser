import re
from datetime import datetime
from pathlib import Path
import shutil


class Markdown_fzf():
    """
    Contains all fzf sink functions
    """
    def __init__(self, nvim):
        self.nvim = nvim
        self.notes_dir = '/Users/mike/Documents/markdown_notes/'
        self.images_dir = '/Users/mike/Documents/markdown_images/'
        self.img = ['.jpeg', '.png', '.jpg', '.svg', '.pdf']

    def markdown_tag_sink(self, lines):
        """
        Opens the selected tag file for the tag fzf searcher.
        """
        try:
            fzf_string = lines[0][0]
            # self.nvim.command(':echo "' + fzf_string + '"')
            fzf_list = re.sub(r'\s+', r' ', fzf_string)
            fzf_list = fzf_list.split(' ')
            self.nvim.command(':cd %:h')
            match = re.match('^@.*', fzf_list[-2])
            parent = '/Users/mike/Documents/markdown_notes/'

            if match:
                self.nvim.command(':e ' + parent + fzf_list[0])
            else:
                self.nvim.command(':e ' + parent + fzf_list[-2] + fzf_list[0])
        except:
            pass

    def markdown_note_sink(self, lines):
        """
        Makes a formatted link to the note selected in the fzf search
        """
        NOTE_REGEX = '(?P<parent>\/[a-zA-Z0-9_\/\.\s\'\"\-]+\/)(?P<date>[\dhm\-]*s?\_?)(?P<name>[a-zA-Z0-9_\/\.\s\'\"\-]+(\.\w+)?)[:0-9]{0,3}(?P<anchor>#[a-zA-Z0-9_\/\.\s\'\"]+(?!\]))?'
        internal_parent = self.notes_dir
        link = ''
        try:
            fzf_string = lines[0][0]
            link_info = re.search(NOTE_REGEX, fzf_string)
            link_info = link_info.groupdict()

            if link_info['parent'] != internal_parent:
                link_info['anchor'] = ''
                if link_info['date']:
                    pass
                else:
                    link_info['date'] = ''
                suffix = re.findall(r'.*(\.[a-z]+$)', link_info['name'])
                if suffix != []:
                    if suffix[0] in self.img:
                        now = datetime.now()
                        dt_string = now.strftime("%Y%m%d-%Hh%Mm%Ss_")

                        date_check = re.search(
                            r'^(\d+\-\d\dh\d\dm\d\ds\_)(.*)',
                            link_info['date'])
                        if not date_check:
                            old_date = link_info['date']
                            move_image = True
                            link_info['date'] = dt_string + link_info['date']
                        else:
                            old_date = None
                        # Move image to markdown_images and put a date string in
                        # front of the name

                        link += '!'
                else:
                    pass
            elif link_info['parent'] == internal_parent:
                link_info['parent'] = ''
                if not link_info['anchor']:
                    link_info['anchor'] = ''

            try:
                if move_image:
                    original = Path(link_info['parent'] + old_date +
                                    link_info['name'])
                    if original.exists():
                        target = Path(self.images_dir + link_info['date'] +
                                      link_info['name'])
                        shutil.copy(str(original), str(target))
                    link_info['name'] = link_info['name'].replace(' ', '\ ')
                    link += '[' + link_info[
                        'name'] + '](' + self.images_dir + link_info[
                            'date'] + link_info['name'] + ')'

            except UnboundLocalError:
                link_info['name'] = link_info['name'].replace(' ', '\ ')
                if len(link_info['date']) < 19:
                    link += '[' + link_info['date'] + link_info[
                        'name'] + link_info['anchor'] + '](' + link_info[
                            'parent'] + link_info['date'] + link_info[
                                'name'] + link_info['anchor'] + ')'
                else:
                    link += '[' + link_info['name'] + link_info[
                        'anchor'] + '](' + link_info['parent'] + link_info[
                            'date'] + link_info['name'] + link_info[
                                'anchor'] + ')'

            if not self.nvim.current.line:
                self.nvim.current.line = link
            else:
                self.nvim.command(':echo "the line is not empty,'+\
                                'so i didn\'t place a link here."')

        except:
            pass

    def fzf_tag_linker(self, lines):
        """
        Similar to markdown_tag_sink, but instead links to selected files. So
        we know that the fzf search with multiple selections returns just a
        list with all selections.
        """
        try:
            # self.nvim.command(':echo "' + str(lines) + '"')
            links = []
            for line in lines[0]:
                note_info = re.sub(r'\s+', r' ', line)
                note_info = note_info.split(' ')
                # self.nvim.command(':echo "' + str(note_info) + '"')
                match = re.match('^@.*', note_info[-2])
                if not match:
                    links.append('[' + note_info[0] + ']' + '(' +
                                 note_info[-2] + note_info[0] + ')')
                else:
                    links.append('[' + note_info[0] + ']' + '(' +
                                 note_info[0] + ')')

            # parent = '/Users/mike/Documents/markdown_notes/'

            pos = self.nvim.current.window.cursor
            currentline = pos[0]
            self.nvim.current.buffer[currentline:currentline] = links
        except:
            pass
