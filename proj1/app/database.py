import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # To access columns by name
    return g.db

def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())
    db.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
