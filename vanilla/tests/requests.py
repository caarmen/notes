"""
Http request functions for tests.
"""
from http.client import HTTPConnection
import dataclasses
import json


@dataclasses.dataclass
class Response:
    """
    Request response.
    """
    status: int
    data: dict | None

def request(conn: HTTPConnection, method: str, path: str, body: dict = None) -> Response:
    """
    Wrapper around lower-level http.client apis to execute a request and return a response.
    """
    conn.request(method, path, body=json.dumps(body) if body else None)
    response = conn.getresponse()
    data = response.read()
    return Response(response.status, json.loads(data) if data else None)
