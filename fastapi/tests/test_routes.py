from typing import List

import pytest
from fastapi.testclient import TestClient
from httpx import Response
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.database.model import Note as DbNote
from app.service.model import Note as ServiceNote
from fastapi import status
from tests.factories import NoteFactory


@pytest.mark.asyncio
async def test_create_note(
    client: TestClient,
    mocked_async_session: AsyncSession,
):
    response: Response = client.post("/notes/", json={"text": "bonjour"})
    assert response.status_code == status.HTTP_201_CREATED
    note: ServiceNote = TypeAdapter(ServiceNote).validate_python(response.json())
    assert note.text == "bonjour"
    db_note: DbNote = await crud.get_note(session=mocked_async_session, id=note.id)
    assert TypeAdapter(ServiceNote).validate_python(db_note) == note


@pytest.mark.asyncio
async def test_list_notes(
    note_factory: NoteFactory,
    client: TestClient,
):
    note_factory(text="hello")
    note_factory(text="there")

    response: Response = client.get("/notes/")
    assert response.status_code == status.HTTP_200_OK
    notes = TypeAdapter(List[ServiceNote]).validate_python(response.json())
    assert len(notes) == 2
    assert notes[0].text == "hello"
    assert notes[1].text == "there"


@pytest.mark.asyncio
async def test_get_note(
    note_factory: NoteFactory,
    client: TestClient,
):
    note: DbNote = note_factory(text="buongiorno")

    response: Response = client.get(f"/notes/{note.id}/")
    assert response.status_code == status.HTTP_200_OK
    response_note: ServiceNote = TypeAdapter(ServiceNote).validate_python(
        response.json()
    )
    assert response_note.text == "buongiorno"


@pytest.mark.asyncio
async def test_update_note(
    note_factory: NoteFactory,
    client: TestClient,
    mocked_async_session: AsyncSession,
):
    note1: DbNote = note_factory(text="hello")
    note2: DbNote = note_factory(text="hola")

    response: Response = client.put(f"/notes/{note1.id}/", json={"text": "hello2"})
    assert response.status_code == status.HTTP_200_OK
    updated_note1: ServiceNote = TypeAdapter(ServiceNote).validate_python(
        response.json()
    )
    assert updated_note1.text == "hello2"
    db_note1: DbNote = await crud.get_note(session=mocked_async_session, id=note1.id)
    assert TypeAdapter(ServiceNote).validate_python(db_note1) == updated_note1

    db_note2: DbNote = await crud.get_note(session=mocked_async_session, id=note2.id)
    assert db_note2.text == "hola"


@pytest.mark.asyncio
async def test_delete_note(
    note_factory: NoteFactory,
    client: TestClient,
    mocked_async_session: AsyncSession,
):
    note: DbNote = note_factory(text="ok")
    response: Response = client.delete(f"/notes/{note.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db_notes: list[DbNote] = await crud.list_notes(session=mocked_async_session)
    assert len(db_notes) == 0
