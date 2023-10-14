from factory import Faker
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from notes.models import Note


@register
class NoteFactory(DjangoModelFactory):
    text = Faker("pystr")

    class Meta:
        model = Note
