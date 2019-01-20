from pprint import pprint
import os
import io
import shutil
import colorama

import click
from tinydb import TinyDB, Query


@click.group()
def cli():
    pass


@cli.command('set-save')
@click.argument('file_path', type=click.Path(exists=True))
def set_save_dir(file_path: str):
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        return
    file_path = os.path.abspath(file_path)
    db = TinyDB('save_dir.json')
    q = Query()
    if len(db) == 0:
        db.insert({'path': file_path})
    else:
        db.update({'path': file_path})


@cli.command('add')
@click.argument('name')
@click.argument('file_path', type=click.Path(exists=True))
def add_dir(name: str, file_path: str):
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        return
    file_path = os.path.abspath(file_path)
    db = TinyDB('dirs.json')
    q = Query()
    db.upsert({'name': name, 'path': file_path}, q['name'] == name)


@cli.command('list')
def list_dir():
    db = TinyDB('dirs.json')
    all_docs = '\n'.join([f"{docs['name']}: {docs['path']}" for docs in db.all()])
    click.echo_via_pager(all_docs, color='blue')


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
    for dir in all_dirs:
        store_dir = os.path.join(dir['name'], os.path.basename(dir['path']))
        store_path = os.path.join(save_path, store_dir)
        shutil.copytree(dir['path'], store_path)
        click.secho(f'Copying {dir["path"]} into {store_path}')


if __name__ == '__main__':
    cli()
