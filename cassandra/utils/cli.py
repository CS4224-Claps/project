import argparse
from datetime import datetime


def parse_cli():
    cli_parser = argparse.ArgumentParser(description='Parse input file and output file dest')

    cli_parser.add_argument('-i',
                            dest='infile',
                            type=argparse.FileType('r'),
                            nargs="?",
                            help='transaction file to run')
    cli_parser.add_argument("-v", "--verbose", action="store_true", help="print debug info")
    cli_parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory for logs",
        default=f"logs/cassandra/{datetime.now().strftime('%d-%m_%H')}",
    )

    args = cli_parser.parse_args()

    return args

