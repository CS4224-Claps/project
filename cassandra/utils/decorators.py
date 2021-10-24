def log_command(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) < 2 and len(args[1]) < 0:
            logging.debug(f"{func.__name__} Error: not enough arguments")
            return

        command_letter = args[1][0]
        logging.debug(f"\n -------> {','.join(args[1])}")

        before = time.time()
        command = func(*args, **kwargs)
        after = time.time()
        time_taken = round((after - before) * 1000, 2)

        # In CSV Format
        logging.info(f"{command_letter},{time_taken}")

        return command

    return wrapper
