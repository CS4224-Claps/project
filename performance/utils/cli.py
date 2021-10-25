from cassandra import ConsistencyLevel
from cassandra.cluster import ExecutionProfile, Cluster
from cassandra.policies import RoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory


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


def get_cassandra_session(conf):
    if "cassandra" not in conf:
        raise ValueError("Missing cassandra field in config.json")

    contact_points = conf["cassandra"]["contact_points"]
    cluster_profile = ExecutionProfile(
        load_balancing_policy=RoundRobinPolicy(),
        retry_policy=DowngradingConsistencyRetryPolicy(),
        consistency_level=ConsistencyLevel.LOCAL_QUORUM,
        serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
        request_timeout=10000,
        row_factory=tuple_factory,
    )
    cluster = Cluster(contact_points, execution_profiles={"profile": cluster_profile})
    session = cluster.connect()

    return session


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
        "-m",
        dest="mode",
        help="mode to get cassandra or cockroach stats",
        type=str,
        default="cockroach",
    )
    parser.add_argument(
        "-s",
        dest="skip",
        help="flag to skip printing client and xact stats",
        action="store_true",
    )
    parser.add_argument(
        "-x", dest="xacts", help="flag to print xact summary stats", action="store_true"
    )
    args = parser.parse_args()

    if args.mode not in ["cassandra", "cockroach"]:
        raise Exception("Unknown mode. Please supply mode as cassandra or cockroach")

    if args.config_file:
        args.__dict__.update(cockroach_dsn=get_cockroach_dsn(load(args.config_file)))

    args.__dict__.update(cass_sess=get_cassandra_session())

    return args


if __name__ == "__main__":
    parse_cmdline()
