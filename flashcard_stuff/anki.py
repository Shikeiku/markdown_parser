from pathlib import Path
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

    def get_cards(self, note, lines):
        """
        Scans the file for cards to add to flash cards later, also for img
        cards checks if the file is in anki media, and if not it copies it
        there.
        """
        cloze_cards = []
        img_cards = []

        for i in range(len(lines)):
            card = ''
            anki_cloze = re.search(
                r'^(?P<upper_fence>\`\`\`(?P<name>anki-cloze))$', lines[i])
            anki_img = re.search(
                r'^(?P<upper_fence>\`\`\`(?P<name>anki-img))$', lines[i])
            if anki_cloze:
                lines[i] = '```anki-cloze [ADDED]\n'
                for j in range(len(lines[i + 1:])):
                    end = re.search(r'(?P<end>^\`\`\`)', lines[i + 1 + j])
                    if end:
                        break
                    card = card + lines[i + 1 + j]
                cloze_cards.append(card)
            if anki_img:
                lines[i] = '```anki-img [ADDED]\n'
                for j in range(len(lines[i + 1:])):
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
                card = card.replace('\n',
                                    ' ').replace('<++divide cloze/prompt++>',
                                                 '\t')
                c.write(card)
                c.write('\n')

        with open(self.img_target, 'w') as i:
            for card in cards['img']:
                card = card.replace('\n',
                                    ' ').replace('<++divide prompt/img++> ',
                                                 '\t')
                i.write(card)
                i.write('\n')
