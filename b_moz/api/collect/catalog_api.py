import logging

from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.exceptions import InternalServerError

from b_moz.usecase.collect_latest_items import create_latest_items_usecase
from b_moz.usecase.collect_spec import (
    create_target_spec_usecase,
    create_pubsub_target_spec_usecase,
    create_save_pubsub_target_spec_usecase,
)

_logger = logging.getLogger(__name__)

catalog_response_fields = {
    "message": fields.String,
    "result": fields.List(fields.Raw),
}


class LatestItemsApi(Resource):

    def __init__(self):
        super().__init__()
        self._usecase = create_latest_items_usecase()

    @marshal_with(catalog_response_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("category", type=str, location="json")
        args = parser.parse_args()
        category = args.get("category")
        if not category:
            _logger.error("No category specified")
            return {"message": "No category specified"}, 400

        _logger.info(f"Query: {category}")
        try:
            new_items = self._usecase.collect(category_query=category)
            _logger.info(f"Collected new items: {new_items}")
            return {"message": "ok", "result": new_items["models"]}, 200
        except Exception as e:
            raise InternalServerError(f"Error: {e}")


class TargetSpecApi(Resource):

    def __init__(self):
        super().__init__()
        self._usecase = create_target_spec_usecase(None)

    @marshal_with(catalog_response_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("target", type=str, location="json")
        parser.add_argument("category", type=str, location="json")
        parser.add_argument("mode", type=str, location="json", required=False)

        args = parser.parse_args()
        target = args.get("target")
        category = args.get("category", "")
        mode = args.get("mode", "")

        if not target:
            return {"message": "No target specified"}, 400

        _logger.info(f"Query: {target}")
        try:
            extracted = self._usecase.collect(
                target_query=target, category=category, mode=mode
            )
            _logger.info(f"Collected specs volume: {len(extracted)}")
            return {"message": "ok", "result": extracted}, 200
        except Exception as e:
            raise InternalServerError(f"Error: {e}")


class PubSubTargetSpecApi(Resource):

    def __init__(self):
        super().__init__()
        self._usecase = create_pubsub_target_spec_usecase(None)

    @marshal_with(catalog_response_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mode", type=str, location="json", required=False)

        args = parser.parse_args()
        mode = args.get("mode", "")

        try:
            extracted = self._usecase.collect(mode=mode)
            _logger.info(f"Collected specs volume: {len(extracted)}")
            return {"message": "ok", "result": extracted}, 200
        except Exception as e:
            raise InternalServerError(f"Error: {e}")


class SavePubSubTargetSpecApi(Resource):

    def __init__(self):
        super().__init__()
        self._usecase = create_save_pubsub_target_spec_usecase()

    @marshal_with(catalog_response_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("num", type=int, location="json", required=False)

        args = parser.parse_args()
        num = args.get("num", 0)

        try:
            _logger.info("Saving for specs in PubSub started...")
            extracted = self._usecase.save(num=num)
            _logger.info("Save completed")
            return {"message": "ok", "result": extracted}, 200
        except Exception as e:
            raise InternalServerError(f"Error: {e}")
