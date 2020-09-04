import tempfile
import os
import subprocess
import readchar
import re

from typing import List
from subprocess import call

from vnnv.config import cfg, console


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
        self.savedPath = None

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def editor(filepath):
    """Use EDITOR to edit file at given path"""
    return call([os.environ.get('EDITOR', 'vim'), filepath])


def edit_text(input_text, prefix=None):
    """Use EDITOR to edit text (from a temporary file)"""
    if prefix is not None:
        prefix = prefix + "_"

    with tempfile.NamedTemporaryFile(mode='w+', prefix=prefix,
                                     suffix=".md") as tf:
        tf.write(input_text)
        tf.flush()
        editor(tf.name)
        tf.seek(0)
        edited_message = tf.read().strip()

    return edited_message


def choose(items, text="Choose from list:"):
    """Choose from list of items"""
    console.print(text)
    for i, element in enumerate(items):
        console.print(f"{i+1}: {element}")
    console.print("> ")

    while True:
        choice = readchar.readchar()

        try:
            index = int(choice)
        except ValueError:
            continue

        try:
            reply = items[index - 1]
            # click.echo(index)
            return reply
        except IndexError:
            continue


def fzf_prompt(items) -> List:
    """
    @todo: Docstring for fzf_promprt
    """
    pass


def pdflatex(lines, latex_build_dir=cfg['latex']['build_dir']) -> None:
    """
    @todo: Docstring for pdflatex

    /args/ @todo

    """
    with tempfile.NamedTemporaryFile(mode='w+',
                                     prefix='latex_note_',
                                     suffix='.tex',
                                     delete=False) as tf:
        tf.write(lines)
        tf.flush()
        with cd(os.path.expandvars(latex_build_dir)):
            with open('latex_wrapper.tex', 'r+') as wrapper:
                lines = wrapper.read()
                # console.print(lines)
                lines = re.sub(r'(begin[\s\S]*?\\input{).*?(})',
                               r'\1' + tf.name + r'\2', lines)
                # console.print(lines)
                wrapper.seek(0)
                wrapper.write(lines)
                wrapper.flush()
            subprocess.call(
                ['pdflatex', '--interaction=batchmode', 'latex_wrapper.tex'])
            subprocess.call(['open', '-a', 'skim', 'latex_wrapper.pdf'])


def render_rmarkdown(
    lines,
    pdf_location='/Users/mikevink/.data/nvim/vnnv/rmarkdown/vnnv_rmarkdown_wrapper.pdf'
):
    console.print(lines)
    with tempfile.NamedTemporaryFile(mode='w+',
                                     prefix='vnnv_rmarkdown_',
                                     suffix='.Rmd',
                                     delete=False) as tf:
        tf.write(lines)
        tf.flush()
        subprocess.call([
            'Rscript', '-e', 'library(rmarkdown);render("' + tf.name +
            '", pdf_document(toc=TRUE), "' + pdf_location + '")'
        ])
        subprocess.call(['open', '-a', 'Skim', pdf_location])


def apy_add_from_file(lines) -> None:
    """
    @todo: Docstring for apy_add_from_file

    /args/ @todo

    """
    with tempfile.NamedTemporaryFile(mode='w+',
                                     prefix='vnnv-anki_',
                                     suffix='.md',
                                     delete=False) as tf:
        tf.seek(0)
        tf.write(lines)
        tf.flush()
        # tf.seek(0)
        # console.print(tf.read())
        # if tags is not None:
        #     call(['apy', 'apy_add_from_file', '-t', tags, tf.name])
        # else:
        call(['apy', 'add-from-file', tf.name])
