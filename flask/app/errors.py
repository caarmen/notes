from http import HTTPStatus

from marshmallow import ValidationError
from sqlalchemy.exc import InvalidRequestError

from flask import jsonify


def handle_validation_error(e: ValidationError):
    return jsonify(e.messages_dict), HTTPStatus.BAD_REQUEST


def handle_invalid_request_error(e: InvalidRequestError):
    return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
