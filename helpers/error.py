import traceback
import time


def restart_on_crash(forever=False, max_attempts=3, delay=0.1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while forever or attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    print("Restarting in {0} seconds...".format(delay))
                    traceback.print_exc()
                    attempts += 1
                    time.sleep(delay)
            raise Exception(
                f"Function {func.__name__} crashed after {attempts} attempts.")
        return wrapper
    return decorator
