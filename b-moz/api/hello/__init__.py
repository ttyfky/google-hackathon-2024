from flask import Blueprint

from . import hello
from ..api_base import ApiBase, GLOBAL_PREFIX

bp = Blueprint("hello_api", __name__, url_prefix=f"{GLOBAL_PREFIX}/hello/v1")
api = ApiBase(bp)

api.add_resource(hello.HelloApi, "/hello")
