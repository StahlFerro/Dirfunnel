from .orm import dirs_db, save_db


def list_dir():
    db = dirs_db()
    # all_docs = '\n'.join([f"{docs['name']}: {docs['path']}" for docs in db.all()])
    all_docs = db.all()
    return all_docs