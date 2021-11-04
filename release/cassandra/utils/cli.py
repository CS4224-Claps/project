from argparse import FileType, ArgumentParser
from datetime import datetime
from json import load


def get_contact_points(conf):
    if "cassandra" not in conf:
        raise ValueError("Missing cassandra field in config.json")

    return conf["cassandra"]["contact_points"]


def parse_cli():
    cli_parser = ArgumentParser(description="Parse input file and output file dest")

    cli_parser.add_argument(
        "-c",
        dest="config_file",
        help="connection config file. defaults to config.json",
        default="config.json",
        type=FileType("r"),
    )
    cli_parser.add_argument(
        "-i",
        dest="infile",
        type=FileType("r"),
        nargs="?",
        help="transaction file to run",
    )
    cli_parser.add_argument(
        "-v", "--verbose", action="store_true", help="print debug info"
    )
    cli_parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory for logs",
        default=f"logs/cassandra/{datetime.now().strftime('%d-%m_%H')}",
    )

    # for setup.py
    cli_parser.add_argument(
        "--schema",
        dest="schema",
        default="cassandra/schema/schema.cql",
        help="schema file to run",
    )
    cli_parser.add_argument(
        "--seed",
        dest="seed_dir",
        help="directory for seed file",
        default="../seed/data_files",
    )

    args = cli_parser.parse_args()

    if args.config_file:
        config = load(args.config_file)
        args.__dict__.update(contact_points=get_contact_points(config))

    return args
