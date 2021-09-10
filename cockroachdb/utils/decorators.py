import functools 
import logging

def validate_command(command):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) < 2:
                logging.debug("{} Error: not enough arguments".format(func.__name__))
                return 

            io_line = args[1]

            if io_line[0] != command: 
                logging.debug("{} Error: Command is not {}".format(func.__name__, command))
                return 

            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
