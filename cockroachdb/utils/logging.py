import logging, logging.handlers
from pathlib import Path


class LogLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def init_logger(infile, outdir):
    filename = Path(infile.name).stem
    logger = logging.getLogger()

    # To handle info statements, mainly for entire Xact times.
    info_file_handler = logging.handlers.WatchedFileHandler(
        f"{outdir}/{filename}_info.csv"
    )
    info_file_handler.addFilter(LogLevelFilter(logging.INFO))
    info_file_handler.setLevel(logging.INFO)
    logger.addHandler(info_file_handler)

    # To handle debug statements.
    debug_file_handler = logging.handlers.WatchedFileHandler(
        f"{outdir}/{filename}_debug.log"
    )
    debug_file_handler.addFilter(LogLevelFilter(logging.DEBUG))
    debug_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(debug_file_handler)

    return logger
