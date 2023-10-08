import dataclasses
from http import HTTPStatus

from app.database import crud
from app.database.model import Note
from app.database.session import CONNECTION_URL, get_session, init_db
from app.service.model import NoteSchema, note_schema, notes_schema
from flask import Flask, Response, request


@dataclasses.dataclass
class AppConfig:
    db_connection_url: str


def create_app(config: AppConfig = AppConfig(db_connection_url=CONNECTION_URL)):
    app = Flask(__name__)

    with app.app_context():
        init_db(url=config.db_connection_url)

    @app.post("/notes/")
    async def create_note():
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.create_note(session, text=note.text)
            return note_schema.dump(db_note), HTTPStatus.CREATED

    @app.get("/notes/")
    async def list_notes() -> list[NoteSchema]:
        async with get_session() as session:
            db_notes = await crud.list_notes(session)
            return notes_schema.dump(db_notes)

    @app.get("/notes/<note_id>")
    async def get_note(note_id: int) -> NoteSchema:
        async with get_session() as session:
            db_note = await crud.get_note(session, id=note_id)
            return note_schema.dump(db_note)

    @app.put("/notes/<note_id>")
    async def update_note(note_id: int):
        async with get_session() as session:
            note: Note = note_schema.load(request.json, session=session)
            db_note = await crud.update_note(session, id=note_id, new_text=note.text)
            return note_schema.dump(db_note)

    @app.delete("/notes/<note_id>")
    async def delete_note(note_id: int):
        async with get_session() as session:
            await crud.delete_note(session, id=note_id)
            return Response(status=HTTPStatus.NO_CONTENT)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
