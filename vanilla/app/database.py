"""
Module for database operations.
"""

import os
import sqlite3

from typing import Self # pylint: disable=E0611

ENV_NOTES_DB_PATH="NOTES_DB_PATH"

def _dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))

def init_db():
    """
    Initialize the database.
    """
    with Database() as notes_db:
        notes_db.create()

def _get_db_path():
    return os.environ.get(ENV_NOTES_DB_PATH, "/tmp/notes.db")

class Database:
    """
    Provides CRUD access to the notes database.
    """

    def __init__(self):
        self.con: sqlite3.Connection|None = None
        self.cursor: sqlite3.Cursor|None = None

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def create_note(self, text: str) -> dict:
        """
        Create a new note.
        """
        self.cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
        note_id = self.cursor.lastrowid
        self.cursor.connection.commit()
        return self.read_note(note_id)


    def list_notes(self) -> list[dict]:
        """
        List all notes.
        """
        self.cursor.execute("SELECT * FROM notes ORDER BY created_at DESC, id DESC")
        return self.cursor.fetchall()


    def read_note(self, note_id: int) -> dict:
        """
        Read one existing note.
        """
        self.cursor.execute("SELECT * from notes where id=?", (note_id,))
        return self.cursor.fetchone()


    def update_note(self, note_id: int, text: str) -> dict:
        """
        Update one existing note.
        """
        self.cursor.execute("UPDATE notes set text=? where id=?", (text, note_id))
        self.cursor.connection.commit()
        return self.read_note(note_id)


    def delete_note(self, note_id):
        """
        Delete one existing note.
        """
        self.cursor.execute("DELETE from notes where id=?", (note_id,))
        self.cursor.connection.commit()

    def create(self):
        """
        Create the database schema if it doesn't exist already.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                text VARCHAR NOT NULL,
                created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
                updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL
            )
            """
        )

    def open(self):
        """
        Open the connection to the database.
        """
        self.con: sqlite3.Connection = sqlite3.connect(_get_db_path())
        self.con.row_factory = _dict_factory
        self.cursor = self.con.cursor()

    def close(self):
        """
        Close the connection to the database.
        """
        self.con.close()
