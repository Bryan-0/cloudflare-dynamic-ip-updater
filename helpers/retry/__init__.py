import functools
import logging
import time

from helpers.retry.exceptions import AbortRetry, Retry, MaxRetriesReached


logger = logging.getLogger("dynamic_ip_updater")


def _exponential_backoff_policy(retry_count):
    return retry_count**2


def with_retries(max_retries=3, retry_policy=_exponential_backoff_policy):
    def inner_with_retries(func):
        @functools.wraps(func)
        def _inner_with_retries(*args, **kwargs):
            if max_retries == 0:
                return func(*args, **kwargs)

            retry_count = 1
            while max_retries >= retry_count:
                try:
                    return func(*args, **kwargs)
                except Retry:
                    logger.info(
                        f"Retrying {func.__name__}... - {retry_count}/{max_retries}"
                    )
                    time.sleep(retry_policy(retry_count))
                    retry_count += 1
                except (AbortRetry, Exception) as exc:
                    logger.info(
                        f"Stopping retries for {func.__name__} as an aborting exception was received"
                    )
                    raise exc

            raise MaxRetriesReached("Max retries reached")

        return _inner_with_retries

    return inner_with_retries
