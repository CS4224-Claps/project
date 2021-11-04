from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from subprocess import Popen
from pathlib import Path


CLIENTS = 40
NODES = 5


def run(opt):
    client_id = opt.node_idx
    # Create folder if not exists
    Path(opt.outdir).mkdir(parents=True, exist_ok=True)

    with open(f"{opt.outdir}/DBTYPE", "w") as f:
        f.write(opt.dbtype)

    commands = {}
    while client_id < CLIENTS:
        command = [
            "python",
            f"{opt.dbtype}/main.py",
            "-i",
            opt.indir.joinpath(f"{client_id}.txt"),
            "-o",
            opt.outdir,
        ]
        if opt.verbose:
            command.append("-v")
        commands[client_id] = command
        client_id += NODES

    procs = []
    for client_id, cmd in commands.items():
        outf = Path(f"{opt.outdir}/{client_id}_out.log")
        errf = Path(f"{opt.outdir}/{client_id}_error.log")
        procs.append(Popen(cmd, stderr=open(errf, "w+"), stdout=open(outf, "w+")))

    print(f"Started {len(procs)} processes")

    for p in procs:
        p.wait()
        print(f"Process {p.args} returned {p.returncode}")


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
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        dest="outdir",
        help="output directory for logs",
        default=f"logs/{datetime.now().strftime('%d-%m_%H-%M')}",
        type=Path,
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    opt = parse_cmd()
    run(opt)
