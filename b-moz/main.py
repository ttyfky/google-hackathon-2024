import logging
import os

# import google.cloud.logging
from flask import Flask
from waitress import serve

import api


def create_app():
    flask_app = Flask(__name__)
    api.register(flask_app)
    return flask_app


if __name__ == "__main__":
    _logger = logging.getLogger(__name__)

    is_local = os.environ.get("IS_LOCAL") == "true"

    if is_local:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        # client = google.cloud.logging.Client()
        # client.setup_logging()

    if is_local:
        create_app().run(host="", port=3000, debug=True)
    else:
        serve(create_app(), port=int(os.environ.get("PORT", 3000)))
