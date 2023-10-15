"""
Implements routes for notes CRUD operations.
"""
from dataclasses import dataclass
from http import HTTPStatus

from app.database import Database

@dataclass
class Response:
    """
    A route response.
    """
    status: HTTPStatus
    data: dict | None = None


def route_note_item(method: str, note_id: int, data: dict) -> Response:
    """
    Process a request for an existing note.
    """
    with Database() as notes_db:
        # Get one note:
        if method == "GET":
            note = notes_db.read_note(note_id)
            if note:
                return Response(HTTPStatus.OK, notes_db.read_note(note_id))
            return Response(
                HTTPStatus.NOT_FOUND,
                {"message": "Unknown note"},
            )

        # Modify one note:
        if method in ("PUT" , "PATCH"):
            text = data["text"]
            updated_note = notes_db.update_note(note_id, text)
            return Response(HTTPStatus.OK, updated_note)

        # Delete one note:
        if method == "DELETE":
            notes_db.delete_note(note_id)
            return Response(HTTPStatus.NO_CONTENT)

        return Response(HTTPStatus.METHOD_NOT_ALLOWED)


def route_note_group(method: str, data: dict) -> Response:
    """
    Process a request for the group of notes.
    """
    with Database() as notes_db:
        # Create one note:
        if method == "POST":
            text = data["text"]
            new_note = notes_db.create_note(text)
            return Response(HTTPStatus.CREATED, new_note)

        # List all notes
        if method == "GET":
            return Response(HTTPStatus.OK, notes_db.list_notes())

        return Response(HTTPStatus.METHOD_NOT_ALLOWED)
