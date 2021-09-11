import functools
import logging


def validate_command(command):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < 2:
                logging.debug(f"{func.__name__} Error: not enough arguments")
                return

            io_line = args[1]

            if io_line[0] != command:
                logging.debug(
                    f"{func.__name__} Error: Got {io_line[0]}, expecting command {command}"
                )
                return

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator
