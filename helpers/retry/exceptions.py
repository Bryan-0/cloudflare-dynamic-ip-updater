class Retry(Exception):
    pass


class MaxRetriesReached(Exception):
    pass


class AbortRetry(Exception):
    pass
