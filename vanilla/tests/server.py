"""
Functions to start the server for tests.
"""
from time import sleep
from wsgiref.simple_server import make_server
import multiprocessing
import socket

from app.main import app


def _start_server(host: str, port: int):
    server = make_server(host, port, app)
    server.serve_forever()

def _wait_for_server(host: str, port: int):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
            return
        except ConnectionRefusedError:
            sleep(0.001) # try again

def start_and_wait_for_server(host: str, port: int) -> multiprocessing.Process:
    """
    Run our server in another process.
    https://stackoverflow.com/a/6564500/1204440
    """
    server_process = multiprocessing.Process(target=_start_server, args=[host, port])
    server_process.start()
    _wait_for_server(host, port)
    return server_process
