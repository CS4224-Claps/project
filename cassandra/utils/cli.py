import argparse
from datetime import datetime


def parse_cli():
    cli_parser = argparse.ArgumentParser(description='Parse input file and output file dest')

    cli_parser.add_argument('-i',
                            dest='infile',
                            type=argparse.FileType('r'),
                            nargs="?",
                            help='transaction file to run')


    args = cli_parser.parse_args()

    return args




