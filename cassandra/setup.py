from utils.connection import connection
from utils.setup import setup
from utils.cli_setup import parse_cli
import sys


def main():
    cli_args = parse_cli()
    session = connection(cli_args.contact_points)
    setup(session, cli_args.schema, cli_args.seed_dir)

    session.shutdown()


if __name__ == "__main__":
    main()
