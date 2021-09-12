import functools
import logging
import time 


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


def log_command(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) < 2 and len(args[1]) < 0:
            logging.debug(f"{func.__name__} Error: not enough arguments")
            return

        command_letter = args[1][0]
        before = time.time() 
        command = func(*args, **kwargs)
        after = time.time()
        time_taken = int((after - before) * 1000)

        # In CSV Format 
        logging.info(f"{command_letter},{time_taken}ms")

        return command 

    return wrapper
