import logging

from flask_restful import Resource, fields, marshal_with
from werkzeug.exceptions import InternalServerError

_logger = logging.getLogger(__name__)

hello_response_fields = {
    "message": fields.String,
}


class HelloApi(Resource):
    @marshal_with(hello_response_fields)
    def get(self):

        try:
            return {"message": "Hello World"}, 200
        except Exception as e:
            raise InternalServerError(f"Error calling OpenAI: {e}")
