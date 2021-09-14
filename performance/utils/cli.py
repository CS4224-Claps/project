from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from json import load



def get_dsn(config):
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
        dest="cockroach_config",
        help="cockroach connection config file. defaults to cockroach_config.json",
        default="cockroach_config.json",
        type=FileType("r"),
    )
    parser.add_argument(
        "-i",
        dest="indir",
        help="input directory containing xact logs",
        type=str,
        default="/",
    )
    parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory containing csv peformance files",
        type=str,
        default="./out",
    )
    args = parser.parse_args()

    if args.cockroach_config:
        args.__dict__.update(dsn=get_dsn(load(args.cockroach_config)))

    return args


if __name__ == "__main__":
    parse_cmdline()
