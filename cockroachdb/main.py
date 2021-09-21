import logging, logging.handlers
import psycopg2

from utils.cli import parse_cmdline
from utils.connection import TimeLoggingConnection
from utils.logging import init_logger
from utils.parser import next_xact
from utils.transactions import run_transaction
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

    conn = psycopg2.connect(dsn=opt.dsn, connection_factory=TimeLoggingConnection)
    conn.initialize(init_logger(opt.infile, opt.outdir))

    with opt.infile as f:
        while True:
            xact = next_xact(f)
            if not xact:
                break

            xact_type, *args = xact
            op = lambda conn: command_to_func[xact_type].execute(conn, *args)
            run_transaction(conn, op)

    conn.close()


if __name__ == "__main__":
    main()
