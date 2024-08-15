from flask import Blueprint

from ..api_base import ApiBase, GLOBAL_PREFIX

bp = Blueprint("hello_api", __name__, url_prefix=f"{GLOBAL_PREFIX}/hello/v1")
api = ApiBase(bp)


from . import hello
