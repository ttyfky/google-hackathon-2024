import json
import logging
import os
from typing import Callable, Optional

from google.api_core import retry
from google.cloud import pubsub_v1

from b_moz.libs.o11y.trace import tracing
from b_moz.repository.base import RepoBase

_TARGET_TOPIC = "moz-target-topic"


class PubSub(RepoBase):
    GOOGLE_CLOUD_PROJECT: str

    def __init__(self, num_pull: int = 3):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._publisher = pubsub_v1.PublisherClient()
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")
        self.GOOGLE_CLOUD_PROJECT = project
        self._num_pull = num_pull

    def save(self, data: dict, **kwargs):
        message = json.dumps(data).encode("utf-8")
        topic = kwargs.get("topic", _TARGET_TOPIC)
        self.publish(message, topic)

    @tracing
    def publish(self, message: bytes, topic):
        topic_path = self._publisher.topic_path(self.GOOGLE_CLOUD_PROJECT, topic)

        future = self._publisher.publish(topic_path, data=message)
        message_id = future.result()

        self._logger.info(f"Published message ID: {message_id}")

    @tracing
    def pull_with(
        self,
        callback: Callable[[bytes], bool],
        postprocess: Optional[Callable[[], None]] = None,
        subscription_id: str = "moz-target-subscription-pull",
        **kwargs,
    ) -> bool:
        with pubsub_v1.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(
                self.GOOGLE_CLOUD_PROJECT, subscription_id
            )
            self._logger.info(f"Pulling messages from {subscription_path}.")
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

            self._logger.info(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
        return True
