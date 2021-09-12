import time
import logging

import psycopg2

from utils.cli import parse_cmdline
from utils.parser import next_xact
from xacts import (
    new_order,
    payment,
    delivery,
    order_status,
    stock,
    popular_item,
    top_balance,
    related_customer,
)

command_to_func = {
    "N": new_order,
    "P": payment,
    "D": delivery,
    "O": order_status,
    "S": stock,
    "I": popular_item,
    "T": top_balance,
    "R": related_customer,
}


def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    logging.debug(f"cli option: {opt}")

    conn = psycopg2.connect(opt.dsn)

    with opt.infile as f:
        while True:
            xact = next_xact(f)
            if not xact:
                break

            xact_type, *args = xact
            command_to_func[xact_type].execute(conn, *args)

    conn.close()


if __name__ == "__main__":
    main()
