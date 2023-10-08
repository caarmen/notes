import datetime

from app.database.model import Note
from tests.factories import NoteFactory


def test_note_factory(
    note_factory: NoteFactory,
):
    note: Note = note_factory()
    assert isinstance(note.id, int)
    assert isinstance(note.text, str)
    assert isinstance(note.created_at, datetime.datetime)
    assert isinstance(note.updated_at, datetime.datetime)
