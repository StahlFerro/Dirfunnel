#!./venv/bin/python3.7

from pprint import pprint
import os
import shutil

import click
from click import FileError
from tinydb import TinyDB, Query
import colorama


@click.group()
def cli():
    pass


@cli.command('set-save')
@click.argument('file_path', type=click.Path(exists=True))
def set_save_dir(file_path: str):
    if not os.path.isdir(file_path):
        raise FileError(file_path, "Is not a directory")
    file_path = os.path.abspath(file_path)
    db = TinyDB('save_dir.json')
    db.purge()
    db.insert({'path': file_path})


@cli.command('save-info')
def print_save_dir():
    db = TinyDB('save_dir.json')
    if not db.all():
        click.secho("No save_dir path found on save_dir.json")
        return
    path = db.all()[0]['path']
    click.secho(f'Save dir path: {path}', fg='cyan')


@cli.command('add')
@click.argument('name')
@click.argument('file_path', type=click.Path(exists=True))
def add_dir(name: str, file_path: str):
    if not os.path.isdir(file_path):
        raise FileError(file_path, "Is not a directory")
    file_path = os.path.abspath(file_path)
    db = TinyDB('dirs.json')
    q = Query()
    db.upsert({'name': name, 'path': file_path}, q['name'] == name)


@cli.command('list')
def list_dir():
    db = TinyDB('dirs.json')
    all_docs = '\n'.join([f"{docs['name']}: {docs['path']}" for docs in db.all()])
    click.secho(all_docs, fg='blue')


@cli.command('remove')
@click.argument('name')
def remove_dir(name: str):
    db = TinyDB('dirs.json')
    q = Query()
    doc = db.get(q['name'] == name)
    if not doc:
        click.secho(f"No dir found with name: {name}")
    db.remove(doc_ids=[doc.doc_id])


@cli.command('clone')
def clone():
    dirs = TinyDB('dirs.json')
    save_path = TinyDB('save_dir.json').all()[0]['path']
    all_dirs = dirs.all()
    with click.progressbar(all_dirs, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as bar:
        for dir in bar:
            store_dir = os.path.join(dir['name'], os.path.basename(dir['path']))
            store_path = os.path.join(save_path, store_dir)
            shutil.copytree(dir['path'], store_path)
            # click.secho(f'Copying {dir["path"]} into {store_path}')


if __name__ == '__main__':
    cli()
