from argparse import ArgumentParser, FileType, RawTextHelpFormatter, Namespace
from json import load 


def get_dsn(config):
    return "postgresql://{}:{}@{}:{}/{}?sslmode=require".format(
        config["username"], 
        config["password"], 
        config["host"], 
        config["port"], 
        config["database"])

def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "config_file",
        help="""\
Connection Configuration File 

Refer to: config.json.example for the necessary 
parameters. 
"""
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    args = parser.parse_args()

    if args.config_file:
        with open(args.config_file, 'r') as f:
            args.__dict__.update(dsn=get_dsn(load(f)))

    return args
