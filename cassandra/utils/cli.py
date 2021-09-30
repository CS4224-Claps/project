import argparse


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
                            nargs=1,
                            help='log file for transaction')

    cli_parser.parse_args()

parse_cli()

