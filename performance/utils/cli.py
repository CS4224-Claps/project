from argparse import ArgumentParser, RawTextHelpFormatter
from json import load


def parse_cmdline():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
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

    return args


if __name__ == "__main__":
    parse_cmdline()
