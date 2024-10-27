import logging
import boto3


class SNS:
    def __init__(self) -> None:
        self.client = boto3.client("sns")
        self._logger = logging.getLogger("dynamic_ip_updater")

    def publish(self, topic_arn: str, message: str) -> None:
        self._logger(f"Sending SNS message to topic {topic_arn}")
        try:
            self.client.publish(
                TopicArn=topic_arn,
                Message=message,
            )
        except Exception as exc:
            self._logger.exception(
                f"Unhanlded exceptions while publishing SNS message to topic {topic_arn}"
            )
