from time import sleep

from datetime import datetime as dt
from traceback import format_exc
from time import sleep

import datetime as dt

from api.telegram.error import error


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            error(f'{format_exc()}')
    return inner_function


def retry(max_attempts: int = 0, forever: bool = True):
    def inner(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while forever or (attempt < max_attempts):
                sleep(1)
                attempt += 1
                try:
                    return func(*args, **kwargs)
                except:
                    try:
                        error(f'{format_exc()}')
                    except Exception as e:
                        print(e)
        return wrapper
    return inner
