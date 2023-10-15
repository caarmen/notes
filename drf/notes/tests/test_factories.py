import datetime

import pytest
from tests.factories import NoteFactory

from notes.models import Note


@pytest.mark.django_db
def test_note_factory(
    note_factory: NoteFactory,
):
    note: Note = note_factory()
    assert isinstance(note.id, int)
    assert isinstance(note.text, str)
    assert isinstance(note.created_at, datetime.datetime)
    assert isinstance(note.updated_at, datetime.datetime)
