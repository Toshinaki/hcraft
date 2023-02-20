from contextlib import contextmanager
from time import sleep


@contextmanager
def waits(before: int = 0, after: int = 0):
    if before:
        sleep(before)

    yield

    if after:
        sleep(after)
