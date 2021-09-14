from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from json import load
from datetime import datetime
import sys


def get_dsn(conf):
    if "cockroach" not in conf:
        raise ValueError("Missing cockroach field in config.json")

    config = conf["cockroach"]

    return "postgresql://{}:{}@{}:{}/{}?sslmode=require".format(
        config["username"],
        config["password"],
        config["host"],
        config["port"],
        config["database"],
    )


def parse_cmdline():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", help="print debug info")
    parser.add_argument(
        "-c",
        dest="config_file",
        help="connection config file. defaults to config.json",
        default="config.json",
        type=FileType("r"),
    )
    parser.add_argument(
        "-i",
        dest="infile",
        help="input file containing xacts",
        nargs="?",
        type=FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory for logs",
        default=f"logs/cockroachdb/{datetime.now().strftime('%d-%m_%H')}",
    )
    args = parser.parse_args()

    if args.config_file:
        args.__dict__.update(dsn=get_dsn(load(args.config_file)))

    return args


if __name__ == "__main__":
    parse_cmdline()
