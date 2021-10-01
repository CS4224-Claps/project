import argparse
from datetime import datetime


def parse_cli():
    cli_parser = argparse.ArgumentParser(description='Parse input file and output file dest')

    cli_parser.add_argument('-i',
                            dest='infile',
                            type=argparse.FileType('r'),
                            nargs=1,
                            help='transaction file to run')

    cli_parser.add_argument('-o',
                            dest='logfile',
                            type=argparse.FileType('w'),
                            nargs='?',
                            help='log file for transaction',
                            default=f'logs/cassandra/{datetime.now().strftime("%d-%m_%H")}')

    args = cli_parser.parse_args()

    return args;



