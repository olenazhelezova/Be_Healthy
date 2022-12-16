import sqlite3
from flask import g

DATABASE = 'application/database.db'

def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
    return conn