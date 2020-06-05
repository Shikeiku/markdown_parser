class FenceLatex():
    """
    Issues the commands for opening a latex markdown block.

    - Write the block contents to the scratch.tex file
    - Open the scratch.tex file in the current buffer
    - Start vimtex autocompile
    """


class FenceAnki(FenceLatex):
    """
    Inherits things from fencelatex
    - Writes the anki block contents to the scratch_anki.tex file.
    - Opens vimtex autcompile
    """
