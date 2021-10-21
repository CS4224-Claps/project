import logging, logging.handlers
import psycopg2
from pathlib import Path

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


def _run_one_xact(xact, conn, opt, fd):
    xact_type, *args = xact
    op = lambda conn: command_to_func[xact_type].execute(conn, *args)
    try:
        run_transaction(conn, op, opt.max_retries)
    except:
        # if there is any error, we write it to the file noted by fd and move on to the next xact

        # args[0] is the io line
        fd.write(",".join(args[0]) + "\n")
        if len(args) > 1:
            # args[1] is the data line
            for data_line in args[1]:
                fd.write(",".join(data_line) + "\n")


def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    logging.debug(f"cli option: {opt}")

    conn = psycopg2.connect(dsn=opt.dsn, connection_factory=TimeLoggingConnection)
    conn.initialize(init_logger(opt.infile, opt.outdir))

    retry_file = f"{opt.outdir}/retry_{Path(opt.infile.name).stem}.txt"

    # do the original transaction from seed file
    with opt.infile as f, open(retry_file, "a") as rf:
        while True:
            xact = next_xact(f.readline(), f)
            if not xact:
                break

            _run_one_xact(xact, conn, opt, rf)

    # do retries if there is any
    rf1 = open(retry_file, "r")
    rf2 = open(retry_file, "a")
    cur_start, cur_end = 0, rf2.tell()

    with rf1, rf2:
        while (
            rf2.tell() > 0 and rf2.tell() > rf1.tell()
        ):  # there is something written in the previous iteration
            rf1.seek(cur_start)
            rf2.write("--------\n")
            while True:
                line = rf1.readline()
                if line.startswith("-"):
                    continue

                xact = next_xact(line, rf1)
                if not xact:
                    break

                _run_one_xact(xact, conn, opt, rf2)

            cur_start, cur_end = cur_end, rf2.tell()
            rf1.seek(cur_start)
            rf1.readline()  # we skip the marker -----

    conn.close()


if __name__ == "__main__":
    main()
