from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from json import load


def get_cockroach_dsn(conf):
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
    parser.add_argument(
        "-c",
        dest="config_file",
        help="config file. defaults to config.json",
        default="config.json",
        type=FileType("r"),
    )
    parser.add_argument(
        "-d",
        dest="directory",
        help="directory containing xact logs",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-x", 
        dest="xacts", 
        help="flag to print xact summary stats", 
        action='store_true'
    )
    args = parser.parse_args()

    if args.config_file:
        args.__dict__.update(cockroach_dsn=get_cockroach_dsn(load(args.config_file)))

    return args


if __name__ == "__main__":
    parse_cmdline()
