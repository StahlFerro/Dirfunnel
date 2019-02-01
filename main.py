#!./venv/bin/python3.7

from pprint import pprint
import os
import shutil

import click
from click import FileError, ClickException
from tinydb import TinyDB, Query
import colorama


def dirs_db():
    return TinyDB('dirs.json', sort_keys=True, indent=4, separators=(',', ': '))


def save_db():
    return TinyDB('save_dir.json', sort_keys=True, indent=4, separators=(',', ': '))


@click.group()
def cli():
    pass


@cli.command('set-save')
@click.argument('file_path', type=click.Path(exists=True))
def set_save_dir(file_path: str):
    if not os.path.isdir(file_path):
        raise FileError(file_path, "Is not a directory")
    file_path = os.path.abspath(file_path)
    db = save_db()
    db.purge()
    db.insert({'path': file_path})
    click.secho(f"Save path set to: {file_path}", fg="green")


@cli.command('save-info')
def print_save_dir():
    db = save_db()
    if not db.all():
        raise ClickException("No save_dir path found on save_dir.json")
    path = db.all()[0]['path']
    click.secho(f"Save dir path: {path}", fg="cyan")


@cli.command('add')
@click.argument('name')
@click.argument('file_path', type=click.Path(exists=True))
def add_dir(name: str, file_path: str):
    if not os.path.isdir(file_path):
        raise FileError(file_path, "Is not a directory")
    file_path = os.path.abspath(file_path)
    db = dirs_db()
    q = Query()
    doc = db.get(q["name"] == name)
    if doc:
        old_path = doc['path']
        click.secho(f"Updating target directory {name}\nFrom: {old_path}\nTo: {file_path}", fg="blue")
    else:
        click.secho(f"Added target directory {name} ({file_path})", fg="green")
    db.upsert({'name': name, 'path': file_path}, q['name'] == name)


@cli.command('list')
def list_dir():
    db = dirs_db()
    all_docs = '\n'.join([f"{docs['name']}: {docs['path']}" for docs in db.all()])
    click.secho(all_docs, fg="blue")


@cli.command('remove')
@click.argument('name')
def remove_dir(name: str):
    db = dirs_db()
    q = Query()
    doc = db.get(q['name'] == name)
    if not doc:
        raise ClickException(f"No dir found with name: {name}")
    path = doc['path']
    db.remove(doc_ids=[doc.doc_id])
    click.secho(f"Successfully removed {name} ({path})", fg="yellow")


@cli.command('clone')
def clone():
    dirs = dirs_db()
    save_path = TinyDB('save_dir.json').all()[0]['path']
    all_dirs = dirs.all()
    # with click.progressbar(all_dirs, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as bar:
    for dir in all_dirs:
        store_dir = os.path.join(dir['name'], os.path.basename(dir['path']))
        store_path = os.path.join(save_path, store_dir)
        if os.path.exists(store_path):
            shutil.rmtree(store_path)
            click.secho(f'Overwriting {dir["path"]} into {store_path}', fg="blue")
        else:
            click.secho(f'Copying {dir["path"]} into {store_path}', fg="green")
        shutil.copytree(dir['path'], store_path)


if __name__ == '__main__':
    cli()
