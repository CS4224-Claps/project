from utils.parser import parse_xact
from utils.cli import parse_cli
from utils.connection import connection
from utils.transaction import run_xact
from utils.setup import setup


def main():
    cli_args = parse_cli()
    ff = cli_args.infile
    session = connection()
    #setup(session, './schema/schema.cql', '../../seed/data_files')    

    with ff as f:
        while True:
            xact = parse_xact(f)
            if not xact:
                break
            xact_type, *args = xact
            run_xact(xact_type, session, *args)

    session.shutdown()

if __name__ == "__main__":
    main()

