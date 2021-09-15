import psycopg2

from utils.cli import parse_cmdline
from utils.output import (
    print_client_stats,
    print_throughput_stats,
    print_cockroach_stats,
)


def main():
    opt = parse_cmdline()

    print_client_stats(opt.directory)
    print_throughput_stats(opt.directory)
    print_cockroach_stats(opt.directory, opt.cockroach_dsn)


if __name__ == "__main__":
    main()
