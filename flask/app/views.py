from http import HTTPStatus

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask.views import MethodView

from app.database import crud
from app.database.model import Note
from app.database.session import get_session
from app.service.model import NoteSchema, note_schema, notes_schema
from flask import Response, render_template, request

spec = APISpec(
    title="Flask Notes",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


class NoteItemApi(MethodView):
    init_every_request = False

    async def get(self, id) -> NoteSchema:
        """Get a note
        ---
        description: Get a note
        responses:
          200:
            content:
              application/json:
                schema: NoteSchema
        """
        async with get_session() as session:
            db_note = await crud.get_note(session, id=id)
            return note_schema.dump(db_note)

    async def put(self, id) -> NoteSchema:
        """Update a note
        ---
        description: Update a note
        requestBody:
          content:
            application/json:
              schema: NoteSchema
        responses:
          200:
            content:
              application/json:
                schema: NoteSchema
        """
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.update_note(session, id=id, new_text=note.text)
            return note_schema.dump(db_note)

    async def delete(self, id):
        """Delete a note
        ---
        description: Delete a note
        responses:
          204:
            description: The note was deleted.
        """
        async with get_session() as session:
            await crud.delete_note(session, id=id)
            return Response(status=HTTPStatus.NO_CONTENT)


class NoteGroupApi(MethodView):
    init_every_request = False

    async def post(self) -> NoteSchema:
        """Create a note
        ---
        description: Create a note
        requestBody:
          content:
            application/json:
              schema: NoteSchema
        responses:
          200:
            content:
              application/json:
                schema: NoteSchema
        """
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.create_note(session, text=note.text)
            return note_schema.dump(db_note), HTTPStatus.CREATED

    async def get(self) -> list[NoteSchema]:
        """List notes
        ---
        description: List notes
        responses:
          200:
            content:
              application/json:
                schema:
                  type: array
                  items: NoteSchema
        """
        async with get_session() as session:
            db_notes = await crud.list_notes(session)
            return notes_schema.dump(db_notes)


def get_openapi():
    return spec.to_dict()


def get_redoc():
    return render_template("redoc.html")


def get_swagger_ui():
    return render_template("swaggerui.html")
