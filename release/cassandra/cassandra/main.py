from utils.parser import parse_xact
from utils.cli import parse_cli
from utils.connection import connection
from utils.logging import init_logger
from utils.transaction import run_xact


import logging


def main():
    cli_args = parse_cli()
    logging.basicConfig(level=logging.DEBUG if cli_args.verbose else logging.INFO)
    logging.debug(f"cli option: {cli_args}")

    init_logger(cli_args.infile, cli_args.outdir)

    ff = cli_args.infile
    session = connection(cli_args.contact_points)

    with ff as f:
        while True:
            xact = parse_xact(f)
            if not xact:
                break
            xact_type, *args = xact
            run_xact(xact_type, session, *args)

    session.shutdown()


if __name__ == "__main__":
    main()
