import asyncio
from http import HTTPStatus

import pytest
from flask.testing import FlaskClient
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.wrappers import Response

from app.database import crud
from app.database.model import Note as DbNote
from app.service.model import note_schema, notes_schema
from tests.factories import NoteFactory


# https://github.com/pallets/flask/issues/4375
# Workaround for a limitation using both sync (FlaskClient)
# and async (db session) apis inside tests.
async def sync_to_async(fn):
    return await asyncio.get_running_loop().run_in_executor(None, lambda: fn())


@pytest.mark.asyncio
async def test_create_note(
    client: FlaskClient,
    mocked_async_session: AsyncSession,
):
    response: Response = await sync_to_async(
        lambda: client.post("/notes/", json={"text": "bonjour"})
    )
    assert response.status_code == HTTPStatus.CREATED
    db_note: DbNote = await crud.get_note(
        session=mocked_async_session, id=response.json["id"]
    )
    assert db_note.text == "bonjour"
    assert note_schema.dump(db_note) == response.json


@pytest.mark.asyncio
async def test_list_notes(
    note_factory: NoteFactory,
    client: FlaskClient,
):
    note1 = note_factory(text="hello")
    note2 = note_factory(text="there")

    response: Response = await sync_to_async(lambda: client.get("/notes/"))
    assert response.status_code == HTTPStatus.OK

    assert response.json[0]["text"] == "there"
    assert response.json[1]["text"] == "hello"

    assert notes_schema.dump([note2, note1]) == response.json


@pytest.mark.asyncio
async def test_get_note(
    note_factory: NoteFactory,
    client: FlaskClient,
):
    note: DbNote = note_factory(text="buongiorno")

    response: Response = await sync_to_async(lambda: client.get(f"/notes/{note.id}/"))
    assert response.status_code == HTTPStatus.OK

    assert response.json["text"] == "buongiorno"

    assert note_schema.dump(note) == response.json


@pytest.mark.asyncio
async def test_update_note(
    note_factory: NoteFactory,
    client: FlaskClient,
    mocked_async_session: AsyncSession,
):
    note1: DbNote = note_factory(text="hello")
    note2: DbNote = note_factory(text="hola")

    response: Response = await sync_to_async(
        lambda: client.put(f"/notes/{note1.id}/", json={"text": "hello2"})
    )
    assert response.status_code == HTTPStatus.OK

    db_note1: DbNote = await crud.get_note(session=mocked_async_session, id=note1.id)
    assert db_note1.text == "hello2"
    assert note_schema.dump(db_note1) == response.json

    db_note2: DbNote = await crud.get_note(session=mocked_async_session, id=note2.id)
    assert db_note2.text == "hola"


@pytest.mark.asyncio
async def test_delete_note(
    note_factory: NoteFactory,
    client: FlaskClient,
    mocked_async_session: AsyncSession,
):
    note: DbNote = note_factory(text="ok")

    response: Response = await sync_to_async(
        lambda: client.delete(f"/notes/{note.id}/")
    )
    assert response.status_code == HTTPStatus.NO_CONTENT

    db_notes: list[DbNote] = await crud.list_notes(session=mocked_async_session)
    assert len(db_notes) == 0
