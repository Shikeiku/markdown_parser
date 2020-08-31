from subprocess import call
import tempfile
import os

from config import console

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
    console.print("> ", nl=False)

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
