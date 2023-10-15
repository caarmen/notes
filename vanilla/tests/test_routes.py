"""
Tests for the vanilla notes application.
"""
from http import HTTPStatus
from unittest import mock
import http.client
import os
import unittest
from app.database import ENV_NOTES_DB_PATH, init_db, Database


from tests import requests, server

DB_PATH="/tmp/test_notes.db"
HOST=""
PORT=8099



@mock.patch.dict(os.environ, {ENV_NOTES_DB_PATH: DB_PATH})
class TestRoutes(unittest.TestCase):
    """
    Test the different routes of the server.
    """


    @mock.patch.dict(os.environ, {ENV_NOTES_DB_PATH: DB_PATH})
    def setUp(self) -> None:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        self.server_process = server.start_and_wait_for_server(HOST, PORT)
        self.conn = http.client.HTTPConnection(HOST, PORT)


    def tearDown(self) -> None:
        self.server_process.terminate()
        self.server_process.join()
        del self.server_process


    def test_create_note(self):
        """
        When a request is performed to create a note
        Then the note is present in the db.
        """

        response = requests.request(self.conn, "POST", "/notes/", body={"text": "hola"})
        assert response.status == HTTPStatus.CREATED.value
        assert response.data["text"] == "hola"

        with Database() as notes_db:
            db_note = notes_db.read_note(response.data["id"])
            assert db_note["text"] == "hola"


    def test_list_notes(self):
        """
        Given some notes in the db
        When a request is performed to list the notes
        Then the response contains the notes in the expected order.
        """

        with Database() as notes_db:
            notes_db.create_note("hello")
            notes_db.create_note("bonjour")

        response = requests.request(self.conn, "GET", "/notes/")

        assert response.status == HTTPStatus.OK.value
        assert len(response.data) == 2
        assert response.data[0]["text"] == "bonjour"
        assert response.data[1]["text"] == "hello"


    def test_get_note(self):
        """
        Given a note in the db
        When a request is performed to read the note
        Then the response contains the note.
        """
        with Database() as notes_db:
            note = notes_db.create_note("buongiorno")

        response = requests.request(self.conn, "GET", f"/notes/{note['id']}/")

        assert response.status == HTTPStatus.OK.value
        assert response.data["text"] == "buongiorno"


    def test_update_note(self):
        """
        Given a note in the db
        When a request is performed to update it
        Then the response contains the updated note
        And the note is updated in the database.
        """
        with Database() as notes_db:
            note = notes_db.create_note("hiya")

        response = requests.request(
            self.conn,
            "PUT",
            f"/notes/{note['id']}/",
            body={"text": 'howdy'}
        )

        assert response.status == HTTPStatus.OK.value
        assert response.data["text"] == "howdy"

        with Database() as notes_db:
            updated_note = notes_db.read_note(note["id"])
        assert updated_note["text"] == "howdy"


    def test_partial_update_note(self):
        """
        Given a note in the db
        When a request is performed to update it using PATCH
        Then the response contains the updated note
        And the note is updated in the database.
        """
        with Database() as notes_db:
            note = notes_db.create_note("hiya")

        response = requests.request(
            self.conn,
            "PATCH",
            f"/notes/{note['id']}/",
            body={"text": 'howdy'}
        )

        assert response.status == HTTPStatus.OK.value
        assert response.data["text"] == "howdy"

        with Database() as notes_db:
            updated_note = notes_db.read_note(note["id"])
        assert updated_note["text"] == "howdy"


    def test_delete_note(self):
        """
        Given a note in the db
        When a request is performed to delete it
        Then the response is succssful
        And the note is deleted in the db
        """
        with Database() as notes_db:
            note = notes_db.create_note("delete me")

        response = requests.request(self.conn, "DELETE", f"/notes/{note['id']}/")

        assert response.status == HTTPStatus.NO_CONTENT
        assert response.data is None
        with Database() as notes_db:
            assert notes_db.read_note(note["id"]) is None
