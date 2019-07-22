#!./venv/bin/python3.7

from tinydb import TinyDB, Query
import os
from click.exceptions import FileError


def _dirs_db():
    return TinyDB('config/dirs.json', sort_keys=True, indent=4, separators=(',', ': '))

    
def _save_db():
    return TinyDB('config/save_dir.json', sort_keys=True, indent=4, separators=(',', ': '))


def list_directories():
    """List the directories being watched"""
    db = _dirs_db()
    # all_docs = '\n'.join([f"{docs['name']}: {docs['path']}" for docs in db.all()])
    all_docs = db.all()
    return all_docs


def get_save_dir():
    db = _save_db()
    if not db.all():
        raise FileNotFoundError("No save_dir path found on save_dir.json")
    path = db.all()[0]['path']
    status_msg = f'Save dir path: {path}'
    return status_msg


def freeze_directories():
    all_directories = list_directories()
    save_path = _save_db().all()[0]['path']
    fname = os.path.join(save_path, "dirclone_list.txt")
    file = open(fname, 'w')
    file.write(all_directories)
    file.close()
    status_msg = f"List written to {fname}"
    return status_msg


def add_update_directory(name: str, file_path: str):
    if not os.path.isdir(file_path):
        raise FileError(file_path, "Is not a directory")
    file_path = os.path.abspath(file_path)
    db = _dirs_db()
    q = Query()
    existing_dir = db.get(q["name"] == name)
    status_msg = ''
    if existing_dir:
        old_path = existing_dir['path']
        status_msg = f"Updating target directory {name}\nFrom: {old_path}\nTo: {file_path}"
    else:
        status_msg = f"Added target directory {name} ({file_path})"
    db.upsert({'name': name, 'path': file_path}, q['name'] == name)
    return status_msg


def remove_directory(name: str):
    db = _dirs_db()
    q = Query()
    doc = db.get(q['name'] == name)
    if not doc:
        raise FileError(f"No dir found with name: {name}")
    path = doc['path']
    db.remove(doc_ids=[doc.doc_id])
    status_msg = f"Successfully removed {name} ({path})"
    return status_msg

