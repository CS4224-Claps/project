from utils.cli import parse_cmdline
from utils.output import print_client_stats


def main():
    opt = parse_cmdline()

    print_client_stats(opt.directory)

if __name__ == "__main__":
    main()
