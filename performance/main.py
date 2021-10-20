import psycopg2

from utils.cli import parse_cmdline
from utils.output import (
    print_client_stats,
    print_throughput_stats,
    print_cockroach_stats,
    print_summary_stats, 
)
from utils.cassandra import get_cassandra_stats


def main():
    opt = parse_cmdline()

    if opt.xacts:
        print_summary_stats(opt.directory)
   
    if not opts.skip:
        print_client_stats(opt.directory)
        print_throughput_stats(opt.directory)

    if opt.mode == "cockroach":
        print_cockroach_stats(opt.directory, opt.cockroach_dsn)
    else: 
        print_cassandra_stats(opt.directory, opt.cass_sess)


if __name__ == "__main__":
    main()
