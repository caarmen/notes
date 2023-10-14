from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.database.model import Note


class NoteSchema(SQLAlchemySchema):
    id = auto_field(dump_only=True)
    text = auto_field()
    updated_at = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)

    class Meta:
        model = Note
        load_instance = True


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
