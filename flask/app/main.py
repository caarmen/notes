import dataclasses

from marshmallow import ValidationError
from sqlalchemy.exc import InvalidRequestError

from app.database.session import CONNECTION_URL, init_db
from app.errors import handle_invalid_request_error, handle_validation_error
from app.views import (
    NoteGroupApi,
    NoteItemApi,
    get_openapi,
    get_redoc,
    get_swagger_ui,
    spec,
)
from flask import Flask


@dataclasses.dataclass
class AppConfig:
    db_connection_url: str


def create_app(config: AppConfig = AppConfig(db_connection_url=CONNECTION_URL)):
    app = Flask(__name__)

    with app.app_context():
        init_db(url=config.db_connection_url)

    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(InvalidRequestError, handle_invalid_request_error)

    note_item_view = NoteItemApi.as_view("note-detail")
    note_group_view = NoteGroupApi.as_view("note-group")
    app.add_url_rule("/notes/", view_func=note_group_view)
    app.add_url_rule("/notes/<int:id>/", view_func=note_item_view)
    app.add_url_rule("/openapi.json", view_func=get_openapi)
    app.add_url_rule("/redoc", view_func=get_redoc)
    app.add_url_rule("/docs", view_func=get_swagger_ui)

    with app.test_request_context():
        spec.path(view=note_group_view)
        spec.path(view=note_item_view)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
