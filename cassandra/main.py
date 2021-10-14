from utils.parser import parse_xact
from utils.cli import parse_cli
from utils.connection import connection


def main():
    cli_args = parse_cli()
    ff = cli_args.infile
    session = connection()

    with ff as f:
        while True:
            xact = parse_xact(f)
            if not xact:
                break
            xact_type, *args = xact

            #command_to_func[xact_type].execute(conn, *args)

    session.shutdown()

if __name__ == "__main__":
    main()

