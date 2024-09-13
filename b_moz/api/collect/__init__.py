from flask import Blueprint

from . import catalog_api as catalog
from ..api_base import ApiBase, GLOBAL_PREFIX

bp = Blueprint("collect_api", __name__, url_prefix=f"{GLOBAL_PREFIX}/collect")
api = ApiBase(bp)

api.add_resource(catalog.LatestItemsApi, "/catalog/latest")
api.add_resource(catalog.TargetSpecApi, "/catalog/spec")
api.add_resource(catalog.PubSubTargetSpecApi, "/catalog/spec/pubsub")
