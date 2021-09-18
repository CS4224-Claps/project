from argparse import ArgumentParser, RawTextHelpFormatter


def parse_cmdline():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-p",
        dest="port",
        help="port number of the fileserver",
        default=3000,
        type=int,
    )
    parser.add_argument(
        "-d",
        dest="directory",
        help="directory to serve the fileserver",
        type=str,
        default="./seed",
        required=True,
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    parse_cmdline()
