from pathlib import Path
import shutil
import re


class BatchCards():
    """
    Searches through the current file or the whole note project for flashcard
    fences, and write the contents to the appropriate txt file for the flashcard
    to be imported right away manually into anki.
    """
    def __init__(self, nvim):
        """
        Should contain the nvim instance for the eas current buffer access, and
        hte path to the notes directory for the python script to scan the whole
        project for non-added flashcards.

        Should also have the paths to the anki batch text cards.
        """
        self.nvim = nvim
        self.md_notes = Path('/Users/mike/Documents/markdown_notes').glob(
            '**/[!\.]*')
        self.cloze_target = Path(
            '/Users/mike/Documents/markdown_notes/anki-cloze.txt')
        self.img_target = Path(
            '/Users/mike/Documents/markdown_notes/anki-img.txt')
        self.anki_media = Path(
            '/Users/mike/Library/Application Support/Anki2/User 1/collection.media'
        )

    def return_notes(self):
        """
        Returns all the cards in the file given in the argument. Will store the
        contents of the cards in a list of lists that will be written to the
        target in another function
        """
        notes = []
        for note in self.md_notes:
            dotfile = re.search(r'(?P<file_name>^\..*)', note.name)
            dotdir = re.search(r'(?P<file_name>^\..*)', note.parent.name)
            md_file = re.search(r'(?P<file_name>.*\.md$)', str(note))
            if not dotfile and not dotdir and md_file:
                notes.append(md_file.group('file_name'))

        # self.nvim.command('echo "' + str(notes) + '"')
        return notes

    def image_link(self, link):
        """
        Takes the line in the current loop and if it is a link to an image then
        it copies the linked image to the anki collection media path
        """
        # This is just what it returns
        link_info = link.groupdict()
        self.nvim.command('echo "' + str(link_info) + '"')
        html_link = r'<img src="' + link_info['url'] + '">'

        # Here I just put the image in anki collections media if it is not in
        # there yet
        file_in_md = Path(link_info['url'])
        file_in_anki = self.anki_media / file_in_md.name
        if file_in_anki.exists():
            pass
        else:
            shutil.copyfile(str(file_in_md), str(file_in_anki))

        return html_link

    def get_cards(self, note, lines):
        """
        Scans the file for cards to add to flash cards later, also for img
        cards checks if the file is in anki media, and if not it copies it
        there.
        """
        cloze_cards = []
        img_cards = []
        LINK_REGEX = r'^\!?\[(?P<name>.*)\]\((?P<url>.*)\)'
        CLOZE_REGEX = r'^(?P<upper_fence>\`\`\`(?P<name>anki-cloze))$'
        IMAGE_REGEX = r'^(?P<upper_fence>\`\`\`(?P<name>anki-img))$'

        for i in range(len(lines)):
            card = ''
            anki_cloze = re.search(CLOZE_REGEX, lines[i])
            anki_img = re.search(IMAGE_REGEX, lines[i])

            # I wan't for both the cards to convert markdownlinks to css links

            # Here operations for cloze cards go
            if anki_cloze:
                lines[i] = '```anki-cloze [ADDED]\n'
                for j in range(len(lines[i + 1:])):
                    link = re.search(LINK_REGEX, lines[i + 1 + j])
                    if link:
                        lines[i + 1 + j] = self.image_link(link)
                    end = re.search(r'(?P<end>^\`\`\`)', lines[i + 1 + j])
                    if end:
                        break
                    card = card + lines[i + 1 + j]
                cloze_cards.append(card)

            # Here operations for image cards go
            if anki_img:
                lines[i] = '```anki-img [ADDED]\n'
                for j in range(len(lines[i + 1:])):
                    link = re.search(LINK_REGEX, lines[i + 1 + j])
                    if link:
                        lines[i + 1 + j] = self.image_link(link)
                    end = re.search(r'(?P<end>^\`\`\`)', lines[i + 1 + j])
                    if end:
                        break
                    card = card + lines[i + 1 + j]
                img_cards.append(card)

        with open(note, 'w') as n:
            for line in lines:
                n.write(line)

        return cloze_cards, img_cards

    def write_flashcards(self):
        """
        Just writes flashcards
        """
        notes = self.return_notes()

        cards = {'img': [], 'cloze': []}
        for note in notes:
            with open(note, 'r') as n:
                lines = n.readlines()
            cloze_cards, img_cards = self.get_cards(note, lines)
            cards['cloze'] += cloze_cards
            cards['img'] += img_cards

        # self.nvim.command(':echo "' + str(cards['cloze']) + '"')
        with open(self.cloze_target, 'w') as c:
            for card in cards['cloze']:
                card = card.replace('\n', '<br>')
                card = card.replace('<++divide cloze/prompt++><br>', '\t')
                card = card.replace('{{', '{ {')
                card = card.replace('}}', '} }')
                card = re.sub(r'(\$.*?\$)', r'[latex]\1[/latex]', card)
                card = re.sub(r'(\\\[.*?\\\])', r'[latex]\1[/latex]', card)
                c.write(card)
                c.write('\n')

        with open(self.img_target, 'w') as i:
            for card in cards['img']:
                card = card.replace('\n', '<br>')
                card = card.replace('<++divide prompt/img++>', '\t')
                i.write(card)
                i.write('\n')
