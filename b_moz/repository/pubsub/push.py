import json
import logging
import os

from google.cloud import pubsub_v1

from b_moz.repository.base import RepositoryBase

PROJECT_ID = os.getenv("PROJECT_ID", "blg-ggl-ht2024")
_TARGET_TOPIC = "moz-target-topic"


class PubSub(RepositoryBase):

    def __init__(self):
        super().__init__()
        self._publisher = pubsub_v1.PublisherClient()

    def save(self, data: dict, **kwargs):
        message = json.dumps(data).encode("utf-8")
        topic = kwargs.get("topic", _TARGET_TOPIC)
        self.publish(message, topic)

    def publish(self, message: bytes, topic):
        topic_path = self._publisher.topic_path(PROJECT_ID, topic)

        future = self._publisher.publish(topic_path, data=message)
        message_id = future.result()

        logging.info(f"Published message ID: {message_id}")
