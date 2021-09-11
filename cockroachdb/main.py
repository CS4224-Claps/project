import time
import logging

import psycopg2

from utils.cli import parse_cmdline
from utils.parser import parse 
from xacts import new_order, top_balance

def main():
    opt = parse_cmdline()

    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)

    conn = psycopg2.connect(opt.dsn)

    """
    # Test 2.1 
    io_line, data_lines = parse("N,1,1,1,2", ["1,1,1","1,1,1"])
    new_order.execute(conn, io_line, data_lines)
    """

    conn.close()


if __name__ == "__main__":
    main()
