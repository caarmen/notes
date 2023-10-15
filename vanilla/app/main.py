"""
WSGI server for a notes CRUD application.
"""
from http import HTTPStatus
from typing import Callable
from urllib.parse import urlparse
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
import json
import re
from app import routes
from app.database import init_db


def read_request_payload(environ: dict) -> dict:
    """
    Read the request payload from the current request.
    """
    content_length = environ.get("CONTENT_LENGTH", "0")
    if not content_length:
        content_length = "0"
    request_body_size = int(content_length)
    request_body = environ['wsgi.input'].read(request_body_size)
    return json.loads(request_body) if request_body else {}


def send_response(response: routes.Response, start_response: Callable):
    """
    Send the given response.
    """
    headers = [('Content-type', 'application/json; charset=utf-8')]
    start_response(f"{response.status.value} {response.status.phrase}", headers)
    return [bytes(json.dumps(response.data), encoding="utf-8")] if response.data is not None else []

def send_file(path: str, content_type: str, start_response: Callable):
    """
    Send the given file as a response.
    """
    headers = [('Content-type', f"{content_type}; charset=utf-8")]
    start_response(f"{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}", headers)
    with open(path, 'r', encoding="utf-8") as file:
        return [bytes(file.read(), encoding="utf-8")]

def app(environ: dict, start_response: Callable):
    """
    WSGI application.
    """
    url = urlparse(request_uri(environ))

    path = url.path
    method  = environ['REQUEST_METHOD']
    data = read_request_payload(environ)

    # Routes for one specific existing note:
    if pattern_match := re.search("^/notes/([0-9]+)/$", path):
        note_id = int(pattern_match.group(1))
        response: routes.Response = routes.route_note_item(method, note_id, data)
        return send_response(response, start_response)

    # Other notes routes:
    if path == "/notes/":
        response: routes.Response = routes.route_note_group(method, data)
        return send_response(response, start_response)

    # Documentation routes:
    if path == "/openapi.json":
        return send_file("static/openapi.json", "application/json", start_response)

    if path == "/docs":
        return send_file("static/swaggerui.html", "text/html", start_response)

    if path == "/redoc":
        return send_file("static/redoc.html", "text/html", start_response)

    # Unknown route:
    return send_response(routes.Response(HTTPStatus.NOT_FOUND), start_response)



if __name__ == "__main__":
    init_db()
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
