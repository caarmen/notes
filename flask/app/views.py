from http import HTTPStatus

from flask.views import MethodView

from app.database import crud
from app.database.model import Note
from app.database.session import get_session
from app.service.model import NoteSchema, note_schema, notes_schema
from flask import Response, request


class NoteItemApi(MethodView):
    init_every_request = False

    async def get(self, id) -> NoteSchema:
        async with get_session() as session:
            db_note = await crud.get_note(session, id=id)
            return note_schema.dump(db_note)

    async def put(self, id) -> NoteSchema:
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.update_note(session, id=id, new_text=note.text)
            return note_schema.dump(db_note)

    async def delete(self, id):
        async with get_session() as session:
            await crud.delete_note(session, id=id)
            return Response(status=HTTPStatus.NO_CONTENT)


class NoteGroupApi(MethodView):
    init_every_request = False

    async def post(self) -> NoteSchema:
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.create_note(session, text=note.text)
            return note_schema.dump(db_note), HTTPStatus.CREATED

    async def get(self) -> list[NoteSchema]:
        async with get_session() as session:
            db_notes = await crud.list_notes(session)
            return notes_schema.dump(db_notes)
