import time
import logging

import psycopg2

from utils.cli import parse_cmdline
from xacts.example import run # TODO: To Delete when starting to implement Xacts 


def main():
    opt = parse_cmdline()

    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)

    conn = psycopg2.connect(opt.dsn)

    test_run(conn)

    conn.close()


if __name__ == "__main__":
    main()
