import dataclasses

from app.database.session import CONNECTION_URL, init_db
from app.views import NoteGroupApi, NoteItemApi
from flask import Flask


@dataclasses.dataclass
class AppConfig:
    db_connection_url: str


def create_app(config: AppConfig = AppConfig(db_connection_url=CONNECTION_URL)):
    app = Flask(__name__)

    with app.app_context():
        init_db(url=config.db_connection_url)

    app.add_url_rule("/notes/", view_func=NoteGroupApi.as_view("note-group"))
    app.add_url_rule("/notes/<int:id>", view_func=NoteItemApi.as_view("note-detail"))
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
