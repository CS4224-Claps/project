import os 
import psycopg2

from utils.cli import parse_cmdline
from utils.output import print_client_stats, print_throughput_stats, print_cockroach_stats

def main():
    opt = parse_cmdline()
    cwd = os.getcwd()
    conn = psycopg2.connect(dsn=opt.dsn)

    print_client_stats(cwd, opt.indir, opt.outdir)
    print_throughput_stats(cwd, opt.outdir)
    print_cockroach_stats(cwd, opt.outdir, conn)

if __name__ == "__main__": 
    main()
