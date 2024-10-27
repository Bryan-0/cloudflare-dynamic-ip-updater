import requests
import logging

from clients.constants import RETRYABLE_HTTP_STATUS_CODES
from helpers.retry import with_retries
from helpers.retry.exceptions import Retry


logger = logging.getLogger("dynamic_ip_updater")


class IPv4:
    @staticmethod
    @with_retries()
    def get_public_ip():
        try:
            logger.info("HTTP Request: GET https://checkip.amazonaws.com")
            ip_response = requests.get("https://checkip.amazonaws.com")
            ip_response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            logger.error(f"Timeout while requesting public ip")
            raise Retry()
        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code
            logger.error(
                f"HTTP Error ({status_code}) raised when requesting for public ip"
            )

            if status_code not in RETRYABLE_HTTP_STATUS_CODES:
                raise exc

            raise Retry()
        except requests.exceptions.RequestException as exc:
            logger.exception(f"Unhanlded request exception raised")
            raise exc
        except Exception as exc:
            logger.exception(f"Unhanlded exception received")
            raise exc

        return ip_response.text.strip()
