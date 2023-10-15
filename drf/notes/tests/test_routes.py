import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from tests.factories import NoteFactory

from notes.models import Note
from notes.serializers import NoteSerializer


@pytest.mark.django_db
def test_create_note(
    client: APIClient,
):
    response: Response = client.post("/notes/", data={"text": "bonjour"})
    assert response.status_code == status.HTTP_201_CREATED
    db_note: Note = Note.objects.all().first()
    assert db_note.text == "bonjour"
    assert NoteSerializer(instance=db_note).data == response.data


@pytest.mark.django_db
def test_list_notes(
    note_factory: NoteFactory,
    client: APIClient,
):
    note1 = note_factory(text="hello")
    note2 = note_factory(text="there")

    response: Response = client.get("/notes/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["text"] == "there"
    assert response.data["results"][1]["text"] == "hello"

    assert [
        NoteSerializer(instance=note2).data,
        NoteSerializer(instance=note1).data,
    ] == response.data["results"]


@pytest.mark.django_db
def test_get_note(
    note_factory: NoteFactory,
    client: APIClient,
):
    note: Note = note_factory(text="buongiorno")
    response: Response = client.get(f"/notes/{note.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == "buongiorno"
    assert NoteSerializer(instance=note).data == response.data


@pytest.mark.parametrize(
    argnames="method",
    argvalues=["patch", "put"],
)
@pytest.mark.django_db
def test_update_note(
    note_factory: NoteFactory,
    client: APIClient,
    method: str,
):
    note1: Note = note_factory(text="hello")
    note2: Note = note_factory(text="hola")

    client_method = getattr(client, method)
    response: Response = client_method(
        f"/notes/{note1.id}/",
        data={"text": "hello2"},
    )
    assert response.status_code == status.HTTP_200_OK
    note1.refresh_from_db()
    assert note1.text == "hello2"
    note2.refresh_from_db()
    assert note2.text == "hola"
    assert NoteSerializer(instance=note1).data == response.data


@pytest.mark.django_db
def test_delete_note(
    note_factory: NoteFactory,
    client: APIClient,
):
    note: Note = note_factory(text="ok")
    response: Response = client.delete(f"/notes/{note.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert Note.objects.all().count() == 0
