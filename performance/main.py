import os 
import csv 

from utils.cli import parse_cmdline
from utils.output import print_client_stats, print_throughput_stats

def main():
    opt = parse_cmdline()
    cwd = os.getcwd()
    indir, outdir = opt.indir, opt.outdir 

    print_client_stats(cwd, indir, outdir)
    print_throughput_stats(cwd, outdir)


if __name__ == "__main__": 
    main()
