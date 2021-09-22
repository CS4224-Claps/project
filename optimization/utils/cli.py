from argparse import ArgumentParser, RawTextHelpFormatter


def parse_cmdline():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-d",
        dest="directory",
        help="directory containing xact logs",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    parse_cmdline()
