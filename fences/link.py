class Link_handler():
    """
    Open the right programs for external links, and switch buffers for internal
    links.
    """
    def __init__(self, nvim, link):
        """
        Gets the current nvim information to switch the buffer to the link
        target if it is a file,

        And it is obvious why we need to get the link in the instance.

        Attributes also contain the relevant commands for opening different
        kinds of things
        """
        self.nvim = nvim
        self.link = link
        self.programs = {
            'md': ':e ',
            'pdf': ':!open -a Preview ',
            'img': ':!open -a Preview ',
            'http': ':!open -a WaterFox\ Current '
        }
        self.img = ['.jpeg', '.png', '.jpg', '.svg', '.pdf']

    def open_link(self):
        """
        Combines other functions in the class to open the correct file
        """
        # self.nvim.command('let b:message="' + 'hello' + '"')
        # self.nvim.command('echo b:message')
        link_info = self.link
        programs = self.programs
        images = self.img

        # self.nvim.command('let b:message="' + str(link_info) + '"')
        # self.nvim.command('echo b:message')

        # {'http': 'https://', 'link': 'www.youtube.com/watch?v=qULTwquOuT4'}

        if 'http' in link_info.keys():
            # self.nvim.command('let b:message="' +
            #                   str(programs['http'] + link_info['link']) + '"')
            # self.nvim.command('echo b:message')
            self.nvim.command(programs['http'] + '"' + link_info['http'] +
                              link_info['link'] + '"')
        elif link_info['suffix'] in images:
            self.nvim.command(programs['img'] + link_info['link'])
        elif link_info['suffix'] == '.md':
            self.nvim.command(programs['md'] + link_info['link'])
        elif link_info['suffix'] is None:
            self.nvim.command(programs['md'] + link_info['link'])
