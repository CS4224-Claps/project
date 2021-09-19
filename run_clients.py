from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from subprocess import Popen
import pathlib


CLIENTS = 40
NODES = 5


def run(opt):
    node_idx = opt.node_idx
    commands = []
    while node_idx < CLIENTS:
        command = [
            "python",
            f"{opt.dbtype}/main.py",
            "-i",
            opt.indir.joinpath(f"{node_idx}.txt"),
            "-o",
            opt.outdir,
        ]
        if opt.verbose:
            command.append("-v")
        commands.append(command)
        node_idx += NODES

    procs = [Popen(cmd) for cmd in commands]
    for p in procs:
        p.wait()


def parse_cmd():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true", help="print debug info")
    parser.add_argument(
        "--db",
        dest="dbtype",
        help="db to run experiment on",
        choices=["cassandra", "cockroachdb"],
        required=True,
    )
    parser.add_argument(
        "-n",
        dest="node_idx",
        help="node index",
        type=int,
        required=True,
        choices=range(NODES),
    )
    parser.add_argument(
        "-i",
        dest="indir",
        help="directory containing input transactions",
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory for logs",
        default=f"logs/cockroachdb/{datetime.now().strftime('%d-%m_%H-%M')}",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    opt = parse_cmd()
    run(opt)
