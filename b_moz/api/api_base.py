import re
import sys

from flask import current_app, got_request_exception
from flask_restful import Api, http_status_message
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException

GLOBAL_PREFIX = "/api/v1"


class ApiBase(Api):

    def handle_error(self, e):
        """Error handler for the API transforms a raised exception into a Flask
        response, with the appropriate HTTP status code and body.

        :param e: the raised Exception object
        :type e: Exception

        """
        got_request_exception.send(current_app, exception=e)

        headers = Headers()
        if isinstance(e, HTTPException):
            if e.response is not None:
                resp = e.get_response()
                return resp

            status_code = e.code
            base_data = {
                "code": re.sub(r"(?<!^)(?=[A-Z])", "_", type(e).__name__).lower(),
                "message": getattr(e, "description", http_status_message(status_code)),
                "status": status_code,
            }

            headers = e.get_response().headers
        elif isinstance(e, ValueError):
            status_code = 400
            base_data = {
                "code": "invalid_param",
                "message": str(e),
                "status": status_code,
            }
        else:
            status_code = 500
            base_data = {
                "message": http_status_message(status_code),
            }

        # Werkzeug exceptions generate a content-length header which is added
        # to the response in addition to the actual content-length header
        # https://github.com/flask-restful/flask-restful/issues/534
        remove_headers = ("Content-Length",)

        for header in remove_headers:
            headers.pop(header, None)

        data = getattr(e, "data", base_data)

        error_cls_name = type(e).__name__
        if error_cls_name in self.errors:
            custom_data = self.errors.get(error_cls_name, {})
            custom_data = custom_data.copy()
            status_code = custom_data.get("status", 500)

            if "message" in custom_data:
                custom_data["message"] = custom_data["message"].format(
                    message=str(e.description if hasattr(e, "description") else e)  # type: ignore
                )
            data.update(custom_data)

        # record the exception in the logs when we have a server error of status code: 500
        if status_code and status_code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)  # type: ignore

        if status_code == 400:
            if isinstance(data.get("message"), dict):
                param_key, param_value = list(data.get("message").items())[0]  # type: ignore
                data = {
                    "code": "invalid_param",
                    "message": param_value,
                    "params": param_key,
                }
            else:
                if "code" not in data:
                    data["code"] = "unknown"

            resp = self.make_response(data, status_code, headers)
        else:
            if "code" not in data:
                data["code"] = "unknown"

            resp = self.make_response(data, status_code, headers)

        if status_code == 401:
            resp = self.unauthorized(resp)
        return resp
