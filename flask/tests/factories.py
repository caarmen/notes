from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory
from pytest_factoryboy import register

from app.database.model import Note


@register
class NoteFactory(SQLAlchemyModelFactory):
    text = Faker("pystr")

    class Meta:
        model = Note
        sqlalchemy_session_persistence = "commit"
