import tempfile
import os
import subprocess
from subprocess import call
import re

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
            click.echo(index)
            return reply
        except IndexError:
            continue


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


def apy_add_from_file(lines, tags=None) -> None:
    """
    @todo: Docstring for apy_add_from_file

    /args/ @todo

    """
    with tempfile.NamedTemporaryFile(mode='w+',
                                     prefix='vnnv-anki_',
                                     suffix='.md',
                                     delete=False) as tf:
        tf.write(lines)
        tf.flush()
        if tags is not None:
            call(['apy', 'apy_add_from_file', '-t', tags, tf.name])
        else:
            call(['apy', 'apy_add_from_file', tf.name])
