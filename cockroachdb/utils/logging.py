import os
import logging, logging.handlers

class LogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

def init_logger(outdir):
    logger = logging.getLogger()

    # To handle info statements, mainly for entire Xact times. 
    info_file_handler = logging.handlers.WatchedFileHandler(f"{outdir}/info_{os.getpid()}.csv") 
    info_file_handler.addFilter(LogLevelFilter(logging.INFO))
    info_file_handler.setLevel(logging.INFO)
    logger.addHandler(info_file_handler)

    # To handle debug statements.
    debug_file_handler = logging.handlers.WatchedFileHandler(f"{outdir}/debug_{os.getpid()}.log") 
    debug_file_handler.addFilter(LogLevelFilter(logging.DEBUG))
    debug_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(debug_file_handler)

    return logger
