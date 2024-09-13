import json
import logging
import os
from typing import Callable, Optional

from google.api_core import retry
from google.cloud import pubsub_v1

from b_moz.repository.base import RepositoryBase

PROJECT_ID = os.getenv("PROJECT_ID", "blg-ggl-ht2024")
_TARGET_TOPIC = "moz-target-topic"


class PubSub(RepositoryBase):

    def __init__(self, num_pull: int = 3):
        super().__init__()
        self._publisher = pubsub_v1.PublisherClient()

        self._num_pull = num_pull

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
        postprocess: Optional[Callable[[], None]] = None,
        subscription_id: str = "moz-target-subscription-pull",
        **kwargs,
    ) -> bool:
        with pubsub_v1.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(
                PROJECT_ID, subscription_id
            )
            logging.info(f"Pulling messages from {subscription_path}.")
            response = subscriber.pull(
                request={
                    "subscription": subscription_path,
                    "max_messages": self._num_pull,
                },
                retry=retry.Retry(deadline=300),
            )

            if len(response.received_messages) == 0:
                return False

            ack_ids = []
            for received_message in response.received_messages:
                if callback(received_message.message.data):
                    ack_ids.append(received_message.ack_id)

            if postprocess:
                postprocess()

            if ack_ids:
                subscriber.acknowledge(
                    request={"subscription": subscription_path, "ack_ids": ack_ids}
                )

            logging.info(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
        return True
