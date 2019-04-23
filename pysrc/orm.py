#!./venv/bin/python3.7

from tinydb import TinyDB


def dirs_db():
    return TinyDB('config/dirs.json', sort_keys=True, indent=4, separators=(',', ': '))


def save_db():
    return TinyDB('config/save_dir.json', sort_keys=True, indent=4, separators=(',', ': '))
