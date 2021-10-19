from argparse import ArgumentParser, FileType, RawTextHelpFormatter
import functools
from json import load
from datetime import datetime
import sys


def get_dsn(conf):
    config = _get_cockroach_config(conf)

    return "postgresql://{}:{}@{}:{}/{}?sslmode=require".format(
        config["username"],
        config["password"],
        config["host"],
        config["port"],
        config["database"],
    )


def get_max_retries(conf):
    config = _get_cockroach_config(conf)
    return config.get("max_retries", 3)


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
        config = load(args.config_file)
        args.__dict__.update(dsn=get_dsn(config))
        args.__dict__.update(max_retries=get_max_retries(config))

    return args


def _get_cockroach_config(conf):
    if "cockroach" not in conf:
        raise ValueError("Missing cockroach field in config.json")

    config = conf["cockroach"]
    return config


if __name__ == "__main__":
    parse_cmdline()
