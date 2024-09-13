import json
import logging
import os

from google.api_core import retry
from google.cloud import pubsub_v1
from typing import Callable

from b_moz.repository.base import RepositoryBase

PROJECT_ID = os.getenv("PROJECT_ID", "blg-ggl-ht2024")
_TARGET_TOPIC = "moz-target-topic"


class PubSub(RepositoryBase):
    NUM_MESSAGES = 1

    def __init__(self):
        super().__init__()
        self._publisher = pubsub_v1.PublisherClient()
        self._subscriber = pubsub_v1.SubscriberClient()

    def save(self, data: dict, **kwargs):
        message = json.dumps(data).encode("utf-8")
        topic = kwargs.get("topic", _TARGET_TOPIC)
        self.publish(message, topic)

    def publish(self, message: bytes, topic):
        topic_path = self._publisher.topic_path(PROJECT_ID, topic)

        future = self._publisher.publish(topic_path, data=message)
        message_id = future.result()

        logging.info(f"Published message ID: {message_id}")

    def pull_with(
        self,
        callback: Callable[[bytes], bool],
        subscription_id: str = "moz-target-subscription-pull",
        **kwargs,
    ):
        subscription_path = self._subscriber.subscription_path(
            PROJECT_ID, subscription_id
        )

        # Wrap the subscriber in a 'with' block to automatically call close() to
        # close the underlying gRPC channel when done.
        with self._subscriber:
            # The subscriber pulls a specific number of messages. The actual
            # number of messages pulled may be smaller than max_messages.
            response = self._subscriber.pull(
                request={
                    "subscription": subscription_path,
                    "max_messages": self.NUM_MESSAGES,
                },
                retry=retry.Retry(deadline=300),
            )

            if len(response.received_messages) == 0:
                return

            ack_ids = []
            for received_message in response.received_messages:
                if callback(received_message.message.data):
                    ack_ids.append(received_message.ack_id)

            self._subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )

            logging.info(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
